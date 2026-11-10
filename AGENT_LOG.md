# Agent log

One entry per agent session, newest at the bottom. Be honest: what went wrong is the useful part.

<!-- Copy this block for each session:

## YYYY-MM-DD · <short title>
- Goal:
- Delegated:
- Checkpoints:
- Went wrong:
- Changed by hand:

-->

## 2026-11-10 · Exercise 1: MCP server in Python
- Goal: a hand-written MCP server (no SDK) in `mcp-server/server.py` that passes `check.mjs` 12/12.
- Delegated: with the lecturer's permission, Claude (Claude Code) wrote `server.py`, `categories.json`, the Python config in `.gemini/settings.json` and `.vscode/mcp.json`, `package.json` and the README transcript, plus a line-by-line guide that I studied to understand the code.
- Checkpoints: `node mcp-server/check.mjs -- python3 mcp-server/server.py` → 12/12; the same through `npm run --silent mcp` → 12/12; the five transcript messages answered as expected.
- Went wrong: the template starts `node mcp-server/server.js`; with a Python server Gemini CLI would not start it until the config was changed.
- Changed by hand: <!-- fill in: what you changed or checked yourself -->
