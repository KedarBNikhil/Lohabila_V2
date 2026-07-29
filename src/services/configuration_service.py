from pathlib import Path
import json


class ConfigurationService:

    def __init__(self):
        self.config_path = Path(
            r"D:\Telegram\Lohabila BackupAgent\Config\config.json"
        )

    def load(self):
        print("Reading config from:", self.config_path)
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)