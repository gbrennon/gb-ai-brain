from typing import Protocol

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef


class McpInstaller(Protocol):
    def install(self, server: McpServerDef) -> bool: ...
