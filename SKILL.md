---
name: archpeep
description: >-
  Use when the user wants a quick, disposable diagram to understand a project's
  or feature's current architecture/design (not to save into the repo).
  Delivers a mermaid.live link instead of ASCII. Triggers: architecture
  overview, module map, structure glance, call flow, archpeep.
---
# archpeep (throwaway architecture glance)

Goal: help the user **understand** the current architecture or design of a project / feature. The diagram is **ephemeral**—do not write it into the repo, README, or docs unless they explicitly ask to keep it. Deliver a **mermaid.live** link, never ASCII art.

## Steps
1. **Scope from the code (or the user's description).** Prefer real modules, calls, and data flow. Do not invent services or edges that are not there. If context is thin, say in one short line what is observed vs inferred.
2. **One diagram, one job.** Default:
   - Module / package map → `flowchart TB` (or `LR` if flatter)
   - Request / call path → `sequenceDiagram`
   - Domain data → `erDiagram`
   Keep nodes few (roughly under ~25). Split into a second diagram only if the user asks.
3. **Label language.** Write human-facing labels (subgraph titles, glosses, edge notes) in the **same language the user is using in this conversation**. Keep code identifiers (module paths, command names, package names) as they appear in the codebase.
4. **Syntax-safe source.**
   - Node ids: ASCII `snake_case` (`api_server`), never reserved words like `end`, `graph`, `subgraph`.
   - Quote any label containing spaces, punctuation, or non-ASCII: `api_server["HTTP 入口 (cli/main.go)"]`, edge `-->|"调用 /v1"|`.
   - No raw `<`, `>`, `;`, `#` in labels; rephrase or quote.
5. **Keep the source in memory.** Do **not** create `.mmd` files, `docs/diagrams/`, or README sections unless asked.
6. **Encode a mermaid.live URL** with `encode_pako_url.py` in this skill's directory (`<skill_dir>` below):

```bash
python3 <skill_dir>/encode_pako_url.py <<'EOF'
flowchart TB
  cli["CLI"] --> core["core"]
EOF
```

   - Default is `https://mermaid.live/view#pako:...` (read-only). Add `--edit` only if they may tweak.
   - The script round-trip-checks the token and warns on stderr if the URL is very long.
   - If the helper is unavailable, this is the same algorithm (mermaid-live-editor `serializeState`):

```bash
python3 -c 'import sys,json,zlib,base64;s={"code":sys.stdin.read(),"mermaid":"{}","updateDiagram":True,"rough":False,"panZoom":True};print("https://mermaid.live/view#pako:"+base64.urlsafe_b64encode(zlib.compress(json.dumps(s,ensure_ascii=False).encode(),9)).decode().rstrip("="))' <<'EOF'
flowchart TB
  cli["CLI"] --> core["core"]
EOF
```

7. **Reply shape:** one sentence of what the diagram covers → Markdown link to the live URL → Mermaid source only if they ask. No ASCII. No "saved to …".

## Common failure modes
| Symptom | Likely cause | Fix |
|--------|----------------|-----|
| mermaid.live shows "Syntax error" | Unquoted label with punctuation / non-ASCII, or reserved id | Apply step 4, re-encode |
| mermaid.live shows "Loading URL failed" | Raw deflate, standard Base64 (`+/`), or truncated link | Use the helper; make sure the whole URL was pasted |
| Link huge / chat truncates | Too many nodes or long labels (helper warns > 6000 chars) | Cut to ~25 nodes; shorten labels |
| Empty diagram | Mermaid source never reached stdin | Feed it via heredoc as shown, not `python3 - <<PY` |
| Invented boxes | Drew without reading code | Re-scope from tree/imports first |
| Secrets on the diagram | Tokens/keys in labels | Redact; show env *names* only |

## Do not
- Persist diagrams without being asked
- Fall back to ASCII art
- Suggest self-hosting Mermaid Live or installing an MCP just for this glance
- Dump huge unreadable graphs; use subgraphs sparingly

## Optional follow-ups (only if asked)
- Regenerate with a different diagram type or focus
- Pin a theme: `--theme dark|forest|neutral|default`
- Save into the repo / README
- Export via mermaid.ink PNG/SVG
