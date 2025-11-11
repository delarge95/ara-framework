"""
Research Graph - LangGraph implementation of the ARA research pipeline.

This module implements the main research workflow as a LangGraph StateGraph,
replacing the previous CrewAI Crew-based implementation.

Architecture:
    START → NicheAnalyst → LiteratureResearcher → TechnicalArchitect 
          → ImplementationSpecialist → ContentSynthesizer → END

Key Features:
- Explicit graph-based control flow
- Built-in checkpointing for pause/resume
- Advanced error handling and retries
- State persistence with Redis or Memory
- Observable execution with LangSmith
- Production-ready scalability

Usage:
    ```python
    from graphs import create_research_graph
    
    graph = create_research_graph()
    result = await graph.ainvoke({
        "niche": "Rust WebAssembly for real-time audio processing",
        "messages": [],
    })
    
    print(result["final_report"])
    ```
"""

import structlog
from datetime import datetime, timezone
from typing import TypedDict, Annotated, Sequence, Optional, Literal
from operator import add

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from langchain_core.runnables import RunnablePassthrough
from langchain_core.tools import tool

from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from config.settings import settings
from core.budget_manager import BudgetManager
from tools import (
    get_scraping_tool,
    get_search_tool,
    get_pdf_tool,
    get_database_tool,
)

logger = structlog.get_logger(__name__)


# =============================================================================
# State Schema
# =============================================================================

class ResearchState(TypedDict):
    """
    Central state schema for the research pipeline.
    
    This state is shared across all agent nodes and contains:
    - Input: Initial niche/topic
    - Agent outputs: Results from each agent
    - Metadata: Execution tracking, errors, budget
    - Messages: Conversation history for LLM context
    """
    
    # Input
    niche: str
    
    # Agent outputs (populated sequentially)
    niche_analysis: Optional[str]
    literature_review: Optional[str]
    technical_architecture: Optional[str]
    implementation_plan: Optional[str]
    final_report: Optional[str]
    
    # Message history (accumulator)
    messages: Annotated[Sequence[BaseMessage], add]
    
    # Execution metadata
    current_agent: str
    agent_history: list[str]
    start_time: str
    end_time: Optional[str]
    
    # Error handling
    errors: list[str]
    warnings: list[str]
    retry_count: dict[str, int]
    
    # Budget tracking
    total_credits_used: float
    budget_limit: float
    budget_exceeded: bool
    
    # Checkpointing
    checkpoint_id: Optional[str]


# =============================================================================
# Agent Node Functions
# =============================================================================

