import json
import os
from pathlib import Path

from jinja2 import Environment

from gb_ai_brain.shared_kernel.dotenv import load_dotenv


def deploy_mcp(
    source_path: Path,
    target_path: Path,
    dotenv_path: Path | None = None,
) -> bool:
    if not source_path.exists():
        print(f"Source {source_path} not found")
        return False

    dotenv_vars: dict[str, str] = {}
    if dotenv_path and dotenv_path.is_file():
        dotenv_vars = load_dotenv(dotenv_path)

    template_context = dict(os.environ)
    template_context.update(dotenv_vars)

    template_source = source_path.read_text(encoding="utf-8")
    env = Environment()
    rendered = env.from_string(template_source).render(template_context)

    try:
        raw = json.loads(rendered)
    except json.JSONDecodeError as e:
        print(f"Failed to parse rendered template as JSON: {e}")
        return False

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Deployed MCP config to {target_path}")
    return True
