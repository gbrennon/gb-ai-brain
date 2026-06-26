from gb_ai_brain.install_mcp_servers.installers.mcp_installer import McpInstaller
from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef


def install_mcp(
    npx_installer: McpInstaller,
    uvx_installer: McpInstaller,
    command_installer: McpInstaller,
    http_installer: McpInstaller,
    servers: list[McpServerDef],
) -> list[str]:
    failed: list[str] = []

    for server in servers:
        if server.disabled:
            print(f"Skipping disabled MCP server: {server.name}")
            continue

        if server.server_type == "streamableHttp":
            success = http_installer.install(server)
        elif server.command == "npx":
            success = npx_installer.install(server)
        elif server.command == "uvx":
            success = uvx_installer.install(server)
        else:
            success = command_installer.install(server)

        if not success:
            failed.append(server.name)

    return failed
