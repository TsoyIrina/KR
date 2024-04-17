from PyQt6.QtWidgets import QWidget

from design.autherization import Ui_widget_autherization
from users_api import take_profile, login


class AuthWidget(QWidget, Ui_widget_autherization):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.connectUi()

    def connectUi(self):
        self.btn_login.clicked.connect(self.login)

    def login(self):
        input_login = self.line_username.text()
        input_password = self.line_password.text()
        sup = login(input_login, input_password)

        if len(sup) == 3:
            self.parent.user = sup

            if self.parent.user is not None:
                self.parent.show_profile()
        else:
            self.line_error.setText(str(sup['non_field']))
