# config_service.py
import json
from pathlib import Path


class ConfigService:

    CONFIG_DIR = (
        Path(__file__).resolve()
        .parents[2]
        / "config"
    )

    @classmethod
    def load_databases(cls):

        file_path = (
            cls.CONFIG_DIR
            / "databases.json"
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        return data["databases"]