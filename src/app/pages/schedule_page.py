from PySide6.QtCore import Qt, QTime
from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QTimeEdit,
    QSpinBox,
)

class SchedulePage(QWizardPage):

    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("Backup Scheduling")
        self.setSubTitle(
            "Choose when automatic backups should run."
        )

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        self.setLayout(layout)


        lblFrequency = QLabel("Backup Frequency")

        self.cmbFrequency = QComboBox()
        self.cmbFrequency.addItems([
    "Daily",
    "Weekly",
    "Monthly"
])

        layout.addWidget(lblFrequency)
        layout.addWidget(self.cmbFrequency)

        lblTime = QLabel("Backup Time")

        self.timeBackup = QTimeEdit()

        self.timeBackup.setDisplayFormat("HH:mm")

        self.timeBackup.setTime(QTime(23, 0))

        layout.addWidget(lblTime)
        layout.addWidget(self.timeBackup)

        self.lblWeekday = QLabel("Day of Week")

        self.cmbWeekday = QComboBox()
        self.cmbWeekday.addItems([
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
])

        layout.addWidget(self.lblWeekday)
        layout.addWidget(self.cmbWeekday)

        self.lblMonthday = QLabel("Day of Month")

        self.spinMonthday = QSpinBox()

        self.spinMonthday.setRange(1, 31)
        self.spinMonthday.setValue(1)

        layout.addWidget(self.lblMonthday)
        layout.addWidget(self.spinMonthday)

        self.lblWeekday.hide()
        self.cmbWeekday.hide()

        self.lblMonthday.hide()
        self.spinMonthday.hide()

        layout.addStretch()
        self.setLayout(layout)

        self.lblWeekday.hide()
        self.cmbWeekday.hide()

        self.lblMonthday.hide()
        self.spinMonthday.hide()

        self.cmbFrequency.currentTextChanged.connect(
            self.update_visibility
)
        self.update_visibility()

    def update_visibility(self):
        frequency = self.cmbFrequency.currentText()

    # Weekly
        show_weekly = frequency == "Weekly"

        self.lblWeekday.setVisible(show_weekly)
        self.cmbWeekday.setVisible(show_weekly)

    # Monthly
        show_monthly = frequency == "Monthly"

        self.lblMonthday.setVisible(show_monthly)
        self.spinMonthday.setVisible(show_monthly)

    def validatePage(self):
        print("Schedule validatePage called")

        self.context.frequency = self.cmbFrequency.currentText()

        self.context.start_time = (
            self.timeBackup.time().toString("HH:mm")
    )

        if self.context.frequency == "Weekly":
            self.context.day_of_week = (
                self.cmbWeekday.currentText()
        )
            self.context.day_of_month = 1

        elif self.context.frequency == "Monthly":
            self.context.day_of_month = (
                self.spinMonthday.value()
        )
            self.context.day_of_week = ""

        else:
            self.context.day_of_week = ""
            self.context.day_of_month = ""

        return True
