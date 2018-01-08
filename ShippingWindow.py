from view import *

class ShippingWindow(QDialog):
    def __init__(self, orderDetailWindow):
        super().__init__()
        self.orderDetailWindow = orderDetailWindow
        self.title = 'Add Shipping'
        self.build_shipping_window()

        self.setWindowTitle(self.title)
        self.setFixedWidth(1200)
        self.mainLayout = QGridLayout()
        self.mainLayout.setRowStretch(0,10)
        self.mainLayout.setRowStretch(1,1)
        self.mainLayout.addWidget(self.address.widget, 0, 0)
        self.mainLayout.addWidget(self.shippingInfo.widget, 0, 1)
        self.mainLayout.addWidget(self.submitBtn.widget, 1, 0, 1, 0)
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

    def build_shipping_window(self):
        self.address = AddressWidget(self)
        self.shippingInfo = ShippingInfoWidget(self)
        self.submitBtn = Button('Submit', self.submit)

    def submit(self):
        """Submit"""



class AddressWidget(QWidget):
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
                    QLineEdit:focus
                    {
                        border-color: #9013FE;
                    }
                    """)

        self.build_widgets()

        header = LabelHeader('Address')

        self.mainLayout = QGridLayout()
        self.mainLayout.addWidget(header.widget, 0, 0)
        self.mainLayout.addWidget(QLabel('Building Number'), 1, 0)
        self.mainLayout.addWidget(self.buildingNumberEdit.widget, 1, 1)
        self.mainLayout.addWidget(QLabel('Street Number'), 2, 0)
        self.mainLayout.addWidget(self.streetNumberEdit.widget, 2, 1)
        self.mainLayout.addWidget(QLabel('City'), 3, 0)
        self.mainLayout.addWidget(self.cityEdit.widget, 3, 1 )
        self.mainLayout.addWidget(QLabel('State'), 4, 0)
        self.mainLayout.addWidget(self.stateCombo.widget, 4, 1)
        self.mainLayout.addWidget(QLabel('Zip Code'), 5, 0)
        self.mainLayout.addWidget(self.zipEdit.widget, 5, 1)
        self.mainLayout.addWidget(QLabel('Country'), 6, 0)
        self.mainLayout.addWidget(self.countryCombo.widget, 6, 1)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.mainLayout)

    def build_widgets(self):
        """Builds all auxillary widgets"""

        self.stateCombo = ComboBox([
            'Alabama',
            'Alaska',
            'Arizona',
            'Arkansas',
            'California',
            'Colorado',
            'Connecticut',
            'Delaware',
            'Florida',
            'Georgia',
            'Hawaii',
            'Idaho',
            'Illinois',
            'Indiana',
            'Iowa',
            'Kansas',
            'Kentucky',
            'Louisiana',
            'Maine',
            'Maryland',
            'Massasschusetts',
            'Michigan',
            'Minnesota',
            'Mississippi',
            'Missouri',
            'Montana',
            'Nebraska',
            'Nevada',
            'New Hampshire',
            'New Jersey',
            'New Mexico',
            'New York',
            'North Carolina',
            'North Dakota',
            'Ohio',
            'Oklahoma',
            'Oregon',
            'Pennsylvania',
            'Rhode Island',
            'South Carolina',
            'South Dakota',
            'Tennessee',
            'Texas',
            'Utah',
            'Vermont',
            'Virginia',
            'Washington',
            'West Virginia',
            'Wisconsin',
            'Wyoming'
        ])

        self.countryCombo = ComboBox([
            'Australia',
            'Canada',
            'United Kingdom',
            'United States',
        ])

        self.buildingNumberEdit = LineEdit()
        self.streetNumberEdit = LineEdit()
        self.cityEdit = LineEdit()
        self.zipEdit = LineEdit()


class ShippingInfoWidget(QWidget):
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
                    QLineEdit:focus
                    {
                        border-color: #9013FE;
                    }
                    """)

        self.mainLayout = QGridLayout()

        header = LabelHeader('Shipping Info')

        self.shippingCostEdit = LineEdit()
        self.trackingNumberEdit = LineEdit()
        self.expectedArrivalEdit = LineEdit()

        self.shippingTypeCombo = ComboBox([
            'Sell Books',
            'Buy Books',
            'Sell Package',
            'Return'
        ])
        self.mainLayout.addWidget(header.widget, 0 ,0)
        self.mainLayout.addWidget(QLabel('Shipping Cost'), 1, 0)
        self.mainLayout.addWidget(self.shippingCostEdit.widget, 1, 1)
        self.mainLayout.addWidget(QLabel('Tracking Number'), 2, 0)
        self.mainLayout.addWidget(self.trackingNumberEdit.widget, 2, 1)
        self.mainLayout.addWidget(QLabel('Expected Arrival Date'), 3, 0)
        self.mainLayout.addWidget(self.expectedArrivalEdit.widget, 3, 1)
        self.mainLayout.addWidget(QLabel('Shipping Type'), 4, 0)
        self.mainLayout.addWidget(self.shippingTypeCombo.widget, 4, 1)
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(self.mainLayout)

def submit(self):
    """Captures the input builds a dictionary of shipping args and passes to the mainWindow"""
    self.shippingCost = self.shippingCostEdit.capture()
    self.tracking = self.trackingNumberEdit.capture()
    self.expectedArrival = self.expectedArrivalEdit.capture()
    self.shippingType = self.shippingTypeCombo.capture()

    self.buildingNumber = self.buildingNumberEdit.capture()
    self.street = self.streetNumberEdit.capture()
    self.city = self.cityEdit.capture()
    self.state = self.stateCombo.capture()
    self.zipCode = self.zipEdit.capture()
    self.country = self.countryCombo.capture()

    addressArgs = {
        'Address ID': None,
        'Customer ID': self.orderDetailWindow.order.customer.ID,
        'Building Number': self.buildingNumber,
        'Street Number': self.street,
        'City': self.city,
        'State': State({'State ID': None, 'State Name': self.state, 'State Tax': None}),
        'Zip Code': self.zipCode,
        'Country': Country({'Country ID': None, 'Country Name': self.country}),
        'Connection': None

    }

    addressObject = Address(addressArgs)

    shippingArgs = {
        'Shipping ID': None,
        'Order ID': self.orderDetailWindow.order.ID,
        'Shipping Cost': self.shippingCost,
        'Tracking': self.tracking,
        'Shipping Date': None,
        'Expected Arrival': self.expectedArrival,
        'Shipping Type': ShippingType({'Shipping Type ID': None, 'Shipping Type Name': self.shippingType}),
        'Shipping Materials': None,
        'Status': Status({'Status ID': None, 'Status Name': 'In-Transit'}),
        'Connection': None
    }

    shippingObject = Shipping_Order(shippingArgs)

    self.orderDetailWindow.mainWindow.add_shipping(shippingObject)
    self.orderDetailWindow.mainWindow.add_address(addressObject)
    self.orderDetailWindow.remove_from_inventory()
    self.orderDetailWindow.mainWindow.update_order_status(self.orderDetailWindow.order.ID, 'In-Transit')
    self.close()
