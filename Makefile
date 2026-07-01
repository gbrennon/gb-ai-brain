.PHONY: setup install-mcp install-skills install test test-unit deploy-mcp clean help

PYTHON      := .venv/bin/python
UV          := uv
MCP_JSON    := mcp/mcp.json
DOTENV      := .env
TARGET_PATH := $(HOME)/.cline/data/settings/cline_mcp_settings.json

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------
setup:
	$(UV) sync

# -------------------------------------------------------------------
# Install
# -------------------------------------------------------------------
install-mcp:
	$(UV) run install-mcp-servers

install-skills:
	$(UV) run install-skills

install: install-mcp install-skills

# -------------------------------------------------------------------
# Deploy
# -------------------------------------------------------------------
deploy-mcp:
	$(UV) run install-mcp-servers

# -------------------------------------------------------------------
# Test
# -------------------------------------------------------------------
test:
	$(UV) run pytest tests/ --tb=short

test-unit:
	$(UV) run pytest tests/ -m unit --tb=short

# -------------------------------------------------------------------
# Clean
# -------------------------------------------------------------------
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info/

# -------------------------------------------------------------------
# Help
# -------------------------------------------------------------------
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  setup          Install dependencies (uv sync)"
	@echo "  install-mcp    Install & deploy MCP servers to all agents (Cline, OpenCode, Pi, Vibe)"
	@echo "  install-skills Install skills"
	@echo "  install        Install everything (mcp + skills)"
	@echo "  deploy-mcp     Same as install-mcp"
	@echo "  test           Run all tests"
	@echo "  test-unit      Run unit tests only"
	@echo "  clean          Remove build artifacts and caches"
