import sys
from pathlib import Path

from gb_ai_brain.install_mcp_servers.installers.command_mcp_installer import (
    CommandMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.http_mcp_installer import (
    HttpMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.install_mcp import install_mcp
from gb_ai_brain.install_mcp_servers.installers.npx_mcp_installer import (
    NpxMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.uvx_mcp_installer import (
    UvxMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.parsing.load_mcp_json import load_mcp_json


def main(mcp_json_path: Path | None = None) -> int:
    mcp_json = mcp_json_path or Path("mcp") / "mcp.json"

    if not mcp_json.exists():
        print(f"{mcp_json} not found")
        return 1

    servers = load_mcp_json(mcp_json)

    if not servers:
        print("No MCP servers configured")
        return 0

    failed = install_mcp(
        NpxMcpInstaller(),
        UvxMcpInstaller(),
        CommandMcpInstaller(),
        HttpMcpInstaller(),
        servers,
    )

    if failed:
        print("\nFailed MCP server installations:")
        for name in failed:
            print(f" - {name}")
        return 1

    print("\nAll MCP servers installed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
