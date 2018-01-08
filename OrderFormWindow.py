import re
from view import *
from ConfirmationWindow import ConfirmationWindow

class OrderFormWindow(QWidget):
    def __init__(self, mainWindow):
        """Initializes an AddOrderWindow"""
        super().__init__()
        self.mainWindow = mainWindow
        self.row = 3
        self.bookEntries = []
        self.build_order_form()

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.orderForm, 0, 0, Qt.AlignCenter)
        self.mainLayout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.mainLayout)
        self.setStyleSheet("""
                QWidget
                {
                    background-color: #76797C;
                }
                QLabel
                {
                    background-color: #76797C;
                }
                QPushButton
                {
                    color: #eff0f1;
                    background-color: #31363b;
                    border-width: 1px;
                    border-color: #76797C;
                    border-style: solid;
                    padding: 5px;
                    min-width: 50px;
                    border-radius: 2px;
                    outline: none;
                    font-family: Avenir Next;
                    font-style: regular;
                }
                QPushButton:pressed
                {
                    background-color: #9013FE;
                    border-color: #9013FE;
                    padding-top: -15px;
                    padding-bottom: -17px;
                }
                QLineEdit
                {
                    background-color: #232629;
                    selection-background-color: #9013FE;
                    padding: 5px;
                    border-style: solid;
                    border: 1px solid #76797C;
                    border-radius: 2px;
                    color: #eff0f1;
                }
                QLineEdit:focus
                {
                    border-color: #9013FE;
                }
                """)

    def build_order_form(self):
        """Builds the add order window"""
        self.contactInfo = ContactWidget()
        self.orderInfo = OrderInfoWidget()
        self.amazonInfo = AmazonWidget()
        self.header = HeaderWidget()
        self.bookScroll = BooksWidget(self)

        self.orderForm = QGroupBox()
        self.orderFormLayout = QGridLayout()
        self.orderFormLayout.setColumnStretch(0, 1)
        self.orderFormLayout.setColumnStretch(1, 1)

        self.addBookBtn = Button('Add Book', self.add_book)
        self.removeBookBtn = Button('Remove Book', self.remove_book)
        self.submitBtn = Button('Submit', self.submit)

        #row, column
        self.orderFormLayout.addWidget(self.header.widget, 0, 0, 1, 0)
        self.orderFormLayout.addWidget(self.contactInfo.widget, 1, 0)
        self.orderFormLayout.addWidget(self.orderInfo.widget, 1, 1)
        self.orderFormLayout.addWidget(self.amazonInfo.widget, 2, 0)
        self.orderFormLayout.addWidget(self.bookScroll.widget, 3, 0, 1, 0)
        self.orderFormLayout.addWidget(self.addBookBtn.widget, 4, 0)
        self.orderFormLayout.addWidget(self.removeBookBtn.widget, 4, 1)
        self.orderFormLayout.addWidget(self.submitBtn.widget, 5, 0, 1, 0)
        self.orderFormLayout.setAlignment(Qt.AlignTop)

        self.orderForm.setLayout(self.orderFormLayout)

    def submitTest(self):
        """Passes the outArgs to the controller to be submitted to the database"""
        self.mainWindow.add_order_to_database(self.order)
        self.confirmationWindow.close_window()

    def add_book(self):
        """Creates a BookEntry instance and adds it to the layout"""
        self.bookScroll.add_book()

    def remove_book(self):
        """Removes a BookEntry instance and updates the layout"""
        self.bookScroll.remove_book()

    def submit(self):
        """Validates all input, packages and passes it to the confirmation"""
        self.capture()
        order = self.structure_order_object()
        self.confirmationWindow = ConfirmationWindow(order, self)
        self.confirmationWindow.show()

    def capture(self):
        """Captures all info on screen"""
        self.contactInfo.capture()
        self.orderInfo.capture()
        self.amazonInfo.capture()
        self.bookScroll.capture()

    def confirm(self):
        """Call the controller to add the order to the database"""

    def close(self):
        self.confirmationWindow.close()

    def structure_order_object(self):
        """Packages info into an order object and returns it"""

        customerArgs = {
            'Customer ID': None,
            'First Name': self.contactInfo.firstName,
            'Last Name': self.contactInfo.lastName,
            'Phone Number': self.contactInfo.phone,
            'Email': self.contactInfo.email,
            'Address': None,
            'Date Joined': None,
            'Referral Code': None,
            'Connection': None
        }

        orderTypeArgs = {
            'Order Type ID': None,
            'Order Type Name': self.orderInfo.orderType
        }

        transactionTypeArgs = {
            'Transaction Type ID': None,
            'Transaction Type Name': self.orderInfo.payMethod
        }

        amazonArgs = {
            'Connection': None,
            'Amazon ID': None,
            'Ship By': self.amazonInfo.amazonShipBy,
            'Deliver By': self.amazonInfo.amazonDeliverBy,
            'Amazon Key': self.amazonInfo.amazonKey
        }

        statusTypeArgs = {
            'Status ID': None,
            'Status Name': 'Processing'
        }

        orderArgs = {
            'Connection': None,
            'Order ID': None,
            'Customer': Customer(customerArgs),
            'Order Type': OrderType(orderTypeArgs),
            'Transaction': TransactionType(transactionTypeArgs),
            'Amazon Order': Amazon_Order(amazonArgs),
            'Order Date': None,
            'Status': Status(statusTypeArgs),
            'Promotion Code': self.orderInfo.referral,
            'Shipping': None,
            'Books': self.bookScroll.orderItems
        }

        return Order(orderArgs)

class BooksWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.bookWidgets = [BookEntry()]
        self.widget = QGroupBox()
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b
            }
            QLabel
            {
                background-color: #31363b
            }
            """)

        self.build_scroll_area()

        header = LabelHeader('Books')

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(header.widget, 0, 0)
        self.mainLayout.addWidget(self.scrollArea, 1, 0)
        self.widget.setLayout(self.mainLayout)

    def build_scroll_area(self):

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QGroupBox()
        self.scrollAreaContentsLayout = QGridLayout()

        for book in self.bookWidgets:
            self.scrollAreaContentsLayout.addWidget(book.widget)

        self.scrollAreaContentsLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaContentsLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)

    def add_book(self):
        bookForm = BookEntry()
        self.bookWidgets.append(bookForm)
        self.scrollAreaContentsLayout.addWidget(bookForm.widget)
        self.scrollAreaContentsLayout.update()

    def remove_book(self):
        bookForm = self.bookWidgets.pop()
        self.scrollAreaContentsLayout.removeWidget(bookForm)
        bookForm.widget.deleteLater()
        self.scrollAreaContentsLayout.update()

    def capture(self):
        self.orderItems = []
        for widget in self.bookWidgets:
            self.orderItems.append(widget.capture())


class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b
            }
            QLabel
            {
                background-color: #31363b
            }
            """)

        header = LabelHeader('Order Form')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        self.widget.setLayout(layout)

class ContactWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()

        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b
            }
                QLabel
            {
                background-color: #31363b
            }
            """)

        header = LabelHeader('Contact')

        firstNameLbl = LabelSubHeader('First Name')
        lastNameLbl = LabelSubHeader('Last Name')
        emailLbl = LabelSubHeader('Email')
        phoneLbl = LabelSubHeader('Phone')

        self.firstNameEdit = LineEdit()
        self.lastNameEdit = LineEdit()
        self.emailEdit = LineEdit()
        self.phoneEdit = LineEdit()

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(firstNameLbl.widget, 1, 0)
        layout.addWidget(self.firstNameEdit.widget, 1, 1)
        layout.addWidget(lastNameLbl.widget, 2, 0)
        layout.addWidget(self.lastNameEdit.widget, 2, 1)
        layout.addWidget(emailLbl.widget, 3, 0)
        layout.addWidget(self.emailEdit.widget, 3, 1)
        layout.addWidget(phoneLbl.widget, 4, 0)
        layout.addWidget(self.phoneEdit.widget, 4, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

    def capture(self):
        """Captures the input fields"""
        self.firstName = self.firstNameEdit.capture()
        self.lastName = self.lastNameEdit.capture()
        self.email = self.emailEdit.capture()
        self.phone = self.phoneEdit.capture()

class OrderInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.widget.setStyleSheet("""
                       QGroupBox
                       {
                           background-color: #31363b
                       }
                       QLabel
                       {
                           background-color: #31363b
                       }
                       """)

        header = LabelHeader('Order Info')

        payMethodLbl = LabelSubHeader('Pay Method')
        orderTypeLbl = LabelSubHeader('Order Type')
        referralLbl = LabelSubHeader('Referral Code')

        self.payCombo = ComboBox(['Paypal', 'Square Cash', 'Venmo'])
        self.orderCombo = ComboBox(['Buy Order', 'Sell Order', 'Return'])
        self.referralEdit = LineEdit()

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(payMethodLbl.widget, 1, 0)
        layout.addWidget(self.payCombo.widget, 1, 1)
        layout.addWidget(orderTypeLbl.widget, 2, 0)
        layout.addWidget(self.orderCombo.widget, 2, 1)
        layout.addWidget(referralLbl.widget, 3, 0)
        layout.addWidget(self.referralEdit.widget, 3, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

    def capture(self):
        self.payMethod = self.payCombo.capture()
        self.orderType = self.orderCombo.capture()
        self.referral = self.referralEdit.capture()

class AmazonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.widget.setStyleSheet("""
                       QGroupBox
                       {
                           background-color: #31363b
                       }
                       QLabel
                       {
                           background-color: #31363b
                       }
                       """)

        header = LabelHeader('Amazon Info')

        amazonKeyLbl = LabelSubHeader('Amazon Key')
        amazonShipByLbl = LabelSubHeader('Ship By')
        amazonDeliverByLbl = LabelSubHeader('Deliver By')

        self.amazonKeyEdit = LineEdit()
        self.amazonShipByEdit = LineEdit()
        self.amazonDeliverByEdit = LineEdit()

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(amazonKeyLbl.widget, 1, 0)
        layout.addWidget(self.amazonKeyEdit.widget, 1, 1)
        layout.addWidget(amazonShipByLbl.widget, 2, 0)
        layout.addWidget(self.amazonShipByEdit.widget, 2, 1)
        layout.addWidget(amazonDeliverByLbl.widget, 3, 0)
        layout.addWidget(self.amazonDeliverByEdit.widget, 3, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

    def capture(self):
        self.amazonKey = self.amazonKeyEdit.capture()
        self.amazonShipBy = self.amazonShipByEdit.capture()
        self.amazonDeliverBy = self.amazonDeliverByEdit.capture()

def capture(self):
    """Captures all the input in the confirmation window"""
    self.firstName = self.firstNameEdit.capture()
    self.lastName = self.lastNameEdit.capture()
    self.referral = self.referralEdit.capture()
    self.transactionTypeName = self.payCombo.capture()
    self.email = self.emailEdit.capture()
    self.phone = self.phoneEdit.capture()

    if self.email == '':
        self.email = None

    if self.phone == '':
        self.phone = None

    if self.amazonWidget != None:
        self.amazonWidget.capture()
    else:
        self.amazonArgs = {
            'Ship By': None,
            'Deliver By': None,
            'Amazon Key': None
        }

    for book in self.bookEntries:
        book.capture()

def convert_bookEntry_to_orderItem(self):
    """Returns a list of orderItems"""
    self.orderItems = []

    for bookEntry in self.bookEntries:
        self.orderItems.append(bookEntry.orderItem)

def build_customer_object(self):
    """Builds a customer object"""
    customerArgs = {
        'Customer ID': None,
        'First Name': self.firstName,
        'Last Name': self.lastName,
        'Phone Number': self.phone,
        'Email': self.email,
        'Address': None,
        'Date Joined': None,
        'Referral Code': None,
        'Connection': None
    }
    self.customer = Customer(customerArgs)

def build_amazon_order_object(self):
    """Builds an amazon order object"""
    if self.amazonWidget != None:

        amazonArgs = {
            'Connection': None,
            'Amazon ID': None,
            'Ship By': self.amazonWidget.shipByDate,
            'Deliver By': self.amazonWidget.deliverByDate,
            'Amazon Key': self.amazonWidget.amazonKey

        }
        self.amazonOrder = Amazon_Order(amazonArgs)
    else:
        self.amazonOrder = None

def build_order_type_object(self):
    """Builds an order type object"""
    orderTypeArgs = {
        'Order Type ID': None,
        'Order Type Name': self.orderTypeName
    }
    self.orderType = OrderType(orderTypeArgs)

def build_status_type_object(self):
    """Builds a status type object"""
    statusTypeArgs = {
        'Status ID': None,
        'Status Name': 'Processing'
    }
    self.status = Status(statusTypeArgs)

def build_transaction_object(self):
    """Builds a transaction type object"""
    transactionTypeArgs ={
        'Transaction Type ID': None,
        'Transaction Type Name': self.transactionTypeName
    }
    self.transactionType = TransactionType(transactionTypeArgs)

def build_order_object(self):
    """Build an order object"""
    orderArgs = {
        'Connection': None,
        'Order ID': None,
        'Customer': self.customer,
        'Order Type': self.orderType,
        'Transaction': self.transactionType,
        'Amazon Order': self.amazonOrder,
        'Order Date': None,
        'Status': self.status,
        'Promotion Code': self.referral,
        'Shipping': None,
        'Books': self.orderItems
    }
    self.order = Order(orderArgs)

class BookEntry(QWidget):
    def __init__(self, parent=None):
        """Initializes an instance of BookEntry"""
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b
            }
            QLabel
            {
                background-color: #31363b
            }
            """)

        titleLbl = LabelSubHeader('Title')
        authorLbl = LabelSubHeader('Author')
        editionLbl = LabelSubHeader('Edition')
        isbnLbl = LabelSubHeader('ISBN')
        conditionLbl = LabelSubHeader('Condition')

        self.titleEdit = LineEdit()
        self.authorEdit = LineEdit()
        self.editionEdit = LineEdit()
        self.isbnEdit = LineEdit()
        self.conditionCombo = ComboBox(['New', 'Like New', 'Very Good', 'Good', 'Acceptable'])

        layout = QGridLayout()
        layout.addWidget(titleLbl.widget, 0, 0)
        layout.addWidget(self.titleEdit.widget, 0, 1)
        layout.addWidget(authorLbl.widget, 1, 0)
        layout.addWidget(self.authorEdit.widget, 1, 1)
        layout.addWidget(editionLbl.widget, 2, 0)
        layout.addWidget(self.editionEdit.widget, 2, 1)
        layout.addWidget(isbnLbl.widget, 3, 0)
        layout.addWidget(self.isbnEdit.widget, 3, 1)
        layout.addWidget(conditionLbl.widget, 4, 0)
        layout.addWidget(self.conditionCombo.widget, 4, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

    def capture(self):
        """Stores all the input provided into attributes"""
        orderItemArgs = {
            'Item Number': None,
            'Title': self.titleEdit.capture(),
            'Author': self.authorEdit.capture(),
            'Edition': self.editionEdit.capture(),
            'ISBN': self.isbnEdit.capture(),
            'Condition': self.conditionCombo.capture(),
            'Price': None
        }
        return Order_Item(orderItemArgs)


