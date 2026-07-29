from PySide6.QtWidgets import QWizardPage


class BaseWizardPage(QWizardPage):
    """
    Base class for every installer page.

    All common functionality shared by wizard pages
    will be implemented here.
    """

    def __init__(self):
        super().__init__()

    def initializePage(self):
        """
        Called whenever the page becomes visible.
        """
        super().initializePage()

    def validatePage(self):
        """
        Called when the user clicks Next.

        Return True to continue.
        Return False to remain on the page.
        """
        return True