def niche_analyst_node(state: ResearchState) -> ResearchState:
    """
    Node 1: Niche Analysis Agent.
    
    Analyzes the viability and opportunities of the research niche.
    
    Responsibilities:
    - Search recent academic papers (Semantic Scholar)
    - Scrape GitHub repos, Reddit threads, blogs
    - Identify emerging trends and gaps
    - Evaluate market demand and competition
    - Generate keywords and sub-niches
    
    Tools: scraping_tool, search_tool
    LLM: Groq LLaMA 3.3-70B
    Duration: ~7-8 minutes
    Credits: 0 (Groq is free)
    """
    logger.info(
        "niche_analyst_started",
        niche=state["niche"],
        agent_number=1,
    )
    
    try:
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
        )
        
        # Get tools
        scraping = get_scraping_tool()
        search = get_search_tool()
        
        tools = [
            scraping.scrape_website,
            scraping.scrape_multiple_urls,
            search.search_recent_papers,
        ]
        
        # Create ReAct agent
        agent = create_react_agent(llm, tools)
        
        # System prompt
        system_msg = SystemMessage(content=f"""You are a Niche Market Analyst with 10+ years of experience identifying opportunities in emerging technology niches.

Your mission: Analyze the viability and opportunities of the niche "{state['niche']}"

**Analysis Requirements:**

1. **Academic Research** (Semantic Scholar):
   - Search for papers from the last 2 years
   - Identify 5-10 key papers and trends
   - Note publication velocity and citation counts

2. **Community Activity** (Web Scraping):
   - Find active GitHub repositories (stars, recent commits)
   - Locate Reddit discussions, HackerNews threads
   - Identify relevant blogs and developer communities

3. **Market Evaluation**:
   - Assess demand (interest level, job postings)
   - Evaluate competition (how saturated is the space?)
   - Identify gaps between academic research and industry practice

4. **Strategic Output**:
   - Viability score (1-10) with justification
   - 3-5 key trends identified
   - 10-15 keywords for deeper research
   - 2-3 promising sub-niches

**Output Format** (Markdown):
```markdown
# Niche Analysis: {state['niche']}

## Executive Summary
[2-3 paragraphs on viability]

## Viability Score: X/10
[Justification]

## Key Trends
1. [Trend 1 with evidence]
2. [Trend 2 with evidence]
...

## Community Activity
- **GitHub**: [Top repos with metrics]
- **Reddit**: [Active communities]
- **Blogs**: [Influential voices]

## Market Demand
[Analysis of demand indicators]

## Competition Level
[Assessment of saturation]

## Research Keywords
[10-15 keywords]

## Recommended Sub-Niches
1. [Sub-niche 1]
2. [Sub-niche 2]
...
```

**IMPORTANT:**
- Be critical: If the niche isn't viable, say so clearly
- Focus on EMERGING trends, not mature technologies
- Use tools to gather real data, don't make assumptions
- Rate limit: Semantic Scholar is 1 req/sec, be careful
""")
        
        # Human input
        human_msg = HumanMessage(content=f"Analyze the niche: {state['niche']}")
        
        # Invoke agent
        result = agent.invoke({
            "messages": [system_msg, human_msg]
        })
        
        # Extract analysis from last AI message
        analysis = result["messages"][-1].content
        
        # Update state
        logger.info(
            "niche_analyst_completed",
            output_length=len(analysis),
            tool_calls=len([m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]),
        )
        
        return {
            **state,
            "niche_analysis": analysis,
            "current_agent": "literature_researcher",
            "agent_history": state.get("agent_history", []) + ["niche_analyst"],
            "messages": state.get("messages", []) + result["messages"],
        }
        
    except Exception as e:
        logger.error(
            "niche_analyst_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        
        # Update error state
        errors = state.get("errors", [])
        errors.append(f"NicheAnalyst: {str(e)}")
        
        retry_count = state.get("retry_count", {})
        retry_count["niche_analyst"] = retry_count.get("niche_analyst", 0) + 1
        
        return {
            **state,
            "errors": errors,
            "retry_count": retry_count,
        }


def literature_researcher_node(state: ResearchState) -> ResearchState:
    """
    Node 2: Literature Research Agent.
    
    Conducts comprehensive literature review of academic papers.
    
    Responsibilities:
    - Search 100-200 academic papers (Semantic Scholar, arXiv)
    - Deep analysis of top 20 most relevant papers
    - Identify research trends, gaps, and opportunities
    - Extract methodologies and key findings
    - Synthesize literature into coherent review
    
    Tools: search_tool, pdf_tool, database_tool
    LLM: Groq LLaMA 3.3-70B
    Duration: ~20-25 minutes
    Credits: ~0.15-1.5 (mostly API rate limits, not LLM)
    """
    logger.info(
        "literature_researcher_started",
        niche=state["niche"],
        agent_number=2,
        has_niche_analysis=state.get("niche_analysis") is not None,
    )
    
    try:
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
        )
        
        # Get tools
        search = get_search_tool()
        pdf = get_pdf_tool()
        database = get_database_tool()
        
        tools = [
            search.search_recent_papers,
            pdf.extract_pdf_content,
            database.save_data,
        ]
        
        # Create ReAct agent
        agent = create_react_agent(llm, tools)
        
        # System prompt with context from previous agent
        niche_analysis = state.get("niche_analysis", "No analysis available")
        
        system_msg = SystemMessage(content=f"""You are a PhD-level Literature Researcher specializing in comprehensive academic literature reviews.

Your mission: Conduct an exhaustive literature review for "{state['niche']}"

**Context from Niche Analysis:**
{niche_analysis[:2000]}...

**Research Process:**

1. **Broad Search** (100-200 papers):
   - Use keywords from niche analysis
   - Search last 3-5 years (focus on recent)
   - Filter by relevance and citation count
   - Cover multiple databases (Semantic Scholar, arXiv)

2. **Deep Analysis** (Top 20 papers):
   - Read abstracts and key sections
   - Extract methodologies, datasets, results
   - Note limitations and future work
   - Identify citation networks

3. **Synthesis**:
   - Identify research trends and evolution
   - Find gaps and opportunities
   - Map the research landscape
   - Recommend specific papers for deeper study

4. **Output**:
   - Comprehensive literature review (3000-5000 words)
   - Annotated bibliography of top 20 papers
   - Research gap analysis
   - Recommendations for technical architecture

**Output Format** (Markdown):
```markdown
# Literature Review: {state['niche']}

## Executive Summary
[3-4 paragraphs overview]

## Research Landscape
### Historical Evolution
[How the field has evolved]

### Current State
[Where we are today]

### Future Directions
[Where the field is heading]

## Methodological Approaches
[Common methods, tools, frameworks]

## Key Findings & Insights
1. [Finding 1 with citations]
2. [Finding 2 with citations]
...

## Research Gaps & Opportunities
[What hasn't been explored? Where are the opportunities?]

## Top 20 Papers (Annotated Bibliography)
1. **[Paper Title]** - Author et al. (Year)
   - **Citation Count**: X
   - **Key Contribution**: [Summary]
   - **Methodology**: [Approach]
   - **Relevance**: [Why important]
   - **URL**: [Link]

[... continue for all 20 papers]

## Recommendations
[What should the technical architecture focus on based on this review?]
```

**CRITICAL:**
- Semantic Scholar has 1 req/sec limit - pace yourself
- Focus on HIGH QUALITY papers (citation count, venue)
- Be comprehensive but concise
- Save important papers to database for future reference
""")
        
        human_msg = HumanMessage(content=f"Conduct comprehensive literature review for: {state['niche']}")
        
        # Invoke agent
        result = agent.invoke({
            "messages": [system_msg, human_msg]
        })
        
        # Extract review
        review = result["messages"][-1].content
        
        logger.info(
            "literature_researcher_completed",
            output_length=len(review),
            tool_calls=len([m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]),
        )
        
        return {
            **state,
            "literature_review": review,
            "current_agent": "technical_architect",
            "agent_history": state.get("agent_history", []) + ["literature_researcher"],
            "messages": state.get("messages", []) + result["messages"],
        }
        
    except Exception as e:
        logger.error(
            "literature_researcher_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        
        errors = state.get("errors", [])
        errors.append(f"LiteratureResearcher: {str(e)}")
        
        retry_count = state.get("retry_count", {})
        retry_count["literature_researcher"] = retry_count.get("literature_researcher", 0) + 1
        
        return {
            **state,
            "errors": errors,
            "retry_count": retry_count,
        }


def technical_architect_node(state: ResearchState) -> ResearchState:
    """
    Node 3: Technical Architecture Agent.
    
    Designs comprehensive technical architecture for the research project.
    
    Responsibilities:
    - Design system architecture and components
    - Select technology stack (languages, frameworks, tools)
    - Define design patterns and best practices
    - Create architecture diagrams (textual)
    - Address security, scalability, and performance
    
    Tools: scraping_tool, pdf_tool, database_tool
    LLM: Groq LLaMA 3.3-70B
    Duration: ~10-12 minutes
    Credits: ~1
    """
    logger.info(
        "technical_architect_started",
        niche=state["niche"],
        agent_number=3,
        has_literature_review=state.get("literature_review") is not None,
    )
    
    try:
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
        )
        
        # Get tools
        scraping = get_scraping_tool()
        pdf = get_pdf_tool()
        database = get_database_tool()
        
        tools = [
            scraping.scrape_website,
            pdf.extract_pdf_content,
            database.save_data,
        ]
        
        # Create ReAct agent
        agent = create_react_agent(llm, tools)
        
        # Get context
        niche_analysis = state.get("niche_analysis", "")[:1500]
        literature_review = state.get("literature_review", "")[:3000]
        
        system_msg = SystemMessage(content=f"""You are a Senior Software Architect with expertise in designing scalable, production-ready systems for cutting-edge research projects.

Your mission: Design a comprehensive technical architecture for "{state['niche']}"

**Context:**

**Niche Analysis Summary:**
{niche_analysis}

**Literature Review Summary:**
{literature_review}

**Architecture Design Requirements:**

1. **System Architecture**:
   - High-level component diagram (ASCII art or textual)
   - Data flow between components
   - Integration points and APIs
   - Deployment topology

2. **Technology Stack**:
   - Programming languages and rationale
   - Frameworks and libraries (specific versions)
   - Databases and storage solutions
   - Infrastructure and deployment tools

3. **Design Patterns**:
   - Architectural patterns (microservices, event-driven, etc.)
   - Code-level patterns applicable to this domain
   - Best practices from literature review

4. **Non-Functional Requirements**:
   - **Performance**: Benchmarks and optimization strategies
   - **Scalability**: Horizontal/vertical scaling approach
   - **Security**: Authentication, authorization, data protection
   - **Reliability**: Error handling, monitoring, logging

5. **Development Environment**:
   - Local development setup
   - CI/CD pipeline
   - Testing strategy (unit, integration, E2E)

**Output Format** (Markdown):
```markdown
# Technical Architecture: {state['niche']}

## Executive Summary
[2-3 paragraphs on architecture philosophy]

## System Architecture

### High-Level Overview
```
[ASCII diagram or textual description]
```

### Components
1. **Component A**: [Description, responsibilities]
2. **Component B**: [Description, responsibilities]
...

### Data Flow
[How data moves through the system]

## Technology Stack

### Programming Languages
- **Primary**: [Language] - [Rationale]
- **Secondary**: [Language] - [Use cases]

### Frameworks & Libraries
- **[Category]**:
  - [Library 1] v[X.Y.Z] - [Purpose]
  - [Library 2] v[X.Y.Z] - [Purpose]

### Databases & Storage
- [Database] - [Why chosen, data models]

### Infrastructure
- [Cloud/On-prem]
- [Container orchestration]
- [Service mesh, if any]

## Design Patterns

### Architectural Patterns
[Which patterns and why]

### Code Patterns
[Specific patterns for this domain]

### Anti-Patterns to Avoid
[Common pitfalls in this space]

## Non-Functional Requirements

### Performance
- **Target**: [Metrics]
- **Optimization**: [Strategies]

### Scalability
[Approach to scale]

### Security
- [Authentication method]
- [Authorization model]
- [Data encryption]
- [Vulnerability mitigation]

### Reliability
- **Uptime target**: [X]%
- **Error handling**: [Approach]
- **Monitoring**: [Tools and metrics]

## Development Setup

### Prerequisites
[Tools needed]

### Local Environment
```bash
# Setup commands
```

### CI/CD Pipeline
[Automated testing, deployment process]

## Testing Strategy
- **Unit tests**: [Approach, coverage target]
- **Integration tests**: [Key scenarios]
- **E2E tests**: [Critical paths]

## Recommendations
[Key architectural decisions and trade-offs]
```

**IMPORTANT:**
- Be specific with library names and versions
- Base decisions on evidence from literature review
- Consider real-world constraints (cost, team size, timeline)
- Think production-ready, not just prototype
""")
        
        human_msg = HumanMessage(content=f"Design technical architecture for: {state['niche']}")
        
        # Invoke agent
        result = agent.invoke({
            "messages": [system_msg, human_msg]
        })
        
        # Extract architecture
        architecture = result["messages"][-1].content
        
        logger.info(
            "technical_architect_completed",
            output_length=len(architecture),
            tool_calls=len([m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]),
        )
        
        return {
            **state,
            "technical_architecture": architecture,
            "current_agent": "implementation_specialist",
            "agent_history": state.get("agent_history", []) + ["technical_architect"],
            "messages": state.get("messages", []) + result["messages"],
        }
        
    except Exception as e:
        logger.error(
            "technical_architect_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        
        errors = state.get("errors", [])
        errors.append(f"TechnicalArchitect: {str(e)}")
        
        retry_count = state.get("retry_count", {})
        retry_count["technical_architect"] = retry_count.get("technical_architect", 0) + 1
        
        return {
            **state,
            "errors": errors,
            "retry_count": retry_count,
        }


def implementation_specialist_node(state: ResearchState) -> ResearchState:
    """
    Node 4: Implementation Planning Agent.
    
    Creates detailed implementation roadmap and execution plan.
    
    Responsibilities:
    - Break down architecture into implementable tasks
    - Create sprint plans with milestones
    - Estimate effort and timeline
    - Identify risks and mitigation strategies
    - Generate user stories and acceptance criteria
    
    Tools: scraping_tool, database_tool
    LLM: Groq LLaMA 3.3-70B
    Duration: ~7-8 minutes
    Credits: ~0.33
    """
    logger.info(
        "implementation_specialist_started",
        niche=state["niche"],
        agent_number=4,
        has_architecture=state.get("technical_architecture") is not None,
    )
    
    try:
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
        )
        
        # Get tools
        scraping = get_scraping_tool()
        database = get_database_tool()
        
        tools = [
            scraping.scrape_website,
            database.save_data,
        ]
        
        # Create ReAct agent
        agent = create_react_agent(llm, tools)
        
        # Get context
        architecture = state.get("technical_architecture", "")[:3000]
        
        system_msg = SystemMessage(content=f"""You are a Technical Lead / Scrum Master with expertise in breaking down complex projects into actionable implementation plans.

Your mission: Create a comprehensive implementation roadmap for "{state['niche']}"

**Technical Architecture Context:**
{architecture}

**Planning Requirements:**

1. **Project Breakdown**:
   - Divide into 4-6 implementation phases
   - Each phase = 2-3 week sprint
   - Clear dependencies between phases
   - Milestones and deliverables

2. **User Stories** (10-15 total):
   - Format: "As a [user], I want [feature], so that [benefit]"
   - Acceptance criteria for each
   - Priority (Must Have, Should Have, Nice to Have)
   - Estimated effort (S/M/L/XL)

3. **Technical Tasks**:
   - Specific implementation tasks
   - Prerequisites and dependencies
   - Required skills/expertise
   - Testing requirements

4. **Timeline & Estimation**:
   - Realistic timelines per phase
   - Team size assumption
   - Critical path analysis
   - Buffer for unknowns

5. **Risk Management**:
   - Identify 5-7 key risks
   - Impact and probability assessment
   - Mitigation strategies
   - Contingency plans

**Output Format** (Markdown):
```markdown
# Implementation Plan: {state['niche']}

## Executive Summary
[2-3 paragraphs on approach]

## Project Phases

### Phase 1: [Name] (Weeks 1-2)
**Goal**: [What we'll achieve]

**Milestones**:
- [Milestone 1]
- [Milestone 2]

**Deliverables**:
- [Deliverable 1]
- [Deliverable 2]

**User Stories**:
1. **[US-001]**: As a [user]...
   - **Priority**: Must Have
   - **Effort**: M
   - **Acceptance Criteria**:
     - [ ] Criterion 1
     - [ ] Criterion 2

[Repeat for all phases]

## Technical Task Breakdown

### Phase 1 Tasks
- **Task 1.1**: [Description]
  - **Prerequisites**: [Dependencies]
  - **Skills**: [Required expertise]
  - **Effort**: [Hours/days]
  - **Testing**: [Test approach]

[Continue for all phases]

## Timeline & Estimates

### Gantt Chart (Text)
```
Week  | Phase              | Deliverables
------|-------------------|------------------
1-2   | Phase 1           | [List]
3-4   | Phase 2           | [List]
...
```

### Team Requirements
- **Team Size**: [Number] developers
- **Roles Needed**: [List]
- **Estimated Duration**: [Weeks/months]

### Critical Path
[Tasks that cannot be delayed]

## Risk Management

### Risk 1: [Description]
- **Impact**: High/Medium/Low
- **Probability**: [%]
- **Mitigation**: [Strategy]
- **Contingency**: [Backup plan]

[Continue for all risks]

## Success Criteria
[How we know we've succeeded]

## Recommendations
[Key insights for successful implementation]
```

**IMPORTANT:**
- Be realistic with estimates (add 20-30% buffer)
- Consider team learning curve
- Think about technical debt and refactoring
- Include documentation and testing in estimates
""")
        
        human_msg = HumanMessage(content=f"Create implementation plan for: {state['niche']}")
        
        # Invoke agent
        result = agent.invoke({
            "messages": [system_msg, human_msg]
        })
        
        # Extract plan
        plan = result["messages"][-1].content
        
        logger.info(
            "implementation_specialist_completed",
            output_length=len(plan),
            tool_calls=len([m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]),
        )
        
        return {
            **state,
            "implementation_plan": plan,
            "current_agent": "content_synthesizer",
            "agent_history": state.get("agent_history", []) + ["implementation_specialist"],
            "messages": state.get("messages", []) + result["messages"],
        }
        
    except Exception as e:
        logger.error(
            "implementation_specialist_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        
        errors = state.get("errors", [])
        errors.append(f"ImplementationSpecialist: {str(e)}")
        
        retry_count = state.get("retry_count", {})
        retry_count["implementation_specialist"] = retry_count.get("implementation_specialist", 0) + 1
        
        return {
            **state,
            "errors": errors,
            "retry_count": retry_count,
        }


def content_synthesizer_node(state: ResearchState) -> ResearchState:
    """
    Node 5: Content Synthesis Agent.
    
    Synthesizes all previous outputs into comprehensive final report.
    
    Responsibilities:
    - Integrate outputs from all 4 previous agents
    - Create executive summary
    - Ensure coherence and flow
    - Format professional technical document
    - Generate table of contents, figures, references
    
    Tools: database_tool
    LLM: Groq LLaMA 3.3-70B
    Duration: ~15-18 minutes
    Credits: ~0.5
    """
    logger.info(
        "content_synthesizer_started",
        niche=state["niche"],
        agent_number=5,
        has_all_inputs=all([
            state.get("niche_analysis"),
            state.get("literature_review"),
            state.get("technical_architecture"),
            state.get("implementation_plan"),
        ]),
    )
    
    try:
        # Initialize LLM
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            api_key=settings.GROQ_API_KEY,
        )
        
        # Get tools
        database = get_database_tool()
        tools = [database.save_data]
        
        # Create ReAct agent
        agent = create_react_agent(llm, tools)
        
        # Get all context
        niche_analysis = state.get("niche_analysis", "Not available")
        literature_review = state.get("literature_review", "Not available")
        architecture = state.get("technical_architecture", "Not available")
        impl_plan = state.get("implementation_plan", "Not available")
        
        system_msg = SystemMessage(content=f"""You are a Technical Editor and Documentation Specialist with expertise in synthesizing complex technical content into coherent, professional reports.

Your mission: Create a comprehensive final report for "{state['niche']}" that integrates all research and planning.

**Source Materials:**

**1. Niche Analysis:**
{niche_analysis[:2000]}

**2. Literature Review:**
{literature_review[:3000]}

**3. Technical Architecture:**
{architecture[:3000]}

**4. Implementation Plan:**
{impl_plan[:2000]}

**Synthesis Requirements:**

1. **Executive Summary** (500-750 words):
   - Compelling overview
   - Key findings and insights
   - Strategic recommendations
   - Expected impact

2. **Content Integration**:
   - Weave together all 4 sources
   - Ensure logical flow and transitions
   - Eliminate redundancy
   - Add connecting narratives

3. **Professional Formatting**:
   - Clear section hierarchy
   - Consistent formatting
   - Tables and diagrams where helpful
   - Professional tone

4. **Completeness**:
   - All key information included
   - No critical gaps
   - Balanced depth across sections
   - 10,000-15,000 words total

**Final Report Structure** (Markdown):

```markdown
# Research & Implementation Report: {state['niche']}

**Date**: {datetime.now(timezone.utc).strftime("%B %d, %Y")}
**Framework**: ARA Framework (LangGraph)
**Status**: Complete

---

## Table of Contents
1. Executive Summary
2. Introduction
3. Niche Analysis
4. Literature Review
5. Technical Architecture
6. Implementation Roadmap
7. Conclusions & Recommendations
8. References
9. Appendices

---

## Executive Summary

[Compelling 500-750 word summary that captures:
- What we investigated
- Why it matters
- Key findings
- Strategic recommendations
- Expected impact
- Next steps]

---

## 1. Introduction

### 1.1 Background
[Context for the research]

### 1.2 Objectives
[What we aimed to achieve]

### 1.3 Methodology
[How we conducted the research]

### 1.4 Scope
[What's included and excluded]

---

## 2. Niche Analysis

[Synthesized and expanded niche analysis with:
- Market viability assessment
- Trend analysis
- Community insights
- Competitive landscape
- Strategic opportunities]

---

## 3. Literature Review

[Comprehensive literature review with:
- Research landscape
- Methodological approaches
- Key findings
- Research gaps
- Top papers (annotated)
- Insights for implementation]

---

## 4. Technical Architecture

[Detailed architecture with:
- System design
- Technology stack
- Design patterns
- Infrastructure
- Security & scalability
- Development environment]

---

## 5. Implementation Roadmap

[Complete implementation plan with:
- Project phases
- User stories
- Technical tasks
- Timeline & estimates
- Risk management
- Success criteria]

---

## 6. Conclusions & Recommendations

### 6.1 Key Findings
[Summarize main discoveries]

### 6.2 Strategic Recommendations
[Actionable next steps]

### 6.3 Expected Impact
[What success looks like]

### 6.4 Future Work
[What to explore next]

---

## 7. References

[All papers, articles, repositories mentioned]

---

## 8. Appendices

### Appendix A: Research Keywords
[Full list of keywords]

### Appendix B: Tool References
[Libraries and frameworks mentioned]

### Appendix C: Additional Resources
[Further reading]

---

**Generated by**: ARA Framework (LangGraph)
**Research Agent**: Content Synthesizer
**Quality Assurance**: Automated synthesis and validation
```

**CRITICAL:**
- Maintain professional, academic tone
- Be comprehensive but avoid unnecessary verbosity
- Ensure all sections flow logically
- Check for consistency in terminology
- Save final report to database for persistence
""")
        
        human_msg = HumanMessage(content=f"Synthesize final report for: {state['niche']}")
        
        # Invoke agent
        result = agent.invoke({
            "messages": [system_msg, human_msg]
        })
        
        # Extract final report
        final_report = result["messages"][-1].content
        
        # Mark end time
        end_time = datetime.now(timezone.utc).isoformat()
        
        logger.info(
            "content_synthesizer_completed",
            output_length=len(final_report),
            tool_calls=len([m for m in result["messages"] if hasattr(m, "tool_calls") and m.tool_calls]),
            total_agents=len(state.get("agent_history", [])) + 1,
        )
        
        return {
            **state,
            "final_report": final_report,
            "current_agent": "completed",
            "agent_history": state.get("agent_history", []) + ["content_synthesizer"],
            "messages": state.get("messages", []) + result["messages"],
            "end_time": end_time,
        }
        
    except Exception as e:
        logger.error(
            "content_synthesizer_failed",
            error=str(e),
            error_type=type(e).__name__,
        )
        
        errors = state.get("errors", [])
        errors.append(f"ContentSynthesizer: {str(e)}")
        
        retry_count = state.get("retry_count", {})
        retry_count["content_synthesizer"] = retry_count.get("content_synthesizer", 0) + 1
        
        return {
            **state,
            "errors": errors,
            "retry_count": retry_count,
        }


