# 🛠️ Development Guide - ARA Framework

Complete guide for setting up your development environment.

---

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/delarge95/ara-framework.git
cd ara-framework/ara_framework

# 2. Setup environment (automated)
./scripts/setup_environment.sh --dev

# 3. Configure
cp .env.example .env
# Edit .env with your API keys

# 4. Test
pytest tests/ -v

# 5. Run
ara run "Your research topic"
```

---

## Detailed Setup

### 1. Python Environment

**Required: Python 3.12+**

Check version:
```bash
python3 --version  # Should be 3.12.0 or higher
```

Install if needed:
```bash
# Ubuntu/Debian
sudo apt install python3.12 python3.12-venv

# macOS (Homebrew)
brew install python@3.12

# Windows
# Download from python.org
```

### 2. Virtual Environment

```bash
# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Verify
which python  # Should point to .venv/bin/python
```

### 3. Dependencies

```bash
# Core dependencies
pip install -r requirements.txt

# Development dependencies (includes core)
pip install -r requirements-dev.txt

# Verify installation
pip list | grep crewai
```

### 4. External Services

#### Redis/Valkey (Required)

**Docker (Recommended):**
```bash
docker run -d --name valkey -p 6379:6379 valkey/valkey:latest
```

**Ubuntu/Debian:**
```bash
sudo apt install valkey
sudo systemctl start valkey
```

**macOS:**
```bash
brew install valkey
brew services start valkey
```

**Verify:**
```bash
redis-cli ping  # Should return "PONG"
```

#### Playwright Browsers

```bash
playwright install chromium
```

#### Supabase (Optional)

- Create account at [supabase.com](https://supabase.com)
- Create new project
- Copy URL and keys to .env

### 5. Environment Variables

```bash
cp .env.example .env
```

**Minimum required:**
```bash
# Free tier - Enough to get started
GEMINI_API_KEY=your_key_here  # Get from ai.google.dev
DEEPSEEK_API_KEY=your_key_here  # Get from platform.deepseek.com
REDIS_URL=redis://localhost:6379/0
```

**Recommended:**
```bash
# Add for full functionality
OPENAI_API_KEY=your_key_here  # Or use Copilot Pro
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=your_key_here
GITHUB_PERSONAL_ACCESS_TOKEN=ghp_xxx
```

---

## Development Workflow

### 1. Code Changes

```bash
# Create feature branch
git checkout -b feature/my-feature

# Make changes
# Edit files...

# Format code
black .

# Lint
ruff check .

# Type check (optional)
mypy ara_framework/
```

### 2. Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_pipeline.py::test_name -v

# With coverage
pytest tests/ --cov=ara_framework --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

### 3. Integration Testing

```bash
# Quick integration test
pytest tests/test_integration_simple.py

# Full E2E test (60-75 min)
pytest tests/test_e2e_full.py
```

### 4. Manual Testing

```bash
# Via CLI
ara run "Rust WebAssembly for audio"

# Via Python
python tests/test_integration_simple.py

# Check budget
ara budget
```

---

## Project Structure

```
ara_framework/
├── agents/           # AI agents
├── core/             # Pipeline & budget manager
├── tools/            # MCP-based tools
├── mcp_servers/      # MCP server implementations
├── cli/              # Command-line interface
├── config/           # Settings & configuration
├── scripts/          # Utility scripts
└── tests/            # All tests here
    ├── test_*.py                # Unit tests
    ├── test_integration_*.py    # Integration tests
    └── test_e2e_*.py            # End-to-end tests
```

---

## Common Tasks

### Add New Agent

1. Create file in `agents/`:
```python
# agents/my_agent.py
from crewai import Agent
from config.settings import settings

def create_my_agent() -> Agent:
    return Agent(
        role="My Role",
        goal="My goal",
        backstory="Context...",
        llm="gemini/gemini-2.5-pro",
        tools=[...],
        verbose=True
    )
```

2. Add to `agents/__init__.py`
3. Update pipeline in `core/pipeline.py`
4. Add tests in `tests/test_agents.py`

### Add New Tool

1. Create file in `tools/`:
```python
# tools/my_tool.py
from crewai.tools import tool

@tool
def my_tool(query: str) -> str:
    """Tool description for LLM."""
    # Implementation
    return result
```

2. Add to `tools/__init__.py`
3. Add tests in `tests/test_tools.py`

### Add New MCP Server

1. Create file in `mcp_servers/`:
```python
# mcp_servers/my_mcp.py
from mcp_servers.base import BaseMCPServer

class MyMCPServer(BaseMCPServer):
    def __init__(self):
        super().__init__(name="my_mcp")
    
    async def execute(self, action: str, params: dict) -> dict:
        # Implementation
        pass
```

2. Integrate into relevant tool
3. Add tests

---

## Debugging

### Enable Debug Logging

```bash
# In .env
DEBUG=true
LOG_LEVEL=DEBUG
```

### Use Python Debugger

```python
import pdb; pdb.set_trace()  # Breakpoint

# Or with ipdb (better)
import ipdb; ipdb.set_trace()
```

### Check Redis Data

```bash
redis-cli
> KEYS *
> GET key_name
> TTL key_name
```

### View Traces

If Uptrace configured:
```bash
# In .env
UPTRACE_DSN=https://token@api.uptrace.dev/project_id

# View at: https://app.uptrace.dev
```

---

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
# Reinstall in editable mode
pip install -e .
```

### Issue: Redis connection error

**Solution:**
```bash
# Check Redis is running
redis-cli ping

# Or start it
docker start valkey
# or
sudo systemctl start redis
```

### Issue: API rate limits

**Solution:**
- Check .env has correct keys
- Wait for rate limit reset
- Use fallback models

### Issue: Tests failing

**Solution:**
```bash
# Clear cache
rm -rf .pytest_cache __pycache__

# Reinstall dependencies
pip install -r requirements-dev.txt --force-reinstall

# Run with verbose output
pytest tests/ -vv
```

---

## IDE Configuration

### VS Code

**Recommended extensions:**
- Python
- Pylance
- Black Formatter
- Ruff

**Settings (.vscode/settings.json):**
```json
{
  "python.defaultInterpreterPath": ".venv/bin/python",
  "python.formatting.provider": "black",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "editor.formatOnSave": true
}
```

### PyCharm

1. File → Settings → Project → Python Interpreter
2. Select `.venv/bin/python`
3. Enable Black formatter
4. Enable Ruff linter

---

## Performance Profiling

### Time Analysis

```python
import time
start = time.time()
# Code to profile
duration = time.time() - start
print(f"Took {duration:.2f}s")
```

### Memory Analysis

```bash
pip install memory-profiler

# Add decorator
from memory_profiler import profile

@profile
def my_function():
    # Code to profile
    pass
```

### Line Profiling

```bash
pip install line-profiler

# Add decorator
from line_profiler import LineProfiler

# Run
kernprof -l -v script.py
```

---

## Release Process

### Version Bump

1. Update version in `setup.py`
2. Update CHANGELOG.md
3. Create git tag:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Build Package

```bash
pip install build
python -m build
```

### Test Package

```bash
pip install dist/ara_framework-1.0.0-py3-none-any.whl
```

---

## Resources

- [CrewAI Docs](https://docs.crewai.com/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [pytest Documentation](https://docs.pytest.org/)

---

**Happy Coding!** 🚀
