from pathlib import Path
from typing import Any, Dict, List

from gb_ai_brain.install_mcp_servers.config_loader import ConfigLoader
from gb_ai_brain.install_mcp_servers.config_paths import ConfigPaths
from gb_ai_brain.install_mcp_servers.env_override_applier import EnvOverrideApplier
from gb_ai_brain.install_mcp_servers.parsing.load_mcp_json import load_mcp_json
from gb_ai_brain.install_mcp_servers.server_config_parser import ServerConfigParser


class ConfigManager:
    """Facade coordinating config discovery, loading, overrides, and parsing.

    Accepts optional dependency instances via constructor injection for
    testability.  Defaults to the real implementations when not provided.
    """

    def __init__(
        self,
        platform: str = "linux",
        config_paths: ConfigPaths | None = None,
        config_loader: ConfigLoader | None = None,
        env_override_applier: EnvOverrideApplier | None = None,
        server_config_parser: ServerConfigParser | None = None,
    ) -> None:
        self.platform = platform
        self._config_paths = config_paths or ConfigPaths()
        self._config_loader = config_loader or ConfigLoader(self._config_paths)
        self._env_override_applier = env_override_applier or EnvOverrideApplier()
        self._server_config_parser = server_config_parser or ServerConfigParser()

    def get_standard_config_paths(self) -> List[Path]:
        return self._config_paths.get_standard_config_paths(self.platform)

    def find_config_files(self) -> List[Path]:
        standard_paths = self.get_standard_config_paths()
        return [path for path in standard_paths if path.exists()]

    def load_config_hierarchy(self) -> Dict[str, Any]:
        config_files = self.find_config_files()
        merged_config = self._config_loader.load_config_hierarchy(config_files)
        merged_config = self._apply_env_overrides(merged_config)
        return merged_config

    def _apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        return self._env_override_applier.apply_env_overrides(config)

    def get_servers_from_config(self) -> List[McpServerDef]:
        config = self.load_config_hierarchy()
        return self._server_config_parser.get_servers_from_config(config)

    def load_from_file(self, file_path: Path) -> List[McpServerDef]:
        return load_mcp_json(file_path)

