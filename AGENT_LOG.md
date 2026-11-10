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
- Changed by hand: Nothing in server.py; I reviewed the code with the line-by-line guide.

## 2026-11-10 · Exercise 1: Gemini CLI and description experiment
- Goal: run my MCP server from Gemini CLI, ask about lecture 7 without naming the tool, record `/stats`, and repeat with the `find_lecture` description cut to "Lectures." to see if the model still picks the tool.
- Delegated: Claude (Claude in Chrome) created the Gemini API key in AI Studio and drove my Codespace: `git pull`, the self-check, both Gemini CLI sessions, the temporary description edit and its restore, and these log entries.
- Checkpoints: self-check 12/12 before the experiment; `/mcp` showed `my-project` Ready with 2 tools (`find_lecture`, `list_categories`); both sessions called `find_lecture(number: 7)` and answered "Evaluating output: non-determinism, false positives, when to trust it"; after restoring the original description `git status` was clean and the self-check was 12/12 again.
- Went wrong: Sign in with Google failed twice (the login did not survive the CLI restart, then `invalid_grant`), so I switched to an API key; `gemini-2.5-flash` is no longer available to new users; `gemini-3.8-flash` (also used by Auto) hung and a direct API call returned 503 "high demand", so both sessions used `gemini-3-flash-preview`.
- Changed by hand: I tried the Google login and pasted the Gemini API key into the terminal myself; no code changed by hand, and `server.py` is back to the original.
