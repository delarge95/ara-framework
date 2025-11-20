# 📋 ARA Framework - Execution Plan

**Version**: 2.2.0  
**Created**: 2025-11-08  
**Last Updated**: 2025-12-19  
**Status**: ARA 2.2 Incremental Upgrade - Sprint Planning  
**Strategy**: Preserve existing LangGraph pipeline while adding enterprise features
**Related**: `.speckit/constitution.md`, `.speckit/specifications.md`, `.speckit/tasks.md`

---

## 🎯 Executive Summary

### Current State ✅

- **LangGraph Pipeline**: Fully migrated from CrewAI, operational
- **6 AI Agents**: All implemented and functional (NicheAnalyst, LiteratureResearcher, TechnicalArchitect, ImplementationSpecialist, ContentSynthesizer, Orchestrator)  
- **Budget System**: Real-time tracking with emergency stops working
- **Frontend**: React dashboard with human gates operational
- **MCP Integration**: Base servers connected (filesystem, GitHub, postgres)
- **Basic Router**: Model factory with simple routing logic in place

### Upgrade Goal 🚀

- **Target**: ARA 2.2 Production Features via Incremental Migration
- **Timeline**: 5 weeks (4 sprints + 1 validation)  
- **Strategy**: Preserve existing functionality while adding enterprise capabilities
- **Priority**: Router upgrade → Telemetry → Security → Chaos → Validation

---

## 🗓️ Sprint Breakdown

### **FASE 0: Estabilización Base** (Semana 0) 🚨 PREREQUISITO

**Objetivo**: Resolver issues existentes ANTES de agregar ARA 2.2

**Situación Actual** (Estado real del código):
```
Total Tests: 23/43 passing (53%)

✅ test_pipeline.py: 16/16 (100%)
❌ test_budget_manager.py: 2/13 (15%)
   - 9 ERRORS: redis import path issues
   - 2 FAILED: BudgetStatus constructor problems
❌ test_tools.py: 5/14 (36%)
   - 3 ERRORS: fixture naming conflicts
   - 6 FAILED: MCP attribute assumptions
```

**Por qué es crítico**: No podemos construir ARA 2.2 sobre una base con 20 tests failing. Primero estabilizar.

**Key Deliverables**:
- [ ] **0.1**: Fix redis import errors in budget_manager tests
- [ ] **0.2**: Resolve BudgetStatus constructor issues  
- [ ] **0.3**: Fix MCP attribute assumptions in tools tests
- [ ] **0.4**: Resolve fixture naming conflicts
- [ ] **0.5**: CLI end-to-end validation working
- [ ] **0.6**: Documentation updated to reflect current state

**Essential Mocking Patterns** (PRESERVAR):
```python
# Session-level mock to avoid import errors
@pytest.fixture(scope="session", autouse=True)
def mock_langchain_google_genai():
    fake_module = MagicMock()
    fake_module.ChatGoogleGenerativeAI = MagicMock()
    sys.modules['langchain_google_genai'] = fake_module
    sys.modules['langchain_google_genai._enums'] = fake_module
    yield

# Test-level mocks for current LangGraph system
with patch('core.pipeline.create_research_graph', return_value=mock_graph):
    with patch('agents.niche_analyst.create_niche_analyst', return_value=(mock_agent, mock_task)):
        # Execute test
```

**Debug Commands** (del archivo viejo):
```bash
# Run specific failing tests
python -m pytest tests/test_budget_manager.py::test_budget_status -v
python -m pytest tests/test_tools.py::test_scraping_tool_scrape -v

# Check import paths
python -c "import core.budget_manager; print('Budget manager OK')"
python -c "import tools; print('Tools import OK')"

# Validate CLI
python -m ara_framework.cli.main --help
```

**Success Criteria**: 43/43 tests passing, CLI working, documentation current

---

### **Sprint 1: Router 2.2 Upgrade** (Weeks 1-2)

