from OrdersWindow import *
from CustomersWindow import *
from CustomerDetailWindow import *
from OrderFormWindow import *

class MainWindow(QWidget):
    def __init__(self, data, controller):
        """Create a new instance of the main window"""
        super().__init__()
        self.data = data
        self.controller = controller
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.showFullScreen()
        self.build_main_window()

    def build_main_window(self):
        """Puts the menu and viewWindow widgets together"""
        self.build_viewWindow()
        self.build_menu()
        self.build_subMenu()

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(1,4)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 10)
        self.layout.addWidget(self.subMenu.widget, 0, 1)
        self.layout.addWidget(self.menu.widget, 1, 0)
        self.layout.addWidget(self.viewWindow.widget, 1, 1)

        self.setLayout(self.layout)

    def build_subMenu(self):
        """Create a new instance of the subMenu widget"""
        self.subMenu = SubMenu()

    def build_viewWindow(self):
        """Create a new instance of the viewWindow widget"""
        self.viewWindow = ViewWindow(self.data, self)

    def build_menu(self):
        """Create a new instance of the menu widget"""
        self.menu = Menu(self)

    def rebuild_menu(self):
        """Delete the layout of the central widgets and rebuilds"""
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.build_viewWindow()
        self.build_menu()
        self.layout.addWidget(self.menu.widget, 0, 0)
        self.layout.addWidget(self.viewWindow.widget, 0, 1)
        self.layout.update()

    def rebuild_menu_two(self):
        self.layout.removeWidget(self.viewWindow)
        self.viewWindow.deleteLater()
        self.build_viewWindow()
        self.layout.addWidget(self.viewWindow.widget, 0, 1)
        self.layout.update()

    def load_order(self, orderID):
        """Calls the controller to load an order with the orderID"""
        return self.controller.load_order(orderID)

    def refresh_data(self):
        """Button method that calls controller to refresh data and update the application"""
        self.data = self.controller.refresh_data()
        self.viewWindow.data = self.data
        self.viewWindow.refresh()

    def add_order_to_database(self, order):
        """Button method that accepts raw data and pushes it to the controller"""
        self.controller.add_order(order)

    def add_quote(self, orderItemObject):
        """Takes an orderItemObject and calls the controller to update it with quote"""
        self.controller.add_quote(orderItemObject)

    def update_order_status(self, orderID, status):
        """Takes the order ID and a status string and calls the controller to update the database"""
        self.controller.update_order_status(orderID, status)

    def add_shipping(self, shippingObject):
        """Takes the shipping object and calls the controller to update the database"""
        self.controller.add_shipping(shippingObject)

    def add_address(self, addressObject):
        """Takes the address object and calls the controller to update the database"""
        self.controller.add_address(addressObject)

    def add_book_to_inventory(self, orderItem):
        """Takes an order Item and inserts into the inventory table"""
        self.controller.add_book_to_inventory(orderItem)

    def remove_book_from_inventory(self, orderItem):
        """Takes and order Item and removes it from the inventory table"""
        self.controller.remove_book_from_inventory(orderItem)

    def move_to_history(self, order):
        """Calls the controller to move order and all supporting rows into the archive"""
        self.controller.move_to_history(order)

    def show_orders(self):
        """Button method that calls ViewWindow to display orders"""
        self.subMenu.show_orders_sub()
        self.viewWindow.show_orders()

    def show_orders_history(self):
        """Button method that calls ViewWindow to diplay orders history"""

    def show_order_detail(self):
        self.viewWindow.show_order_detail()

    def show_customers(self):
        """Button method that calls ViewWindow to display customers"""
        self.subMenu.show_customers_sub()
        self.viewWindow.show_customers()

    def show_customer_detail(self):
        """Button method that calls ViewWindow to display customer detail"""
        self.viewWindow.show_customer_detail()

    def show_order_form(self):
        """Button method that calls ViewWindow to display the buy order form"""
        self.viewWindow.show_order_form()

class SubMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QStackedWidget()
        self.widget.setStyleSheet("""
            QStackedWidget
            {
                background-color: #31363b
            }
        """)
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.ordersSub = OrderSub()
        self.customersSub = CustomersSub()

        self.widget.addWidget(self.ordersSub.widget)
        self.widget.addWidget(self.customersSub.widget)
        self.widget.setCurrentWidget(self.ordersSub.widget)

    def show_customers_sub(self):
        self.widget.setCurrentWidget(self.customersSub.widget)

    def show_orders_sub(self):
        self.widget.setCurrentWidget(self.ordersSub.widget)

class OrderSub(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()
        self.widget.setStyleSheet("""
                    QGroupBox
                    {
                        background-color: #31363b;
                    }
                """)
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


        self.header = LabelHeader('Orders')
        self.ordersBtn = Button('Orders', self.show_orders)
        self.orderHistoryBtn = Button('Orders History', self.show_orders_history)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.header.widget)
        self.mainLayout.addWidget(self.ordersBtn.widget)
        self.mainLayout.addWidget(self.orderHistoryBtn.widget)
        self.widget.setLayout(self.mainLayout)

    def show_orders(self):
        """Show orders"""

    def show_orders_history(self):
        """Show orders history"""

class CustomersSub(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.widget = QGroupBox()

        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.header = LabelHeader('Customers')
        self.customersBtn = Button('Customers', self.show_customers)

        self.mainLayout = QHBoxLayout()
        self.mainLayout.addWidget(self.header.widget)
        self.mainLayout.addWidget(self.customersBtn.widget)
        self.widget.setLayout(self.mainLayout)

    def show_customers(self):
        """Show Customers"""

class ViewWindow(QWidget):
    def __init__(self, data, mainWindow):
        """Create an instance of ViewWindow which holds all the windows"""
        super().__init__()
        self.data = data
        self.mainWindow = mainWindow
        self.widget = QStackedWidget()
        self.widget.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.orders = OrdersListWindow(self.data, self.mainWindow)
        self.customers = CustomersWindow(self.data, self.mainWindow)
        self.customerDetail = CustomerDetailWindow()
        self.addOrder = OrderFormWindow(self.mainWindow)
        self.currentOrderDetailWidget = None

        self.orders.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.customers.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.customerDetail.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.addOrder.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.widget.addWidget(self.orders)
        self.widget.addWidget(self.customers)
        self.widget.addWidget(self.customerDetail)
        self.widget.addWidget(self.addOrder)

        self.widget.setCurrentWidget(self.orders)

    def refresh(self):
        self.orders.data = self.data
        self.orders.refresh()

    def show_orders(self):
        self.widget.setCurrentWidget(self.orders)

    def show_customers(self):
        self.widget.setCurrentWidget(self.customers)

    def show_customer_detail(self):
        self.widget.setCurrentWidget(self.customerDetail)

    def show_order_detail(self):
        self.widget.addWidget(self.orders.orderDetailWindow)
        self.widget.setCurrentWidget(self.orders.orderDetailWindow)

    def show_order_form(self):
        self.widget.setCurrentWidget(self.addOrder)

class Menu(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.widget = QGroupBox()
        self.widget.setStyleSheet("""
            QGroupBox
            {
                background-color: #31363b;
            }
        """)
        self.mainWindow = mainWindow
        self.orderBtn = Button('Orders', self.mainWindow.show_orders)
        self.customersBtn = Button('Customers', self.mainWindow.show_customers)
        self.customerDetailBtn = Button('Customer Detail', self.mainWindow.show_orders)
        self.addOrderBtn = Button('Order Form', self.mainWindow.show_order_form)
        self.refreshBtn = Button('Refresh', self.mainWindow.refresh_data)

        layout = QVBoxLayout()
        layout.addWidget(self.orderBtn.widget)
        layout.addWidget(self.customersBtn.widget)
        layout.addWidget(self.customerDetailBtn.widget)
        layout.addWidget(self.addOrderBtn.widget)
        layout.addWidget(self.refreshBtn.widget)
        self.widget.setLayout(layout)