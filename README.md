# AI Agent Skill Library

Curated skills for AI coding agents: architecture patterns (Clean, Hexagonal, CQRS, Event-driven) and testing strategies (Unit, Integration, E2E).

Each skill is a reusable prompt fragment that teaches an agent a specific practice.

## Quick Start

```bash
uv sync                    # install dependencies
make install-mcp           # install & deploy MCP servers
make install-skills        # install skills
make install               # install both
```

## Make Targets

| Command | Description |
|---------|-------------|
| `make setup` | Install dependencies (`uv sync`) |
| `make install-mcp` | Install MCP servers from `mcp/mcp.json` |
| `make install-skills` | Install skills |
| `make install` | Install everything |
| `make deploy-mcp` | Deploy MCP config to Cline |
| `make test` | Run all tests |
| `make test-unit` | Run unit tests only |
| `make clean` | Remove build artifacts and caches |
| `make help` | Show available targets |

## Configuration

Place secrets in `.env`:

```
GITHUB_TOKEN=...
FORGEJO_ACCESS_TOKEN=...
```

The `mcp/mcp.json` template uses Jinja2 expressions — missing variables fall back to human-readable placeholders.
