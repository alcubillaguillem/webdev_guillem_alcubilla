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
Plain HTML and JavaScript served by FastAPI, styled with CSS design tokens. Five screens: sign in, create an account, my groups, one group (expenses and balances), add expense (with receipt upload). The checklist is in `docs/UI.md`.

## Architecture
<!-- Exercise 3. One request traced through every layer, naming the file for each one,
     plus one place where your own code does not match this layering. -->

## Acceptance criteria
<!-- Every criterion carries an id. A test proves it by naming that id in its title, for example
     test('AC-3 a booking that overlaps another is refused with 409', ...).
     Say who acts, what they see, and what must be true in the database. -->
- [AC-1] A member who adds an expense of 30.00 € split equally among three members sees it in the group's list, and `expense_shares` holds three rows of 1000 cents each.
- [AC-2] A member who adds an expense whose shares do not add up to the total gets 422 with "The shares must add up to the total", and no row appears in `expenses`.
- [AC-3] A signed-in user who is not a member of a group and tries to add an expense to it gets 403, and no row appears in `expenses`.
- [AC-4] A member who tries to edit or delete an expense paid by another member gets 403, and the expense is unchanged; without a session the same request gets 401.
- [AC-5] After Ana pays 30.00 € split equally with Ben and Carla, the group screen shows "Ben owes Ana 10.00 €" and "Carla owes Ana 10.00 €".
- [AC-6] A member with a non-zero balance who tries to leave the group gets 409 with "Settle your balance before leaving", and their row in `memberships` remains.
- [AC-7] Only the owner can remove a member: a member who tries gets 403; the owner's request deletes the row in `memberships`.
- [AC-8] Signing in with Google with a verified address that already has a password account signs into that account: no second row appears in `users`.
- [AC-9] With no model key set, uploading a receipt leaves the amount, date, merchant and category fields empty and shows "Could not read the receipt, type it in"; no row appears in `expenses`.
- [AC-10] A receipt for which the model returns a category outside the fixed list is shown with the category `other`, and a date in the future is left blank.
- [AC-11] The MCP tool `add_expense` with shares that do not add up returns `isError: true` with the same message as the API (AC-2), and no row appears in `expenses`.

### Slice 1: sign-in and the my groups list
- [AC-12] A visitor who opens `/groups` without signing in lands on `/login`, and `GET /api/groups` without a session returns 401.
- [AC-13] After signing in with a seeded account (`ana@example.com`), `/groups` shows the two seeded groups she belongs to, each with its name and her role, and not the seeded group she is not in.
- [AC-14] Signing in with a wrong password shows "Wrong e-mail or password" and no row appears in `sessions`.
- [AC-15] Deleting Ana's row in `memberships` for one group and reloading `/groups` removes that group from the screen.
- [AC-16] Pressing "Sign out" on `/groups` deletes the user's row in `sessions`, and reloading `/groups` lands on `/login`.
- [AC-17] A visitor who creates an account on `/register` with a new e-mail, a name and a password of 8 or more characters lands on `/groups` signed in; `users` has one new row whose `password_hash` is a bcrypt hash, never the password.
- [AC-18] Creating an account with an e-mail that already exists gets 409 with "An account with this e-mail already exists", and no new row appears in `users`; a password shorter than 8 characters gets 422 and no row either.

## Traceability
<!-- Filled in from Exercise 3 onward: each AC id, and the test that names it. -->
| Criterion | Test |
| --- | --- |
| AC-12 | `tests/test_slice1.py::test_ac12_groups_page_without_session_redirects_to_login`, `test_ac12_groups_api_without_session_returns_401` |
| AC-13 | `tests/test_slice1.py::test_ac13_signed_in_user_sees_only_her_groups_with_role` |
| AC-14 | `tests/test_slice1.py::test_ac14_wrong_password_is_refused_and_creates_no_session` |
| AC-15 | `tests/test_slice1.py::test_ac15_removed_membership_disappears_from_the_list` |
| AC-16 | `tests/test_slice1.py::test_ac16_sign_out_deletes_the_session` |
| AC-17 | `tests/test_register.py::test_ac17_new_account_is_created_hashed_and_signed_in` |
| AC-18 | `tests/test_register.py::test_ac18_existing_email_is_refused_with_409`, `test_ac18_short_password_is_refused_with_422` |
| AC-1 to AC-11 | (from Exercise 3) |

## Spec vs result
<!-- After the agent builds the slice: which criteria passed, which it missed or reinterpreted, and what you changed in this spec because of it. -->
- Passed: AC-12 to AC-15, checked by hand against PostgreSQL: `curl -i /groups` → 302 to `/login`, `curl -i /api/groups` → 401; Ana sees her two groups with her role and not the Rila trip; a wrong password shows "Wrong e-mail or password" with 0 rows in `sessions`; deleting her Plovdiv membership removed it on reload.
- Reinterpreted: the agent added a "Sign out" button and matched e-mails case-insensitively. Neither was in any criterion, so nothing said what signing out must do to the database.
- Changed: added [AC-16]: signing out deletes the row in `sessions` and `/groups` goes back to `/login`.
