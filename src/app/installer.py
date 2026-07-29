from PySide6.QtWidgets import QWizard

from src.models.installer_context import InstallerContext

from src.app.pages.welcome_page import WelcomePage

from src.app.pages.customer_page import CustomerPage

from src.app.pages.backup_page import BackupPage

from src.app.pages.acknowledgement_page import AcknowledgementPage

from src.app.pages.password_page import PasswordPage

from src.services.installer_engine import InstallerEngine

from src.app.pages.schedule_page import SchedulePage

from src.app.pages.execution_settings_page import ExecutionSettingsPage

from src.app.pages.installation_location_page import InstallationLocationPage

from src.app.pages.review_page import ReviewPage


class InstallerWizard(QWizard):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lohabila Backup Agent Installer")
        self.setMinimumSize(900, 600)
        self.context = InstallerContext()
        self.addPage(WelcomePage())
        self.addPage(CustomerPage())
        self.addPage(BackupPage())
        self.addPage(AcknowledgementPage(self.context))
        self.addPage(PasswordPage(self.context))
        self.addPage(SchedulePage(self.context))
        self.addPage(ExecutionSettingsPage(self.context))
        self.addPage(InstallationLocationPage(self.context))
        self.addPage(ReviewPage(self.context))

    def accept(self):
        super().accept()
    