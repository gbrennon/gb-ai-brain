import json
import os
from pathlib import Path
from typing import Any, Dict, List

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.install_mcp_servers.parsing.load_mcp_json import load_mcp_json


class ConfigPaths:
    """Discovers standard MCP config file locations on each platform."""

    @staticmethod
    def get_standard_config_paths(platform: str) -> List[Path]:
        paths: List[Path] = []

        if platform == "windows":
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

            if platform == "linux":
                paths.append(Path("/etc/opt/mcp/config.json"))
        return paths


class ConfigLoader:
    """Finds existing config files and merges them hierarchically."""

    @staticmethod
    def find_config_files(platform: str) -> List[Path]:
        standard_paths = ConfigPaths.get_standard_config_paths(platform)
        return [path for path in standard_paths if path.exists()]

    @staticmethod
    def load_config_hierarchy(config_files: List[Path]) -> Dict[str, Any]:
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

        return merged_config


class EnvOverrideApplier:
    """Applies MCP_CONFIG_PATH environment variable overrides to a config dict."""

    @staticmethod
    def apply_env_overrides(config: Dict[str, Any]) -> Dict[str, Any]:
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


class ServerConfigParser:
    """Parses a merged config dict into McpServerDef instances."""

    @staticmethod
    def get_servers_from_config(config: Dict[str, Any]) -> List[McpServerDef]:
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


class ConfigManager:
    """Facade coordinating config discovery, loading, overrides, and parsing.

    Uses ConfigPaths, ConfigLoader, EnvOverrideApplier, and ServerConfigParser
    internally while preserving the same public API for backward compatibility.
    """

    def __init__(self, platform: str = "linux") -> None:
        self.platform = platform

    def get_standard_config_paths(self) -> List[Path]:
        return ConfigPaths.get_standard_config_paths(self.platform)

    def find_config_files(self) -> List[Path]:
        standard_paths = self.get_standard_config_paths()
        return [path for path in standard_paths if path.exists()]

    def load_config_hierarchy(self) -> Dict[str, Any]:
        config_files = self.find_config_files()
        merged_config = ConfigLoader.load_config_hierarchy(config_files)
        merged_config = self._apply_env_overrides(merged_config)
        return merged_config

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return EnvOverrideApplier.apply_env_overrides(config)

    def get_servers_from_config(self) -> List[McpServerDef]:
        config = self.load_config_hierarchy()
        return ServerConfigParser.get_servers_from_config(config)

    def load_from_file(self, file_path: Path) -> List[McpServerDef]:
        return load_mcp_json(file_path)

