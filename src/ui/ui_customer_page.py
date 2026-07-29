# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'customer_page.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 382)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setFamilies([u"Perpetua"])
        font.setPointSize(16)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout.addWidget(self.label)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lblCustomerName = QLabel(Form)
        self.lblCustomerName.setObjectName(u"lblCustomerName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblCustomerName)

        self.lblCompanyName = QLabel(Form)
        self.lblCompanyName.setObjectName(u"lblCompanyName")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblCompanyName)

        self.lblEmail = QLabel(Form)
        self.lblEmail.setObjectName(u"lblEmail")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblEmail)

        self.lblPhone = QLabel(Form)
        self.lblPhone.setObjectName(u"lblPhone")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblPhone)

        self.lblDeviceName = QLabel(Form)
        self.lblDeviceName.setObjectName(u"lblDeviceName")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblDeviceName)

        self.txtCustomerName = QLineEdit(Form)
        self.txtCustomerName.setObjectName(u"txtCustomerName")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.txtCustomerName)

        self.txtCompanyName = QLineEdit(Form)
        self.txtCompanyName.setObjectName(u"txtCompanyName")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.txtCompanyName)

        self.txtEmail = QLineEdit(Form)
        self.txtEmail.setObjectName(u"txtEmail")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.txtEmail)

        self.txtPhone = QLineEdit(Form)
        self.txtPhone.setObjectName(u"txtPhone")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.txtPhone)

        self.txtDeviceName = QLineEdit(Form)
        self.txtDeviceName.setObjectName(u"txtDeviceName")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.txtDeviceName)


        self.verticalLayout.addLayout(self.formLayout)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Customer Information", None))
        self.lblCustomerName.setText(QCoreApplication.translate("Form", u"Customer Name", None))
        self.lblCompanyName.setText(QCoreApplication.translate("Form", u"Company Name", None))
        self.lblEmail.setText(QCoreApplication.translate("Form", u"Email Address", None))
        self.lblPhone.setText(QCoreApplication.translate("Form", u"Phone Number", None))
        self.lblDeviceName.setText(QCoreApplication.translate("Form", u"Device Name", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Fields marked as required must be completed before continuing. ", None))
    # retranslateUi

