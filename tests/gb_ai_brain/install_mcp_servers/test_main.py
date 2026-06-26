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
        result = main(mcp_json_path=missing)
        assert result == 1

    @pytest.mark.unit
    def test_main_when_no_servers_configured_then_returns_zero(
        self,
        tmp_path: Path,
    ) -> None:
        mcp_json = tmp_path / "mcp.json"
        mcp_json.write_text('{"mcpServers": {}}')
        result = main(mcp_json_path=mcp_json)
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
        with patch(
            "gb_ai_brain.install_mcp_servers.main.install_mcp",
            return_value=["a"],
        ):
            result = main(mcp_json_path=mcp_json)
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
        with patch(
            "gb_ai_brain.install_mcp_servers.main.install_mcp",
            return_value=[],
        ):
            result = main(mcp_json_path=mcp_json)
            assert result == 0
