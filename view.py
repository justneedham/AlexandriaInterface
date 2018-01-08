from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QMainWindow, QVBoxLayout, QGridLayout, QGroupBox, \
    QStackedWidget, QLabel, QLineEdit, QComboBox, QScrollArea, QDialog, QSizePolicy, QCheckBox, QLayout, QHBoxLayout
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QColor
from model import *


class Button(QWidget):
    def __init__(self, name, method, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent
        self.method = method
        self.widget.clicked.connect(self.method)

class LinkOrderButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent
        self.widget.clicked.connect(self.link_order)

    def link_order(self):
        self.parent.show_order_detail_window(self.name)

class LinkCustomerButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent

    def link_customer(self):
        self.parent.show_customer_detail_window(self.name)

class LinkQuoteButton(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QPushButton(name, self)
        self.name = name
        self.parent = parent

class Label(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QLabel(name)
        self.parent = parent

    def update_text(self, text):
        self.widget.setText(text)

class LabelHeader(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QLabel(name)
        self.parent = parent
        self.widget.setStyleSheet("""
        QLabel
        {
            background-color: rgba(255, 255, 255, 0);
            font-size: 30pt;
        }
        """)

    def update_text(self, text):
        self.widget.setText(text)

class LabelSubHeader(QWidget):
    def __init__(self, name, parent=None):
        super().__init__()
        self.widget = QLabel(name)
        self.parent = parent
        self.widget.setStyleSheet("""
        QLabel
        {
            background-color: rgba(255, 255, 255, 0);
            font-size: 18pt;
        }
        """)

    def update_text(self, text):
        self.widget.setText(text)

class Picture(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QLabel()
        self.parent = parent
        self.pixMap = QPixmap('logo.png')
        self.widget.setPixmap(self.pixMap)
        self.widget.setFixedWidth(518)
        self.widget.setFixedHeight(175)

class LineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QLineEdit()
        self.parent = parent

    def capture(self):
        self.text = self.widget.text()
        return self.text

class ComboBox(QWidget):
    def __init__(self, options, parent=None):
        super().__init__()
        self.widget = QComboBox()
        self.parent = parent
        self.options = options
        self.build_combo_box()

    def build_combo_box(self):
        for option in self.options:
            self.widget.addItem(option)

    def capture(self):
        self.text = str(self.widget.currentText())
        return self.text

class CheckBox(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.widget = QCheckBox()
        self.parent = parent
        self.widget.stateChanged.connect(self.display_amazon_order)
        self.widget.toggle()

    def display_amazon_order(self, state):
        if state == Qt.Checked:
            self.parent.display_amazon_order_box()
        else:
            self.parent.remove_amazon_order_box()










