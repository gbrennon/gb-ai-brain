import json
from pathlib import Path

import pytest

from gb_ai_brain.install_mcp_servers.parsing.deploy_mcp import deploy_mcp


class TestDeployMcp:
    @pytest.mark.unit
    def test_deploy_when_source_missing_then_returns_false(
        self,
        tmp_path: Path,
    ) -> None:
        missing = tmp_path / "nope.json"
        result = deploy_mcp(missing, tmp_path / "out.json")
        assert result is False

    @pytest.mark.unit
    def test_deploy_when_no_secrets_then_writes_identical(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text('{"mcpServers": {"a": {"command": "npx"}}}')
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        assert target.exists()
        written = json.loads(target.read_text())
        assert written == {"mcpServers": {"a": {"command": "npx"}}}

    @pytest.mark.unit
    def test_deploy_when_env_placeholder_resolved_from_dotenv_then_writes_real(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("MY_TOKEN", raising=False)
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "srv": {
                    "env": {"MY_TOKEN": "YOUR_TOKEN_HERE"},
                },
            },
        }))
        dotenv = tmp_path / ".env"
        dotenv.write_text("MY_TOKEN=real_value\n")
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target, dotenv_path=dotenv)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["MY_TOKEN"] == "real_value"

    @pytest.mark.unit
    def test_deploy_when_env_placeholder_resolved_from_environ_then_writes_real(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("MY_TOKEN", "from_environ")
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "srv": {
                    "env": {"MY_TOKEN": "PLACEHOLDER"},
                },
            },
        }))
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target, dotenv_path=None)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["MY_TOKEN"] == "from_environ"

    @pytest.mark.unit
    def test_deploy_when_env_already_real_then_keeps_it(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "srv": {
                    "env": {"KEY": "already_real"},
                },
            },
        }))
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["KEY"] == "already_real"

    @pytest.mark.unit
    def test_deploy_when_header_your_token_here_resolved_from_environ(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_real")
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "github": {
                    "headers": {
                        "Authorization": "Bearer YOUR_GITHUB_TOKEN_HERE",
                    },
                },
            },
        }))
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert (
            written["mcpServers"]["github"]["headers"]["Authorization"]
            == "Bearer ghp_real"
        )

    @pytest.mark.unit
    def test_deploy_when_header_still_placeholder_then_keeps_it(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "github": {
                    "headers": {
                        "Authorization": "Bearer YOUR_GITHUB_TOKEN_HERE",
                    },
                },
            },
        }))
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert (
            written["mcpServers"]["github"]["headers"]["Authorization"]
            == "Bearer YOUR_GITHUB_TOKEN_HERE"
        )

    @pytest.mark.unit
    def test_deploy_preserves_extra_fields(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text(json.dumps({
            "mcpServers": {
                "srv": {
                    "command": "npx",
                    "autoApprove": [],
                    "disabled": False,
                },
            },
        }))
        target = tmp_path / "out.json"

        deploy_mcp(source, target)
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["autoApprove"] == []
        assert written["mcpServers"]["srv"]["disabled"] is False
