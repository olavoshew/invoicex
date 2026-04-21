# PROJECT.md — CLI Automation Tool

## Concept
A Python CLI tool that solves a specific, real workflow pain point. Built because a real process was slow, not to demonstrate a skill set.

## Target User / Problem
You. Pick a task that you actually do manually more than twice a week. The specificity of the real problem is what makes this impressive — "I saved 45 minutes per week" beats any feature list.

## Candidate Problems (pick one before building)
1. **Rename batch of media files** from camera-format to date-slug-title format using metadata
2. **Weekly status report generator** — scrapes git log, summarises commits, outputs markdown report
3. **Job application tracker** — reads career-ops CSV, generates a status summary email draft
4. **Screenshot organiser** — finds unorganised screenshots, reads clipboard, renames with context
5. **PDF invoice extractor** — reads invoices in a folder, outputs a CSV with totals and dates

## Key Features (universal requirements)
- Config file for customisation (`config.yaml` or `.env`)
- Clear progress output using `rich` library
- Friendly error messages — no bare exceptions with stack traces
- `--dry-run` flag — show what would happen without changing anything
- Basic unit tests on the core transformation logic
- README includes: the before/after time savings in the first paragraph

## Tech Stack
- Python 3.11+
- `click` (CLI framework)
- `rich` (terminal output)
- PyPI-packaged (installable via `pip install .`)

## File Structure
```
src/
  cli.py         click entry point
  core.py        main business logic (testable without CLI)
  config.py      config loading
tests/
  test_core.py
pyproject.toml
README.md
```

## Definition of Done
- [ ] `pip install -e .` installs cleanly
- [ ] `--dry-run` mode works correctly
- [ ] Core logic has unit tests
- [ ] README first paragraph: "This saves me X minutes per week because..."
- [ ] GitHub repo public

## Why This Impresses Recruiters
Engineering mindset signal: you identified a real pain point and built a precise solution. Personal story is authentic and specific. Clean CLI with `--dry-run` and friendly errors shows production thinking beyond tutorial quality.