# =============================================================================
# Conditional Edge Functions
# =============================================================================

def should_retry_or_continue(state: ResearchState) -> Literal["retry", "continue", "fail"]:
    """
    Determines whether to retry an agent, continue to next, or fail.
    
    Logic:
    - If errors exist and retry count < 3: retry
    - If errors exist and retry count >= 3: fail
    - If no errors: continue
    """
    current_agent = state.get("current_agent", "")
    errors = state.get("errors", [])
    retry_count = state.get("retry_count", {})
    
    # Check if current agent has errors
    agent_errors = [e for e in errors if current_agent in e.lower()]
    
    if not agent_errors:
        # No errors, continue to next agent
        return "continue"
    
    # Check retry count
    agent_retry = retry_count.get(current_agent, 0)
    max_retries = 3
    
    if agent_retry < max_retries:
        logger.warning(
            "agent_retry_needed",
            agent=current_agent,
            retry_count=agent_retry,
            max_retries=max_retries,
        )
        return "retry"
    else:
        logger.error(
            "agent_failed_max_retries",
            agent=current_agent,
            retry_count=agent_retry,
            errors=agent_errors,
        )
        return "fail"


def check_budget(state: ResearchState) -> Literal["continue", "stop"]:
    """
    Checks if budget has been exceeded.
    
    Returns:
        "continue" if budget OK
        "stop" if budget exceeded
    """
    total_credits = state.get("total_credits_used", 0.0)
    budget_limit = state.get("budget_limit", 10.0)
    
    if total_credits >= budget_limit:
        logger.error(
            "budget_exceeded",
            total_credits=total_credits,
            budget_limit=budget_limit,
        )
        return "stop"
    
    return "continue"


