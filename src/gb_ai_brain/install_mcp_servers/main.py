import sys
from pathlib import Path

from gb_ai_brain.install_mcp_servers.config_manager import ConfigManager
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
from gb_ai_brain.install_mcp_servers.installers.opencode_installer import (
    OpenCodeMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.pi_installer import (
    PiMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.uvx_mcp_installer import (
    UvxMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.installers.vibe_installer import (
    VibeMcpInstaller,
)
from gb_ai_brain.install_mcp_servers.parsing.deploy_mcp import deploy_mcp
from gb_ai_brain.install_mcp_servers.parsing.load_mcp_json import load_mcp_json
from gb_ai_brain.install_mcp_servers.secrets import check_mcp_secrets

_DEFAULT_TARGET = Path.home() / ".cline" / "data" / "settings" / "cline_mcp_settings.json"


def main(
    mcp_json_path: Path | None = None,
    dotenv_path: Path | None = None,
    target_path: Path | None = None,
    platform: str | None = None,
) -> int:
    mcp_json = mcp_json_path or Path("mcp") / "mcp.json"
    dotenv = dotenv_path or Path(".env")
    target = target_path or _DEFAULT_TARGET
    platform = platform or "linux"

    if not mcp_json.exists():
        print(f"{mcp_json} not found")
        return 1

    config_manager = ConfigManager(platform=platform)
    servers = config_manager.load_from_file(mcp_json)

    if not servers:
        print("No MCP servers configured")
        return 0

    missing_keys = check_mcp_secrets(servers, dotenv_path=dotenv)
    if missing_keys:
        print("\nMissing secrets — add these to .env or your environment:")
        for key in missing_keys:
            print(f" - {key}")

    opencode_installer = OpenCodeMcpInstaller(platform=platform)
    pi_installer = PiMcpInstaller(platform=platform)
    vibe_installer = VibeMcpInstaller(platform=platform)

    failed = install_mcp(
        NpxMcpInstaller(),
        UvxMcpInstaller(),
        CommandMcpInstaller(),
        HttpMcpInstaller(dotenv_path=dotenv),
        opencode_installer,
        pi_installer,
        vibe_installer,
        servers,
    )

    if failed:
        print(f"\nFailed MCP server installations for platform {platform}:")
        for name in failed:
            print(f" - {name}")
        return 1

    if missing_keys:
        print(f"\nAll commands found for platform {platform}, but secrets are missing (see above)")

    deployed = deploy_mcp(mcp_json, target, dotenv_path=dotenv)
    if not deployed:
        print(f"\nFailed to deploy MCP config to {target} for platform {platform}")
        return 1

    print(f"\nAll MCP servers installed successfully for platform {platform}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
