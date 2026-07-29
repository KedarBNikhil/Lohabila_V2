import sys
from PySide6.QtWidgets import QApplication

from src.app.installer import InstallerWizard

app = QApplication(sys.argv)

wizard = InstallerWizard()
wizard.show()

sys.exit(app.exec())