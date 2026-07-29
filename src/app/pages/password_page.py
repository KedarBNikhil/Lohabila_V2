from PySide6.QtWidgets import (
    QWizardPage,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QFormLayout,
    QMessageBox,
    QSizePolicy,
    QCheckBox
)

from PySide6.QtCore import Qt

class PasswordPage(QWizardPage):

    def __init__(self, context):
        super().__init__()

        self.context = context

        self.setTitle("Repository Security")
        self.setSubTitle(
            "Create a password to secure your backup repository."
        )

        self.build_ui()

    def build_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(40,30,40,30)

        main_layout.setSpacing(10)


        info_label = QLabel(
            "This password will be used to encrypt and protect your backup repository. "
            "Please remember it because it cannot be recovered."
        )

        info_label.setWordWrap(True)


        form_layout = QFormLayout()

        form_layout.setSpacing(15)


        self.txtPassword = QLineEdit()

        self.txtPassword.setEchoMode(
            QLineEdit.Password
        )

        self.txtPassword.setPlaceholderText(
            "Enter repository password"
        )

        self.txtPassword.setMinimumHeight(30)

        self.txtPassword.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )


        self.txtConfirmPassword = QLineEdit()

        self.txtConfirmPassword.setEchoMode(
            QLineEdit.Password
        )

        self.txtConfirmPassword.setPlaceholderText(
            "Re-enter repository password"
        )

        self.txtConfirmPassword.setMinimumHeight(30)

        self.txtConfirmPassword.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        self.password_requirements = {
    "length": QLabel("☐ Minimum 8 characters"),
    "upper": QLabel("☐ Contains uppercase letter"),
    "lower": QLabel("☐ Contains lowercase letter"),
    "number": QLabel("☐ Contains number"),
    "special": QLabel("☐ Contains special character"),
}

        self.match_label = QLabel(
    "☐ Passwords match"
)

        for label in self.password_requirements.values():
            label.setContentsMargins(0, 0, 0, 0)

        self.match_label.setContentsMargins(0, 0, 0, 0)

        form_layout.addRow(
            "Password:",
            self.txtPassword
        )

        form_layout.addRow(
            "Confirm Password:",
            self.txtConfirmPassword
        )

        self.show_password = QCheckBox(
    "Show password"
)

        self.show_password.stateChanged.connect(
            self.toggle_password_visibility 
)

        main_layout.addWidget(info_label)
        main_layout.addSpacing(10)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(
         self.show_password
)


        requirements_label = QLabel(
    "Password requirements:"
)

        main_layout.addWidget(
         requirements_label
)


        requirements_layout = QVBoxLayout()

        requirements_layout.setSpacing(0)
        requirements_layout.setContentsMargins(0, 0, 0, 0)


        for item in self.password_requirements.values():
            item.setFixedHeight(22)
            requirements_layout.addWidget(item)

        self.match_label.setFixedHeight(22)

        requirements_layout.addWidget(
            self.match_label
)


        main_layout.addLayout(
            requirements_layout
)
        


        self.setLayout(main_layout)

        self.txtPassword.textChanged.connect(
        self.check_password_requirements
)

        self.txtConfirmPassword.textChanged.connect(
        self.check_password_match
)


    def validatePage(self):

        password = self.txtPassword.text().strip()
        confirm = self.txtConfirmPassword.text().strip()


        if not password:
            QMessageBox.warning(
                self,
                "Password Required",
                "Please enter a repository password."
            )
            return False


        if len(password) < 8:
            QMessageBox.warning(
                self,
                "Weak Password",
                "Password must contain at least 8 characters."
            )
            return False


        if password != confirm:
            QMessageBox.warning(
                self,
                "Password Mismatch",
                "Passwords do not match."
            )
            return False


        self.context.repository_password = password

        return True
    
    def toggle_password_visibility(self, state):

        if state:

            self.txtPassword.setEchoMode(
            QLineEdit.Normal
        )

            self.txtConfirmPassword.setEchoMode(
            QLineEdit.Normal
        )

        else:

            self.txtPassword.setEchoMode(
            QLineEdit.Password
        )

            self.txtConfirmPassword.setEchoMode(
            QLineEdit.Password
        )



    def update_requirement(self, key, passed, text):

        if passed:
            self.password_requirements[key].setText(
            "☑ " + text
        )
        else:
            self.password_requirements[key].setText(
            "☐ " + text
        )



    def check_password_requirements(self):

        password = self.txtPassword.text()


        self.update_requirement(
        "length",
        len(password) >= 8,
        "Minimum 8 characters"
    )


        self.update_requirement(
        "upper",
        any(c.isupper() for c in password),
        "Contains uppercase letter"
    )


        self.update_requirement(
        "lower",
        any(c.islower() for c in password),
        "Contains lowercase letter"
    )


        self.update_requirement(
        "number",
        any(c.isdigit() for c in password),
        "Contains number"
    )


        self.update_requirement(
        "special",
        any(
            not c.isalnum()
            for c in password
        ),
        "Contains special character"
    )


        self.check_password_match()



    def check_password_match(self):

        password = self.txtPassword.text()
        confirm = self.txtConfirmPassword.text()


        matched = (
        password != ""
        and password == confirm
    )


        if matched:

            self.match_label.setText(
            "☑ Passwords match"
        )

        else:

            self.match_label.setText(
            "☐ Passwords match"
        )
            
