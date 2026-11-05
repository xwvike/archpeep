---
name: archpeep
description: >-
  Use when the user wants a disposable Mermaid diagram to understand a project's
  or feature's current architecture/design (not to save into the repo), and
  prefers opening it on mermaid.live instead of ASCII. Triggers: architecture
  overview, module map, structure glance, archpeep.
---
# archpeep (throwaway architecture glance)

Goal: help the user **understand** the current architecture or design of a project / feature. The diagram is **ephemeral**—do not write it into the repo, README, or docs unless they explicitly ask to keep it. Deliver a **mermaid.live** link, never ASCII art.

## Triggers (any of these agents)
- **Grok Bot:** Skill `archpeep`, or user asks for a structure/architecture/module overview and wants Mermaid Live.
- **Claude Code / Codex / OpenCode:** same ask, or `/archpeep` / `@archpeep` if the host lists skills that way. Use this recipe's encode path; do not invent another.

## Steps
1. **Scope from the code (or the user's description).** Prefer real modules, calls, and data flow. Do not invent services or edges that are not there. If context is thin, say in one short line what is observed vs inferred.
2. **One diagram, one job.** Default:
   - Module / package map → `flowchart TB` (or `LR` if flatter)
   - Request / call path → `sequenceDiagram`
   - Domain data → `erDiagram`
   Keep nodes few (roughly under ~25). Split into a second diagram only if the user asks.
3. **Label language.** Write human-facing labels (subgraph titles, glosses, edge notes) in the **same language the user is using in this conversation**. Keep code identifiers (module paths, command names, package names) as they appear in the codebase so the diagram stays grounded. Do not add language or topology rules beyond that.
4. **Write Mermaid source only in memory** (scratch / tool stdout). Do **not** create `.mmd` files, `docs/diagrams/`, or README sections unless asked.
5. **Encode a mermaid.live URL** (matches mermaid-live-editor `serializeState`):
   - Prefer `https://mermaid.live/view#pako:...` (read-only). Use `/edit#pako:...` only if they may tweak.
   - Payload JSON: `{"code":"<mermaid source>","mermaid":{"theme":"default"}}`
   - Pipeline: UTF-8 JSON → **zlib compress** (same as JS `pako.deflate`, *not* raw deflate) → **Base64 URL-safe** → strip `=` padding → `#pako:<token>`.
   - One-liner:

```bash
python3 - <<'PY'
import json, zlib, base64, sys
code = sys.stdin.read()
payload = {"code": code, "mermaid": {"theme": "default"}}
raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
token = base64.urlsafe_b64encode(zlib.compress(raw, 9)).decode("ascii").rstrip("=")
print("https://mermaid.live/view#pako:" + token)
PY
```

   Pipe the Mermaid source into that script. Helper (if present): `encode_pako_url.py` beside this skill — same algorithm.
   - Sanity-check: non-empty token; URL starts with `https://mermaid.live/view#pako:`.
6. **Reply shape:** one sentence of what the diagram covers → Markdown link to the live URL → Mermaid source only if they ask. No ASCII. No "saved to …".

## Common failure modes
| Symptom | Likely cause | Fix |
|--------|----------------|-----|
| mermaid.live blank / decode error | Raw deflate or standard Base64 (`+/`) | `zlib.compress` + `urlsafe_b64encode`, strip `=` |
| Link huge / chat truncates | Too many nodes or long labels | Cut to ~25 nodes; shorten labels |
| Invented boxes | Drew without reading code | Re-scope from tree/imports first |
| Secrets on the diagram | Tokens/keys in labels | Redact; show env *names* only |
| ASCII fallback | Skipped encode | Always ship `#pako:` link |

## Do not
- Persist diagrams without being asked
- Suggest self-hosting Mermaid Live or installing an MCP just for this glance
- Dump huge unreadable graphs; use subgraphs sparingly
- Add extra process constraints (e.g. "never change topology when relabeling") that second-guess how the agent should read the real structure

## Optional follow-ups (only if asked)
- Regenerate with a different diagram type or focus
- Save into the repo / README
- Export via mermaid.ink PNG/SVG
