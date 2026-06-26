from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.uvx_mcp_installer import (
    UvxMcpInstaller,
)


class TestUvxMcpInstaller:
    @pytest.mark.unit
    def test_uvx_install_when_on_path_then_returns_true(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = "/usr/bin/uvx"
            installer = UvxMcpInstaller()
            server = McpServerDef(
                name="fetch",
                command="uvx",
                args=("mcp-server-fetch",),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is True
            mock_which.assert_called_once_with("uvx")

    @pytest.mark.unit
    def test_uvx_install_when_not_on_path_then_returns_false(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = None
            installer = UvxMcpInstaller()
            server = McpServerDef(
                name="fail",
                command="uvx",
                args=("broken",),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is False
