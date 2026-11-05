#!/usr/bin/env python3
"""Encode Mermaid source (stdin) to a mermaid.live view URL (#pako:).

Matches mermaid-live-editor serializeState: JSON → zlib (pako.deflate) → base64url.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import zlib


def encode(code: str, *, edit: bool = False, theme: str = "default") -> str:
    payload = {"code": code, "mermaid": {"theme": theme}}
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    token = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii").rstrip("=")
    path = "edit" if edit else "view"
    return f"https://mermaid.live/{path}#pako:{token}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--edit", action="store_true", help="Use /edit instead of /view")
    p.add_argument("--theme", default="default")
    args = p.parse_args()
    code = sys.stdin.read()
    if not code.strip():
        print("empty mermaid source on stdin", file=sys.stderr)
        return 2
    print(encode(code, edit=args.edit, theme=args.theme))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
