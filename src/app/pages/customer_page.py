import socket
from PySide6.QtWidgets import QMessageBox

from src.app.pages.base_wizard_page import BaseWizardPage
from src.ui.ui_customer_page import Ui_Form


class CustomerPage(BaseWizardPage):
    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.txtDeviceName.setText(socket.gethostname())

        self.setTitle("Customer Information")

    def validatePage(self):
        customer_name = self.ui.txtCustomerName.text().strip()
        email = self.ui.txtEmail.text().strip()
        phone = self.ui.txtPhone.text().strip()
        device = self.ui.txtDeviceName.text().strip()

        if customer_name == "":
            QMessageBox.warning(
                self,
                "Validation Error",
                "Customer Name is required."
            )
            return False

        if email == "":
            QMessageBox.warning(
                self,
                "Validation Error",
                "Email Address is required."
            )
            return False

        if phone == "":
            QMessageBox.warning(
                self,
                "Validation Error",
                "Phone Number is required."
            )
            return False

        if device == "":
            QMessageBox.warning(
                self,
                "Validation Error",
                "Device Name is required."
            )
            return False
        wizard = self.wizard()
        context = wizard.context

        context.customer_name = customer_name
        context.company_name = self.ui.txtCompanyName.text().strip()
        context.email = email
        context.phone = phone
        context.device_name = device

        return True