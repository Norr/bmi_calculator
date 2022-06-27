import sys

from PySide2 import QtCore, QtWidgets, QtGui
from datetime import datetime
from dateutil.relativedelta import relativedelta

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
        self.onlyInt = QtGui.QIntValidator(bottom=100, top=250)
        self.birth_date_label = QtWidgets.QLabel("Podaj datę urodzenia:")
        self.birth_date_widget = QtWidgets.QDateEdit(calendarPopup=True) # noqa
        self.weight_label = QtWidgets.QLabel("Podaj obecną wagę w kg:")
        self.weight_widget = QtWidgets.QLineEdit("50")
        self.height_label = QtWidgets.QLabel("Podaj wzrost w cm:")
        self.height_widget = QtWidgets.QLineEdit("150")
        self.result_label = QtWidgets.QLabel("Wynik:")
        self.result_widget = QtWidgets.QLabel()
        self.description_widget = QtWidgets.QLabel()
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
        self.height_widget.setValidator(self.onlyInt)
        self.result_widget.setFont(QtGui.QFont("Helvetica", 24))

        # for next version
        # window_layout.addWidget(self.birth_date_label, 0, 0)
        # window_layout.addWidget(self.birth_date_widget, 0, 1)
        window_layout.addWidget(self.weight_label, 1, 0)
        window_layout.addWidget(self.weight_widget, 1, 1)
        window_layout.addWidget(self.height_label, 2, 0)
        window_layout.addWidget(self.height_widget, 2, 1)
        window_layout.addWidget(self.calculate, 3, 1)
        window_layout.addWidget(self.result_label, 4, 0)
        window_layout.addWidget(self.result_widget, 4, 1)
        window_layout.addWidget(self.description_widget, 5, 0, 1, 2)
        self.calculate.clicked.connect(lambda: self.calculate_bmi())

        return window_layout

    def calculate_bmi(self):
        birthdate = self.birth_date_widget.date().toPython()
        age = (relativedelta(datetime.today().date(), birthdate)).years
        height = self.height_widget.text().replace(",", ".")
        weight = self.weight_widget.text().replace(",", ".")
        try:
            height = int(height) / 100
        except ValueError:
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Wzrost musi być liczbą")

        try:
            weight = float(weight)
        except ValueError:
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Waga musi być liczbą")

        result = round((weight / height ** 2), 1)
        result_value = f'<font color="{self.get_description(bmi_result=result).get("color", "green")}">' \
                       f'{str(result)}</font>'
        self.result_widget.setText(result_value)
        self.description_widget.setText(self.get_description(bmi_result=result).get("description", "brak opisu"))

    def get_description(self, bmi_result: float) -> int | dict[str, str | None]:
        """Method that's return description of BMI result and color.

        :param bmi_result: `float` numer of calculated result.
        :return: `dict` description and color message
        """

        result = {
            "color": None,
            "description": None,
        }
        if 3 <= bmi_result < 16.0:
            result["color"] = "red"
            result["description"] = "wygłodzenie"
        elif 16 <= bmi_result <= 17:
            result["color"] = "red"
            result["description"] = "wychudzenie (spowodowane często przez ciężką chorobę)"
        elif 17 <= bmi_result <= 18.5:
            result["color"] = "orange"
            result["description"] = "niedowaga"
        elif 18.5 <= bmi_result < 25:
            result["color"] = "green"
            result["description"] = "waga prawidłowa"
        elif 25 <= bmi_result < 30:
            result["color"] = "orange"
            result["description"] = "nadwaga"
        elif 30 <= bmi_result < 35:
            result["color"] = "red"
            result["description"] = "I stopień otyłości"
        elif 35 <= bmi_result < 40:
            result["color"] = "red"
            result["description"] = "II stopień otyłości"
        elif 40 <= bmi_result <= 720:
            result["color"] = "red"
            result["description"] = "III stopień otyłości (otyłość skrajna)"
        else:
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Podano nieprawidłową wagę lub wzrost") # noqa

        return result


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app_widget = AppWidget()
    app_widget.setWindowTitle("Kalkulator BMI")
    app_widget.show()
    sys.exit(app.exec_())
