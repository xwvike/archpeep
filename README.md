# archpeep

Disposable agent skill: glance at a project/feature architecture as Mermaid, open on [mermaid.live](https://mermaid.live) via `#pako:` link. Does not write diagrams into the repo unless you ask.

## Install

Copy or symlink into your agent skills directory, e.g.:

```bash
mkdir -p ~/.claude/skills/archpeep
ln -sf /path/to/archpeep/SKILL.md ~/.claude/skills/archpeep/SKILL.md
ln -sf /path/to/archpeep/encode_pako_url.py ~/.claude/skills/archpeep/encode_pako_url.py
```

Or with skills.sh-style installers that accept a GitHub skill folder: point them at this repo.

## Usage

Ask the agent to run `archpeep` / `@archpeep`, or say you want a throwaway structure/architecture overview on mermaid.live (not ASCII, not saved to disk).

## Files

- `SKILL.md` — recipe
- `encode_pako_url.py` — optional helper (stdin Mermaid → mermaid.live URL)
