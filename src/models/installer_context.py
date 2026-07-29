from dataclasses import dataclass, field
from typing import List


@dataclass
class InstallerContext:
    """
    Stores all information collected during the installation wizard.
    """

    # Customer Information
    customer_name: str = ""
    company_name: str = ""
    email: str = ""
    phone: str = ""
    device_name: str = ""

    # Installation
    install_directory: str = ""

    # Backup
    backup_sources: list[str] = field(default_factory=list)
    custom_backup_sources: list[str] = field(default_factory=list)

    # Security
    repository_password: str = ""

    # Schedule
    schedule_enabled: bool = True
    frequency: str = "Daily"

    start_date: str = ""
    start_time: str = ""

    day_of_week: str = ""
    day_of_month: int = ""

    # Execution Settings
    run_missed_backup: bool = True
    retry_failed_backup: bool = True
    retry_attempts: int = 3
    retry_interval: int = 5
    wake_computer: bool = False
    skip_metered_connection: bool = True
    
    # Azure
    customer_id: str = ""

    # Runtime
    installation_complete: bool = False

    # Additional Execution Settings
    prevent_overlapping_backups: bool = True
    run_only_when_user_logged_on: bool = True