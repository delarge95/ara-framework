# 🔧 ARA Framework - Technical Specifications

**Version**: 2.2.0  
**Created**: 2025-11-08  
**Last Updated**: 2025-12-19  
**Status**: ARA 2.2 Incremental Upgrade Specifications  
**Strategy**: Maintain existing interfaces while upgrading implementations
**Related**: `.speckit/constitution.md`, `.speckit/plan.md`

---

## 📦 Module Specifications - ARA 2.2

### 0. Current Module Status - MUST STABILIZE FIRST

**CRITICAL**: Los siguientes módulos están ROTOS y deben arreglarse antes de ARA 2.2:

#### Budget Manager (`core/budget_manager.py`) - BROKEN TESTS
**Current Issues**:
- 9 ERRORS: redis import path problems
- 2 FAILED: BudgetStatus constructor issues

**Current Working Mocks** (PRESERVE):
```python
# Mock patterns that work for current code
@patch('core.budget_manager.get_redis_client')
def test_budget_manager(mock_redis):
    mock_redis.return_value = MagicMock()
    # Test budget manager functionality
```

#### Tools Module (`tools/*.py`) - BROKEN TESTS  
**Current Issues**:
- 6 FAILED: MCP attribute assumptions
- 3 ERRORS: fixture naming conflicts

**Current Working Interface** (PRESERVE):
```python
# Current tool structure - DO NOT BREAK
class ScrapingTool:
    def scrape(self, url: str) -> str:
        # Current implementation works in pipeline
        pass

class DatabaseTool:
    def execute(self, query: str) -> Any:
        # Current implementation works in pipeline
        pass
```

#### Testing Strategy for Current Code
```python
# Critical mocking patterns that MUST be preserved
@pytest.fixture(scope="session", autouse=True)
def mock_langchain_google_genai():
    fake_module = MagicMock()
    fake_module.ChatGoogleGenerativeAI = MagicMock()
    sys.modules['langchain_google_genai'] = fake_module
    sys.modules['langchain_google_genai._enums'] = fake_module
    yield

# LangGraph mocking (current system)
@patch('core.pipeline.create_research_graph')
def test_pipeline(mock_graph):
    mock_graph.return_value = MagicMock()
    # Test current pipeline
```

---

### 1. AdaptiveRouter (`core/router/AdaptiveRouter.ts`) - NEW

#### Purpose
Replace basic model factory with intelligent, cache-first routing system.

#### Migration Strategy
- Preserve `ModelFactory` interface from `model_factory.py`
- Implement underneath with TypeScript for performance
- Feature flag controlled cutover

#### Implementation

```typescript
interface ModelCard {
  modelId: string;
  gpqaDiamond: number;
  swebenchVerified: number;
  contextWindow: number;
  costPerMln: number;
  latencyP95: number;
  lastUpdated: Timestamp;
  signature: string; // ed25519 for integrity
}

class AdaptiveRouter {
  private cache: LRUCache<string, RoutingDecision>;
  private localEmbedder: GTEEmbeddingModel;
  private modelCards: Observable<ModelCard[]>;
  private classifier: NoveltyDetector; // LightGBM

  async route(task: Task): Promise<RoutingDecision> {
    // 1. Novelty detection (2ms)
    if (this.classifier.predictNovelty(task) > 0.85) {
      return await this._routeWithGemini(task);
    }

    // 2. Cache lookup (0.5ms) 
    const cacheKey = this._computeCacheKey(task);
    const cached = this.cache.get(cacheKey);
    if (cached) return cached;

    // 3. Local routing with embeddings (5ms)
    const decision = await this._localRoute(task);
    
    // 4. Async cache update
    this._updateCache(cacheKey, decision).catch(console.error);
    
    return decision;
  }
}
```

#### Performance Requirements
- Cache hit rate: >94%
- Latency p95: <15ms for cache hit, <300ms for novelty path
- Model card invalidation: <30s after update
- Misroute rate: <0.1% vs ground truth

---

### 2. Telemetry Engine (`telemetry/`) - NEW

#### Purpose
Production-grade observability overlaid on existing system.

#### Components

##### Prometheus Metrics
```yaml
metrics:
  # Router performance
  - name: ara_router_cache_hit_rate
    type: gauge
    labels: [model_id, route_type]
    
  - name: ara_router_latency_ms
    type: histogram
    buckets: [1, 5, 10, 25, 50, 100, 250, 500]
    
  # Gate management
  - name: ara_gate_pending_total
    type: gauge
    labels: [gate_type]
    
  - name: ara_gate_approval_time_seconds
    type: histogram
    labels: [gate_type, batch_size]
    
  # Economic tracking
  - name: ara_cost_per_mvp_usd
    type: histogram
    buckets: [1000, 2000, 3000, 5000, 10000]
    labels: [mvp_mode]
    
  # Security
  - name: ara_shield_hallucination_blocked_total
    type: counter
    labels: [shield_type, confidence]
```

