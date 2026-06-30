import json
import os
from pathlib import Path
from typing import Any, Dict, List

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.parsing.load_mcp_json import load_mcp_json


class ConfigManager:
    def __init__(self, platform: str = "linux") -> None:
        self.platform = platform

    def get_standard_config_paths(self) -> List[Path]:
        paths: List[Path] = []

        if self.platform == "windows":
            appdata = os.environ.get("APPDATA")
            if appdata:
                paths.append(Path(appdata) / "mcp" / "mcp.json")
            paths.append(Path(".mcp") / "mcp.json")
        else:
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config:
                paths.append(Path(xdg_config) / "mcp" / "mcp.json")
            else:
                paths.append(Path.home() / ".config" / "mcp" / "mcp.json")

            paths.append(Path.home() / ".mcp.json")
            paths.append(Path(".mcp") / "mcp.json")

            if self.platform == "linux":
                paths.append(Path("/etc/opt/mcp/config.json"))
        return paths

    def find_config_files(self) -> List[Path]:
        standard_paths = self.get_standard_config_paths()
        existing_paths = [path for path in standard_paths if path.exists()]
        return existing_paths

    def load_config_hierarchy(self) -> Dict[str, Any]:
        config_files = self.find_config_files()
        merged_config: Dict[str, Any] = {}

        for config_file in reversed(config_files):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
                    if "mcpServers" in config_data:
                        if "mcpServers" not in merged_config:
                            merged_config["mcpServers"] = {}
                        for server_name, server_config in config_data["mcpServers"].items():
                            merged_config["mcpServers"][server_name] = server_config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {config_file}: {e}")

        merged_config = self._apply_env_overrides(merged_config)
        return merged_config

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        override_config_path = os.environ.get("MCP_CONFIG_PATH")
        if override_config_path and Path(override_config_path).exists():
            try:
                with open(override_config_path, 'r', encoding='utf-8') as f:
                    env_config = json.load(f)
                    for key, value in env_config.items():
                        if key == "mcpServers" and "mcpServers" in config:
                            for server_name, server_config in value.items():
                                config["mcpServers"][server_name] = server_config
                        else:
                            config[key] = value
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load env config file {override_config_path}: {e}")
        return config

    def get_servers_from_config(self) -> List[McpServerDef]:
        config = self.load_config_hierarchy()

        if "mcpServers" not in config:
            return []

        servers_data = config["mcpServers"]
        result: List[McpServerDef] = []

        for name, cfg in servers_data.items():
            result.append(McpServerDef(
                name=str(name),
                command=cfg.get("command"),
                args=tuple(cfg.get("args", [])),
                env=tuple(
                    (str(k), str(v))
                    for k, v in cfg.get("env", {}).items()
                ),
                server_type=cfg.get("type"),
                url=cfg.get("url"),
                disabled=cfg.get("disabled", False),
            ))
        return result

    def load_from_file(self, file_path: Path) -> List[McpServerDef]:
        return load_mcp_json(file_path)
