import os
from pathlib import Path

from gb_ai_brain.install_mcp_servers.models.mcp_server_def import McpServerDef
from gb_ai_brain.shared_kernel.dotenv import load_dotenv


def check_mcp_secrets(
    servers: list[McpServerDef],
    dotenv_path: Path | None = None,
) -> list[str]:
    """Verify that every server's env keys have a secret value.

    Priority:
    1. os.environ (runtime)
    2. .env file (development)

    Returns list of missing env keys like ["GITHUB_TOKEN", "FORGEJO_ACCESS_TOKEN"].
    An empty list means every key was found.
    """
    dotenv_vars: dict[str, str] = {}
    if dotenv_path is not None:
        dotenv_vars = load_dotenv(dotenv_path)

    missing: list[str] = []

    for server in servers:
        if server.disabled:
            continue
        for key, _value in server.env:
            # Priority: os.environ > dotenv file
            real_value = os.environ.get(key) or dotenv_vars.get(key)
            if not real_value:
                missing.append(key)

    return missing