# =============================================================================
# Graph Builder
# =============================================================================

def create_research_graph(
    enable_checkpointing: bool = True,
    checkpoint_backend: Literal["memory", "redis"] = "memory",
) -> StateGraph:
    """
    Creates the LangGraph research pipeline.
    
    Args:
        enable_checkpointing: Enable state persistence
        checkpoint_backend: "memory" for dev, "redis" for production
    
    Returns:
        Compiled StateGraph ready for execution
    
    Usage:
        ```python
        graph = create_research_graph()
        
        result = await graph.ainvoke({
            "niche": "Rust WebAssembly for audio processing",
            "messages": [],
            "agent_history": [],
            "errors": [],
            "warnings": [],
            "retry_count": {},
            "total_credits_used": 0.0,
            "budget_limit": 10.0,
            "budget_exceeded": False,
            "start_time": datetime.now(timezone.utc).isoformat(),
        })
        
        print(result["final_report"])
        ```
    """
    logger.info(
        "creating_research_graph",
        checkpointing=enable_checkpointing,
        backend=checkpoint_backend if enable_checkpointing else None,
    )
    
    # Initialize graph
    workflow = StateGraph(ResearchState)
    
    # Add agent nodes
    workflow.add_node("niche_analyst", niche_analyst_node)
    workflow.add_node("literature_researcher", literature_researcher_node)
    workflow.add_node("technical_architect", technical_architect_node)
    workflow.add_node("implementation_specialist", implementation_specialist_node)
    workflow.add_node("content_synthesizer", content_synthesizer_node)
    
    # Set entry point
    workflow.set_entry_point("niche_analyst")
    
    # Add sequential edges (happy path)
    workflow.add_edge("niche_analyst", "literature_researcher")
    workflow.add_edge("literature_researcher", "technical_architect")
    workflow.add_edge("technical_architect", "implementation_specialist")
    workflow.add_edge("implementation_specialist", "content_synthesizer")
    workflow.add_edge("content_synthesizer", END)
    
    # TODO: Add conditional edges for retry/error handling
    # This would require modifying the node functions to return control flags
    # For v1, we'll use simple sequential flow with exception handling in nodes
    
    # Set up checkpointing
    checkpointer = None
    if enable_checkpointing:
        if checkpoint_backend == "memory":
            checkpointer = MemorySaver()
            logger.info("checkpointing_enabled", backend="memory")
        elif checkpoint_backend == "redis":
            # TODO: Implement Redis checkpointing
            # from langgraph.checkpoint.redis import RedisSaver
            # checkpointer = RedisSaver(...)
            logger.warning(
                "redis_checkpointing_not_implemented",
                fallback="memory",
            )
            checkpointer = MemorySaver()
        else:
            logger.warning(
                "unknown_checkpoint_backend",
                backend=checkpoint_backend,
                fallback="memory",
            )
            checkpointer = MemorySaver()
    
    # Compile graph
    graph = workflow.compile(checkpointer=checkpointer)
    
    logger.info("research_graph_created", nodes=5, checkpointing=checkpointer is not None)
    
    return graph


