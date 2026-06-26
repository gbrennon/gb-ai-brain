from pathlib import Path

import pytest

from tests.gb_ai_brain.install_mcp_servers.fakes import FakeMcpInstaller


@pytest.fixture
def fake_installer() -> FakeMcpInstaller:
    return FakeMcpInstaller()


@pytest.fixture
def sample_mcp_json(tmp_path: Path) -> Path:
    content = """
{
  "mcpServers": {
    "github": {
      "type": "streamableHttp",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_TOKEN_HERE"
      },
      "disabled": false,
      "autoApprove": []
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "disabled": false,
      "autoApprove": []
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "disabled": false,
      "autoApprove": []
    },
    "forgejo": {
      "command": "forgejo-mcp",
      "args": ["--transport", "stdio", "--url", "https://codeberg.org"],
      "env": {
        "FORGEJO_ACCESS_TOKEN": "YOUR_CODEBERG_TOKEN_HERE"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
"""
    p = tmp_path / "mcp.json"
    p.write_text(content)
    return p


@pytest.fixture
def mcp_dir(tmp_path: Path) -> Path:
    d = tmp_path / "mcp"
    d.mkdir()
    return d
