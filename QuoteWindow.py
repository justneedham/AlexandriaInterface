from view import *

class QuoteWindow(QDialog):
    def __init__(self, orderItems, orderDetailWindow):
        super().__init__()
        self.orderItems = orderItems
        self.orderDetailWindow = orderDetailWindow
        self.title = 'Add Quote'
        self.build_quote_window()

        self.setWindowTitle(self.title)
        self.setFixedHeight(600)
        self.setFixedWidth(1200)
        self.mainLayout = QGridLayout()
        #self.mainLayout.setRowStretch(0, 10)
        #self.mainLayout.setRowStretch(1, 1)
        self.mainLayout.addWidget(self.header.widget, 0, 0)
        self.mainLayout.addWidget(self.quoteRows.widget, 1, 0)
        self.mainLayout.addWidget(self.submitBtn.widget, 2, 0)
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
                        QGroupBox
                        {
                            background-color: #31363b;
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
                            selection-background-color: #9013FE;
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

    def build_quote_window(self):
        self.quoteRows = QuoteRows(self.orderItems)
        self.submitBtn = Button('Submit', self.submit)
        self.header = HeaderWidget()

    def submit(self):
        for quoteRow in self.quoteRows.rows:
            quoteRow.capture()
            self.orderDetailWindow.add_quote(quoteRow.order)

        self.close()

class QuoteRows(QWidget):
    def __init__(self, orderItems, parent=None):
        super().__init__()
        self.orderItems = orderItems
        self.parent = parent
        self.widget = QGroupBox()

        self.build_title_box()
        self.build_scroll_area()
        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(self.titleBox, 0, 0)
        self.mainLayout.addWidget(self.scrollArea, 1, 0)
        self.widget.setLayout(self.mainLayout)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.rows = []

    def build_scroll_area(self):

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QGroupBox()
        self.scrollAreaContentsLayout = QGridLayout()

        for orderItem in self.orderItems:
            row = QuoteEntry(orderItem)
            self.scrollAreaContentsLayout.addWidget(row.widget)

        self.scrollAreaContentsLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaContentsLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)

    def build_title_box(self):
        self.titleBox = QGroupBox()
        self.titleBox.setFixedHeight(40)
        self.titleBox.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b;
            }
            QLabel
            {
                background-color: #31363b;
            }
        """)
        titleLbl = LabelSubHeader('   Title')
        authorLbl = LabelSubHeader('  Author')
        editionLbl = LabelSubHeader('Edition')
        isbnLbl = LabelSubHeader('ISBN')
        conditionLbl = LabelSubHeader('Condition')
        priceLbl = LabelSubHeader('Price')

        quoteLbl = LabelSubHeader('Quote')

        layout = QGridLayout()
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 3)
        layout.setColumnStretch(4, 2)
        layout.setColumnStretch(5, 1)
        layout.setColumnStretch(6, 1)
        layout.setColumnStretch(7, 1)

        layout.addWidget(titleLbl.widget, 0, 0)
        layout.addWidget(authorLbl.widget, 0, 1)
        layout.addWidget(editionLbl.widget, 0, 2)
        layout.addWidget(isbnLbl.widget, 0, 3)
        layout.addWidget(conditionLbl.widget, 0, 4)
        layout.addWidget(priceLbl.widget, 0, 5)
        layout.addWidget(quoteLbl.widget, 0, 6)
        self.titleBox.setLayout(layout)

class HeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
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

        header = LabelHeader('Add Quote')

        layout = QGridLayout()
        layout.addWidget(header.widget, 0, 0)
        self.widget.setLayout(layout)

class QuoteEntry(QWidget):
    def __init__(self, orderItemObject, parent=None):
        """Initializes an instance of QuoteEntry which holds an orderItemObject"""
        super().__init__()
        self.order = orderItemObject
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #76797C;
            }
            QLabel
            {
                background-color: #76797C;
            }
            QLineEdit:focus
            {
                border-color: #9013FE;
            }
            QLineEdit
            {
                border-color: #31363b
            }
            QComboBox
            {
                background-color: #31363b;
                selection-background-color: #31363b;
                border-style: solid;
                border: 1px solid #76797C;
                border-radius: 2px;
                padding: 5px;
                min-width: 75px;
            }
            """)
        self.layout = QGridLayout()
        self.build_quote_entry_widget()

    def build_quote_entry_widget(self):
        """Builds the quote entry widget"""
        self.build_widgets()

        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 3)
        self.layout.setColumnStretch(2, 1)
        self.layout.setColumnStretch(3, 3)
        self.layout.setColumnStretch(4, 2)
        self.layout.setColumnStretch(5, 1)
        self.layout.setColumnStretch(6, 1)
        self.layout.setColumnStretch(7, 1)

        self.layout.addWidget(self.titleLbl.widget, 0, 0)
        self.layout.addWidget(self.authorLbl.widget, 0, 1)
        self.layout.addWidget(self.editionLbl.widget, 0, 2)
        self.layout.addWidget(self.ISBNLbl.widget, 0, 3)
        self.layout.addWidget(self.conditionCombo.widget, 0, 4)
        self.layout.addWidget(self.priceLbl.widget, 0, 5)
        self.layout.addWidget(self.quoteEdit.widget, 0, 6)
        self.widget.setLayout(self.layout)

    def build_widgets(self):
        """Build the widgets"""
        self.quoteEdit = LineEdit()
        self.conditionCombo = ComboBox(['New', 'Like New', 'Very Good', 'Good', 'Acceptable'])
        self.titleLbl = Label(self.order.title)
        self.authorLbl = Label(self.order.author)
        self.ISBNLbl = Label(self.order.ISBN)
        self.priceLbl = Label('None')
        self.priceLbl.setStyleSheet("""
            QLabel
            {
                padding-right: 80px;
                padding-left: 80px;
            }
        """)

        if self.order.edition != None:
            self.editionLbl = Label(str(self.order.edition))
        else:
            self.editionLbl = Label('None')

    def capture(self):
        """Captures the input and assigns it to the orderItemObject"""
        self.quote = self.quoteEdit.capture()
        self.condition = self.conditionCombo.capture()
        self.order.price = self.quote
        self.order.condition = self.condition
