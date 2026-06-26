import subprocess

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

        # Resolve the package name from args (skip -y, --yes flags)
        pkg_args = [a for a in server.args if not a.startswith("-")]
        if not pkg_args:
            print(
                f"MCP server '{server.name}': no package name found "
                f"in args {server.args}"
            )
            return False

        pkg = pkg_args[0]
        print(f"Installing MCP server '{server.name}' via npx: {pkg}")

        result = subprocess.run(
            [self._npx_command, "--force", "--package", pkg, "--", "true"],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            print(f"MCP server '{server.name}': npx install failed")
            return False

        print(f"MCP server '{server.name}': installed")
        return True
