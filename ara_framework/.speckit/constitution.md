# 📜 ARA Framework - Project Constitution

**Version**: 2.2.0  
**Created**: 2025-11-08  
**Last Updated**: 2025-12-19  
**Status**: Active - Incremental Upgrade to ARA 2.2

---

## 🎯 Project Vision

**Mission Statement**:  
Build a production-ready, multi-LLM orchestration framework that autonomously constructs complete MVPs from concept to deployment, with intelligent model routing, human gates for critical decisions, and enterprise-grade observability.

**Evolution**: Migrating from academic research focus to full-stack MVP construction framework with integrated security, chaos engineering, and budget optimization.

**Core Purpose**:

- **MVP Construction**: Orchestrate 6-phase workflow from architecture to deployment
- **Intelligent Routing**: Cache-first model selection with event-driven invalidation
- **Budget Optimization**: Real-time cost tracking with automatic circuit breakers
- **Enterprise Security**: Supply chain protection with ARAShield 2.2
- **Human Governance**: Async gates with optimistic locking for critical decisions
- **Full Observability**: Prometheus + Jaeger + ClickHouse telemetry pipeline

---

## 🏛️ Architectural Principles

### 1. **Incremental Upgrade Strategy**

- Maintain existing LangGraph pipeline while upgrading components
- Preserve current agent structure and interfaces
- Add new features as overlays without breaking existing functionality
- Migration path: Current → ARA 2.2 over 4 sprints

### 2. **Production-Grade Observability**

- **Router Metrics**: Cache hit rate >94%, latency p95 <15ms, misroute rate <0.1%
- **Gate Metrics**: TOCTOU conflicts <0.1%, approval time p95 <30min
- **Security Metrics**: Package hallucination <0.3%, FP rate <8%
- **Economic Metrics**: Cost per MVP tracking, budget compliance >95%

### 3. **Multi-Model Intelligence**

- **Cache-First Routing**: GTE embeddings + LRU cache with 15min TTL
- **Event-Driven Updates**: Model card changes trigger cache invalidation
- **Fallback Chains**: Local → Cloud → Premium models based on task complexity
- **Budget-Aware**: Kill switches at 90% budget depletion

### 4. **Enterprise Security**

- **Two-Tier Validation**: Fast whitelist + async Gemini verification
- **Supply Chain Protection**: Registry validation + CVE scanning
- **PII Sanitization**: Dual-phase NER + async scrubbing
- **Audit Trails**: Immutable logs with ed25519 signatures
- Accept known version conflicts if non-blocking:
  - openai 2.7.1 vs <2.0.0 (langchain-openai)
  - protobuf 6.33.0 vs <6.0.0 (google packages)
- Mock problematic imports at test level

### 4. **Data Persistence**

- Primary: Supabase (PostgreSQL)
- Fallback: Local JSON files
- Caching: Redis (optional)
- No vendor lock-in - easily swappable backends

### 5. **Observability**

- Structured logging with structlog
- Budget alerts at 80% usage
- Execution time tracking per agent
- Error context preservation

---

## 📐 Technical Stack

### Core Dependencies

```
Python: 3.12.10
CrewAI: 0.100.0
pytest: 8.4.2
Pydantic: 2.12.4
```

### LLM Providers

```
openai: 2.7.1 (GPT-5)
anthropic: 0.72.0 (Claude Sonnet 4.5)
google-generativeai: TBD (Gemini 2.5 Pro)
deepseek: TBD (DeepSeek V3)
```

### Infrastructure

```
Supabase: PostgreSQL + Auth
Redis: Optional caching
Playwright: Web scraping
Semantic Scholar API: Academic search
```

---

## 🚧 Development Workflow

### 1. **Code Changes**

```bash
# Always work in feature branch
git checkout -b fix/test-budget-manager

# Make changes
# Run tests
pytest tests/test_budget_manager.py -v

# Commit with conventional commits
git commit -m "fix(tests): correct Redis mock patch path"
```

### 2. **Testing Protocol**

