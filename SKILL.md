---
name: archpeep
description: >-
  Use when the user wants a quick, disposable diagram to understand a project's
  or feature's current architecture/design (not to save into the repo).
  Delivers a mermaid.live link instead of ASCII. Triggers: architecture
  overview, module map, structure glance, call flow, archpeep. Chinese: 看下现有架构,
  模块关系, 调用链. Not for designing a new architecture or for diagrams meant
  for docs or slides.
---
# archpeep (throwaway architecture glance)

Goal: help the user **understand** the current architecture or design of a project / feature. The diagram is **ephemeral**—do not write it into the repo, README, or docs unless they explicitly ask to keep it. Deliver a **mermaid.live** link, never ASCII art.

This skill governs the diagram portion of the task only. Continue any analysis, implementation, refactoring, or testing requested by the user; apply the reply format below only to the diagram portion. If code changes, depict the final state unless the user requests a comparison.

## Steps
1. **Scope from the code (or the user's description).** Prefer real modules, calls, and data flow. Do not invent services or edges that are not there. If context is thin, say in one short line what is observed vs inferred.
   - For module maps, inspect dependencies and how components are wired together. For call paths, trace the relevant entry point, actual calls, and branches; directory names and imports alone do not establish runtime flow. Omit uncertain relationships or mark them as inferred.
2. **One diagram, one job.** Default:
   - Module / package map → `flowchart TB` (or `LR` if flatter)
   - Request / call path → `sequenceDiagram`
   - Domain data → `erDiagram`
   Keep nodes few (roughly under ~25). Default to one focused diagram; use a second when the request spans distinct views and separating them makes the explanation clearer.
3. **Label language.** Write human-facing labels (subgraph titles, glosses, edge notes) in the **same language the user is using in this conversation**. Keep code identifiers (module paths, command names, package names) as they appear in the codebase.
4. **Syntax-safe source.**
   Use the syntax of the selected diagram type. For flowcharts:

   - Node ids: ASCII `snake_case` (`api_server`), never reserved words like `end`, `graph`, `subgraph`.
   - Quote any label containing spaces, punctuation, or non-ASCII: `api_server["HTTP 入口 (cli/main.go)"]`, edge `-->|"调用 /v1"|`.
   - No raw `<`, `>`, `;`, `#` in labels; rephrase or quote.

   For sequence diagrams, use participants and messages; for ER diagrams, use entities and relationship cardinalities rather than flowchart nodes and edges. Use an available Mermaid parser or renderer to check syntax before delivery; if none is available, do not claim rendering was verified.
5. **Keep the source in memory.** Do **not** create `.mmd` files, `docs/diagrams/`, or README sections unless asked.
6. **Encode a mermaid.live URL** with `encode_pako_url.py` in this skill's directory (`<skill_dir>` below):

```bash
python3 <skill_dir>/encode_pako_url.py <<'EOF'
flowchart TB
  cli["CLI"] --> core["core"]
EOF
```

   - Default is `https://mermaid.live/view#pako:...` (read-only). Add `--edit` only if they may tweak.
   - The script round-trip-checks the token and warns on stderr if the URL is very long. This verifies encoding integrity, not Mermaid syntax or successful rendering.
   - If the helper is unavailable, this is the same algorithm (mermaid-live-editor `serializeState`):

```bash
python3 -c 'import sys,json,zlib,base64;s={"code":sys.stdin.read(),"mermaid":"{}","updateDiagram":True,"rough":False,"panZoom":True};print("https://mermaid.live/view#pako:"+base64.urlsafe_b64encode(zlib.compress(json.dumps(s,ensure_ascii=False).encode(),9)).decode().rstrip("="))' <<'EOF'
flowchart TB
  cli["CLI"] --> core["core"]
EOF
```

7. **Diagram reply shape:** one sentence of what the diagram covers → Markdown link to each live URL → Mermaid source only if they ask. Include analysis, changes, and validation results as needed for the rest of the user's task. No ASCII. No "saved to …" unless the user requested persistence and the diagram was actually saved.

## Common failure modes
| Symptom | Likely cause | Fix |
|--------|----------------|-----|
| mermaid.live shows "Syntax error" | Unquoted label with punctuation / non-ASCII, or reserved id | Apply step 4, re-encode |
| mermaid.live shows "Loading URL failed" | Raw deflate, standard Base64 (`+/`), or truncated link | Use the helper; make sure the whole URL was pasted |
| Link huge / chat truncates | Too many nodes or long labels (helper warns > 6000 chars) | Cut to ~25 nodes; shorten labels |
| Empty diagram | Mermaid source never reached stdin | Feed it via heredoc as shown, not `python3 - <<PY` |
| Invented boxes or edges | Drew without checking implementation | Inspect the relevant dependencies, wiring, and call sites; omit or mark inferred relationships |
| Secrets on the diagram | Tokens/keys in labels | Redact; show env *names* only |

## Do not
- Persist diagrams without being asked
- Fall back to ASCII art
- Suggest self-hosting Mermaid Live or installing an MCP just for this glance
- Dump huge unreadable graphs; use subgraphs sparingly

## Optional diagram follow-ups (when requested, including in the original task)
- Regenerate with a different diagram type or focus
- Pin a theme: `--theme dark|forest|neutral|default`
- Save into the repo / README
- Export via mermaid.ink PNG/SVG
