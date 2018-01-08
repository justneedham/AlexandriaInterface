from view import *
from ShippingWindow import ShippingWindow
from QuoteWindow import QuoteWindow
from decimal import Decimal

class OrderDetailWindow(QWidget):
    def __init__(self, order, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.order = order
        self.resize(self.sizeHint())
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.build_order_detail_window()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.orderOverview, 0, 0, 1, 3)
        self.mainLayout.addWidget(self.amazonOverview, 0, 3, 1, 1)
        self.mainLayout.addWidget(self.shippingDetail, 1, 0, 1, 3)
        self.mainLayout.addWidget(self.orderBasket, 2, 0, 1, 3)
        self.mainLayout.addWidget(self.paymentDetail, 1, 3, 1, 1)
        self.mainLayout.addWidget(self.orderActions, 2, 3, 1, 1)
        #Row, Column, ColumenStretch, RowStretch
        self.setLayout(self.mainLayout)
        self.setStyleSheet("""
        QGroupBox
        {
            background-color: #76797C;
        }
        QLabel
        {
            background-color: #76797C;
        }
        """)

    def build_order_detail_window(self):
        self.build_order_overview()
        self.build_order_basket()
        self.create_payment_detail()
        self.build_shipping_detail()
        self.create_order_actions()
        self.build_amazon_overview()

    def add_shipping_screen(self):
        self.screen = ShippingWindow()
        self.screen.show()

    def build_amazon_overview(self):
        self.amazonOverview = QGroupBox()

        header = LabelHeader('Amazon Overview')
        keyLabel = LabelSubHeader('Amazon Key')
        shipByLabel = LabelSubHeader('Ship By')
        deliverByLabel = LabelSubHeader('Deliver By')

        amazonOverviewLayout = QGridLayout()
        amazonOverviewLayout.addWidget(header.widget, 0 ,0)
        amazonOverviewLayout.addWidget(keyLabel.widget, 1, 0)
        amazonOverviewLayout.addWidget(shipByLabel.widget, 2, 0)
        amazonOverviewLayout.addWidget(deliverByLabel.widget, 3, 0)
        amazonOverviewLayout.setAlignment(Qt.AlignTop)
        self.amazonOverview.setLayout(amazonOverviewLayout)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.addQuoteBtn = Button('Add Quote', self.show_quote_window)
        self.acceptBtn = Button('Accept', self.accept_order)
        self.addToInventoryBtn = Button('Add To Inventory', self.add_to_inventory)
        self.removeFromInventoryBtn = Button('Remove From Inventory', self.remove_from_inventory)
        self.getCurrentPricesBtn = Button('Get Current Prices', self.get_current_prices)
        self.cancelBtn = QPushButton('Cancel')

        header = LabelHeader('Actions')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(self.cancelBtn, 7, 0)

        self.orderActions.setLayout(layout)

    def build_order_overview(self):
        self.orderOverview = QGroupBox()
        self.orderOverview.setMaximumHeight(300)
        self.orderOverview.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        orderNumberTitleLbl = LabelSubHeader('Order Number')
        firstNameTitleLbl = LabelSubHeader('First Name')
        lastNameTitleLbl = LabelSubHeader('Last Name')
        typeTitleLbl = LabelSubHeader('Type')
        transactionTitleLbl = LabelSubHeader('Transaction')
        amazonTitleLbl = LabelSubHeader('Amazon')
        dateTitleLbl = LabelSubHeader('Date')
        statusTitleLbl = LabelSubHeader('Status')

        self.orderNumberLbl = Label(str(self.order.ID))
        self.firstNameLbl = Label(self.order.customer.firstName)
        self.lastNameLbl = Label(self.order.customer.lastName)
        self.orderTypeLbl = Label(self.order.orderType.name)
        self.transactionLbl = Label(self.order.transaction.name)

        if self.order.amazonOrder != None:
            self.amazonOrderLbl = Label(str(self.order.amazonOrder.ID))
        else:
            self.amazonOrderLbl = Label('None')
        self.dateLbl = Label(str(self.order.date))
        self.statusLbl = Label(self.order.status.name)

        header = LabelHeader('Overview')
        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(orderNumberTitleLbl.widget, 1, 0)
        layout.addWidget(self.orderNumberLbl.widget, 1, 1)
        layout.addWidget(firstNameTitleLbl.widget, 2, 0)
        layout.addWidget(self.firstNameLbl.widget, 2, 1)
        layout.addWidget(lastNameTitleLbl.widget, 3, 0)
        layout.addWidget(self.lastNameLbl.widget, 3, 1)
        layout.addWidget(typeTitleLbl.widget, 4, 0)
        layout.addWidget(self.orderTypeLbl.widget, 4, 1)
        layout.addWidget(transactionTitleLbl.widget, 1, 2)
        layout.addWidget(self.transactionLbl.widget, 1, 3)
        layout.addWidget(amazonTitleLbl.widget, 2, 2)
        layout.addWidget(self.amazonOrderLbl.widget, 2, 3)
        layout.addWidget(dateTitleLbl.widget, 3, 2)
        layout.addWidget(self.dateLbl.widget, 3, 3)
        layout.addWidget(statusTitleLbl.widget, 4, 2)
        layout.addWidget(self.statusLbl.widget, 4, 3)
        layout.setAlignment(Qt.AlignTop)

        self.orderOverview.setLayout(layout)

    def build_order_basket(self):

        self.orderBasketScroll = QScrollArea(self)
        self.orderBasketScroll.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.orderBasketScroll.setWidgetResizable(True)
        self.orderBasketScrollContents = QGroupBox()
        self.orderBasketScrollLayout = QGridLayout()

        itemLabel = LabelSubHeader('Item')
        titleLabel = LabelSubHeader('Title')
        authorLabel = LabelSubHeader('Author')
        editionLabel = LabelSubHeader('Edition')
        isbnLabel = LabelSubHeader('ISBN')
        conditionLabel = LabelSubHeader('Condition')
        priceLabel = LabelSubHeader('Price')

        titleBox = QGroupBox()
        titleBox.setFixedHeight(40)
        titleBoxLayout = QGridLayout()

        titleBoxLayout.setColumnStretch(0, 1)
        titleBoxLayout.setColumnStretch(1, 4)
        titleBoxLayout.setColumnStretch(2, 4)
        titleBoxLayout.setColumnStretch(3, 2)
        titleBoxLayout.setColumnStretch(4, 4)
        titleBoxLayout.setColumnStretch(5, 2)
        titleBoxLayout.setColumnStretch(6, 1)

        titleBoxLayout.addWidget(itemLabel.widget, 0, 0)
        titleBoxLayout.addWidget(titleLabel.widget, 0, 1)
        titleBoxLayout.addWidget(authorLabel.widget, 0, 2)
        titleBoxLayout.addWidget(editionLabel.widget, 0, 3)
        titleBoxLayout.addWidget(isbnLabel.widget, 0, 4)
        titleBoxLayout.addWidget(conditionLabel.widget, 0, 5)
        titleBoxLayout.addWidget(priceLabel.widget, 0, 6)
        titleBox.setLayout(titleBoxLayout)
        self.orderBasketScrollLayout.addWidget(titleBox)

        for book in self.order.books:
            itemBox = QGroupBox()
            itemBox.setFixedHeight(60)
            itemBoxLayout = QGridLayout()

            itemBoxLayout.setColumnStretch(0, 1)
            itemBoxLayout.setColumnStretch(1, 4)
            itemBoxLayout.setColumnStretch(2, 4)
            itemBoxLayout.setColumnStretch(3, 2)
            itemBoxLayout.setColumnStretch(4, 4)
            itemBoxLayout.setColumnStretch(5, 2)
            itemBoxLayout.setColumnStretch(6, 1)

            itemBoxLayout.addWidget(QLabel(str(book.itemNumber)), 0, 0)
            itemBoxLayout.addWidget(QLabel(book.title), 0, 1)
            itemBoxLayout.addWidget(QLabel(book.author), 0, 2)
            itemBoxLayout.addWidget(QLabel(str(book.edition)), 0, 3)
            itemBoxLayout.addWidget(QLabel(book.ISBN), 0, 4)
            itemBoxLayout.addWidget(QLabel(book.condition), 0, 5)
            itemBoxLayout.addWidget(QLabel(str(book.price)), 0, 6)
            itemBox.setLayout(itemBoxLayout)
            self.orderBasketScrollLayout.addWidget(itemBox)

        self.orderBasketScrollLayout.setAlignment(Qt.AlignTop)
        self.orderBasketScrollContents.setLayout(self.orderBasketScrollLayout)
        self.orderBasketScroll.setWidget(self.orderBasketScrollContents)

        header = LabelHeader('Order Basket')

        self.orderBasket = QGroupBox()
        self.orderBasket.setMaximumHeight(300)
        self.orderBasketLayout = QGridLayout()
        self.orderBasketLayout.addWidget(header.widget, 0, 0)
        self.orderBasketLayout.addWidget(self.orderBasketScroll, 1, 0)
        self.orderBasket.setLayout(self.orderBasketLayout)

    def create_payment_detail(self):
        self.paymentDetail = QGroupBox()
        self.paymentDetail.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)

        header = LabelHeader('Price Detail')
        paymentLabel = LabelSubHeader('Payment Type')
        subTotalLabel = LabelSubHeader('Sub Total')
        discountLabel = LabelSubHeader('Discount')
        taxLabel = LabelSubHeader('Tax')
        totalLabel = LabelSubHeader('Total')
        marginLabel = LabelSubHeader('Estimated Profit')

        self.subTotal = round(self.calculate_sub_total(), 2)
        self.discount = 0
        self.tax = round((self.subTotal * 0.0685), 2)

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(paymentLabel.widget, 1, 0)
        layout.addWidget(QLabel(self.order.transaction.name), 1, 1)
        layout.addWidget(subTotalLabel.widget, 2, 0)
        layout.addWidget(QLabel('$ '+str(self.subTotal)), 2, 1)
        layout.addWidget(discountLabel.widget, 3, 0)
        layout.addWidget(QLabel('$ '+str(self.discount)), 3, 1)
        layout.addWidget(taxLabel.widget, 4, 0)
        layout.addWidget(QLabel('$ '+str(self.tax)), 4, 1)
        layout.addWidget(totalLabel.widget, 5, 0)
        layout.addWidget(QLabel('$ '+str(self.subTotal+self.tax)), 5, 1)
        layout.addWidget(marginLabel.widget, 6, 0)
        layout.setAlignment(Qt.AlignTop)
        self.calculate_sub_total()

        self.paymentDetail.setLayout(layout)

    def calculate_sub_total(self):

        subTotal = 0.00
        for orderItem in self.order.books:
            subTotal += round(orderItem.price,2)
        return subTotal

    def build_shipping_detail(self):

        # Width, Height
        self.shippingDetailScroll = QScrollArea(self)
        self.shippingDetailScroll.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.shippingDetailScroll.setWidgetResizable(True)
        self.shippingDetailScrollContents = QGroupBox()
        self.shippingDetailScrollLayout = QGridLayout()

        idLabel = LabelSubHeader('ID')
        costLabel = LabelSubHeader('Cost')
        trackingLabel = LabelSubHeader('Tracking')
        shippedLabel = LabelSubHeader('Shipped')
        expectedLabel = LabelSubHeader('Expected')
        shippingTypeLabel = LabelSubHeader('Type')
        statusLabel = LabelSubHeader('Status')


        titleBox = QGroupBox()
        titleBox.setFixedHeight(40)
        titleBoxLayout = QGridLayout()

        titleBoxLayout.setColumnStretch(0, 1)
        titleBoxLayout.setColumnStretch(1, 1)
        titleBoxLayout.setColumnStretch(2, 4)
        titleBoxLayout.setColumnStretch(3, 2)
        titleBoxLayout.setColumnStretch(4, 2)
        titleBoxLayout.setColumnStretch(5, 2)
        titleBoxLayout.setColumnStretch(6, 2)

        titleBoxLayout.addWidget(idLabel.widget, 0, 0)
        titleBoxLayout.addWidget(costLabel.widget, 0, 1)
        titleBoxLayout.addWidget(trackingLabel.widget, 0, 2)
        titleBoxLayout.addWidget(shippedLabel.widget, 0, 3)
        titleBoxLayout.addWidget(expectedLabel.widget, 0, 4)
        titleBoxLayout.addWidget(shippingTypeLabel.widget, 0, 5)
        titleBoxLayout.addWidget(statusLabel.widget, 0, 6)
        titleBox.setLayout(titleBoxLayout)

        self.shippingDetailScrollLayout.addWidget(titleBox)

        if self.order.shipping != None:

            for shipping in self.order.shipping:
                itemBox = QGroupBox()
                itemBox.setFixedHeight(60)
                itemBoxLayout = QGridLayout()

                itemBoxLayout.setColumnStretch(0, 1)
                itemBoxLayout.setColumnStretch(1, 1)
                itemBoxLayout.setColumnStretch(2, 4)
                itemBoxLayout.setColumnStretch(3, 2)
                itemBoxLayout.setColumnStretch(4, 2)
                itemBoxLayout.setColumnStretch(5, 2)
                itemBoxLayout.setColumnStretch(6, 2)

                itemBoxLayout.addWidget(QLabel(str(shipping.ID)), 0, 0)
                itemBoxLayout.addWidget(QLabel(str(shipping.shippingCost)), 0, 1)
                itemBoxLayout.addWidget(QLabel(shipping.tracking), 0, 2)
                itemBoxLayout.addWidget(QLabel(str(shipping.shipDate)), 0, 3)
                itemBoxLayout.addWidget(QLabel(str(shipping.expectedArrival)), 0, 4)
                itemBoxLayout.addWidget(QLabel(shipping.shipType.name), 0, 5)
                itemBoxLayout.addWidget(QLabel(shipping.status.name), 0, 6)
                itemBox.setLayout(itemBoxLayout)
                self.shippingDetailScrollLayout.addWidget(itemBox)

        self.shippingDetailScrollLayout.setAlignment(Qt.AlignTop)
        self.shippingDetailScrollContents.setLayout(self.shippingDetailScrollLayout)
        self.shippingDetailScroll.setWidget(self.shippingDetailScrollContents)

        header = LabelHeader('Shipping Detail')

        self.shippingDetail = QGroupBox()
        self.shippingDetail.setMaximumHeight(300)
        self.shippingDetailLayout = QGridLayout()
        self.shippingDetailLayout.addWidget(header.widget, 0, 0)
        self.shippingDetailLayout.addWidget(self.shippingDetailScroll, 1, 0)
        self.shippingDetailLayout.setAlignment(Qt.AlignTop)
        self.shippingDetail.setLayout(self.shippingDetailLayout)

    def accept_order(self):
        """Calls the main window to accept the order"""
        self.mainWindow.update_order_status(self.order.ID, 'Accepted')

    def show_quote_window(self):
        """Builds a QuoteWindow and displays"""
        self.quoteWindow = QuoteWindow(self.order.books, self)
        self.quoteWindow.show()

    def add_quote(self, orderItem):
        """Calls the main window to add quotes to the items in the order"""
        self.mainWindow.add_quote(orderItem)
        self.mainWindow.update_order_status(self.order.ID, 'Quoted')

    def show_shipping_window(self):
        """Builds a ShippingWindow and displays"""
        self.shippingWindow = ShippingWindow(self)
        self.shippingWindow.show()

    def add_to_inventory(self):
        """Completes order and moves book into inventory"""
        self.mainWindow.update_order_status(self.order.ID, 'Complete')
        for orderItem in self.order.books:
            self.mainWindow.add_book_to_inventory(orderItem)

    def remove_from_inventory(self):
        """Completes a selling order and removes book from inventory"""
        for orderItem in self.order.books:
            self.mainWindow.remove_book_from_inventory(orderItem)

    def get_current_prices(self):
        """Calls the main window for all buy order items"""
        for orderItem in self.order.books:
            orderItem.price = self.mainWindow.get_current_price(orderItem)

    def complete_order(self):
        """Calls the main window to update the status to complete"""
        self.mainWindow.update_order_status(self.order.ID, 'Complete')
        self.move_to_history()

    def move_to_history(self):
        """Calls the main window to archive the order"""
        self.mainWindow.move_to_history(self.order)

    def order_picked_up(self):
        """Calls the main window to update the status to picked up"""
        self.mainWindow.update_order_status(self.order.ID, 'Picked Up')

