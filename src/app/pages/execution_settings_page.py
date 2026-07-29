from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QVBoxLayout,
    QFormLayout,
    QCheckBox,
    QSpinBox,
    QHBoxLayout,
    QScrollArea,
    QWidget,
    QRadioButton
)

from PySide6.QtCore import Qt 


class ExecutionSettingsPage(QWizardPage):

    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("Backup Execution Settings")

        self.setSubTitle(
            "Configure how your backup jobs should behave."
        )

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
        40, 30, 40, 30
    )

        main_layout.setSpacing(20)

        info_label = QLabel(
    "These settings determine how BackupAgent "
    "handles backup execution."
)

        info_label.setWordWrap(True)

        main_layout.addWidget(info_label)

        self.chkRunMissed = QCheckBox(
    "Run missed backup after next startup"
)

        self.chkRunMissed.setChecked(True)


        self.chkRetry = QCheckBox(
    "Retry failed backups automatically"
)

        self.chkRetry.setChecked(True)

        main_layout.addWidget(
        self.chkRunMissed
)

        main_layout.addWidget(
        self.chkRetry
)


        self.chkWakeComputer = QCheckBox(
    "Wake computer for scheduled backups"
)

        self.chkWakeComputer.setChecked(False)


        self.chkSkipMetered = QCheckBox(
    "Skip backup on metered connections"
)

        self.chkSkipMetered.setChecked(True)

        form_layout = QFormLayout()

        form_layout.setSpacing(15)

        self.spinRetryAttempts = QSpinBox()

        self.spinRetryAttempts.setRange(1, 10)

        self.spinRetryAttempts.setValue(3)

        retry_layout = QHBoxLayout()

        self.spinRetryInterval = QSpinBox()

        self.spinRetryInterval.setRange(1, 60)

        self.spinRetryInterval.setValue(5)

        retry_layout.addWidget(
            self.spinRetryInterval
)

        retry_layout.addWidget(
            QLabel("minutes")
)

        retry_layout.addStretch()

        form_layout.addRow(
    "Maximum Retry Attempts:",
        self.spinRetryAttempts
)

        form_layout.addRow(
    "Retry Interval:",
        retry_layout
)
        
        main_layout.addLayout(form_layout)

        main_layout.addWidget(
        self.chkWakeComputer
)

        main_layout.addWidget(
        self.chkSkipMetered
)
        
        self.chkRetry.stateChanged.connect(
            self.update_retry_controls
)
        
        self.update_retry_controls()

        separator = QLabel("Additional Execution Settings")
        separator.setStyleSheet("font-weight: bold;")

        main_layout.addSpacing(15)
        main_layout.addWidget(separator)

        self.chkPreventOverlap = QCheckBox(
    "Prevent overlapping backup jobs"
)
        self.chkPreventOverlap.setChecked(True)

        main_layout.addWidget(self.chkPreventOverlap)

        run_as_label = QLabel("Run backup as:")
        main_layout.addWidget(run_as_label)

        self.radioLoggedOn = QRadioButton(
    "Only when the current user is logged on"
)

        self.radioRunAlways = QRadioButton(
    "Whether user is logged on or not"
)

        self.radioLoggedOn.setChecked(True)

        main_layout.addWidget(self.radioLoggedOn)
        main_layout.addWidget(self.radioRunAlways)

        self.update_retry_controls()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container.setLayout(main_layout)

        scroll.setWidget(container)

        page_layout = QVBoxLayout()
        page_layout.addWidget(scroll)

        self.setLayout(page_layout)

    def update_retry_controls(self):

        enabled = self.chkRetry.isChecked()

        self.spinRetryAttempts.setEnabled(
        enabled
    )

        self.spinRetryInterval.setEnabled(
        enabled
    )
        
    def validatePage(self):

        self.context.run_missed_backup = (
            self.chkRunMissed.isChecked()
    )

        self.context.retry_failed_backup = (
            self.chkRetry.isChecked()
    )

        self.context.retry_attempts = (
            self.spinRetryAttempts.value()
    )

        self.context.retry_interval = (
            self.spinRetryInterval.value()
    )

        self.context.wake_computer = (
            self.chkWakeComputer.isChecked()
    )

        self.context.skip_metered_connection = (
            self.chkSkipMetered.isChecked()
    )
        
        self.context.prevent_overlapping_backups = (
            self.chkPreventOverlap.isChecked()
)

        self.context.run_only_when_user_logged_on = (
            self.radioLoggedOn.isChecked()
)

        return True
    
    def initializePage(self):

        self.chkRunMissed.setChecked(
            self.context.run_missed_backup
    )

        self.chkRetry.setChecked(
            self.context.retry_failed_backup
    )

        self.spinRetryAttempts.setValue(
            self.context.retry_attempts
    )

        self.spinRetryInterval.setValue(
            self.context.retry_interval
    )

        self.chkWakeComputer.setChecked(
            self.context.wake_computer
    )

        self.chkSkipMetered.setChecked(
            self.context.skip_metered_connection
    )

        self.update_retry_controls()

        self.chkPreventOverlap.setChecked(
            self.context.prevent_overlapping_backups
)

        self.radioLoggedOn.setChecked(
            self.context.run_only_when_user_logged_on
)

        self.radioRunAlways.setChecked(
            not self.context.run_only_when_user_logged_on
)