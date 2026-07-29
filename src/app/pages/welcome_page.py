from src.app.pages.base_wizard_page import BaseWizardPage

from src.ui.ui_welcome_page import Ui_welcomePage


class WelcomePage(BaseWizardPage):
    def __init__(self):
        super().__init__()

        self.ui = Ui_welcomePage()
        self.ui.setupUi(self)

        self.setTitle("Welcome")
        self.setFinalPage(False)