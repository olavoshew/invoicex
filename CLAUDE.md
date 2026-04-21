# CLAUDE.md — CLI Automation Tool

<!-- .claude-governance-start -->
## .claude Governance (Mandatory)

**Do NOT start coding until this boot sequence is complete.**

1. Read `c:\Code\.claude\GOVERNANCE.md` -- rules, skill resolution, boundaries
2. Read `c:\Code\.claude\skills-registry.md` -- per-project skill mappings
3. Read `c:\Code\.claude\vault\CHANGELOG.md` -- what evolved since last session

For first session on this project, also read:
4. `c:\Code\.claude\vault\04-projects\08-cli-tool.md` -- current phase, session log
5. Each SKILL.md listed below
6. `c:\Code\.claude\vault\03-patterns\` -- reusable patterns from earlier projects

All rules, skill resolution, evolution protocol, and session end protocol are in GOVERNANCE.md.
<!-- .claude-governance-end -->

## Skills to Read Before Starting
```
c:\Code\Skills\antigravity-awesome-skills\skills\python-cli\SKILL.md
c:\Code\Skills\antigravity-awesome-skills\skills\click\SKILL.md
```

## Phase 1 — Problem Selection + Setup (~1hr)

**Goal:** Real problem locked. Package installs. `[tool] --help` works.

**Prompt:**
```
I'm building a CLI Automation Tool — a Python CLI that solves a specific workflow problem I actually have.

Working directory: c:\Code\Portfolio\08-cli-tool\

Phase 1: problem selection and project setup.

First, help me select the problem. The rule: must save real time on something I do more than twice a week. Options from PROJECT.md:
1. Rename batch media files (camera format → date-slug-title)
2. Weekly git status report → markdown draft
3. Job application tracker status summary from CSV
4. Screenshot organiser with context from clipboard
5. PDF invoice extractor → CSV with totals

For each option: (a) is this a real 5-minute manual task? (b) how hard to test? (c) does it have a clean --dry-run story?

Once problem is chosen:
1. `pyproject.toml` — Python 3.11+, entry point `[tool-name] = "src.cli:cli"`, deps: click, rich, python-dotenv. Package name should match the tool.
2. `.env.example` if needed
3. `src/cli.py` — click group with at minimum: main command + --dry-run flag + --help
4. `pip install -e .` installs cleanly

Rules: no comments, no docstrings, no em dashes.
```

## Phase 2 — Core Logic (~3hr)

**Goal:** The transformation works correctly. Testable without CLI. --dry-run is accurate.

**Prompt:**
```
Continue the CLI tool. Problem chosen: [PROBLEM]. Package installs. CLI skeleton works.

Working directory: c:\Code\Portfolio\08-cli-tool\

Phase 2: core business logic. The most important rule: core logic lives in src/core.py as pure functions — no click, no Rich, no file I/O side effects. The CLI in src/cli.py calls core.py and handles all output.

1. `src/core.py`:
   - Main transformation function(s) that take clean inputs and return clean outputs
   - No side effects — caller decides what to do with the result
   - No exceptions with bare tracebacks — raise ValueError with a clear message the user can act on

2. --dry-run behaviour in `src/cli.py`:
   - Calls core.py to determine what WOULD happen
   - Prints each action: "Would rename: [old] → [new]" (or equivalent for chosen problem)
   - Makes zero changes to filesystem/data

3. `src/config.py`:
   - Loads config from config.yaml (or .env) with sensible defaults
   - Config keys appropriate to the problem (e.g., date format string, output folder, CSV column names)

Rules: no comments, no docstrings, no em dashes. Core.py must be importable without side effects.
```

## Phase 3 — Config + Output (~1hr)

**Goal:** Configurable settings. Rich progress display. Friendly error messages.

**Prompt:**
```
Continue the CLI tool. Core logic works, --dry-run accurate. Phase 3: UX polish.

Working directory: c:\Code\Portfolio\08-cli-tool\

1. Rich output in `src/cli.py`:
   - Progress bar or spinner for any operation over 1 second
   - Summary table at end: "Processed: X items, Renamed: Y, Skipped: Z" (adjust columns for the problem)
   - Use Rich console.print for all output — not print()

2. Error handling in `src/cli.py`:
   - Catch ValueError from core.py, print as Rich error panel (not traceback)
   - Catch FileNotFoundError, print: "Could not find [path] — check the path and try again"
   - If ANTHROPIC_API_KEY is needed and missing, print: "Set ANTHROPIC_API_KEY in .env or as environment variable"
   - No bare except blocks anywhere

3. `config.yaml` (default config file in project root):
   - Populated with sensible defaults for the chosen problem
   - User can override any setting without touching code

Rules: no comments, no docstrings, no em dashes. All error messages end with a suggestion for what to do next.
```

## Phase 4 — Tests + README (~1hr)

**Goal:** Core logic tested. README leads with time savings. GitHub public.

**Prompt:**
```
Final phase for the CLI tool. Full tool works with Rich output and error handling.

Working directory: c:\Code\Portfolio\08-cli-tool\

1. `tests/test_core.py` — pytest tests for core.py:
   - Test the main transformation with known inputs → known outputs
   - Test that invalid input raises ValueError with a message that contains enough info to debug
   - Test edge cases: empty input, single item, maximum typical input
   - Zero I/O in tests — pass in-memory data, assert returned data

2. Verify: `pytest tests/test_core.py` passes with no real file system changes

3. `README.md`:
   - First paragraph: "This saves me [X] minutes per week because [specific reason]. Without it I had to [manual steps]." — be specific and honest.
   - Install: `pip install -e .`
   - Usage examples: normal run, --dry-run, custom config
   - --dry-run screenshot/output example

Rules: no em dashes, no AI vocabulary, no filler phrases. The README must sound like a real developer talking about a real problem.
```