```bash
# Unit tests (fast, mocked)
pytest tests/ -v -m "not integration"

# Integration tests (slow, real APIs)
pytest tests/ -v -m integration

# Coverage report
pytest --cov=core --cov=agents --cov=tools --cov-report=html
```

### 3. **Documentation Requirements**

- Every new module needs docstring with examples
- Update README.md for user-facing changes
- Update ROADMAP_FUNCIONAL.md for architectural changes
- API changes require migration guide

---

## 🎭 Agent Design Philosophy

### Agent Hierarchy

```
1. NicheAnalyst (Gemini 2.5 Pro)
   ↓ Market viability, trends, opportunities
2. LiteratureResearcher (GPT-5)
   ↓ Academic papers, state-of-art
3. TechnicalArchitect (Claude Sonnet 4.5)
   ↓ System design, tech stack
4. ImplementationSpecialist (DeepSeek V3)
   ↓ Implementation roadmap
5. ContentSynthesizer (GPT-5)
   ↓ Final executive report
```

### Agent Constraints

- Sequential execution (no parallel for now)
- Context passing via Crew tasks
- Max 3 retries per agent
- Budget check before each agent execution
- Timeout: 30min default, 60min for researcher

---

## 📊 Success Metrics - ARA 2.2 Migration

### FASE 0: Estabilización Base (Semana 0) 🚨 PREREQUISITO

- [ ] **Fix failing tests**: 23/43 → 43/43 passing
- [ ] **Budget Manager**: Resolve 11 failing tests (redis imports + constructor)
- [ ] **Tools Module**: Fix 9 failing tests (MCP assumptions + fixtures)  
- [ ] **CLI Validation**: End-to-end functionality verified
- [ ] **Documentation**: Updated to reflect current LangGraph implementation

**CRITICAL**: Base debe estar estable antes de agregar ARA 2.2 features

### Sprint 1: Router Upgrade (Weeks 1-2)

- [ ] AdaptiveRouter.ts with cache-first + GTE embeddings
- [ ] Cache hit rate >90% on test corpus
- [ ] Model card subscription + event-driven invalidation
- [ ] Router latency p95 <50ms (current interface preserved)
- [ ] All existing agents work without modification
- [ ] **PREREQUISITE**: FASE 0 completed (43/43 tests passing)

### Sprint 2: Telemetry Integration (Week 3)

- [ ] Prometheus metrics endpoint `/metrics`
- [ ] Structured logging with correlation IDs
- [ ] Router, gates, security, economic metrics instrumented
- [ ] Real-time dashboard connected to existing frontend
- [ ] Alert definitions: P0/P1/P2 classification

### Sprint 3: Security & Gates Upgrade (Week 4)

- [ ] ARAShield 2.2: Two-tier package validation
- [ ] GateOrchestrator with optimistic locking
- [ ] Supply chain CVE scanning <24h detection
- [ ] Human gates UI with batch approval
- [ ] PII sanitization pipeline (dual-phase)

### Sprint 4: Chaos Engineering & Validation (Week 5)

- [ ] Threat model matrix: 3 basic models implemented
- [ ] 200 prompts routing corpus for validation
- [ ] Robustness score calculator
- [ ] End-to-end MVP construction test
- [ ] Performance benchmarks vs current system

---

## 🔒 Non-Negotiables

### Security

- ✅ No API keys in code (use .env)
- ✅ Supabase RLS policies enabled
- ✅ Input validation for all user inputs
- ✅ Rate limiting to prevent abuse

### Code Quality

- ✅ Type hints for all functions
- ✅ Docstrings for public APIs
- ✅ pytest markers for test categorization
- ✅ Black formatting enforced

### Testing

- ✅ No test changes pipeline code
- ✅ Mocks isolate external dependencies
- ✅ Integration tests tagged separately
- ✅ Fixtures reusable across test files

---

## 🚫 Anti-Patterns to Avoid

### 1. **Avoid Stubbing CrewAI Internals**

❌ **Bad**: Patching `crewai.rag.embeddings`  
✅ **Good**: Patching `Crew()` constructor

