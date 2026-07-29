# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'welcome_page.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_welcomePage(object):
    def setupUi(self, welcomePage):
        if not welcomePage.objectName():
            welcomePage.setObjectName(u"welcomePage")
        welcomePage.resize(800, 500)
        welcomePage.setMinimumSize(QSize(800, 500))
        self.widget = QWidget(welcomePage)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(150, 70, 406, 121))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.lblTitle = QLabel(self.widget)
        self.lblTitle.setObjectName(u"lblTitle")
        font = QFont()
        font.setFamilies([u"Perpetua"])
        font.setPointSize(20)
        font.setBold(True)
        self.lblTitle.setFont(font)

        self.verticalLayout.addWidget(self.lblTitle)

        self.lblHeading = QLabel(self.widget)
        self.lblHeading.setObjectName(u"lblHeading")
        font1 = QFont()
        font1.setFamilies([u"Perpetua"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.lblHeading.setFont(font1)

        self.verticalLayout.addWidget(self.lblHeading)

        self.lblDescription = QLabel(self.widget)
        self.lblDescription.setObjectName(u"lblDescription")
        font2 = QFont()
        font2.setFamilies([u"Perpetua"])
        font2.setPointSize(12)
        self.lblDescription.setFont(font2)
        self.lblDescription.setWordWrap(True)

        self.verticalLayout.addWidget(self.lblDescription)


        self.retranslateUi(welcomePage)

        QMetaObject.connectSlotsByName(welcomePage)
    # setupUi

    def retranslateUi(self, welcomePage):
        welcomePage.setWindowTitle(QCoreApplication.translate("welcomePage", u"Form", None))
        self.lblTitle.setText(QCoreApplication.translate("welcomePage", u"Lohabila Backup Agent", None))
        self.lblHeading.setText(QCoreApplication.translate("welcomePage", u"Welcome to the Setup Wizard", None))
        self.lblDescription.setText(QCoreApplication.translate("welcomePage", u"This wizard will guide you through the installation of Lohabila Backup Agent.\n"
"\n"
"Click Next to continue.", None))
    # retranslateUi

