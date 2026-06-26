"""Minimal local MCP-style server entrypoint for ContextForge MCP Lab.

This module intentionally exposes named tool calls instead of raw SQL. It can
be used directly for local demos or adapted to a full MCP transport layer.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from src.tools import TOOL_REGISTRY


def call_tool(name: str, arguments: dict[str, Any] | None = None) -> Any:
    """Call a registered tool by name with JSON-compatible arguments."""
    if name not in TOOL_REGISTRY:
        available = ", ".join(sorted(TOOL_REGISTRY))
        raise ValueError(f"unknown tool '{name}'. Available tools: {available}")
    return TOOL_REGISTRY[name](**(arguments or {}))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local ContextForge MCP-style tool call.")
    parser.add_argument("tool", help="Tool name to call")
    parser.add_argument(
        "--args",
        default="{}",
        help='JSON object of tool arguments, for example: \'{"query": "RAG"}\'',
    )
    args = parser.parse_args()

    try:
        arguments = json.loads(args.args)
        if not isinstance(arguments, dict):
            raise ValueError("--args must be a JSON object")
        result = call_tool(args.tool, arguments)
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, indent=2))
        raise SystemExit(1) from exc

    print(json.dumps({"ok": True, "result": result}, indent=2))


if __name__ == "__main__":
    main()

