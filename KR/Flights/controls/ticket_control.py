from PyQt6.QtWidgets import QWidget

from design.ticket import Ui_ticket


class TicketWidget(QWidget, Ui_ticket):
    def __init__(self, widget_ticket: QWidget, ticket_list):
        super().__init__()
        self.tick_li = ticket_list
        self.m_widget = widget_ticket
        self.setupUi(widget_ticket)
        self.componentsUi()


    def componentsUi(self):
        self.line_ticket_from.setText(str(self.tick_li['from_airport']['code'] +'  '+ self.tick_li['from_airport']['name'] ))
        self.line_ticket_to.setText(str(self.tick_li['to_airport']['code'] +'  '+ self.tick_li['to_airport']['name']))
        self.line_ticket_airline.setText(str(self.tick_li['airline']['name']))
        self.line_ticket_price.setText(str(self.tick_li['price']))

