# DataWhisper

DataWhisper is a lightweight Python tool that turns raw CSV/Excel data into readable, story-style insights.
It loads tabular data, validates and cleans it, then prints a polished console summary using `rich`.

## What it does
- loads CSV or Excel files
- removes empty rows and columns
- standardizes field names
- summarizes numeric statistics
- extracts top categorical values
- displays everything in a beautiful Rich console layout

## Requirements
- Python 3.10+
- `pandas`
- `openpyxl`
- `rich`

## Install
```bash
cd "C:\Users\naipa\OneDrive\Dokumen\PYTHON"
pip install -r requirements.txt
```

## Run
```bash
python3 main.py sample_data.csv
```

## Run as a Web Application
```bash
python3 app.py
```

## Sample data
A sample dataset is included in `sample_data.csv` and `sample_missing_data.csv` so you can try the tool immediately.

## Files
- `main.py`: main DataWhisper application
- `requirements.txt`: dependencies for the project
- `sample_data.csv`: sample sales dataset for testing
