import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.http_mcp_installer import (
    HttpMcpInstaller,
)


class TestHttpMcpInstaller:
    @pytest.mark.unit
    def test_http_install_always_returns_true(self) -> None:
        installer = HttpMcpInstaller()
        server = McpServerDef(
            name="github",
            command=None,
            args=(),
            env=(),
            server_type="streamableHttp",
            url="https://api.githubcopilot.com/mcp/",
            disabled=False,
        )
        result = installer.install(server)
        assert result is True
