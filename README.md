# archpeep

Disposable agent skill: glance at a project/feature architecture as Mermaid, open on [mermaid.live](https://mermaid.live) via `#pako:` link. Does not write diagrams into the repo unless you ask.

## Usage

Ask for a throwaway architecture / module / call-flow overview, or invoke `archpeep` directly. The agent replies with a mermaid.live link (not ASCII, not saved to disk).

## Files

- `SKILL.md` — recipe
- `encode_pako_url.py` — stdin Mermaid → mermaid.live URL (round-trip checked, warns on long URLs)
