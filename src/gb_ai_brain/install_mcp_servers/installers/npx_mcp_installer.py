from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.shared_kernel.shell import run_command


class NpxMcpInstaller:
    def __init__(self, npx_command: str | None = None) -> None:
        self._npx_command = npx_command or "npx"

    def install(self, server: McpServerDef) -> bool:
        cmd = [self._npx_command, *server.args]
        print(f"Installing MCP server '{server.name}' via npx: {' '.join(cmd)}")
        return run_command(cmd)