**Objective**: Replace basic model factory with cache-first adaptive router

**Migration Strategy**: 
- Keep existing `model_factory.py` interface
- Implement new `AdaptiveRouter.ts` underneath
- Gradual cutover with feature flags

**Key Deliverables**:
- [ ] **AdaptiveRouter.ts**: Cache-first with GTE embeddings
- [ ] **Model Cards**: Event-driven subscription system  
- [ ] **Cache System**: LRU cache with 15min TTL + invalidation
- [ ] **Novelty Detection**: LightGBM classifier for routing decisions
- [ ] **Performance**: Cache hit >90%, latency p95 <50ms

**Testing Requirements**:
- [ ] 200 prompt routing corpus for validation
- [ ] Cache invalidation tests
- [ ] Fallback chain verification
- [ ] Existing agent compatibility confirmation

---

### **Sprint 2: Telemetry Pipeline** (Week 3)

**Objective**: Add production observability without disrupting current system

**Migration Strategy**:
- Overlay telemetry on existing components
- Connect to current React dashboard
- Non-breaking instrumentation

**Key Deliverables**:
- [ ] **Prometheus Metrics**: `/metrics` endpoint with 15+ metrics
- [ ] **Structured Logging**: Correlation IDs across components
- [ ] **Real-time Dashboard**: Connect metrics to existing frontend
- [ ] **Alert Definitions**: P0/P1/P2 classification system
- [ ] **Jaeger Tracing**: Distributed tracing for MVP lifecycle

**Metrics to Implement**:
- Router: `ara_router_cache_hit_rate`, `ara_router_latency_ms`
- Gates: `ara_gate_pending_total`, `ara_gate_approval_time_seconds`  
- Economic: `ara_cost_per_mvp_usd`, `ara_token_usage_millions`
- Security: `ara_shield_hallucination_blocked_total`

---

### **Sprint 3: Security & Gates Upgrade** (Week 4)

**Objective**: Enhance security and human governance systems

**Migration Strategy**:
- Upgrade existing security tools to ARAShield 2.2
- Replace current gate system with optimistic locking
- Maintain current UI while adding batch capabilities

**Key Deliverables**:
- [ ] **ARAShield 2.2**: Two-tier package validation (fast + async)
- [ ] **Supply Chain Protection**: CVE scanning + registry validation
- [ ] **GateOrchestrator**: Optimistic locking with TOCTOU prevention
- [ ] **Batch Approvals**: UI for approving multiple gates
- [ ] **PII Sanitization**: Dual-phase NER + async scrubbing
- [ ] **Audit Logs**: Immutable trails with ed25519 signatures

**Security Standards**:
- Package hallucination detection: >99.5% accuracy
- False positive rate: <8%
- CVE detection: <24h from disclosure
- TOCTOU conflicts: <0.1%

---

### **Sprint 4: Chaos Engineering** (Week 5)

**Objective**: Implement automated robustness testing

**Migration Strategy**:
- Add chaos system as separate module
- Non-invasive testing of current pipeline
- Configurable threat models

**Key Deliverables**:
- [ ] **Threat Models**: 3 basic attack patterns implemented
- [ ] **Attack Generator**: Automated prompt generation for testing
- [ ] **Robustness Scoring**: Quantified resistance metrics
- [ ] **Failure Classification**: Categorize and track failure types
- [ ] **Reporting System**: Automated robustness reports

**Chaos Capabilities**:
- Routing poisoning tests (50 attacks)
- Package hallucination tests (100 attacks)  
- Drift cascade tests (30 attacks)
- Budget >$50 for meaningful testing

---

## 🔧 Migration Architecture

### Interface Preservation Strategy

