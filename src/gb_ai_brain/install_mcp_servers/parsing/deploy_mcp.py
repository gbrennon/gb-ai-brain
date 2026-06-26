import json
import os
import re
from pathlib import Path

from gb_ai_brain.shared_kernel.dotenv import load_dotenv


# Pattern to match placeholder values like YOUR_X_TOKEN_HERE, REPLACE_ME, etc.
_PLACEHOLDER_RE = re.compile(
    r"YOUR_.*_HERE|REPLACE_ME|PASTE_.*|placeholder",
    re.IGNORECASE,
)


def deploy_mcp(
    source_path: Path,
    target_path: Path,
    dotenv_path: Path | None = None,
) -> bool:
    """Read mcp.json, resolve secrets, write resolved config to target.

    For every env-like value found in the raw JSON (env values and headers),
    if it looks like a placeholder, try to resolve it from os.environ or .env.
    """
    if not source_path.exists():
        print(f"Source {source_path} not found")
        return False

    raw = json.loads(source_path.read_text(encoding="utf-8"))

    dotenv_vars: dict[str, str] = {}
    if dotenv_path and dotenv_path.is_file():
        dotenv_vars = load_dotenv(dotenv_path)

    servers = raw.get("mcpServers", {})
    for _name, cfg in servers.items():
        if not isinstance(cfg, dict):
            continue

        # Resolve env values
        env = cfg.get("env", {})
        if isinstance(env, dict):
            for key, value in env.items():
                env[key] = _resolve_value(key, str(value), dotenv_vars)

        # Resolve headers values (e.g. Authorization: Bearer YOUR_TOKEN_HERE)
        headers = cfg.get("headers", {})
        if isinstance(headers, dict):
            for key, value in headers.items():
                if isinstance(value, str):
                    headers[key] = _resolve_in_string(value, dotenv_vars)

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Deployed MCP config to {target_path}")
    return True


def _resolve_value(key: str, raw_value: str, dotenv_vars: dict[str, str]) -> str:
    """If raw_value looks like a placeholder, resolve from env or dotenv."""
    if not _PLACEHOLDER_RE.search(raw_value):
        return raw_value

    real = os.environ.get(key) or dotenv_vars.get(key)
    return real if real else raw_value


def _resolve_in_string(template: str, dotenv_vars: dict[str, str]) -> str:
    """Replace placeholder tokens inside a larger string.

    E.g. 'Bearer YOUR_GITHUB_TOKEN_HERE' -> 'Bearer ghp_abc123'
    E.g. 'Bearer GITHUB_TOKEN' -> 'Bearer ghp_abc123'
    """
    if not _PLACEHOLDER_RE.search(template):
        return template

    # First: try YOUR_X_HERE pattern
    for match in re.finditer(r"YOUR_(\w+)_HERE", template):
        candidate = match.group(1)
        # Generate candidate keys to try
        candidates = [candidate]
        # YOUR_GITHUB_TOKEN_HERE -> also try GITHUB_TOKEN, GITHUB
        if candidate.endswith("_TOKEN"):
            candidates.append(candidate[:-6])
        candidates.extend([
            f"{candidate}_TOKEN",
            f"{candidate}_KEY",
            f"{candidate}_SECRET",
        ])
        for candidate_key in candidates:
            real = os.environ.get(candidate_key) or dotenv_vars.get(candidate_key, "")
            if real:
                return template.replace(match.group(0), real)

    # Second: try to find any known env key name in the template
    for key in (*os.environ.keys(), *dotenv_vars.keys()):
        if key in template:
            real = os.environ.get(key) or dotenv_vars.get(key, "")
            if real:
                return template.replace(key, real)

    return template
