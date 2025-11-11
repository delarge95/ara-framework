# 🤝 Contributing to ARA Framework

Thank you for your interest in contributing to ARA Framework!

---

## 📋 Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Making Changes](#making-changes)
5. [Testing](#testing)
6. [Pull Request Process](#pull-request-process)
7. [Style Guidelines](#style-guidelines)

---

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the best solution for the project
- Help others learn and grow

---

## Getting Started

### Prerequisites

- Python 3.12+
- Git
- Redis/Valkey (for testing)
- API keys (see .env.example)

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork:
git clone https://github.com/YOUR_USERNAME/ara-framework.git
cd ara-framework/ara_framework
```

---

## Development Setup

### 1. Create Virtual Environment

```bash
# Using the automated script
./scripts/setup_environment.sh --dev

# Or manually:
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or .venv\Scripts\activate  # Windows

pip install -r requirements-dev.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Install Pre-commit Hooks (Optional)

```bash
pip install pre-commit
pre-commit install
```

---

## Making Changes

### Branch Naming Convention

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation
- `refactor/description` - Code refactoring
- `test/description` - Test improvements

### Commit Message Format

```
type(scope): Brief description

Detailed explanation if needed.

- Bullet points for details
- Reference issues: #123
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, etc.)
- `refactor` - Code refactoring
- `test` - Adding/updating tests
- `chore` - Maintenance tasks

**Example:**
```
feat(agents): Add retry logic to LiteratureResearcher

Implements exponential backoff for Semantic Scholar API calls
to handle rate limiting more gracefully.

- Added retry decorator with max 3 attempts
- Added delay between retries (1s, 2s, 4s)
- Fixes #45
```

---

## Testing

### Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_pipeline.py -v

# With coverage
pytest tests/ --cov=ara_framework --cov-report=html

# Integration tests only
pytest tests/test_integration_*.py

# E2E tests (slow, ~60 min)
pytest tests/test_e2e_*.py
```

### Writing Tests

- Unit tests in `tests/` with `test_*.py` naming
- Integration tests with `test_integration_*.py` prefix
- E2E tests with `test_e2e_*.py` prefix
- Document test limitations in docstrings

**Example:**
```python
def test_budget_manager_initialization():
    """Test BudgetManager initializes with correct defaults."""
    manager = BudgetManager()
    assert manager.monthly_limit == 300
    assert manager.alert_threshold == 0.80
```

---

## Pull Request Process

### Before Submitting

1. **Test your changes**
   ```bash
   pytest tests/ -v
   ```

2. **Format code**
   ```bash
   black .
   ```

3. **Lint**
   ```bash
   ruff check .
   ```

4. **Update documentation** if needed

### Submitting PR

1. Push your branch to your fork
2. Open PR against `main` branch
3. Fill out PR template:
   - Description of changes
   - Issue references
   - Testing done
   - Breaking changes (if any)

### Review Process

- Maintainers will review within 2-3 days
- Address feedback promptly
- Be patient and respectful
- Once approved, we'll merge your PR

---

## Style Guidelines

### Python Code Style

- Follow PEP 8
- Use **black** for formatting (line length: 88)
- Use **ruff** for linting
- Type hints encouraged (not required)

### Documentation Style

- Use Markdown for docs
- Clear, concise writing
- Code examples when helpful
- Keep docs up-to-date with code

### Docstring Format

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief one-line description.
    
    More detailed explanation if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ExceptionType: When this error occurs
    """
    pass
```

---

## Areas to Contribute

### High Priority

- 🐛 Bug fixes
- 📝 Documentation improvements
- ✅ Test coverage
- 🔧 Tool integrations (new MCP servers)

### Medium Priority

- ⚡ Performance optimizations
- 🤖 New agent types
- 🌐 Internationalization
- 📊 Dashboard/UI

### Future Ideas

- 🔌 Plugin system
- 🚀 CI/CD improvements
- 📦 Packaging improvements
- 🎨 CLI enhancements

---

## Questions?

- 💬 Open an issue for discussion
- 📧 Contact maintainers
- 📚 Check existing documentation

---

**Thank you for contributing to ARA Framework!** 🎉
