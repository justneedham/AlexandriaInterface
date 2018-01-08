from view import *

class CustomersWindow(QWidget):
    def __init__(self, data, mainWindow):
        super().__init__()
        self.data = data
        self.mainWindow = mainWindow
        self.layout = QGridLayout()
        self.rows = 1

        self.build()

    def build(self):

        self.layout = QGridLayout()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContentsLayout = QGridLayout()

        titleBox = QGroupBox()
        titleBox.setFixedHeight(60)
        titleLayout = QGridLayout()
        titleLayout.addWidget(QLabel('Customer ID'), 0, 0)
        titleLayout.addWidget(QLabel('First Name'), 0, 1)
        titleLayout.addWidget(QLabel('Last Name'), 0, 2)
        titleLayout.addWidget(QLabel('Phone'), 0, 3)
        titleLayout.addWidget(QLabel('Email'), 0, 4)
        titleLayout.addWidget(QLabel('Account Created'), 0, 5)
        titleBox.setLayout(titleLayout)
        self.rows = 1

        self.scrollAreaContentsLayout.addWidget(titleBox)

        if self.data != None:

            for row in self.data['Views']['Customers']:
                button = LinkCustomerButton(str(row.customerID), self)
                subBox = QGroupBox()
                subBox.setFixedHeight(60)
                subLayout = QGridLayout()
                subLayout.addWidget(button, 0, 0)
                subLayout.addWidget(QLabel(row.firstName), 0, 1)
                subLayout.addWidget(QLabel(row.lastName), 0, 2)
                if row.phone != None:
                    subLayout.addWidget(QLabel(row.phone), 0, 3)
                else:
                    subLayout.addWidget(QLabel('None'), 0, 3)
                if row.email != None:
                    subLayout.addWidget(QLabel(row.email), 0, 4)
                else:
                    subLayout.addWidget(QLabel('None'), 0, 4)
                subLayout.addWidget(QLabel(str(row.date)), 0, 5)
                subBox.setLayout(subLayout)
                self.rows += 1
                self.scrollAreaContentsLayout.addWidget(subBox, self.rows, 0, 1, 0)

        self.scrollAreaContentsLayout.setAlignment(Qt.AlignTop)
        self.scrollAreaContents.setLayout(self.scrollAreaContentsLayout)
        self.scrollArea.setWidget(self.scrollAreaContents)
        self.scrollArea.setFixedWidth(1400)
        self.scrollArea.setFixedHeight(800)
        self.layout.addWidget(self.scrollArea)

        self.setLayout(self.layout)

    def updateData(self, data):
        self.data = data