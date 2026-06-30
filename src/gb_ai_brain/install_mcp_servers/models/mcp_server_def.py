from dataclasses import dataclass


@dataclass(frozen=True)
class McpServerDef:
    name: str
    command: str | None
    args: tuple[str, ...]
    env: tuple[tuple[str, str], ...]
    server_type: str | None
    url: str | None
    disabled: bool
