from loguru import logger
from pathlib import Path
import pandas as pd
import re


# ---------------------------------------------------------------------
# PUBLIC ENTRYPOINT
# ---------------------------------------------------------------------

def processor() -> None:
    """
    Load the latest raw CSV file, apply user-defined processing,
    and write the processed output to the processed/ directory.
    """
    logger.info("Starting data processing step")

    raw_file = _get_latest_raw_file()
    logger.info(f"Loading raw data from: {raw_file.name}")

    df = pd.read_csv(raw_file)

    # --------------------------------------------------
    # USER-DEFINED PROCESSING LOGIC
    # --------------------------------------------------
    df_processed = _process_logic(df)

    output_path = _format_processed_output_path(raw_file)
    df_processed.to_csv(output_path, index=False)

    logger.info(f"Processed data written to: {output_path.name}")


# ---------------------------------------------------------------------
# USER-DEFINED PROCESSING LOGIC
# ---------------------------------------------------------------------

def _process_logic(df: pd.DataFrame) -> pd.DataFrame:
    """
    User-defined data processing logic.
    Modify this function freely.
    """

    # Example placeholder logic
    df = df.copy()

    # Example: add ingestion timestamp
    df["processed"] = True

    return df


# ---------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------

def _get_latest_raw_file() -> Path:
    """
    Returns the Path to the raw_data_{N}.csv file with the highest N.
    """
    script_dir = Path(__file__).parent
    raw_dir = script_dir / "raw"

    if not raw_dir.exists():
        raise FileNotFoundError("raw/ directory does not exist")

    raw_files = list(raw_dir.glob("raw_data_*.csv"))

    if not raw_files:
        raise FileNotFoundError("No raw_data_*.csv files found")

    def extract_number(path: Path) -> int:
        match = re.search(r"raw_data_(\d+)\.csv", path.name)
        if not match:
            raise ValueError(f"Invalid raw file name: {path.name}")
        return int(match.group(1))

    latest_file = max(raw_files, key=extract_number)
    return latest_file


def _format_processed_output_path(raw_file: Path) -> Path:
    """
    Generate processed/processed_data_{N}.csv corresponding to raw_data_{N}.csv.
    """
    script_dir = Path(__file__).parent
    processed_dir = script_dir / "processed"
    processed_dir.mkdir(exist_ok=True)

    match = re.search(r"raw_data_(\d+)\.csv", raw_file.name)
    if not match:
        raise ValueError(f"Invalid raw file name: {raw_file.name}")

    file_num = match.group(1)
    output_file = processed_dir / f"processed_data_{file_num}.csv"

    return output_file


# ---------------------------------------------------------------------
# SCRIPT ENTRY
# ---------------------------------------------------------------------

if __name__ == "__main__":
    processor()
