from pathlib import Path
from unittest.mock import patch

import pytest

from gb_ai_brain.install_mcp_servers.main import main


class TestMain:
    @pytest.mark.unit
    def test_main_when_mcp_json_missing_then_returns_one(
        self,
        tmp_path: Path,
    ) -> None:
        missing = tmp_path / "does-not-exist.json"
        dotenv = tmp_path / ".env"
        dotenv.write_text("")
        result = main(mcp_json_path=missing, dotenv_path=dotenv)
        assert result == 1

    @pytest.mark.unit
    def test_main_when_no_servers_configured_then_returns_zero(
        self,
        tmp_path: Path,
    ) -> None:
        mcp_json = tmp_path / "mcp.json"
        mcp_json.write_text('{"mcpServers": {}}')
        dotenv = tmp_path / ".env"
        dotenv.write_text("")
        result = main(mcp_json_path=mcp_json, dotenv_path=dotenv)
        assert result == 0

    @pytest.mark.unit
    def test_main_when_some_installations_fail_then_returns_one(
        self,
        tmp_path: Path,
    ) -> None:
        mcp_json = tmp_path / "mcp.json"
        mcp_json.write_text(
            '{"mcpServers": {"a": {"command": "npx", '
            '"args": ["pkg"], "disabled": false}}}'
        )
        dotenv = tmp_path / ".env"
        dotenv.write_text("")
        with patch(
            "gb_ai_brain.install_mcp_servers.main.install_mcp",
            return_value=["a"],
        ):
            result = main(mcp_json_path=mcp_json, dotenv_path=dotenv)
            assert result == 1

    @pytest.mark.unit
    def test_main_when_all_succeed_then_returns_zero(
        self,
        tmp_path: Path,
    ) -> None:
        mcp_json = tmp_path / "mcp.json"
        mcp_json.write_text(
            '{"mcpServers": {"a": {"command": "npx", '
            '"args": ["pkg"], "disabled": false}}}'
        )
        dotenv = tmp_path / ".env"
        dotenv.write_text("")
        with patch(
            "gb_ai_brain.install_mcp_servers.main.install_mcp",
            return_value=[],
        ):
            result = main(mcp_json_path=mcp_json, dotenv_path=dotenv)
            assert result == 0

    @pytest.mark.unit
    def test_main_when_secrets_missing_but_commands_ok_then_still_returns_zero(
        self,
        tmp_path: Path,
    ) -> None:
        mcp_json = tmp_path / "mcp.json"
        mcp_json.write_text(
            '{"mcpServers": {"a": {"command": "npx", '
            '"args": ["pkg"], '
            '"env": {"GITHUB_TOKEN": "placeholder"}, '
            '"disabled": false}}}'
        )
        dotenv = tmp_path / ".env"
        dotenv.write_text("")
        with patch(
            "gb_ai_brain.install_mcp_servers.main.install_mcp",
            return_value=[],
        ):
            result = main(mcp_json_path=mcp_json, dotenv_path=dotenv)
            assert result == 0
