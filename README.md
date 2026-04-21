# invoicex

I was copying data from 10 to 20 PDF invoices into a spreadsheet every month -- about 20 minutes of tedious copy-paste. Without this tool I had to open each PDF, read the vendor name, invoice number, date, total, and GST amount, and type them into a CSV by hand. `invoicex` does the whole folder in under 5 seconds.

## Install

```bash
pip install -e .
```

## Usage

Extract all PDFs in a folder to CSV:

```bash
invoicex extract --input ./invoices --output summary.csv
```

Preview what would be extracted without writing anything:

```bash
invoicex extract --input ./invoices --dry-run
```

Use a custom config file:

```bash
invoicex extract --input ./invoices --config my_config.yaml
```

### Dry-run output example

```
Dry run -- no files will be written. Found 3 PDF(s).

  invoice_jan.pdf  vendor=Acme Web Services Pty Ltd  total=1,100.00  gst=100.00
  invoice_feb.pdf  vendor=Freelance Design Co        total=550.00    gst=50.00
  invoice_mar.pdf  vendor=?                          total=2,200.00  gst=200.00

Would write 3 row(s) to invoices.csv
┏━━━━━━━━━━━┳━━━━━━━━━┓
┃ Processed ┃ Skipped ┃
┡━━━━━━━━━━━╇━━━━━━━━━┩
│         3 │       0 │
└───────────┴─────────┘
```

## Configuration

Copy `config.yaml` from the project root and edit as needed:

```yaml
date_format: "%d/%m/%Y"

csv_columns:
  - filename
  - vendor
  - invoice_number
  - date
  - total
  - gst
```

If `config.yaml` is not found, the tool runs with the defaults above.

## Fields extracted

| Field | Description |
|---|---|
| `filename` | PDF filename |
| `vendor` | First meaningful line of the document (usually the business name) |
| `invoice_number` | Matched from "Invoice No:", "Inv #", etc. |
| `date` | First date found in DD/MM/YYYY, D Month YYYY, Month D YYYY, or YYYY-MM-DD format |
| `total` | Matched from "Total", "Amount due", "Balance due", including "inc. GST" variants |
| `gst` | Matched from a standalone "GST:" or "Tax:" line |

Missing fields are written as blank cells -- the row is never skipped.

## Running tests

```bash
pip install -e ".[dev]"
pytest tests/test_core.py -v
```
