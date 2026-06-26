from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer import (
    NpxMcpInstaller,
)


class TestNpxMcpInstaller:
    @pytest.mark.unit
    def test_npx_install_when_on_path_then_returns_true(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = "/usr/bin/npx"
            installer = NpxMcpInstaller()
            server = McpServerDef(
                name="memory",
                command="npx",
                args=("-y", "@modelcontextprotocol/server-memory"),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is True
            mock_which.assert_called_once_with("npx")

    @pytest.mark.unit
    def test_npx_install_when_not_on_path_then_returns_false(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = None
            installer = NpxMcpInstaller()
            server = McpServerDef(
                name="fail-server",
                command="npx",
                args=("-y", "broken"),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is False

    @pytest.mark.unit
    def test_npx_install_when_custom_npx_path_checks_it(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = "/custom/npx"
            installer = NpxMcpInstaller(npx_command="/custom/npx")
            server = McpServerDef(
                name="skill",
                command="npx",
                args=("-y", "pkg"),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is True
            mock_which.assert_called_once_with("/custom/npx")
