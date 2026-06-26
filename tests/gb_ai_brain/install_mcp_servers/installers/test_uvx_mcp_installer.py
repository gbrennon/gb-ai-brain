from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.uvx_mcp_installer import (
    UvxMcpInstaller,
)


class TestUvxMcpInstaller:
    @pytest.mark.unit
    def test_uvx_install_when_subprocess_succeeds_then_returns_true(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.subprocess.run"
        ) as mock_run:
            mock_run.return_value.returncode = 0
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
            mock_run.assert_called_once_with(
                ["uvx", "mcp-server-fetch"],
                check=False,
            )

    @pytest.mark.unit
    def test_uvx_install_when_subprocess_fails_then_returns_false(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.subprocess.run"
        ) as mock_run:
            mock_run.return_value.returncode = 1
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
