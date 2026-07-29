from multiprocessing import context

from PySide6.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QCheckBox,
    QPushButton,
    QListWidget,
    QHBoxLayout,
    QFileDialog,
)

from src.app.pages.base_wizard_page import BaseWizardPage

from pathlib import Path


class BackupPage(BaseWizardPage):
    def __init__(self):
        super().__init__()

        self.setTitle("Backup Source Selection")
        self.setSubTitle(
    "Select the files and folders you want Lohabila Backup Agent to protect."
)

        main_layout = QVBoxLayout(self)
        
        # Common Locations
        common_group = QGroupBox("Common Locations")
        common_layout = QVBoxLayout()

        self.chkDesktop = QCheckBox("Desktop")
        self.chkDocuments = QCheckBox("Documents")
        self.chkDownloads = QCheckBox("Downloads")
        self.chkPictures = QCheckBox("Pictures")
        self.chkVideos = QCheckBox("Videos")
        self.chkMusic = QCheckBox("Music")

        self.common_locations = {
        self.chkDesktop: ("Desktop", Path.home() / "Desktop"),
        self.chkDocuments: ("Documents", Path.home() / "Documents"),
        self.chkDownloads: ("Downloads", Path.home() / "Downloads"),
        self.chkPictures: ("Pictures", Path.home() / "Pictures"),
        self.chkVideos: ("Videos", Path.home() / "Videos"),
        self.chkMusic: ("Music", Path.home() / "Music"),
}

        self.custom_folders = []

        self.chkDesktop.toggled.connect(self.update_common_locations)
        self.chkDocuments.toggled.connect(self.update_common_locations)
        self.chkDownloads.toggled.connect(self.update_common_locations)
        self.chkPictures.toggled.connect(self.update_common_locations)
        self.chkVideos.toggled.connect(self.update_common_locations)
        self.chkMusic.toggled.connect(self.update_common_locations)
        

        common_layout.addWidget(self.chkDesktop)
        common_layout.addWidget(self.chkDocuments)
        common_layout.addWidget(self.chkDownloads)
        common_layout.addWidget(self.chkPictures)
        common_layout.addWidget(self.chkVideos)
        common_layout.addWidget(self.chkMusic)

        common_group.setLayout(common_layout)

        main_layout.addWidget(common_group)

        # Custom Folders
        custom_group = QGroupBox("Custom Folders")
        custom_layout = QHBoxLayout()

        self.btnAddFolder = QPushButton("Add Folder...")
        self.btnRemoveFolder = QPushButton("Remove Selected")

        self.btnAddFolder.clicked.connect(self.add_folder)
        self.btnRemoveFolder.clicked.connect(self.remove_selected_folder)

        custom_layout.addWidget(self.btnAddFolder)
        custom_layout.addWidget(self.btnRemoveFolder)

        custom_group.setLayout(custom_layout)

        main_layout.addWidget(custom_group)

        # Selected Sources
        selected_group = QGroupBox("Selected Backup Sources")

        selected_layout = QVBoxLayout()

        self.lstBackupSources = QListWidget()

        selected_layout.addWidget(self.lstBackupSources)

        selected_group.setLayout(selected_layout)

        main_layout.addWidget(selected_group)

    def update_common_locations(self):

        self.lstBackupSources.clear()

        standard_sources = []
        custom_sources = []

        for checkbox, (display_name, path) in self.common_locations.items():

            if checkbox.isChecked():
                self.lstBackupSources.addItem(display_name)
                standard_sources.append(display_name)

        for folder in self.custom_folders:
            self.lstBackupSources.addItem(folder)
            custom_sources.append(folder)

        context = self.wizard().context

        context.backup_sources = standard_sources
        context.custom_backup_sources = custom_sources

    def add_folder(self):
        folder = QFileDialog.getExistingDirectory(
        self,
        "Select Folder to Backup"
    )

        if not folder:
            return

    # Prevent duplicates
        if folder in self.custom_folders:
            return

        self.custom_folders.append(folder)

    # Refresh the UI
        self.update_common_locations()

    def remove_selected_folder(self):
        current_item = self.lstBackupSources.currentItem()

        if current_item is None:
            return

        folder = current_item.text()

    # Only remove custom folders
        if folder in self.custom_folders:
            self.custom_folders.remove(folder)
            self.update_common_locations()