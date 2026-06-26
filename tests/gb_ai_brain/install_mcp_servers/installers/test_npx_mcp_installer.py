import subprocess
from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer import (
    NpxMcpInstaller,
)


def _server(name: str = "memory", args: tuple[str, ...] = ("-y", "pkg")) -> McpServerDef:
    return McpServerDef(
        name=name,
        command="npx",
        args=args,
        env=(),
        server_type=None,
        url=None,
        disabled=False,
    )


class TestNpxMcpInstaller:
    @pytest.mark.unit
    def test_npx_install_when_package_resolves_then_returns_true(self) -> None:
        with (
            patch(
                "gb_ai_brain.shared_kernel.shell.which",
                return_value="/usr/bin/npx",
            ),
            patch(
                "gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer.subprocess.run",
            ) as mock_run,
        ):
            mock_run.return_value.returncode = 0
            installer = NpxMcpInstaller()
            result = installer.install(_server())
            assert result is True
            mock_run.assert_called_once_with(
                ["npx", "--force", "--package", "pkg", "--", "true"],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_npx_install_when_npx_not_on_path_then_returns_false(self) -> None:
        with patch(
            "gb_ai_brain.shared_kernel.shell.which",
            return_value=None,
        ):
            installer = NpxMcpInstaller()
            result = installer.install(_server())
            assert result is False

    @pytest.mark.unit
    def test_npx_install_when_package_fails_then_returns_false(self) -> None:
        with (
            patch(
                "gb_ai_brain.shared_kernel.shell.which",
                return_value="/usr/bin/npx",
            ),
            patch(
                "gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer.subprocess.run",
            ) as mock_run,
        ):
            mock_run.return_value.returncode = 1
            installer = NpxMcpInstaller()
            result = installer.install(_server(args=("broken",)))
            assert result is False
