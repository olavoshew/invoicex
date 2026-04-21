import csv
from pathlib import Path

import pytest

from src.config import DEFAULT_CONFIG, load_config
from src.core import (
    InvoiceResult,
    _DATE_PATTERNS,
    _GST_PATTERNS,
    _INVOICE_NUMBER_PATTERNS,
    _TOTAL_PATTERNS,
    _parse_field,
    _parse_vendor,
    find_pdfs,
    write_csv,
)


class TestParseVendor:
    def test_returns_first_meaningful_line(self):
        text = "Acme Web Services Pty Ltd\nABN: 12 345 678 901\nInvoice No: INV-001"
        assert _parse_vendor(text) == "Acme Web Services Pty Ltd"

    def test_skips_leading_numeric_lines(self):
        text = "12345\n---\nFreelance Design Co"
        assert _parse_vendor(text) == "Freelance Design Co"

    def test_empty_string_returns_none(self):
        assert _parse_vendor("") is None

    def test_only_symbols_returns_none(self):
        assert _parse_vendor("---\n***\n...") is None


class TestParseInvoiceNumber:
    def test_standard_invoice_no(self):
        result = _parse_field("Invoice No: INV-2024-042", _INVOICE_NUMBER_PATTERNS)
        assert result == "INV-2024-042"

    def test_inv_hash_format(self):
        result = _parse_field("Inv #AB-99", _INVOICE_NUMBER_PATTERNS)
        assert result == "AB-99"

    def test_no_match_returns_none(self):
        result = _parse_field("Nothing useful here", _INVOICE_NUMBER_PATTERNS)
        assert result is None


class TestParseDate:
    def test_dd_mm_yyyy(self):
        result = _parse_field("Date: 15/03/2024", _DATE_PATTERNS)
        assert result == "15/03/2024"

    def test_d_month_yyyy(self):
        result = _parse_field("Issued: 15 March 2024", _DATE_PATTERNS)
        assert result == "15 March 2024"

    def test_month_d_yyyy(self):
        result = _parse_field("March 15, 2024", _DATE_PATTERNS)
        assert result == "March 15, 2024"

    def test_iso_format(self):
        result = _parse_field("2024-03-15", _DATE_PATTERNS)
        assert result == "2024-03-15"

    def test_no_match_returns_none(self):
        result = _parse_field("No date here", _DATE_PATTERNS)
        assert result is None


class TestParseTotal:
    def test_total_inc_gst(self):
        result = _parse_field("Total inc. GST: $1,100.00", _TOTAL_PATTERNS)
        assert result == "1,100.00"

    def test_amount_due(self):
        result = _parse_field("Amount due: $550", _TOTAL_PATTERNS)
        assert result == "550"

    def test_no_match_returns_none(self):
        result = _parse_field("Nothing here", _TOTAL_PATTERNS)
        assert result is None


class TestParseGst:
    def test_standalone_gst_line(self):
        result = _parse_field("GST: $100.00", _GST_PATTERNS)
        assert result == "100.00"

    def test_does_not_match_total_inc_gst_line(self):
        text = "Total inc. GST: $1,100.00\nGST: $100.00"
        result = _parse_field(text, _GST_PATTERNS)
        assert result == "100.00"

    def test_no_match_returns_none(self):
        result = _parse_field("Total inc. GST: $1,100.00", _GST_PATTERNS)
        assert result is None


class TestWriteCsv:
    def test_writes_correct_headers_and_row(self, tmp_path):
        results = [
            InvoiceResult(
                filename="inv_001.pdf",
                vendor="Acme Pty Ltd",
                invoice_number="INV-001",
                date="15/03/2024",
                total="1100.00",
                gst="100.00",
            )
        ]
        output = tmp_path / "out.csv"
        columns = ["filename", "vendor", "invoice_number", "date", "total", "gst"]
        write_csv(results, output, columns)

        with open(output, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["filename"] == "inv_001.pdf"
        assert rows[0]["vendor"] == "Acme Pty Ltd"
        assert rows[0]["invoice_number"] == "INV-001"
        assert rows[0]["date"] == "15/03/2024"
        assert rows[0]["total"] == "1100.00"
        assert rows[0]["gst"] == "100.00"

    def test_columns_arg_controls_output_fields(self, tmp_path):
        results = [
            InvoiceResult(
                filename="inv_001.pdf",
                vendor="Acme Pty Ltd",
                invoice_number="INV-001",
                date="15/03/2024",
                total="1100.00",
                gst="100.00",
            )
        ]
        output = tmp_path / "partial.csv"
        write_csv(results, output, ["filename", "total"])

        with open(output, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert list(rows[0].keys()) == ["filename", "total"]

    def test_empty_results_writes_headers_only(self, tmp_path):
        output = tmp_path / "empty.csv"
        columns = ["filename", "vendor", "invoice_number", "date", "total", "gst"]
        write_csv([], output, columns)

        with open(output, encoding="utf-8") as f:
            content = f.read()

        assert content.strip() == ",".join(columns)

    def test_none_fields_written_as_empty_string(self, tmp_path):
        results = [
            InvoiceResult(
                filename="inv_002.pdf",
                vendor=None,
                invoice_number=None,
                date=None,
                total=None,
                gst=None,
            )
        ]
        output = tmp_path / "nulls.csv"
        columns = ["filename", "vendor", "total", "gst"]
        write_csv(results, output, columns)

        with open(output, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert rows[0]["vendor"] == ""
        assert rows[0]["total"] == ""


class TestFindPdfs:
    def test_finds_pdf_files_case_insensitive(self, tmp_path):
        (tmp_path / "a.pdf").write_text("a", encoding="utf-8")
        (tmp_path / "b.PDF").write_text("b", encoding="utf-8")
        (tmp_path / "c.txt").write_text("c", encoding="utf-8")

        files = find_pdfs(tmp_path)

        assert [file.name for file in files] == ["a.pdf", "b.PDF"]


class TestLoadConfig:
    def test_missing_config_returns_isolated_defaults(self, tmp_path):
        config_path = tmp_path / "missing.yaml"

        config_one = load_config(str(config_path))
        config_one["csv_columns"].append("extra")
        config_two = load_config(str(config_path))

        assert config_two["csv_columns"] == DEFAULT_CONFIG["csv_columns"]

    def test_invalid_yaml_raises_value_error(self, tmp_path):
        config_path = tmp_path / "bad.yaml"
        config_path.write_text("csv_columns: [filename, vendor\n", encoding="utf-8")

        with pytest.raises(ValueError, match="not valid YAML"):
            load_config(str(config_path))

    def test_non_mapping_yaml_raises_value_error(self, tmp_path):
        config_path = tmp_path / "bad_shape.yaml"
        config_path.write_text("- filename\n- vendor\n", encoding="utf-8")

        with pytest.raises(ValueError, match="must contain key/value mappings"):
            load_config(str(config_path))

    def test_invalid_csv_columns_type_raises_value_error(self, tmp_path):
        config_path = tmp_path / "bad_columns.yaml"
        config_path.write_text("csv_columns: vendor\n", encoding="utf-8")

        with pytest.raises(ValueError, match="csv_columns must be a list"):
            load_config(str(config_path))
