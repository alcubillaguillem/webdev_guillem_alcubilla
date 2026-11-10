# SplitMate · shared expenses for Erasmus students

<!-- Exercise 2. Write the non-goals first. Every acceptance criterion must be checkable in under a minute.
     Keep these headings exactly as they are: the self-checks look for them by name.
     The full target is on the course site under Resources → The course project. -->

## Project option
<!-- One line: lab booking, study groups, club events, or the own project the lecturer approved. -->
SplitMate (own project, approved by the lecturer).

## Goals
- A student signs in, sees the groups (flat or trip) they belong to, adds an expense and splits it among the members.
- Every member sees the group's expenses and who owes whom, computed from the expenses and their shares.
- The owner of a group invites and removes members; only the payer edits or deletes an expense.

## Non-goals
- No real payments or bank integration: the app only records who owes whom.
- No currency conversion: each group has one currency.
- No notifications (e-mail or push): members check the site.
- No mobile app: one web UI that also works on a phone screen.

## Constraints
- Python 3.12, FastAPI, SQLAlchemy Core; plain HTML and JavaScript in the UI, no framework.
- PostgreSQL on Neon from the first day; every schema change is a numbered SQL file in `migrations/`.
- Passwords are stored only as a bcrypt hash, never as readable text.
- Amounts are stored as integer cents, never as floats.
- Business rules and ownership checks live in `src/services/`, never in a route handler.
- No secret in the repository: keys come from environment variables.

## The model feature
<!-- Which model, which modality, and what it does for a user.
     Name three things or the check fails: the input it receives, the output it produces,
     and what happens when the model is slow, rate-limited or wrong. -->
- Model: Gemini 2.5 Flash (vision), called from `src/services/receipts.py` and nowhere else. Chosen because it reads a photo, has a free tier and is the course's recommended provider.
- Input: the receipt photo the user uploads, and nothing else about any user.
- Output: a suggested amount, date, merchant and category, shown in the add-expense form for the user to correct. Checked before it is shown: the amount must be a positive decimal, the date must parse and not be in the future, the category must be one of the fixed list (otherwise `other`).
- When it fails: no key, a timeout after 8 s or a 429 all leave the form empty with a note saying to type it in. Nothing is saved until the user presses save.
- Data that leaves the app: only the image. A receipt can carry the last digits of a card, so the image is neither stored nor logged.

## Auth
<!-- Local sign-in plus at least one provider. Say how an account signing in both ways stays one account. -->
- Local: e-mail and password, stored as a bcrypt hash; a server-side session in a `sessions` table, sent as an HttpOnly cookie.
- Provider: Sign in with Google, the authorization-code flow on the server, with `state`.
- Linking: matched on Google's account id; an e-mail is linked to an existing password account only when Google marks it as verified. Both ways end in the same session and the same `users` row.

## MCP tools
<!-- At least three tools your own MCP server exposes over this project's data.
     Each tool calls the same service functions the HTTP API calls, so the same rules apply.
     A description shorter than 20 characters is not a description. -->
| Tool | What it does | Who may call it |
| --- | --- | --- |
| `my_groups` | Lists the groups the signed-in user belongs to, with their role and current balance in each | the token's owner |
| `group_balance` | Shows who owes whom in one group, computed from its expenses and shares | members of that group |
| `list_expenses` | Lists the expenses of one group with payer, amount, date and category | members of that group |
| `add_expense` | Adds an expense to a group and splits it; refuses shares that do not add up to the total | members of that group |
| `read_receipt` | Reads a receipt photo and suggests amount, date, merchant and category, without saving anything | the token's owner |

Every tool calls the same function in `src/services/` as the matching HTTP route, as the user of `MCP_TOKEN`.

## UI
<!-- Stack, and the three or more screens. The graded checklist lives in docs/UI.md. -->
Plain HTML and JavaScript served by FastAPI, styled with CSS design tokens. Four screens: sign in, my groups, one group (expenses and balances), add expense (with receipt upload). The checklist is in `docs/UI.md`.

## Architecture
<!-- Exercise 3. One request traced through every layer, naming the file for each one,
     plus one place where your own code does not match this layering. -->

## Acceptance criteria
<!-- Every criterion carries an id. A test proves it by naming that id in its title, for example
     test('AC-3 a booking that overlaps another is refused with 409', ...).
     Say who acts, what they see, and what must be true in the database. -->
<!-- TODO Guillem: at least eight criteria for the whole project, ids AC-1, AC-2... -->

### Slice 1: sign-in and the my groups list
<!-- TODO Guillem: at least three more criteria, ids continuing. -->

## Traceability
<!-- Filled in from Exercise 3 onward: each AC id, and the test that names it. -->
| Criterion | Test |
| --- | --- |
| AC-1 |  |

## Spec vs result
<!-- After the agent builds the slice: which criteria passed, which it missed or reinterpreted, and what you changed in this spec because of it. -->
