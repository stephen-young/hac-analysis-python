"""
Module for loading and searching the metadata
"""

from pathlib import Path
from datetime import datetime
import json


def load_metadata(loc: str, names: dict) -> dict:
    bm_index = Path(loc) / names["benchmark"]
    calibration = Path(loc) / names["calibration"]
    constants = Path(loc) / names["constants"]
    database = Path(loc) / names["database"]

    bm_data = load_json_file(bm_index)
    calib_data = load_json_file(calibration)
    const_data = load_json_file(constants)
    db_data = load_json_file(database)

    data = {
        "benchmark": bm_data,
        "calibration": calib_data,
        "constants": const_data,
        "database": db_data,
    }

    return data


def load_json_file(file: Path) -> list[dict]:
    if not file.is_file() or not file.exists():
        raise FileNotFoundError(f"Could not {file.absolute()}")
    elif file.suffix != ".json":
        raise ValueError(f"{file.absolute()} is not a json file")
    with open(file, "r") as f:
        data = json.load(f)
    return data


def find_benchmark_data(num: int, bm_index: list[dict]) -> list[dict]:
    result = [bm for bm in bm_index if bm["number"] == num]
    return result


def find_calibration_data(tag: str, calib_data: list[dict]) -> list[dict]:
    result = [c for c in calib_data if c["short_tag"] == tag or c["long_tag"] == tag]
    return result


def find_database_table(
    start_time: datetime, end_time: datetime, table_data: list[dict]
) -> list[dict]:
    # TODO: Handle start_time and end_time spanning multiple tables
    if end_time < start_time:
        ValueError("End time is before start time")
    result = [
        tab
        for tab in table_data
        if start_time <= datetime.fromisoformat(tab["end"])
        and end_time >= datetime.fromisoformat(tab["start"])
    ]
    return result
