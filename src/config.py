from copy import deepcopy
from pathlib import Path

import yaml

DEFAULT_CONFIG: dict = {
    "date_format": "%d/%m/%Y",
    "csv_columns": [
        "filename",
        "vendor",
        "invoice_number",
        "date",
        "total",
        "gst",
    ],
}


def load_config(path: str) -> dict:
    config_path = Path(path)
    if not config_path.exists():
        return deepcopy(DEFAULT_CONFIG)

    try:
        with open(config_path, encoding="utf-8") as f:
            loaded = yaml.safe_load(f) or {}
    except OSError as exc:
        raise ValueError(
            f"Could not read config file at {config_path} -- check the path and try again. ({exc})"
        )
    except yaml.YAMLError as exc:
        raise ValueError(
            f"Config file at {config_path} is not valid YAML -- fix the file and try again. ({exc})"
        )

    if not isinstance(loaded, dict):
        raise ValueError(
            f"Config file at {config_path} must contain key/value mappings -- update the file and try again."
        )

    merged = deepcopy(DEFAULT_CONFIG)
    merged.update(loaded)

    csv_columns = merged.get("csv_columns")
    if not isinstance(csv_columns, list) or not all(isinstance(item, str) for item in csv_columns):
        raise ValueError(
            "Config key csv_columns must be a list of column names -- update config.yaml and try again."
        )

    return merged
