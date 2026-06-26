import subprocess
from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer import (
    NpxMcpInstaller,
)


class TestNpxMcpInstaller:
    @pytest.mark.unit
    def test_npx_install_when_subprocess_succeeds_then_returns_true(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.subprocess.run"
        ) as mock_run:
            mock_run.return_value.returncode = 0
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
            mock_run.assert_called_once_with(
                ["npx", "-y", "@modelcontextprotocol/server-memory"],
                check=False,
                stdin=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_npx_install_when_subprocess_fails_then_returns_false(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.subprocess.run"
        ) as mock_run:
            mock_run.return_value.returncode = 1
            installer = NpxMcpInstaller(npx_command="npx")
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
    def test_npx_install_when_custom_npx_path_uses_it(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.subprocess.run"
        ) as mock_run:
            mock_run.return_value.returncode = 0
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
            installer.install(server)
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "/custom/npx"
