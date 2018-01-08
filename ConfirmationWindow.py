from view import *

class ConfirmationWindow(QDialog):
    def __init__(self, order, parent=None):
        """Initializes an AddOrderWindow"""
        super().__init__()
        self.order = order
        self.parent = parent
        self.title = 'Confirm Order'
        self.bookEntries = []
        self.build_order_form()

        self.setWindowTitle(self.title)
        self.setFixedWidth(800)
        self.setFixedHeight(800)
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.orderForm)
        self.mainLayout.setAlignment(Qt.AlignVCenter)
        self.setLayout(self.mainLayout)
        self.setStyleSheet("""
                QWidget
                {
                    color: #eff0f1;
                    background-color: #76797C;
                    selection-background-color: #3daee9;
                    selection-color: #eff0f1;
                    background-clip: border;
                    border-image: none;
                    border: 0px transparent black;
                    outline: 0;
                }
                QWidget:item:hover
                {
                    background-color: #18465d;
                    color: #eff0f1;
                }
                QWidget:item:selected
                {
                    background-color: #18465d;
                }
                QLineEdit
                {
                    background-color: #232629;
                    padding: 5px;
                    border-style: solid;
                    border: 1px solid #76797C;
                    border-radius: 2px;
                    color: #eff0f1;
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
                QComboBox
                {
                    selection-background-color: #3daee9;
                    border-style: solid;
                    border: 1px solid #76797C;
                    border-radius: 2px;
                    padding: 5px;
                    min-width: 75px;
                }
                QComboBox:focus
                {
                    border-color: #9013FE;
                }
                QLabel 
                {
                     border: 0px solid black;
                     font-family: Avenir Next;
                     font-style: regular;
                }
            """)
    def build_order_form(self):
        """Builds the add order window"""
        self.contactInfo = ContactWidget(self)
        self.orderInfo = OrderInfoWidget(self)
        self.amazonInfo = AmazonWidget(self)
        self.header = HeaderWidget(self)
        self.bookScroll = BooksWidget(self)

        self.orderForm = QGroupBox()
        self.orderFormLayout = QGridLayout()
        self.orderFormLayout.setColumnStretch(0, 1)
        self.orderFormLayout.setColumnStretch(1, 1)

        self.yesBtn = Button('Yes', self.parent.confirm)
        self.noBtn = Button('No', self.parent.close)

        #row, column
        self.orderFormLayout.addWidget(self.header.widget, 0, 0, 1, 0)
        self.orderFormLayout.addWidget(self.contactInfo.widget, 1, 0)
        self.orderFormLayout.addWidget(self.orderInfo.widget, 1, 1)
        self.orderFormLayout.addWidget(self.amazonInfo.widget, 2, 0)
        self.orderFormLayout.addWidget(self.bookScroll.widget, 3, 0, 1, 0)
        self.orderFormLayout.addWidget(self.yesBtn.widget, 4, 0)
        self.orderFormLayout.addWidget(self.noBtn.widget, 4, 1)
        self.orderFormLayout.setAlignment(Qt.AlignTop)

        self.orderForm.setLayout(self.orderFormLayout)

class BooksWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.orderItem = self.parent.order.books
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
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QGroupBox()
        self.scrollAreaContentsLayout = QGridLayout()

        for orderItem in self.orderItem:
            widget = BookEntry(orderItem)
            self.scrollAreaContentsLayout.addWidget(widget.widget)

        self.scrollAreaContentsLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaContentsLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
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

        header = LabelHeader('Confirm Order')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        self.widget.setLayout(layout)

class ContactWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
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

        header = LabelHeader('Contact')

        firstNameLbl = LabelSubHeader('First Name')
        lastNameLbl = LabelSubHeader('Last Name')
        emailLbl = LabelSubHeader('Email')
        phoneLbl = LabelSubHeader('Phone')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(firstNameLbl.widget, 1, 0)
        layout.addWidget(QLabel(self.parent.order.customer.firstName), 1, 1)
        layout.addWidget(lastNameLbl.widget, 2, 0)
        layout.addWidget(QLabel(self.parent.order.customer.lastName), 2, 1)
        layout.addWidget(emailLbl.widget, 3, 0)
        layout.addWidget(QLabel(self.parent.order.customer.email), 3, 1)
        layout.addWidget(phoneLbl.widget, 4, 0)
        layout.addWidget(QLabel(self.parent.order.customer.phone), 4, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

class OrderInfoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
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

        header = LabelHeader('Order Info')

        payMethodLbl = LabelSubHeader('Pay Method')
        orderTypeLbl = LabelSubHeader('Order Type')
        referralLbl = LabelSubHeader('Referral Code')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(payMethodLbl.widget, 1, 0)
        layout.addWidget(QLabel(self.parent.order.transaction.name), 1, 1)
        layout.addWidget(orderTypeLbl.widget, 2, 0)
        layout.addWidget(QLabel(self.parent.order.orderType.name), 2, 1)
        layout.addWidget(referralLbl.widget, 3, 0)
        layout.addWidget(QLabel(self.parent.order.promotion), 3, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

class AmazonWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
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

        header = LabelHeader('Amazon Info')

        amazonKeyLbl = LabelSubHeader('Amazon Key')
        amazonShipByLbl = LabelSubHeader('Ship By')
        amazonDeliverByLbl = LabelSubHeader('Deliver By')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        layout.addWidget(amazonKeyLbl.widget, 1, 0)
        layout.addWidget(QLabel(self.parent.order.amazonOrder.code), 1, 1)
        layout.addWidget(amazonShipByLbl.widget, 2, 0)
        layout.addWidget(QLabel(self.parent.order.amazonOrder.shipBy), 2, 1)
        layout.addWidget(amazonDeliverByLbl.widget, 3, 0)
        layout.addWidget(QLabel(self.parent.order.amazonOrder.deliverBy), 3, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)

class BookEntry(QWidget):
    def __init__(self, orderItem, parent=None):
        """Initializes an instance of BookEntry"""
        super().__init__()
        self.parent = parent
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
        layout.addWidget(QLabel(orderItem.title), 0, 1)
        layout.addWidget(authorLbl.widget, 1, 0)
        layout.addWidget(QLabel(orderItem.author), 1, 1)
        layout.addWidget(editionLbl.widget, 2, 0)
        layout.addWidget(QLabel(orderItem.edition), 2, 1)
        layout.addWidget(isbnLbl.widget, 3, 0)
        layout.addWidget(QLabel(orderItem.ISBN), 3, 1)
        layout.addWidget(conditionLbl.widget, 4, 0)
        layout.addWidget(QLabel(orderItem.condition), 4, 1)
        layout.setAlignment(Qt.AlignTop)

        self.widget.setLayout(layout)