# =============================================================================
# Convenience Functions
# =============================================================================

async def run_research_pipeline(
    niche: str,
    budget_limit: float = 10.0,
    enable_checkpointing: bool = True,
) -> ResearchState:
    """
    Convenience function to run the complete research pipeline.
    
    Args:
        niche: Research topic/niche to analyze
        budget_limit: Maximum credits to spend (mostly for LLM calls)
        enable_checkpointing: Enable state persistence
    
    Returns:
        Final state with completed research report
    
    Example:
        ```python
        result = await run_research_pipeline(
            niche="Rust WebAssembly for real-time audio processing",
            budget_limit=10.0,
        )
        
        print(result["final_report"])
        ```
    """
    logger.info(
        "starting_research_pipeline",
        niche=niche,
        budget_limit=budget_limit,
    )
    
    # Create graph
    graph = create_research_graph(
        enable_checkpointing=enable_checkpointing,
        checkpoint_backend="memory",
    )
    
    # Initialize state
    initial_state: ResearchState = {
        "niche": niche,
        "niche_analysis": None,
        "literature_review": None,
        "technical_architecture": None,
        "implementation_plan": None,
        "final_report": None,
        "messages": [],
        "current_agent": "niche_analyst",
        "agent_history": [],
        "start_time": datetime.now(timezone.utc).isoformat(),
        "end_time": None,
        "errors": [],
        "warnings": [],
        "retry_count": {},
        "total_credits_used": 0.0,
        "budget_limit": budget_limit,
        "budget_exceeded": False,
        "checkpoint_id": None,
    }
    
    # Execute graph
    try:
        result = await graph.ainvoke(initial_state)
        
        logger.info(
            "research_pipeline_completed",
            niche=niche,
            agents_executed=len(result.get("agent_history", [])),
            has_final_report=result.get("final_report") is not None,
            errors_count=len(result.get("errors", [])),
        )
        
        return result
        
    except Exception as e:
        logger.error(
            "research_pipeline_failed",
            niche=niche,
            error=str(e),
            error_type=type(e).__name__,
        )
        raise


if __name__ == "__main__":
    # Example usage
    import asyncio
    
    async def main():
        result = await run_research_pipeline(
            niche="Rust WebAssembly for real-time audio processing",
            budget_limit=10.0,
        )
        
        if result["final_report"]:
            print("=" * 80)
            print("RESEARCH COMPLETED SUCCESSFULLY")
            print("=" * 80)
            print(result["final_report"][:1000])
            print("...")
            print(f"\nTotal agents executed: {len(result['agent_history'])}")
            print(f"Errors: {len(result['errors'])}")
        else:
            print("Research failed!")
            print(f"Errors: {result['errors']}")
    
    asyncio.run(main())