##### Integration Pattern (Non-Breaking)
```python
# Current code (preserved)
def execute_pipeline(task):
    result = pipeline.run(task)
    return result

# Instrumented version
@telemetry.trace("pipeline_execution")
def execute_pipeline(task):
    with telemetry.timer("pipeline_duration"):
        result = pipeline.run(task)
        telemetry.increment("pipeline_calls")
        telemetry.histogram("pipeline_cost", result.cost)
    return result
```

#### Requirements
- Telemetry overhead: <2ms per request
- Metrics export: `/metrics` endpoint
- Real-time dashboard: Connect to existing React frontend
- Alert latency: P0 alerts within 5 minutes

---

### 3. ARAShield 2.2 (`shields/`) - ENHANCED

#### Purpose
Upgrade existing security tools with two-tier validation and supply chain protection.

#### Current Enhancement Strategy
```python
# Existing tool (preserved interface)
class DatabaseTool:
    def execute(self, query):
        return self.db.query(query)

# Enhanced with ARAShield 2.2
class DatabaseTool:
    def __init__(self):
        self.shield = SupplyChainShield()  # NEW
        
    def execute(self, query):
        # NEW: Two-tier validation
        validation = await self.shield.validate_dependency(query)
        if not validation.approved:
            raise SecurityError(f"Blocked: {validation.reason}")
            
        result = self.db.query(query)
        
        # NEW: Audit logging
        self.shield.audit_log.append({
            "action": "database_query",
            "query": sanitize_pii(query),
            "result_size": len(result),
            "timestamp": datetime.now()
        })
        
        return result
```

#### Two-Tier Validation System
```python
class SupplyChainShield:
    async def validate_dependency(self, package: str) -> ValidationResult:
        # Tier 1: Fast path (10ms)
        if package in self.whitelist:
            return ValidationResult(approved=True, tier=1)
            
        # Tier 2: Cache lookup (50ms)
        cached = await self.registry_cache.get(package)
        if cached:
            return cached
            
        # Tier 3: Registry API + async Gemini verification (100ms)
        exists = await self._check_registry_fast(package)
        if not exists:
            return ValidationResult(
                approved=False,
                reason='HALLUCINATED_PACKAGE',
                confidence=0.98
            )
            
        # Async background verification
        asyncio.create_task(self._gemini_verify_package(package))
        
        result = ValidationResult(approved=True, tier=3)
        await self.registry_cache.set(package, result)
        return result
```

#### Requirements
- Package hallucination detection: >99.5% accuracy
- False positive rate: <5% for legitimate packages  
- CVE detection: <24h from disclosure
- Registry lookup: 99.9% <100ms without rate limits

---

### 4. GateOrchestrator (`core/gates/`) - ENHANCED

#### Purpose
Upgrade current human gates with optimistic locking and batch processing.

#### Enhanced Implementation
```typescript
interface Gate {
  id: string;
  type: 'critical' | 'advisory';
  commitHash: string;
  snapshotHash: string; // NEW: TOCTOU prevention
  requiredApprovals: number;
  currentApprovals: Map<string, Approval>;
  createdAt: Timestamp;
  expiresAt: Timestamp;
}

class GateOrchestrator {
  async approveGate(gateId: string, userId: string): Promise<Result> {
    const gate = await this.queue.get(gateId);
    
    // NEW: Optimistic locking check
    const currentHash = await this._getCurrentProjectSnapshotHash();
    if (currentHash !== gate.snapshotHash) {
      return {
        success: false,
        error: 'TOCTOU_DETECTED',
        message: 'Project changed since gate created. Re-review required.'
      };
    }

    gate.currentApprovals.set(userId, {
      timestamp: now(),
      userId,
      ip: getClientIP()
    });

    // Critical gates require multi-approval
    if (gate.type === 'critical' && 
        gate.currentApprovals.size < gate.requiredApprovals) {
      await this._notifyNextApprover(gate);
      return { success: true, status: 'PENDING_SECOND_APPROVAL' };
    }

    await this._executeGateAction(gate);
    
    // NEW: Immutable audit log
    await this.auditLog.append({
      gateId,
      action: 'EXECUTED',
      approvers: Array.from(gate.currentApprovals.keys()),
      hash: this._computeAuditHash(gate)
    });

    return { success: true, status: 'EXECUTED' };
  }
  
  // NEW: Batch approval capability
  async batchApprove(gateIds: string[], userId: string): Promise<BatchResult> {
    const results = await Promise.all(
      gateIds.map(id => this.approveGate(id, userId))
    );
    
    return {
      approved: results.filter(r => r.success).length,
      rejected: results.filter(r => !r.success).length,
      details: results
    };
  }
}
```

#### Requirements
- TOCTOU conflicts: <0.1%
- Batch approval time: <3 min for 5 gates
- Audit log: append-only, cryptographically signed
- Multi-signer support for critical gates

---

### 5. Chaos Engineering (`chaos/`) - NEW

#### Purpose
Automated robustness testing with threat model matrix.

