from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QTextBrowser,
    QCheckBox,
    QVBoxLayout,
)

from PySide6.QtCore import Qt


class AcknowledgementPage(QWizardPage):
    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("Repository Encryption & Customer Acknowledgement")
        self.setSubTitle(
            "Please read the following information carefully before continuing."
        )

        self.build_ui()
        self.connect_signals()

    def build_ui(self):
        # Main layout
        layout = QVBoxLayout()

        layout.setSpacing(12)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Information panel
        self.information = QTextBrowser()

        self.information.setReadOnly(True)
        self.information.setOpenExternalLinks(True)

        self.information.setMinimumHeight(220)
        self.information.setMaximumHeight(260)
        self.information.setHtml("""
<h2>🔒 Repository Encryption</h2>

<h3>Protecting Your Data</h3>

<p>
Every backup created by <b>Lohabila Systems</b> is encrypted using a unique repository password that only you control.
</p>

<p>
This encryption helps ensure that your backup data remains private and secure.
</p>

<p>
For security reasons, <b>Lohabila Systems</b> does not store, transmit, or have access to your repository password.
</p>

<hr>

<h2>📋 Important Information</h2>

<ul>
<li>Your repository password encrypts all backup data.</li>

<li>The same password is required whenever your data needs to be restored.</li>

<li>Store your repository password in a secure password manager or another safe location.</li>

<li>Lohabila Systems cannot recover or reset your repository password.</li>

<li>If the password is lost, encrypted backup data may become permanently inaccessible.</li>

<li>Without the correct repository password, backups cannot be decrypted or restored.</li>

<li>Never share your repository password with unauthorized individuals.</li>

<li>Use a unique password that is not reused for any other application or online service.</li>

</ul>
""")
        # Customer acknowledgement checkboxes
        self.chkResponsibility = QCheckBox(
    "I understand that I am solely responsible for securely storing my repository password."
)

        self.chkRecovery = QCheckBox(
    "I understand that Lohabila Systems cannot recover or reset my repository password."
)

        self.chkRestore = QCheckBox(
    "I understand that encrypted backups cannot be restored without the correct repository password."
)

        self.chkRead = QCheckBox(
    "I have read and understood the information provided above."
)
        # Add widgets to the layout
        layout.addWidget(self.information)
        layout.addSpacing(15)

        ackLabel = QLabel("<b>Customer Acknowledgement</b>")
        layout.addWidget(ackLabel)

        layout.addWidget(self.chkResponsibility)
        layout.addWidget(self.chkRecovery)
        layout.addWidget(self.chkRestore)
        layout.addWidget(self.chkRead)

        # Push everything to the top of the page
        layout.addStretch()

        # Apply the layout to the page
        self.setLayout(layout)

    def connect_signals(self):
        self.chkResponsibility.stateChanged.connect(self.on_checkbox_changed)
        self.chkRecovery.stateChanged.connect(self.on_checkbox_changed)
        self.chkRestore.stateChanged.connect(self.on_checkbox_changed)
        self.chkRead.stateChanged.connect(self.on_checkbox_changed)

    def on_checkbox_changed(self):
        self.completeChanged.emit()

    def isComplete(self):
        return (
            self.chkResponsibility.isChecked()
            and self.chkRecovery.isChecked()
            and self.chkRestore.isChecked()
            and self.chkRead.isChecked()
    )