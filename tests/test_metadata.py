from hydra import initialize, compose
from datetime import datetime
from hac_analysis import metadata as md
import pytest


@pytest.fixture
def metadata():
    with initialize(version_base=None, config_path="../src/hac_analysis/conf"):
        cfg = compose(config_name="config")
        return md.load_metadata(cfg.paths.metadata_dir, cfg.metadata)


def test_find_benchmark(metadata):
    num = 92
    data = md.find_benchmark_data(num, metadata["benchmark"])
    assert len(data) == 1
    data = data[0]
    assert data["number"] == 92
    assert data["lid_state"]
    assert data["profiling"]
    assert data["mixing_head"] == "Taylor"
    assert data["dip_stick"] is None
    assert data["liquid"] == "water"
    assert data["volume"] is None
    assert data["start_time"] == "2018-01-11 09:25:27.000"
    assert data["end_time"] == "2018-01-11 09:49:51.000"
    assert data["notes"] == "testing"


def test_find_calibration_data(metadata):
    # Test searching with short tag
    tag = "TT1"
    data = md.find_calibration_data(tag, metadata["calibration"])
    assert len(data) == 1
    data = data[0]
    assert data["pid_ref"] == "TT17"
    assert data["short_tag"] == "TT1"
    assert data["long_tag"] == "GTW-1 Port 3 (T+RH) Top.Temp/RH 1.TT1"
    assert data["description"] == "Intake air temperature"
    assert data["raw_type"] == "int16"
    # assert data["eng_units"] == "°C"
    assert data["ref_offset"] == 0
    assert data["span"] == 1
    assert data["num_divs"] == 10
    assert data["coeff"] is None
    assert data["elevation_ref"] is None
    assert data["elevation_alt"] is None

    # Test searching with long tag
    long_tag = "GTW-1 Port 3 (T+RH) Top.Temp/RH 1.TT1"
    data = md.find_calibration_data(long_tag, metadata["calibration"])
    assert len(data) == 1
    data = data[0]
    assert data["pid_ref"] == "TT17"
    assert data["short_tag"] == "TT1"
    assert data["long_tag"] == "GTW-1 Port 3 (T+RH) Top.Temp/RH 1.TT1"
    assert data["description"] == "Intake air temperature"
    assert data["raw_type"] == "int16"
    # assert data["eng_units"] == "°C"
    assert data["ref_offset"] == 0
    assert data["span"] == 1
    assert data["num_divs"] == 10
    assert data["coeff"] is None
    assert data["elevation_ref"] is None
    assert data["elevation_alt"] is None


def test_find_database_table(metadata):
    start_time = datetime.fromisoformat("2018-01-29 10:51:41")
    end_time = datetime.fromisoformat("2018-01-29 11:55:49")
    data = md.find_database_table(start_time, end_time, metadata["database"]["tables"])
    assert len(data) == 1
    data = data[0]
    assert data["name"] == "Nov13th2017"
    assert data["database"] == "HAC"