class BuyOrderDetailWindowProcess(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the buttons for the first step of a buy order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):

        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.addShippingBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)

class BuyOrderDetailWindowInTransit(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the buttons for the second step of a buy order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.completeBtn = Button('Order Complete', self.complete_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.completeBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowProcess(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the first step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.addQuoteBtn = Button('Add Quote', self.show_quote_window)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.addQuoteBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowQuoted(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the second step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.acceptedBtn = Button('Customer Accepted', self.accept_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.acceptedBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowAccepted(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the third step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.addShippingBtn = Button('Add Shipping', self.show_shipping_window)
        self.addLocalBtn = Button('Local Pick Up', self.order_picked_up)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.addShippingBtn.widget, 1, 0)
        layout.addWidget(self.addLocalBtn.widget, 2, 0)
        layout.addWidget(self.cancelBtn, 3, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)

class SellOrderDetailWindowInTransit(OrderDetailWindow):
    def __init__(self, order, mainWindow):
        """Shows the button for the fourth step of a sell order"""
        super().__init__(order, mainWindow)

    def create_order_actions(self):
        self.orderActions = QGroupBox()
        self.header = LabelHeader('Actions')
        self.completeBtn = Button('Order Complete', self.complete_order)
        self.cancelBtn = QPushButton('Cancel')

        layout = QGridLayout()
        layout.addWidget(self.header.widget, 0, 0)
        layout.addWidget(self.completeBtn.widget, 1, 0)
        layout.addWidget(self.cancelBtn, 2, 0)
        layout.setAlignment(Qt.AlignTop)

        self.orderActions.setLayout(layout)