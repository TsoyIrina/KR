from PyQt6.QtWidgets import QWidget

from db import take_airports
from design.profile_update import Ui_UpdateForm
from users_api import update_profile, take_profile


class UpdateProfile(QWidget, Ui_UpdateForm):
    def __init__(self, parent, user):
        super().__init__()
        self.parent = parent
        self.user = user

        self.setupUi(self)
        self.line_first_name.setText(self.user['user']['first_name'])
        self.line_last_name.setText(self.user['user']['last_name'])
        self.line_email.setText(self.user['user']['email'])


        self.list_airports_code, list = take_airports()
        self.line_airport.addItems(list)
        self.line_airport.setEditable(True)

        self.connect_ui()

    def connect_ui(self):
        self.btn_update_profile.clicked.connect(self.update_profile)

    def update_profile(self):
        c = self.list_airports_code[self.line_airport.currentIndex()]['code']
        body = {
            "user":
                {
                    "email": self.line_email.text(),
                    "first_name": self.line_first_name.text(),
                    "last_name": self.line_last_name.text()
                },
            "location": c}

        update_profile(self.user['id'], body)
        self.hide()
        self.parent.user = take_profile(self.user['user']['username'])
        self.parent.update()


