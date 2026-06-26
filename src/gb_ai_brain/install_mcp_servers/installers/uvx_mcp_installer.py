from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.shared_kernel.shell import shell_command_exists


class UvxMcpInstaller:
    def install(self, server: McpServerDef) -> bool:
        if not shell_command_exists("uvx"):
            print(
                f"MCP server '{server.name}' requires 'uvx' "
                f"which is not on PATH"
            )
            return False

        args = " ".join(server.args)
        print(
            f"MCP server '{server.name}': 'uvx' found "
            f"on PATH (package: {args})"
        )
        return True
