from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from src.services.installer_engine import InstallerEngine

class ReviewPage(QWizardPage):

    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("Review & Install")

        self.setSubTitle(
            "Review your configuration before installing BackupAgent."
        )

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        info = QLabel(
        "Please review your installation settings below. "
        "If everything looks correct, click Install to begin installation."
    )

        info.setWordWrap(True)

        layout.addWidget(info)

        self.summaryBox = QTextEdit()

        self.summaryBox.setReadOnly(True)

        layout.addWidget(self.summaryBox)

        note = QLabel(
        "Click Install to configure BackupAgent, create the backup repository, "
        "register scheduled backups and complete the installation."
    )

        note.setWordWrap(True)

        layout.addWidget(note)

        self.btnInstall = QPushButton("Install")

        self.btnInstall.clicked.connect(
        self.install_backup_agent
    )

        layout.addWidget(self.btnInstall)

        self.setLayout(layout)

    def initializePage(self):

        if self.context.frequency == "Weekly":

            schedule = (
            f"Weekly ({self.context.day_of_week}) "
            f"at {self.context.start_time}"
        )

        elif self.context.frequency == "Monthly":

            schedule = (
            f"Monthly (Day {self.context.day_of_month}) "
            f"at {self.context.start_time}"
        )

        else:

            schedule = (
            f"Daily at {self.context.start_time}"
        )
            
        sources = ""

        for source in self.context.backup_sources:

            sources += f"• {source}\n"

        summary = f"""
Customer Information
----------------------------

Customer Name : {self.context.customer_name}
Company Name  : {self.context.company_name}
Email         : {self.context.email}
Phone         : {self.context.phone}

Backup Configuration
----------------------------

Backup Sources

{sources}

Schedule
----------------------------

{schedule}

Execution Settings
----------------------------

Run missed backup          : {"Yes" if self.context.run_missed_backup else "No"}

Retry failed backups       : {"Yes" if self.context.retry_failed_backup else "No"}

Retry attempts             : {self.context.retry_attempts}

Retry interval             : {self.context.retry_interval} minutes

Wake computer              : {"Yes" if self.context.wake_computer else "No"}

Skip metered connection    : {"Yes" if self.context.skip_metered_connection else "No"}

Prevent overlapping jobs   : {"Yes" if self.context.prevent_overlapping_backups else "No"}

Run only when logged on    : {"Yes" if self.context.run_only_when_user_logged_on else "No"}

Installation
----------------------------

Install Location

{self.context.install_directory}
"""
        self.summaryBox.setPlainText(summary)

    def install_backup_agent(self):

        self.btnInstall.setEnabled(False)

        engine = InstallerEngine(self.context)

        result = engine.install()

        if result.success:

            QMessageBox.information(

            self,

            "Installation Complete",

            "BackupAgent was installed successfully."

        )

            self.wizard().accept()

        else:

            QMessageBox.critical(

            self,

            "Installation Failed",

            result.stderr

        )

            self.btnInstall.setEnabled(True)