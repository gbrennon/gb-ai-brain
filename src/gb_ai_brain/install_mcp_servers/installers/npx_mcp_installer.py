from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.shared_kernel.shell import shell_command_exists


class NpxMcpInstaller:
    def __init__(self, npx_command: str | None = None) -> None:
        self._npx_command = npx_command or "npx"

    def install(self, server: McpServerDef) -> bool:
        if not shell_command_exists(self._npx_command):
            print(
                f"MCP server '{server.name}' requires '{self._npx_command}' "
                f"which is not on PATH"
            )
            return False

        args = " ".join(server.args)
        print(
            f"MCP server '{server.name}': '{self._npx_command}' found "
            f"on PATH (package: {args})"
        )
        return True
