from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from src.config import load_config
from src.core import extract_invoice, find_pdfs, write_csv

console = Console()


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--input",
    "input_dir",
    default=".",
    show_default=True,
    type=click.Path(exists=False, file_okay=False),
    help="Folder containing PDF invoices.",
)
@click.option(
    "--output",
    "output_path",
    default="invoices.csv",
    show_default=True,
    type=click.Path(),
    help="Path for the output CSV file.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Show what would be extracted without writing any files.",
)
@click.option(
    "--config",
    "config_path",
    default="config.yaml",
    show_default=True,
    type=click.Path(),
    help="Path to config file.",
)
def extract(input_dir, output_path, dry_run, config_path):
    try:
        config = load_config(config_path)
    except ValueError as exc:
        console.print(
            Panel(str(exc), title="[red]Config Error[/red]", border_style="red")
        )
        return

    folder = Path(input_dir)

    if not folder.exists():
        console.print(f"[red]Could not find [bold]{folder}[/bold] -- check the path and try again.[/red]")
        return

    if not folder.is_dir():
        console.print(f"[red]{folder} is not a folder -- provide a directory path and try again.[/red]")
        return

    try:
        pdfs = find_pdfs(folder)
    except OSError as exc:
        console.print(
            Panel(
                f"Could not list files in {folder} -- check folder permissions and try again. ({exc})",
                title="[red]Input Error[/red]",
                border_style="red",
            )
        )
        return

    if not pdfs:
        console.print(f"[yellow]No PDF files found in [bold]{folder}[/bold] -- check the path and try again.[/yellow]")
        return

    if dry_run:
        console.print(f"[bold yellow]Dry run[/bold yellow] -- no files will be written. Found [bold]{len(pdfs)}[/bold] PDF(s).\n")

    results = []
    skipped = 0

    if dry_run:
        for pdf_path in pdfs:
            try:
                result = extract_invoice(pdf_path)
                results.append(result)
                console.print(
                    f"  [cyan]{result.filename}[/cyan]"
                    f"  vendor=[green]{result.vendor or '?'}[/green]"
                    f"  total=[green]{result.total or '?'}[/green]"
                    f"  gst=[green]{result.gst or '?'}[/green]"
                )
            except ValueError as exc:
                console.print(
                    Panel(str(exc), title=f"[red]Skipped: {pdf_path.name}[/red]", border_style="red")
                )
                skipped += 1
    else:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task("Extracting...", total=len(pdfs))
            for pdf_path in pdfs:
                progress.update(task, description=f"Reading [cyan]{pdf_path.name}[/cyan]")
                try:
                    result = extract_invoice(pdf_path)
                    results.append(result)
                except ValueError as exc:
                    console.print(
                        Panel(str(exc), title=f"[red]Skipped: {pdf_path.name}[/red]", border_style="red")
                    )
                    skipped += 1
                progress.advance(task)

    table = Table(show_header=True, header_style="bold")
    table.add_column("Processed", justify="right")
    table.add_column("Skipped", justify="right")
    table.add_row(str(len(results)), str(skipped))

    if dry_run:
        console.print(f"\n[bold]Would write {len(results)} row(s) to [cyan]{output_path}[/cyan][/bold]")
        console.print(table)
        return

    try:
        write_csv(results, Path(output_path), config["csv_columns"])
    except FileNotFoundError:
        console.print(
            f"[red]Could not find {output_path} -- check the output path and try again.[/red]"
        )
        return
    except PermissionError:
        console.print(
            f"[red]Could not write to {output_path} -- check file permissions and try again.[/red]"
        )
        return
    except OSError as exc:
        console.print(
            Panel(
                f"Could not write CSV to {output_path} -- check the output path and try again. ({exc})",
                title="[red]Write Error[/red]",
                border_style="red",
            )
        )
        return

    console.print(f"\n[bold green]Wrote {len(results)} row(s) to [cyan]{output_path}[/cyan][/bold green]")
    console.print(table)
