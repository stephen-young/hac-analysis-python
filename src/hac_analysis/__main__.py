import tomllib
import pprint
from pathlib import Path
from .metadata import load_metadata

# TODO: Add command-line interface

# Default values for configuration parameters
CONFIG_PATH = "config.toml"  # TODO: expose config path file in CLI
DEFAULT_CONFIG = {
    "paths": {"metadata_dir": "./metadata"},
    "metadata": {
        "benchmark": "benchmark_test_index.json",
        "calibration": "calibration_constants.json",
        "constants": "analysis_constants.json",
        "database": "database.json",
    },
}


def main() -> None:
    print(Path.cwd())
    config = DEFAULT_CONFIG
    config_file = Path(CONFIG_PATH)
    if config_file.exists():
        file_config = tomllib.loads(config_file.read_text())
        config = merge_config(config, file_config)
    pprint.pp(config)
    data = load_metadata(config["paths"]["metadata_dir"], config["metadata"])
    pprint.pp(data["benchmark"][0])


def merge_config(original: dict, new: dict) -> dict:
    # Merge default config and values from config file
    #   Recursively searches dictionaries to override default values with values in config file

    for key in original.keys():
        if isinstance(original[key], dict) and key in new:
            original[key] = merge_config(original[key], new[key])
        else:
            original[key] = new[key] if key in new else original[key]

    return original


if __name__ == "__main__":
    main()
