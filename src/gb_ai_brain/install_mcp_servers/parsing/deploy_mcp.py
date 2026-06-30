import json
import os
import re
from pathlib import Path

from gb_ai_brain.shared_kernel.dotenv import load_dotenv


_PLACEHOLDER_RE = re.compile(
    r"YOUR_.*_HERE|REPLACE_ME|PASTE_.*|placeholder",
    re.IGNORECASE,
)


def deploy_mcp(
    source_path: Path,
    target_path: Path,
    dotenv_path: Path | None = None,
) -> bool:
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

        env = cfg.get("env", {})
        if isinstance(env, dict):
            for key, value in env.items():
                env[key] = _resolve_value(key, str(value), dotenv_vars)

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
    if not _PLACEHOLDER_RE.search(raw_value):
        return raw_value

    real = os.environ.get(key)
    if real is None:
        real = dotenv_vars.get(key)
    return real if real else raw_value


def _resolve_in_string(template: str, dotenv_vars: dict[str, str]) -> str:
    if not _PLACEHOLDER_RE.search(template):
        return template

    for match in re.finditer(r"YOUR_(\w+)_HERE", template):
        captured_name = match.group(1)
        candidates = [captured_name]
        if captured_name.endswith("_TOKEN"):
            candidates.append(captured_name[:-6])
        candidates.extend([
            f"{captured_name}_TOKEN",
            f"{captured_name}_KEY",
            f"{captured_name}_SECRET",
        ])
        for candidate_key in candidates:
            real = os.environ.get(candidate_key)
            if real is None:
                real = dotenv_vars.get(candidate_key)
            if real:
                return template.replace(match.group(0), real)

    for env_key in (*os.environ.keys(), *dotenv_vars.keys()):
        if len(env_key) < 3:
            continue
        if env_key in template:
            real = os.environ.get(env_key)
            if real is None:
                real = dotenv_vars.get(env_key)
            if real:
                return template.replace(env_key, real)

    return template
