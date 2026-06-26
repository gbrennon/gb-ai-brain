from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.shared_kernel.shell import run_command


class UvxMcpInstaller:
    def install(self, server: McpServerDef) -> bool:
        cmd = ["uvx", *server.args]
        print(f"Installing MCP server '{server.name}' via uvx: {' '.join(cmd)}")
        return run_command(cmd)
