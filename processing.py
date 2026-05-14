from pathlib import Path
import pandas as pd

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