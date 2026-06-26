from pathlib import Path
from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.http_mcp_installer import (
    HttpMcpInstaller,
)


def _http_server(
    env: tuple[tuple[str, str], ...] = (),
) -> McpServerDef:
    return McpServerDef(
        name="github",
        command=None,
        args=(),
        env=env,
        server_type="streamableHttp",
        url="https://api.githubcopilot.com/mcp/",
        disabled=False,
    )


class TestHttpMcpInstaller:
    @pytest.mark.unit
    def test_http_install_when_no_env_then_returns_true(self) -> None:
        installer = HttpMcpInstaller(dotenv_path=None)
        result = installer.install(_http_server())
        assert result is True

    @pytest.mark.unit
    def test_http_install_when_env_contains_secret_in_environ_then_returns_true(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_real_value")
        installer = HttpMcpInstaller(dotenv_path=None)
        result = installer.install(_http_server(env=(("GITHUB_TOKEN", "PLACEHOLDER"),)))
        assert result is True

    @pytest.mark.unit
    def test_http_install_when_env_contains_secret_in_dotenv_then_returns_true(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        dotenv = tmp_path / ".env"
        dotenv.write_text("GITHUB_TOKEN=ghp_real_value\n")
        installer = HttpMcpInstaller(dotenv_path=dotenv)
        result = installer.install(_http_server(env=(("GITHUB_TOKEN", "PLACEHOLDER"),)))
        assert result is True

    @pytest.mark.unit
    def test_http_install_when_env_still_placeholder_then_returns_true(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        installer = HttpMcpInstaller(dotenv_path=None)
        result = installer.install(
            _http_server(env=(("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN_HERE"),))
        )
        assert result is True
