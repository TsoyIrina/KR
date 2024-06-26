# Form implementation generated from reading ui file 'design/main_tick.ui'
#
# Created by: PyQt6 UI code generator 6.6.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_main_tick(object):
    def setupUi(self, main_tick):
        main_tick.setObjectName("main_tick")
        main_tick.resize(500, 159)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(main_tick.sizePolicy().hasHeightForWidth())
        main_tick.setSizePolicy(sizePolicy)
        self.layout = QtWidgets.QVBoxLayout(main_tick)
        self.layout.setObjectName("layout")
        self.widget_main = QtWidgets.QWidget(parent=main_tick)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_main.sizePolicy().hasHeightForWidth())
        self.widget_main.setSizePolicy(sizePolicy)
        self.widget_main.setStyleSheet("QWidget#widget_main{border-radius:20px;\n"
"border: 1px solid rgb(83, 123, 255)}")
        self.widget_main.setObjectName("widget_main")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_main)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget_2 = QtWidgets.QWidget(parent=self.widget_main)
        self.widget_2.setObjectName("widget_2")
        self.formLayout = QtWidgets.QFormLayout(self.widget_2)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(parent=self.widget_2)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.line_stop_val = QtWidgets.QLineEdit(parent=self.widget_2)
        self.line_stop_val.setReadOnly(True)
        self.line_stop_val.setObjectName("line_stop_val")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_stop_val)
        self.label_3 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.label_4 = QtWidgets.QLabel(parent=self.widget_2)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.date_tick_when = QtWidgets.QDateEdit(parent=self.widget_2)
        self.date_tick_when.setReadOnly(True)
        self.date_tick_when.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.date_tick_when.setObjectName("date_tick_when")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.date_tick_when)
        self.line_ticket_who = QtWidgets.QLineEdit(parent=self.widget_2)
        self.line_ticket_who.setObjectName("line_ticket_who")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.line_ticket_who)
        self.verticalLayout_2.addWidget(self.widget_2)
        self.widget_3 = QtWidgets.QWidget(parent=self.widget_main)
        self.widget_3.setObjectName("widget_3")
        self.main_tick_layout = QtWidgets.QVBoxLayout(self.widget_3)
        self.main_tick_layout.setObjectName("main_tick_layout")
        self.verticalLayout_2.addWidget(self.widget_3)
        self.widget_4 = QtWidgets.QWidget(parent=self.widget_main)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.widget_4)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.line_total_price = QtWidgets.QLineEdit(parent=self.widget_4)
        self.line_total_price.setReadOnly(True)
        self.line_total_price.setObjectName("line_total_price")
        self.horizontalLayout_2.addWidget(self.line_total_price)
        self.btn_ticket_buy = QtWidgets.QPushButton(parent=self.widget_4)
        self.btn_ticket_buy.setStyleSheet("background-color: rgb(70, 103, 213);")
        self.btn_ticket_buy.setObjectName("btn_ticket_buy")
        self.horizontalLayout_2.addWidget(self.btn_ticket_buy)
        self.btn_del = QtWidgets.QPushButton(parent=self.widget_4)
        self.btn_del.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.btn_del.setObjectName("btn_del")
        self.horizontalLayout_2.addWidget(self.btn_del)
        self.verticalLayout_2.addWidget(self.widget_4)
        self.layout.addWidget(self.widget_main)

        self.retranslateUi(main_tick)
        QtCore.QMetaObject.connectSlotsByName(main_tick)

    def retranslateUi(self, main_tick):
        _translate = QtCore.QCoreApplication.translate
        main_tick.setWindowTitle(_translate("main_tick", "Form"))
        self.label.setText(_translate("main_tick", "Пересадок:"))
        self.label_3.setText(_translate("main_tick", "Пассажиры:"))
        self.label_4.setText(_translate("main_tick", "Дата:"))
        self.label_2.setText(_translate("main_tick", "ИТОГ:"))
        self.btn_ticket_buy.setText(_translate("main_tick", "Купить"))
        self.btn_del.setText(_translate("main_tick", "Удалить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_tick = QtWidgets.QWidget()
    ui = Ui_main_tick()
    ui.setupUi(main_tick)
    main_tick.show()
    sys.exit(app.exec())