#### Implementation
```python
class ChaosOrchestrator:
    def __init__(self, mode: str, budget: float):
        self.mode = mode  # lean | research | deeptech
        self.budget = self._allocate_budget(budget)
        self.threat_models = self._load_threat_models()
    
    def _allocate_budget(self, total: float) -> float:
        if self.mode == 'lean':
            return 0  # Manual chaos only
        elif self.mode == 'research':
            return total * 0.03  # 3% for ~150 attacks
        else:  # deeptech
            return total * 0.08  # 8% for ~500 attacks
    
    async def run_chaos_experiment(self, workflow: Workflow):
        for threat in self.threat_models:
            if self.budget < threat.cost_per_run:
                continue
                
            attacks = await self._generate_attacks(threat, workflow)
            
            for attack in attacks:
                result = await workflow.run(
                    attack.prompt, 
                    inject_fault=attack.fault
                )
                
                self._evaluate_resistance(threat, result)
                self.budget -= attack.cost
                
                if self.budget <= 0:
                    break
        
        await self._generate_robustness_report()
```

#### Threat Models
```python
THREAT_MODELS = [
    {
        "id": "routing_poisoning",
        "description": "Cache poisoning via crafted prompts",
        "cost_per_run": 0.015,
        "required_runs": 50,
        "success_criteria": "Router must maintain >98% accuracy"
    },
    {
        "id": "package_hallucination", 
        "description": "Model suggests vulnerable packages",
        "cost_per_run": 0.01,
        "required_runs": 100,
        "success_criteria": "Shield must block >99%"
    },
    {
        "id": "drift_cascade",
        "description": "Agent introduces breaking changes", 
        "cost_per_run": 0.02,
        "required_runs": 30,
        "success_criteria": "Drift detection triggers gate"
    }
]
```

#### Requirements
- Chaos runs: 1x/week in Research mode
- New failure classes: >0.5/quarter discovered
- Robustness score: quantified and trending
- Budget allocation: 3-8% based on mode

---

### 6. Model Context Protocol (`mcp/`) - ENHANCED

#### Purpose
Upgrade existing MCP integration to universal client.

#### Enhanced Implementation
```typescript
class UniversalMCPClient {
  private client: Client;
  private activeServer: string;
  
  async executeTool(toolName: string, args: any): Promise<any> {
    // NEW: Model-specific argument normalization
    const normalizedArgs = this._normalizeArgs(toolName, args);
    
    // NEW: Automatic instrumentation
    const start = Date.now();
    const result = await this.client.callTool(toolName, normalizedArgs);
    
    MCP_CLIENT_METRICS.latency_ms.record(Date.now() - start, {
      model_id: this.modelId,
      tool_name: toolName,
      server_id: this.activeServer
    });
    
    return result;
  }
  
  private _normalizeArgs(toolName: string, args: any): any {
    // Handle model-specific formats
    if (this.modelId.startsWith('claude')) {
      return toSnakeCase(args);
    } else if (this.modelId.startsWith('gpt')) {
      return toCamelCase(args);
    }
    return args;
  }
}
```

#### Requirements
- Connect time: <2s
- Tool call success: >98%
- Latency overhead: <10ms vs raw API
- Model compatibility: Claude, GPT, Gemini normalization

---

## 🧪 Testing Strategy for ARA 2.2

### Migration Testing
- **Backward Compatibility**: All existing agents must work unchanged
- **Performance Regression**: No degradation in current functionality
- **Feature Flag Testing**: Safe rollback for each component

### New Feature Testing
- **Router**: 200 prompt corpus + cache validation + fallback chains
- **Telemetry**: Metrics accuracy + overhead measurement + alerting
- **Security**: Package hallucination + CVE detection + audit trail verification
- **Gates**: TOCTOU simulation + batch approval + multi-signer workflows
- **Chaos**: Attack generation + robustness scoring + failure classification

### Integration Testing
- **End-to-End MVP**: Complete workflow from concept to deployment
- **Performance Benchmarks**: Latency, throughput, resource usage
- **Error Recovery**: Failure injection + graceful degradation
- **Budget Compliance**: Cost tracking + circuit breaker validation

---

## 📊 Architecture Decision Records

### ADR-001: Preserve LangGraph Pipeline
**Decision**: Maintain current LangGraph implementation as foundation
**Rationale**: Working system with 6 agents operational
**Consequences**: New features overlay existing architecture

### ADR-002: TypeScript for Router
**Decision**: Implement AdaptiveRouter in TypeScript
**Rationale**: Performance requirements + better caching control
**Consequences**: Mixed codebase but interfaces bridge cleanly

### ADR-003: Non-Breaking Telemetry
**Decision**: Instrument existing code without interface changes
**Rationale**: Minimize migration risk + preserve current functionality
**Consequences**: Decorator/wrapper patterns throughout

### ADR-004: Two-Tier Security
**Decision**: Fast whitelist + slow verification pattern
**Rationale**: Balance security with performance requirements
**Consequences**: More complex validation logic but better UX

### ADR-005: Optimistic Locking for Gates
**Decision**: Snapshot-based TOCTOU prevention
**Rationale**: Prevent race conditions in approval workflow
**Consequences**: More complex state management but safer operations

---

**Next**: Update `.speckit/tasks.md` with specific implementation tasks for each sprint.