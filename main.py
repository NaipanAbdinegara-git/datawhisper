import argparse
from pathlib import Path

import pandas as pd
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


console = Console()


def load_data(file_path: Path) -> pd.DataFrame:
    """Load CSV or Excel into a DataFrame."""
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() in {".csv"}:
        df = pd.read_csv(file_path)
    elif file_path.suffix.lower() in {".xlsx", ".xls"}:
        df = pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Use CSV or Excel.")

    return df


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic validation and cleanup for raw tabular data."""
    if df.empty:
        raise ValueError("The data file is empty. Please provide a file with rows.")

    df = df.dropna(axis=1, how="all")
    df = df.dropna(axis=0, how="all")
    df.columns = [str(col).strip().replace(" ", "_").lower() for col in df.columns]

    return df


def summarize_data(df: pd.DataFrame) -> dict:
    """Build numerical and categorical insights for storytelling."""
    summary = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": int(df.isna().sum().sum()),
        "numeric_summary": {},
        "top_categories": {},
    }

    numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
    for col in numeric_columns:
        stats = df[col].describe()
        summary["numeric_summary"][col] = {
            "mean": float(stats["mean"]),
            "min": float(stats["min"]),
            "max": float(stats["max"]),
            "std": float(stats["std"]),
        }

    categorical_columns = _get_categorical_columns(df)
    for col in categorical_columns:
        top_values = df[col].value_counts(dropna=False).head(3).to_dict()
        summary["top_categories"][col] = top_values

    return summary


def _get_categorical_columns(df: pd.DataFrame) -> list[str]:
    string_columns = df.select_dtypes(include=["string", "category"]).columns.tolist()
    object_columns = [col for col in df.columns if df[col].dtype == object]

    for col in object_columns:
        sample = df[col].dropna()
        if sample.empty or sample.map(lambda value: isinstance(value, str)).all():
            string_columns.append(col)

    return list(dict.fromkeys(string_columns))


def build_summary_panel(summary: dict) -> Panel:
    content = Text()
    content.append(f"Rows: {summary['rows']}\n", style="bold cyan")
    content.append(f"Columns: {summary['columns']}\n", style="bold cyan")
    content.append(f"Fields: {', '.join(summary['column_names'])}\n")
    content.append(f"Missing values: {summary['missing_values']}\n")
    return Panel(content, title="DataWhisper Summary", border_style="bright_blue")


def build_numeric_table(summary: dict) -> Table:
    table = Table(title="Numeric Summary", header_style="bold magenta")
    table.add_column("Field", style="bold")
    table.add_column("Mean", justify="right")
    table.add_column("Min", justify="right")
    table.add_column("Max", justify="right")
    table.add_column("Std", justify="right")

    for col, stats in summary["numeric_summary"].items():
        table.add_row(
            col,
            f"{stats['mean']:.2f}",
            f"{stats['min']:.2f}",
            f"{stats['max']:.2f}",
            f"{stats['std']:.2f}",
        )

    return table


def build_category_table(summary: dict) -> Table:
    table = Table(title="Top Categories", header_style="bold magenta")
    table.add_column("Field", style="bold")
    table.add_column("Top values")

    for col, values in summary["top_categories"].items():
        formatted = ", ".join(f"{key} ({count})" for key, count in values.items())
        table.add_row(col, formatted)

    return table


def print_summary(summary: dict) -> None:
    console.print(build_summary_panel(summary))

    if summary["numeric_summary"]:
        console.print(build_numeric_table(summary))
    else:
        console.print("[yellow]No numeric columns found in the dataset.[/]")

    if summary["top_categories"]:
        console.print(build_category_table(summary))
    else:
        console.print("[yellow]No categorical columns found in the dataset.[/]")

    if summary["missing_values"] > 0:
        console.print(
            Panel(
                f"There are {summary['missing_values']} missing values in the dataset.",
                title="Data Quality",
                border_style="yellow",
            )
        )
    else:
        console.print(
            Panel(
                "No missing values detected. The dataset is clean enough for a first pass.",
                title="Data Quality",
                border_style="green",
            )
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DataWhisper - Convert raw CSV/Excel data into human story insights."
    )
    parser.add_argument(
        "file",
        type=Path,
        help="Path to a CSV or Excel file to analyze.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = args.file.resolve()

    try:
        df = load_data(file_path)
        df = validate_data(df)
        summary = summarize_data(df)
        print_summary(summary)
    except Exception as exc:
        console.print(f"[red]Error:[/] {exc}")
        console.print("Please make sure the file exists and is a valid CSV/XLSX file.")


if __name__ == "__main__":
    main()
