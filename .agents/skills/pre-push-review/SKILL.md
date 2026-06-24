# Skill: pre-push-review

## Activation

Invoke this skill before pushing a branch to the remote repository.

Explicit activation phrases:
- "Review before push"
- "Pre-push review"
- "Is this ready to push?"
- "Check my changes before pushing"
- "Run pre-push review"

---

## Purpose

Inspect every file changed on this branch against the framework's architecture rules, SOLID checklist, and common failure patterns. Produces a go / no-go verdict before the branch becomes a PR.

This skill is complementary to the `automation-framework-guardrails` skill (which runs during generation) — it catches drift, regressions, and oversights after the fact.

---

## Instructions for Claude

Work through the five phases below in order. Do not skip a phase. Do not return output until all five phases are complete.

---

### Phase 1 — Collect the diff

Run:

```bash
git diff main...HEAD --name-only
git diff main...HEAD
```

From the output:
- Build a list of every changed file and its layer (step, flow, factory, assertion, client, context, world, hooks, constants, utils, docs).
- Note whether any new files were added.
- Note whether any files were deleted.

If `main...HEAD` yields no output, try `origin/main...HEAD`. If the branch has no commits ahead of main, report "Nothing to review — branch is even with main" and stop.

---

### Phase 2 — Read changed files

Read every changed file in full. Do not rely on the diff alone — context outside the diff matters for layer rule checks.

---

### Phase 3 — Apply framework checks

For each check below, record **PASS**, **FAIL**, or **N/A** (if no relevant files changed).

#### 3A — Architecture guardrails (`standards/agent/architecture-guardrails.md`)

Read the file, then verify:

| # | Check |
|---|-------|
| 1 | Steps contain no raw Axios, no `HttpClient`, no business logic |
| 2 | Steps call only flows, assertions, and world context methods — no `if`/`switch`, no data lookups from JSON/constants, no `throw` statements |
| 3 | Flows contain no Cucumber imports |
| 4 | Flows use `StorageKeys` — no hardcoded storage key strings |
| 5 | Factories contain no HTTP calls, assertions, or world access |
| 6 | Assertions contain no API calls or payload construction |
| 7 | Clients/services contain no Cucumber imports, no world access |
| 8 | Correct world type used (`ApiWorld` / `E2EWorld` / `HybridWorld`) — not `ICustomWorld` in new code |
| 9 | B2B client constructed via `B2BClientFactory.fromWorld(world)` — not duplicated |
| 10 | Storage reads use `world.api.read<T>()` or `world.api.require<T>()` — not `world.api.storedValues[key]` directly |
| 11 | Storage writes use `world.api.store(key, value)` — not `world.api.storedValues[key] = value` directly |

#### 3A.12 — Feature file strategy tag conflicts

For every `.feature` file in the diff, scan the feature-level and scenario-level tags for conflicting strategy combinations. The framework's `resolveTestStrategy` throws at runtime — the Cucumber dry-run will NOT catch this because the Before hook is skipped in dry-run mode.

Conflicting combinations (any of these is a blocker):
- `@api` + `@e2e` on the same feature or scenario
- `@api` + `@hybrid` on the same feature or scenario
- `@e2e` + `@api` on the same feature or scenario

Valid combinations:
- `@api` alone (pure API scenarios)
- `@e2e` alone (browser + extension scenarios)
- `@hybrid` alone (API + browser scenarios)
- Any of the above with additional non-strategy tags (`@smoke`, `@eventbridge`, `@runners`, etc.)

**How to check:** grep for features using `@api` and verify none of the scenarios in that file also carry `@e2e` or `@hybrid` (inherited from feature level or added at scenario level). Repeat for `@e2e` and `@hybrid` features.

#### 3B — Common failure patterns (`standards/agent/common-failure-patterns.md`)

Read the file, then verify none of these patterns appear in the diff:

