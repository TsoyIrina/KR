from PyQt6.QtWidgets import QWidget, QMessageBox

from controls.ticket_control import TicketWidget
from design.main_tick import Ui_main_tick
from users_api import create_tick, update_tick, del_tick


class TicketMainWidget(QWidget, Ui_main_tick):
    def __init__(self, widget_main_ticket: QWidget, parent, user_id, flights, count_stop, total_price, passengers, when,
                 btn_txt=None, tick_id=None):
        super().__init__()
        self.tick_id = tick_id
        self.pay_widget = ''
        self.buy_tick_slot = ''
        self.parent = parent
        self.user_id = user_id
        self.flights = flights
        self.stops = count_stop
        self.price = total_price
        self.passengers = passengers
        self.when = when
        self.btn_txt = btn_txt
        self.m_widget = widget_main_ticket
        self.setupUi(widget_main_ticket)
        self.componentUi()
        self.connectUi()

    def componentUi(self):
        self.line_stop_val.setText(str(self.stops))
        self.line_total_price.setText(str(self.price))
        self.line_ticket_who.setText(str(''.join('{}:{}, '.format(key, val) for key, val in self.passengers.items())))
        self.date_tick_when.setDate(self.when)
        self.btn_ticket_buy.setText('Выбрать')
        self.btn_del.hide()
        if self.btn_txt == True:
            self.btn_ticket_buy.hide()
        elif self.btn_txt == False:
            self.btn_del.show()
            self.btn_ticket_buy.setText('Оплатить')

    def connectUi(self):
        if self.btn_ticket_buy.text() == 'Выбрать':
            self.btn_ticket_buy.clicked.connect(lambda: self.buy_tick(self))
        else:
            self.btn_ticket_buy.clicked.connect(lambda: self.pay_tick(self))
            self.btn_del.clicked.connect(lambda: self.del_tick(self))

    @staticmethod
    def pay_tick(self):
        update_tick(self.tick_id)
        self.parent.update()

    @staticmethod
    def del_tick(self):
        del_tick(self.tick_id)
        self.parent.update()

    def print_ticket(self, res):
        ticket_widget = QWidget()
        TicketWidget(ticket_widget, res)
        self.main_tick_layout.addWidget(ticket_widget)

    @staticmethod
    def buy_tick(self):
        for i in self.flights:
            del i['id']
        date = self.when.toString('yyyy-MM-dd')
        body = {
            "profile": self.user_id,
            "flights": self.flights,
            "num_stops": self.stops,
            "ad": self.passengers['Взрослых'],
            "ch": self.passengers['Детей'],
            "inf": self.passengers['Младенцев'],
            "date": date,
            "price": self.price,
            "paid": 'false'
        }
        create_tick(body)

        self.parent.update()
