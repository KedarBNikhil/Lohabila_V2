from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox
)

from PySide6.QtCore import Qt

from src.services.installer_engine import InstallerEngine

from pathlib import Path

class InstallationLocationPage(QWizardPage):

    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("BackupAgent Installation Location")

        self.setSubTitle(
            "Choose where BackupAgent should be installed."
        )

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
        40, 30, 40, 30
    )

        main_layout.setSpacing(20)

        info_label = QLabel(
    "Select the folder where BackupAgent will be installed."
)

        info_label.setWordWrap(True)

        main_layout.addWidget(info_label)

        path_layout = QHBoxLayout()

        self.txtInstallDirectory = QLineEdit()

        self.txtInstallDirectory.setText(
    r"C:\Program Files\Lohabila BackupAgent"
)
        self.txtInstallDirectory.setReadOnly(True)

        self.btnBrowse = QPushButton("Browse...")

        path_layout.addWidget(
            self.txtInstallDirectory
)

        path_layout.addWidget(
            self.btnBrowse
)

        main_layout.addLayout(path_layout)

        self.btnBrowse.clicked.connect(
            self.browse_folder
)
        
        self.setLayout(main_layout)

    def browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
        self,
        "Select Installation Folder",
        self.txtInstallDirectory.text()
    )

        if folder:

            self.txtInstallDirectory.setText(folder)

    def validatePage(self):

        install_directory = (
            self.txtInstallDirectory.text().strip()
    )

        if not install_directory:

            QMessageBox.warning(
            self,
            "Installation Folder Required",
            "Please select an installation folder."
        )

            return False

        parent = Path(install_directory)
        self.context.install_directory = str(
            parent / "Lohabila BackupAgent"
)

        return True
    
    def initializePage(self):

        if self.context.install_directory:

            self.txtInstallDirectory.setText(
            self.context.install_directory
        )