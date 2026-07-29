import json
from multiprocessing import context
import traceback
from pathlib import Path

from src.models.installer_context import InstallerContext


class ConfigWriter:

    def __init__(self, context: InstallerContext):
        self.context = context

    def write(self):

        print("ConfigWriter.write() called")
        traceback.print_stack(limit=10)

        install_dir = Path(self.context.install_directory)

        config_dir = install_dir / "config"

        config_dir.mkdir(parents=True, exist_ok=True)

        config = self._build_config()

        config_file = config_dir / "config.json"

        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)

        return config_file

    def _build_config(self):

        return {

        "application": {

            "name": "Lohabila BackupAgent",

            "version": "2.0.0",

            "config_version": 1
        },

        "customer": {

            "customer_name": self.context.customer_name,

            "company_name": self.context.company_name,

            "email": self.context.email,

            "phone": self.context.phone
        },

        "installation": {

            "install_directory": self.context.install_directory
        },

        "backup": {
        
            "standard_sources": self.context.backup_sources,
            "custom_sources": self.context.custom_backup_sources
},

        "repository": {

            "password_file": "config/repo_password.enc"
        },

        "schedule": {

            "enabled": self.context.schedule_enabled,

            "frequency": self.context.frequency,

            "start_date": self.context.start_date,

            "start_time": self.context.start_time,

            "day_of_week": self.context.day_of_week,

            "day_of_month": self.context.day_of_month
        },

        "execution": {

            "run_missed_backup": self.context.run_missed_backup,

            "retry_failed_backup": self.context.retry_failed_backup,

            "retry_attempts": self.context.retry_attempts,

            "retry_interval_minutes": self.context.retry_interval,

            "wake_computer": self.context.wake_computer,

            "skip_metered_connection": self.context.skip_metered_connection,

            "prevent_overlapping_backups": self.context.prevent_overlapping_backups,

            "run_only_when_user_logged_on": self.context.run_only_when_user_logged_on
        }
    }