```typescript
// Keep existing interface working
interface ModelFactory {
  getModel(task: Task): Promise<Model>;
}

// Current implementation (model_factory.py)
class CurrentModelFactory implements ModelFactory {
  // Existing logic preserved
}

// New implementation (AdaptiveRouter.ts) 
class AdaptiveRouterFactory implements ModelFactory {
  // ARA 2.2 logic with same interface
}

// Feature flag controlled cutover
const factory: ModelFactory = 
  config.useAdaptiveRouter ? 
    new AdaptiveRouterFactory() : 
    new CurrentModelFactory();
```

### Telemetry Overlay Pattern

```python
# Existing code (preserved)
def execute_agent(agent, task):
    result = agent.run(task)
    return result

# Instrumented version (non-breaking)
@telemetry.trace("agent_execution")
def execute_agent(agent, task):
    with telemetry.timer("agent_duration"):
        result = agent.run(task)
        telemetry.increment("agent_calls", tags={"agent": agent.name})
    return result
```

### Security Enhancement Pattern

```python
# Current tool (preserved)
class DatabaseTool:
    def execute(self, query):
        return self.db.query(query)

# Enhanced version (backward compatible)
class DatabaseTool:
    def execute(self, query):
        # Add ARAShield validation
        if self.shield.validate_query(query):
            result = self.db.query(query)
            self.audit.log_access(query, result)
            return result
        else:
            raise SecurityError("Query blocked by ARAShield")
```

---

## 📊 Success Criteria by Sprint

### Sprint 1 Success Metrics
- **Functional**: All existing agents work without modification
- **Performance**: Router latency p95 <50ms, cache hit >90%
- **Compatibility**: Zero breaking changes to current API
- **Quality**: Router accuracy >98% vs ground truth

### Sprint 2 Success Metrics  
- **Observability**: 15+ metrics exposed on `/metrics`
- **Performance**: Telemetry overhead <2ms per request
- **Integration**: Real-time dashboard showing live metrics
- **Alerting**: P0/P1 alerts fire within 5 minutes

### Sprint 3 Success Metrics
- **Security**: Package hallucination <0.3% false negative
- **Governance**: TOCTOU conflicts <0.1%
- **Usability**: Batch approval reduces gate time by 60%
- **Compliance**: Audit logs pass external review

### Sprint 4 Success Metrics
- **Robustness**: Find ≥1 new vulnerability per threat model
- **Coverage**: All major attack vectors tested
- **Automation**: Chaos runs without human intervention
- **Reporting**: Clear robustness score trends

---

## 🛡️ Risk Management

### High-Priority Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|---------|------------|
| **Router migration breaks agents** | Medium | High | Feature flag + rollback plan |
| **Telemetry overhead degrades performance** | Low | High | Performance budget + monitoring |
| **Security changes block legitimate code** | Medium | Medium | Whitelist + manual override |
| **Chaos testing breaks production** | Low | High | Isolated test environment |

### Rollback Strategy

Each sprint has a clean rollback path:
- **Sprint 1**: Feature flag to disable AdaptiveRouter
- **Sprint 2**: Telemetry can be disabled via config
- **Sprint 3**: Security policies configurable
- **Sprint 4**: Chaos testing is optional module

---

## 🎯 Final Validation (Week 6)

### End-to-End MVP Test
- **Input**: "Build a todo app with auth"
- **Expected**: Complete MVP from architecture → deployment
- **Metrics**: <6 hours total, <$50 cost, <20% human intervention

### Performance Benchmarks
- **Router**: Cache hit >94%, latency p95 <15ms
- **Gates**: Approval time p95 <30min, TOCTOU <0.1%  
- **Security**: False positive <8%, hallucination detection >99.5%
- **Overall**: MVP success rate >80%

### Production Readiness Checklist
- [ ] All tests passing (including new ARA 2.2 features)
- [ ] Documentation updated for new capabilities
- [ ] Monitoring dashboard operational
- [ ] Security policies configured
- [ ] Chaos testing demonstrates robustness >baseline

---

**Next Steps**: Begin Sprint 1 with AdaptiveRouter implementation. All work should maintain backward compatibility with existing LangGraph pipeline.