### 2. **Avoid Hardcoded Paths**

❌ **Bad**: `/home/user/outputs/result.json`  
✅ **Good**: `Path(settings.OUTPUT_DIR) / "result.json"`

### 3. **Avoid Silent Failures**

❌ **Bad**: `except Exception: pass`  
✅ **Good**: `except Exception as e: logger.error(...); raise`

### 4. **Avoid Blocking I/O**

❌ **Bad**: `requests.get(url, timeout=None)`  
✅ **Good**: `async with httpx.AsyncClient() as client: await client.get(url, timeout=30.0)`

---

## 🔄 Change Management

### Breaking Changes

- Require approval in GitHub PR
- Update CHANGELOG.md with migration path
- Deprecation warnings for 2 versions before removal

### Feature Additions

- Must include tests (min 80% coverage)
- Update docs/examples
- Add to ROADMAP_FUNCIONAL.md

### Bug Fixes

- Regression test mandatory
- Root cause analysis in PR description
- Update error handling docs if needed

---

## 📞 Support & Communication

### Issue Reporting

```markdown
**Bug Report Template**:

- Environment: Python version, OS
- Steps to reproduce
- Expected vs Actual behavior
- Logs (with sensitive data redacted)
- Related test failures
```

### Feature Requests

```markdown
**Feature Request Template**:

- Use case / problem statement
- Proposed solution
- Alternatives considered
- Impact on existing features
```

---

## 🎓 Learning Resources

### For New Contributors

1. Read `INSTALLATION.md` - Setup guide
2. Read `PYTHON_COMPATIBILITY.md` - Dependency gotchas
3. Run `python test_api_connections.py` - Validate setup
4. Read `tests/conftest.py` - Understand fixtures
5. Read `ROADMAP_FUNCIONAL.md` - Current priorities

### For Core Development

1. Read `ANALISIS_ULTRATHINK_2025.md` - Architecture deep dive
2. Read `DEPENDENCY_FIX.md` - CrewAI migration history
3. Review `core/pipeline.py` - Orchestration logic
4. Review `agents/orchestrator.py` - Agent creation patterns

---

## 📋 Governance

### Decision Authority

- **Architectural Changes**: Require consensus
- **Dependency Updates**: Require testing validation
- **API Changes**: Require backward compatibility
- **Test Strategy**: Documented in TESTING.md

### Code Review Standards

- Min 1 approval for merges
- All tests must pass
- Coverage must not decrease
- Linting/formatting checks pass

---

## 🚀 Current State (as of 2025-12-19)

### Completed ✅

- **LangGraph Pipeline**: Migrated from CrewAI, fully functional
- **6 AI Agents**: All implemented and working (NicheAnalyst, LiteratureResearcher, TechnicalArchitect, ImplementationSpecialist, ContentSynthesizer, Orchestrator)
- **Budget Manager**: Real-time tracking with kill switches
- **Frontend Dashboard**: React-based with budget tracking and human gates
- **MCP Integration**: Base servers for filesystem, GitHub, PostgreSQL
- **Basic Router**: Model factory with simple routing logic

### Ready for Upgrade 🔄

- **Router → AdaptiveRouter 2.2**: Cache-first + GTE embeddings + model cards
- **Telemetry → Production Pipeline**: Prometheus + Jaeger + ClickHouse
- **Security → ARAShield 2.2**: Two-tier validation + supply chain protection
- **Gates → Optimistic Locking**: TOCTOU prevention + batch approval
- **Tests → 2.2 Compatibility**: Update existing tests for new features

### ARA 2.2 Features (Planned) 📅

- **Chaos Engineering**: Automated robustness testing
- **Model Cards**: Real-time capability tracking
- **PII Sanitization**: Dual-phase scrubbing pipeline
- **Advanced Caching**: Event-driven invalidation
- **Enterprise Security**: CVE scanning + audit trails

---

**Next Review**: After Phase 1 completion (43/43 tests passing)  
**Constitution Owner**: GitHub Copilot  
**Ratified**: 2025-11-08
