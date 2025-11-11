# 🏗️ ARA Framework - Architecture Documentation

**Last Updated:** November 11, 2025  
**Version:** 1.0

---

## System Overview

ARA Framework is a **multi-agent research automation system** built on CrewAI that orchestrates specialized AI agents to produce comprehensive academic research reports.

### Core Principles

- **Modularity**: Each agent is independent and specialized
- **Sequential Processing**: Agents pass context through task dependencies
- **Cost Optimization**: Strategic use of free and paid LLM models
- **Observability**: Full telemetry with OpenTelemetry and structured logging

---

## Architecture Layers

### Layer 1: Entry Points (CLI/API)
- `cli/main.py` - Command-line interface
- `core/pipeline.py` - Programmatic API

### Layer 2: Orchestration
- `agents/orchestrator.py` - Pipeline coordinator
- `core/budget_manager.py` - Cost tracking

### Layer 3: Agents (5 specialized)
1. **NicheAnalyst** - Market viability (Gemini 2.5 Pro)
2. **LiteratureResearcher** - Academic review (Gemini 2.5 Pro)
3. **TechnicalArchitect** - System design (DeepSeek V3)
4. **ImplementationSpecialist** - Roadmap (Claude Haiku)
5. **ContentSynthesizer** - Report generation (GPT-4o)

### Layer 4: Tools (MCP-based)
- **SearchTool** - Semantic Scholar API
- **ScrapingTool** - Playwright MCP
- **PDFTool** - MarkItDown MCP
- **DatabaseTool** - Redis + Supabase

### Layer 5: MCP Servers
- semantic_scholar.py
- playwright_mcp.py
- markitdown_mcp.py
- supabase_mcp.py

---

## Multi-Agent Pipeline

**Total Time:** 60-75 minutes

```
Agent 1 (7-8 min) → Agent 2 (20-25 min) → Agent 3 (10-12 min) → 
Agent 4 (7-8 min) → Agent 5 (9-10 min) → Final Report
```

**Bottleneck:** LiteratureResearcher due to Semantic Scholar 1 RPS limit

---

## Technology Stack

**Core:**
- Python 3.12+
- CrewAI 0.80.0+
- FastAPI (async)
- Pydantic

**LLMs:**
- Gemini 2.5 Pro (FREE)
- DeepSeek V3 (FREE beta)
- Claude Haiku (0.33x credits)
- GPT-4o/GPT-5 (via Copilot Pro)

**Storage:**
- Redis/Valkey (cache)
- Supabase (optional persistence)
- ChromaDB (vector memory)

**Observability:**
- OpenTelemetry + Uptrace
- Structlog

---

## Performance & SLA

**Target:** 60-75 minutes per analysis

**Optimizations:**
- Caching (papers: 7 days, content: 3 days)
- Parallel queries
- Smart fallbacks

---

## Cost Model

**Monthly Budget:** $10-18
- Copilot Pro: $10/month
- Free models: Gemini, DeepSeek, GPT-4o

**Per Analysis:** $0.10-0.20
**Capacity:** 100 analyses/month with 85% buffer

---

For complete details, see [full analysis document](../ANALISIS_REPOSITORIO_COMPLETO.md).
