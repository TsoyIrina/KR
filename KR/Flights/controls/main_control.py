import datetime
import sys
from datetime import date

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QMainWindow, QDateEdit, QWidget, QPushButton, QLineEdit, QApplication
from PyQt6 import QtGui, QtCore

from controls.autherization_control import AuthWidget
from controls.main_tick_control import TicketMainWidget
from controls.update_profile_control import UpdateProfile
from controls.who_control import WidgetWho
from design.main import Ui_MainWindow
from db import *
from users_api import take_profile, take_tickets


class MainControl(Ui_MainWindow, QMainWindow):
    def __init__(self, window: QMainWindow):
        super().__init__()
        self.m_widget = window
        self.user = None
        self.profile_widget = AuthWidget(self)
        self.update_profile_widget = None
        self.dateEdit = QDateEdit(self)
        self.setupUi(window)
        self.list_airports_code = []
        self.print_profile()
        self.control_who = QWidget()
        self.passengers = {'Взрослых': 1, 'Детей': 0, 'Младенцев': 0}
        self.list_who = ''

        self.componentsUi()
        self.connectUi()

    def setupUi(self, window):
        super().setupUi(window)

    def connectUi(self):
        self.btn_clear.clicked.connect(self.clear)
        self.btn_search.clicked.connect(
            lambda: self.search_flights(self.take_code('from'), self.take_code('to'), layout=self.ticket_layout))
        self.btn_logout.clicked.connect(self.logout)
        self.btn_test.clicked.connect(self.show_who)
        self.btn_update_profile.clicked.connect(self.update_profile)

    def componentsUi(self):
        self.list_airports_code, list = take_airports()
        self.boxfrom.addItems(list)
        self.boxfrom.setEditable(True)

        self.boxto.addItems(list)
        self.boxto.setEditable(True)

        font = QtGui.QFont()
        font.setPointSize(12)
        self.dateEdit.setFont(font)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setGeometry(QtCore.QRect(220, 31, 133, 20))

        # self.boxwho.insertSeparator(1)
        # self.boxwho.insertSeparator(3)
        self.update_who()
        self.m_widget.showMaximized()

        d = QDate(date.today())
        self.datewhen.setDate(d)

    # очищение полей
    def clear(self):
        for i in reversed(range(self.ticket_layout.count())):
            self.ticket_layout.itemAt(i).widget().deleteLater()
        self.line_res.clear()

    # ввод пассажиров
    def update_who(self):
        self.boxwho.clear()
        # self.parent.list_who = f'Взрослых: {self.line_ad.text()}\nДетей: {self.line_ch.text()}\nМладенцев: {self.line_inf.text()}'
        self.list_who = ''.join('{}:{}, '.format(key, val) for key, val in self.passengers.items())
        self.boxwho.addItem(self.list_who)

    def take_code(self, ind):
        i = None
        if ind == 'from':
            i = self.boxfrom.currentIndex()
        elif ind == 'to':
            i = self.boxto.currentIndex()
        c = self.list_airports_code[i]
        code = c['code']
        return code

    # поиск билетов
    def search_flights(self, air_from, air_to, layout, stops=2):
        self.clear()
        when = self.datewhen.date()
        price_percent = self.passengers['Взрослых'] + self.passengers['Детей'] * 0.8 + self.passengers[
            'Младенцев'] * 0.2

        if air_from == air_to:
            self.line_res.setText('Зачем?')
        else:
            lf = take_flights(air_from, air_to, stops)
            for flight in lf:
                self.print_flights(lf, round(flight['total_price'] * price_percent, 2), self.passengers, when, layout)

    # печать инофрмации о билете
    def print_main_ticket(self, flights, stops_count, total_price, passengers, when, layout, btn_txt, tick_id=None):
        ticket_widget = QWidget()
        tmw = TicketMainWidget(ticket_widget, self, self.user['id'], flights, stops_count, total_price, passengers,
                               when, btn_txt=btn_txt, tick_id=tick_id)
        layout.addWidget(ticket_widget)
        ticket_widget.parent()
        return tmw

    def show_who(self):
        self.control_who = WidgetWho(parent=self)
        self.control_who.show()

    def clear_l(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    # вывод биелтов пользователя
    def print_user_ticket(self, paid, layout):
        self.clear_l(layout)
        if self.user is not None:
            ticks = take_tickets(self.user['id'])

            for tick in ticks:
                tick_list = []
                if tick['paid'] == paid:
                    tick_list.append(tick)
                    when = datetime.datetime.strptime(str(tick['date']), '%Y-%m-%d')
                    passengers = {'Взрослых': tick['ad'], 'Детей': tick['ch'], 'Младенцев': tick['inf']}
                    price_percent = passengers['Взрослых'] + passengers['Детей'] * 0.8 + passengers[
                        'Младенцев'] * 0.2
                    self.print_flights(tick_list, float(tick['price']), passengers=passengers, when=when, layout=layout,
                                       btn_txt=paid, tick_id=tick['id'])

    # вывод инфо билетов
    def print_flights(self, list_fl, total_price, passengers, when, layout, btn_txt=None, tick_id=None):
        self.line_res.setText(f'Найдено: {len(list_fl)}')
        if len(list_fl) == 0:
            return
        for i in list_fl:
            tmw = self.print_main_ticket(i['flights'], i['num_stops'], total_price, passengers, when, layout, btn_txt,
                                         tick_id=tick_id)
            for j in i['flights']:
                tmw.print_ticket(j)

    # выход из уч.записи
    def logout(self):
        self.user = None
        self.update()

    # вывод инфы пользователя
    def print_profile(self):

        if self.user is None:
            self.widget_profile.hide()
            self.widget_profile_layout.addWidget(self.profile_widget)
            self.tittle_profile.setText('Вход')
            self.profile_widget.show()
        else:
            self.tittle_profile.setText('Личные данные')
            self.profile_widget.hide()
            self.line_username.setText(self.user['user']['username'])
            self.line_first_name.setText(self.user['user']['first_name'])
            self.line_last_name.setText(self.user['user']['last_name'])
            self.line_email.setText(self.user['user']['email'])
            self.line_location.setText(self.user['location'])
            self.widget_profile.show()

    def show_profile(self):
        self.widget_profile_layout.removeWidget(self.profile_widget)
        self.update()

    #изменение данных пользователя
    def update_profile(self):
        self.update_profile_widget = UpdateProfile(parent=self, user=self.user)
        self.update_profile_widget.show()

    #Обновление приложения
    def update(self):
        self.print_profile()
        self.print_user_ticket(False, self.ticks_unpaid_layout)
        self.print_user_ticket(True, self.ticks_paid_layout)
        self.clear()


    def open_data(self):
        self.dateEdit.show()
