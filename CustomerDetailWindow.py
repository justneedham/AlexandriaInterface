from view import *

class CustomerDetailWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.window = QVBoxLayout()
        self.create_customer_overview()
        self.create_address_overview()
        self.create_referral_overview()
        self.create_order_history()

        layout = QGridLayout()
        layout.addWidget(self.customerOverview, 0, 0, 1, 0)
        layout.addWidget(self.referralOverview, 1, 0)
        layout.addWidget(self.addressOverview, 1, 1)
        layout.addWidget(self.orderOverview, 2, 0, 1, 0)

        self.setLayout(layout)

    def create_customer_overview(self):
        self.customerOverview = QGroupBox('Customer Overview')
        layout = QGridLayout()
        layout.addWidget(QLabel('First Name:'), 0, 0)
        layout.addWidget(QLabel('Last Name:'), 1, 0)
        layout.addWidget(QLabel('Phone:'), 0, 1)
        layout.addWidget(QLabel('Email:'), 1, 1)
        layout.addWidget(QLabel('Referral Code:'), 2, 0)
        layout.addWidget(QLabel('Account Created:'), 2, 1)

        self.customerOverview.setLayout(layout)

    def create_address_overview(self):
        self.addressOverview = QGroupBox('Address')
        layout = QGridLayout()
        layout.addWidget(QLabel('House/Apt:'), 0, 0)
        layout.addWidget(QLabel('Street:'), 1, 0)
        layout.addWidget(QLabel('City:'), 2, 0)
        layout.addWidget(QLabel('State:'), 3, 0)
        layout.addWidget(QLabel('Zip Code:'), 4, 0)
        layout.addWidget(QLabel('Country:'), 5, 0)

        self.addressOverview.setLayout(layout)

    def create_referral_overview(self):
        self.referralOverview = QGroupBox('Referrals')
        layout = QGridLayout()

        self.referralOverview.setLayout(layout)

    def create_order_history(self):
        self.orderOverview = QGroupBox('Orders')
        layout = QGridLayout()

        self.orderOverview.setLayout(layout)