| # | Pattern |
|---|---------|
| 1 | Fat steps (raw HTTP inside a step) |
| 2 | Magic storage keys (string literals instead of `StorageKeys`) |
| 3 | Direct `storedValues` write bypass |
| 4 | Flow doing assertions (`expect()` inside a flow) |
| 5 | Runtime setup (browser launch) inside a flow |
| 6 | `HybridWorld` used for pure API code |
| 7 | Logic added to `GenericApiFlow` that should live in a named flow |
| 8 | Duplicated B2B client construction |
| 9 | Unconditional browser or API bootstrap in hooks |

#### 3C — Post-generation checklist (`standards/agent/validation/post-generation-checklist.md`)

Read the file and verify each item against the diff.

#### 3D — PR readiness checklist (`standards/agent/validation/pr-readiness-checklist.md`)

Read the file. Verify the architecture, documentation, and final-answer items (static checks are in Phase 4).

If new steps were added: confirm `docs/STEPS-INVENTORY.md` was updated.

---

### Phase 4 — Run static checks

Run all three commands. Capture and report full output.

```bash
npx tsc --noEmit
```

```bash
npm run test:api -- --dry-run --format summary
```

```bash
npm run test:ui -- --dry-run --format summary
```

A TypeScript error is a blocker. A Cucumber dry-run failure (undefined step, ambiguous match) is a blocker in either suite.

---

### Phase 5 — Deliver the verdict

Return a structured report in this exact format:

---

## Pre-Push Review Report

**Branch:** `<branch name>`
**Files changed:** `<count>` (`<count>` modified, `<count>` added, `<count>` deleted)

### Architecture Checks

| # | Check | Result |
|---|-------|--------|
| 1 | Steps thin — no raw HTTP | :white_check_mark: / :x: |
| 2 | Steps call only flows/assertions | :white_check_mark: / :x: |
| 3 | No Cucumber imports in flows | :white_check_mark: / :x: |
| 4 | No hardcoded storage keys | :white_check_mark: / :x: |
| 5 | Factories pure — no HTTP/assertions | :white_check_mark: / :x: |
| 6 | Assertions pure — no API calls | :white_check_mark: / :x: |
| 7 | Clients have no Cucumber/world access | :white_check_mark: / :x: |
| 8 | Correct world type | :white_check_mark: / :x: |
| 9 | B2B client via `B2BClientFactory` | :white_check_mark: / :x: |
| 10 | Storage reads via `read()`/`require()` | :white_check_mark: / :x: |
| 11 | Storage writes via `store()` | :white_check_mark: / :x: |
| 12 | No conflicting strategy tags (`@api`+`@e2e`, `@api`+`@hybrid`) in feature files | :white_check_mark: / :x: |

### Failure Pattern Checks

| # | Pattern | Result |
|---|---------|--------|
| 1 | No fat steps | :white_check_mark: / :x: |
| 2 | No magic keys | :white_check_mark: / :x: |
| 3 | No direct `storedValues` writes | :white_check_mark: / :x: |
| 4 | No assertions in flows | :white_check_mark: / :x: |
| 5 | No browser setup in flows | :white_check_mark: / :x: |
| 6 | No `HybridWorld` for pure API code | :white_check_mark: / :x: |
| 7 | No unrelated additions to `GenericApiFlow` | :white_check_mark: / :x: |
| 8 | No duplicated B2B client construction | :white_check_mark: / :x: |
| 9 | No unconditional hook expansion | :white_check_mark: / :x: |

### Static Checks

| Check | Result |
|-------|--------|
| `npx tsc --noEmit` | :white_check_mark: Clean / :x: `<error summary>` |
| Cucumber dry-run (API) | :white_check_mark: Clean / :x: `<error summary>` |
| Cucumber dry-run (UI) | :white_check_mark: Clean / :x: `<error summary>` |

### Documentation

| Check | Result |
|-------|--------|
| `STEPS-INVENTORY.md` updated (if steps added) | :white_check_mark: / :x: / N/A |
| No stale file references in docs | :white_check_mark: / :x: |

---

### Verdict

**GO** — all checks pass. Safe to push.

or

**NO-GO** — the following blockers must be resolved before pushing:

1. [blocker description with file and line reference]
2. ...

---

If any check is :x:, it is a blocker unless it is clearly pre-existing (present before this branch's changes). Pre-existing issues are noted but do not block the push.