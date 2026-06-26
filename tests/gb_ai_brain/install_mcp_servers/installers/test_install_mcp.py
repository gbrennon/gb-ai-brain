import pytest

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.installers.install_mcp import install_mcp
from tests.gb_ai_brain.install_mcp_servers.fakes import FakeMcpInstaller


def _make_server(
    name: str,
    command: str | None = "npx",
    server_type: str | None = None,
) -> McpServerDef:
    return McpServerDef(
        name=name,
        command=command,
        args=("-y", "pkg") if command else (),
        env=(),
        server_type=server_type,
        url="https://example.com" if server_type == "streamableHttp" else None,
        disabled=False,
    )


class TestInstallMcp:
    @pytest.mark.unit
    def test_install_when_all_succeed_then_returns_empty(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        servers = [_make_server("a"), _make_server("b")]
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, servers)
        assert failed == []
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_install_when_some_fail_then_returns_failed_list(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        fake_installer.fail_on = ["b"]
        servers = [_make_server("a"), _make_server("b")]
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, servers)
        assert failed == ["b"]

    @pytest.mark.unit
    def test_install_when_empty_then_returns_empty(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, [])
        assert failed == []

    @pytest.mark.unit
    def test_install_when_disabled_server_then_skips(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        enabled = _make_server("enabled")
        disabled = McpServerDef(
            name="disabled",
            command="npx",
            args=("-y", "pkg"),
            env=(),
            server_type=None,
            url=None,
            disabled=True,
        )
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, [enabled, disabled])
        assert failed == []
        assert fake_installer.installed == [enabled]

    @pytest.mark.unit
    def test_install_routes_npx_to_npx_installer(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        servers = [_make_server("npx-server", command="npx")]
        install_mcp(fake_installer, FakeMcpInstaller(), FakeMcpInstaller(), FakeMcpInstaller(), servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_install_routes_uvx_to_uvx_installer(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        servers = [_make_server("uvx-server", command="uvx")]
        install_mcp(FakeMcpInstaller(), fake_installer, FakeMcpInstaller(), FakeMcpInstaller(), servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_install_routes_custom_command_to_command_installer(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        servers = [_make_server("custom", command="forgejo-mcp")]
        install_mcp(FakeMcpInstaller(), FakeMcpInstaller(), fake_installer, FakeMcpInstaller(), servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_install_routes_http_to_http_installer(
        self,
        fake_installer: FakeMcpInstaller,
    ) -> None:
        servers = [_make_server("github", command=None, server_type="streamableHttp")]
        install_mcp(FakeMcpInstaller(), FakeMcpInstaller(), FakeMcpInstaller(), fake_installer, servers)
        assert fake_installer.installed == servers
