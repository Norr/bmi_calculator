import sys

from PySide2 import QtCore, QtWidgets, QtGui
from datetime import datetime

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 200
WINDOW_TITLE = "Kalkulator BMI"


class AppWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.data = {
            "birth_date": None,
            "weight": None,
            "height": None,
        }
        self.onlyDouble = QtGui.QDoubleValidator(decimals=1, bottom=2, top=500)
        self.birth_date_label = QtWidgets.QLabel("Podaj datę urodzenia:")
        self.birth_date_widget = QtWidgets.QDateEdit(calendarPopup=True)
        self.weight_label = QtWidgets.QLabel("Podaj obecną wagę:")
        self.weight_widget = QtWidgets.QLineEdit()
        self.height_label = QtWidgets.QLabel("Podaj wzrost:")
        self.height_widget = QtWidgets.QLineEdit()
        self.result_label = QtWidgets.QLabel("Wynik:")
        self.result_widget = QtWidgets.QLabel()
        self.calculate = QtWidgets.QPushButton("Oblicz")

        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.setLayout(self.initialize_layout())


    def initialize_layout(self) -> QtWidgets.QLayout:
        """Method that initilize app layout.

        :param: list of witgets in layout
        :return: return object of  `QtWidgets.QLayout`
        """

        today = QtCore.QDate.currentDate()
        window_layout = QtWidgets.QGridLayout()
        self.birth_date_widget.setDate(today)
        self.birth_date_widget.setMaximumDate(today)
        self.weight_widget.setValidator(self.onlyDouble)

        window_layout.addWidget(self.birth_date_label, 0, 0)
        window_layout.addWidget(self.birth_date_widget, 0, 1)
        window_layout.addWidget(self.weight_label, 1, 0)
        window_layout.addWidget(self.weight_widget, 1, 1)
        window_layout.addWidget(self.height_label, 2, 0)
        window_layout.addWidget(self.height_widget, 2, 1)
        window_layout.addWidget(self.calculate, 3, 1)
        window_layout.addWidget(self.result_label, 4, 0)
        window_layout.addWidget(self.result_widget, 4, 1)

        self.birth_date_widget.dateTimeChanged.connect(lambda: self.get_selected_date())
        return window_layout


    def get_selected_date(self) -> None:
        """
        Method that set data dictionary with key "birth_ate".
        :return: None
        """
        selected_date = self.birth_date_widget.dateTime().toPython()
        self.data['birth_date'] = selected_date

        print(self.data)

    def get_weight(self):
        ...


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app_widget = AppWidget()
    app_widget.setWindowTitle("Kalkulator BMI")
    app_widget.show()
    sys.exit(app.exec_())
