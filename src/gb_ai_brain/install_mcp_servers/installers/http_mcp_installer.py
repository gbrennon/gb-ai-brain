from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef


class HttpMcpInstaller:
    def install(self, server: McpServerDef) -> bool:
        url = server.url or "(no url)"
        print(
            f"MCP server '{server.name}' is streamableHttp ({url}) — "
            f"no local install needed"
        )
        return True
