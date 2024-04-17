from PyQt6.QtWidgets import QWidget

from design.who import Ui_WhoWidget


class WidgetWho(QWidget, Ui_WhoWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connectUi()

    def connectUi(self):
        self.btn_ok.clicked.connect(self.who_ok)

    def who_ok(self):
        if self.line_ch.text() == '':
            self.line_ch.setText('0')
        if self.line_inf.text() == '':
            self.line_inf.setText('0')

        if int(self.line_ad.text()) < 1:
            self.error.setText('А кто тогда едет?')
        elif int(self.line_inf.text()) > int(self.line_ad.text()):
            self.error.setText('Младенцев не может быть больше взрослых')
        else:
            # self.parent.list_who = f'Взрослых: {self.line_ad.text()}\nДетей: {self.line_ch.text()}\nМладенцев: {self.line_inf.text()}'
            self.parent.passengers['Взрослых'] = int(self.line_ad.text())
            self.parent.passengers['Детей'] = int(self.line_ch.text())
            self.parent.passengers['Младенцев'] = int(self.line_inf.text())
            self.parent.update_who()
            self.hide()
