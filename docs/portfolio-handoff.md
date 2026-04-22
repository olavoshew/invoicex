# Portfolio Handoff: invoicex

## Quick Metadata

- Project name: invoicex
- Repo URL: https://github.com/olavoshew/invoicex
- GitHub About: Bulk extract invoice data from PDF folders to CSV with a Python CLI, dry-run preview, config, and test coverage.
- GitHub topics: python, cli-tool, automation, pdf-extraction, invoice-processing, batch-processing, click, rich

## One-Line Summary

A Python CLI that batch-extracts invoice fields from PDF folders into CSV, replacing repetitive manual spreadsheet entry.

## Problem

I was manually opening PDF invoices, reading vendor names, invoice numbers, dates, totals, and GST amounts, then typing them into a spreadsheet. It was repetitive, easy to get wrong, and took about 20 minutes each week.

## Solution

invoicex scans a folder of invoice PDFs, extracts the key fields, and writes a clean CSV in one command. It also supports dry-run previews, configurable output columns, and clear terminal feedback.

## Why It Matters

This is a real automation tool built around a repeated workflow I actually had. The value is easy to explain, the time saved is measurable, and the implementation shows production-minded CLI design instead of a one-off script.

## Portfolio Card Copy

invoicex is a Python CLI that extracts vendor, invoice number, date, total, and GST from PDF invoices and writes the results to CSV. I built it to replace a weekly manual copy-paste workflow with a repeatable batch command.

## Portfolio Case Study Copy

I built invoicex to automate a small but recurring admin task: copying invoice data from PDF files into a spreadsheet. The tool reads a folder of invoices, extracts the useful fields, and exports them to CSV in seconds. I kept the extraction logic separate from the CLI so it could be tested cleanly, added a dry-run mode so the output can be checked before writing files, and used Rich for readable terminal feedback and error handling.

## Key Signals

- Real workflow problem with specific time savings
- Clean split between CLI and core business logic
- Pure extraction functions that are testable without CLI wiring
- Dry-run support before writing output
- YAML config for output control
- Rich terminal UX and friendly error handling
- Automated tests for parsing and config behavior

## Tech Stack

- Python 3.11+
- Click
- Rich
- pdfplumber
- PyYAML
- pytest

## Demo Commands

```bash
pip install -e .
invoicex extract --input ./invoices --dry-run
invoicex extract --input ./invoices --output summary.csv
pytest tests/test_core.py -v
```

## Project Structure Notes

- `src/cli.py` handles commands, terminal output, and user-facing errors
- `src/core.py` holds the extraction logic and CSV writing helpers
- `src/config.py` loads config defaults and validates YAML input
- `tests/test_core.py` covers parsing, config loading, CSV output, and PDF discovery behavior

## Scope Boundaries

- Best suited to text-based PDF invoices
- Extraction is regex-driven, so very unusual invoice layouts can reduce recall
- This tool exports CSV data, it does not perform OCR or accounting platform sync

## When Adding This To The Portfolio Repo

Use the one-line summary for the project card, use the case study copy for the project detail page, and carry over the GitHub About text and topics as written above.