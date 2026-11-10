# Usage

One row per agent session. In Gemini CLI, type `/stats` before you quit and copy the input and output tokens. Copilot shows credits instead of tokens: write those in the credits column. The free tier charges nothing, so record what the session **would cost at the provider's published list price**, and note once below the table which price list you used. Leave the cost empty for rows that only show credits.

| Date | Tool | Input tokens | Output tokens | Credits (if no tokens) | List-price cost |
|---|---|---|---|---|---|
| 2026-11-10 | Gemini CLI | 24,771 (8,121 cached) | 57 | | $0.0089 |
| 2026-11-10 | Gemini CLI | 24,742 (8,121 cached) | 53 | | $0.0089 |
| 2026-11-10 | Claude Code (claude.ai project) | not shown | not shown | | not shown: Claude Code in a claude.ai project does not report tokens per session |

Price list: Gemini 3 Flash Preview (`gemini-3-flash-preview`), paid tier Standard, from https://ai.google.dev/gemini-api/docs/pricing on 2026-11-10: $0.50 per 1M input tokens, $0.05 per 1M cached input tokens, $3.00 per 1M output tokens. Cost = ((input − cached) × 0.50 + cached × 0.05 + output × 3.00) / 1M. I planned to use Gemini 2.5 Flash ($0.30 input, $2.50 output), but the API answers that it is no longer available to new users.
