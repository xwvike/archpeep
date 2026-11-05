#!/usr/bin/env python3
"""Encode Mermaid source (stdin) to a mermaid.live URL (#pako:).

Mirrors mermaid-live-editor serializeState: JSON(State) → zlib (pako.deflate) → base64url.
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import zlib

URL_WARN_LEN = 16000


def encode(code: str, *, edit: bool = False, theme: str | None = None) -> str:
    config = {"theme": theme} if theme else {}
    state = {
        "code": code,
        "mermaid": json.dumps(config),
        "updateDiagram": True,
        "rough": False,
        "panZoom": True,
    }
    raw = json.dumps(state, ensure_ascii=False).encode("utf-8")
    token = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii").rstrip("=")
    decoded = json.loads(zlib.decompress(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))))
    if decoded["code"] != code:
        raise ValueError("round-trip mismatch")
    path = "edit" if edit else "view"
    return f"https://mermaid.live/{path}#pako:{token}"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--edit", action="store_true", help="Use /edit instead of /view")
    p.add_argument("--theme", help="Pin a Mermaid theme; omit to let mermaid.live pick per diagram type and site mode")
    args = p.parse_args()
    code = sys.stdin.read()
    if not code.strip():
        print("empty mermaid source on stdin", file=sys.stderr)
        return 2
    url = encode(code, edit=args.edit, theme=args.theme)
    if len(url) > URL_WARN_LEN:
        print(f"note: URL is {len(url)} chars; some chat clients truncate long links", file=sys.stderr)
    print(url)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
