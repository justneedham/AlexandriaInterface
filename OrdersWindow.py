from view import *
from OrderDetailWindow import *

class OrdersListWindow(QGroupBox):
    def __init__(self, data, mainWindow):
        super().__init__()
        self.data = data
        self.mainWindow = mainWindow
        self.layout = QGridLayout()
        self.build()

    def build(self):
        self.sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setSizePolicy(self.sizePolicy)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaLayout = QGridLayout()

        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleLayout = QGridLayout()
        titleLayout.addWidget(QLabel('ID'), 0, 0)
        titleLayout.addWidget(QLabel('First Name'), 0, 1)
        titleLayout.addWidget(QLabel('Last Name'), 0, 2)
        titleLayout.addWidget(QLabel('Order Type'), 0, 3)
        titleLayout.addWidget(QLabel('Pay Method'), 0, 4)
        titleLayout.addWidget(QLabel('Amazon ID'), 0, 5)
        titleLayout.addWidget(QLabel('Date'), 0, 6)
        titleLayout.addWidget(QLabel('Status'), 0, 7)
        self.rows = 1

        titleBox.setLayout(titleLayout)
        self.scrollAreaLayout.addWidget(titleBox)

        if self.data != None:

            for row in self.data['Views']['Orders']:
                button = LinkOrderButton(str(row.orderID), self)
                subBox = QGroupBox()
                subBox.setFixedHeight(60)
                sublayout = QGridLayout()
                sublayout.addWidget(button, 0, 0)
                sublayout.addWidget(QLabel(row.firstName), 0, 1)
                sublayout.addWidget(QLabel(row.lastName), 0, 2)
                sublayout.addWidget(QLabel(row.orderType), 0, 3)
                sublayout.addWidget(QLabel(row.payMethod), 0, 4)
                if row.amazonID != None:

                    sublayout.addWidget(QLabel(str(row.amazonID)), 0, 5)
                else:
                    sublayout.addWidget(QLabel('None'), 0, 5)
                sublayout.addWidget(QLabel(str(row.date)), 0, 6)
                sublayout.addWidget(QLabel(row.status), 0, 7)
                subBox.setLayout(sublayout)
                self.rows += 1
                self.scrollAreaLayout.addWidget(subBox, self.rows, 0, 1, 0)

        self.scrollAreaLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.scrollArea.setFixedWidth(1400)
        self.scrollArea.setFixedHeight(800)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

    def show_order_detail_window(self, orderNumber):
        """Shows the specific order detail view dependent on the order status"""
        order = self.load_order(orderNumber)
        if order.orderType.name == 'Sell Order':
            if order.status.name == 'Processing':
                self.orderDetailWindow = SellOrderDetailWindowProcess(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Quoted':
                self.orderDetailWindow = SellOrderDetailWindowQuoted(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Accepted':
                self.orderDetailWindow = SellOrderDetailWindowAccepted(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'In-Transit':
                self.orderDetailWindow = SellOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'Picked Up':
                self.orderDetailWindow = SellOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            else:
                print('Sell Order Detail Status Error')

        elif order.orderType.name == 'Buy Order':
            if order.status.name == 'Processing':
                self.orderDetailWindow = BuyOrderDetailWindowProcess(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            elif order.status.name == 'In-Transit':
                self.orderDetailWindow = BuyOrderDetailWindowInTransit(order, self.mainWindow)
                self.mainWindow.show_order_detail()
            else:
                print('Buy Order Detail Status Error')
        else:
            print('Order Detail Window Error')

    def load_order(self, orderID):
        """Checks to see if order has been previously loaded and if not calls the controller to load"""
        order = None
        for x in self.data['Data']['Orders']:
            if str(x.ID) == orderID:
                order = x
            else:
                continue

        if order == None:
            order = self.mainWindow.load_order(orderID)
            self.mainWindow.data['Data']['Orders'].append(order)

        return order

    def refresh(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.build()
        self.layout.update()

