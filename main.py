import sys
from pathlib import Path


from PySide2 import QtCore, QtWidgets, QtGui
from datetime import datetime
from dateutil.relativedelta import relativedelta
from Overrides.QPushButton import QPushButton

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 300
WINDOW_TITLE = "Kalkulator dietetyczny"
CRITICAL_BMI_COLOR = "#cc3300"
BAD_BMI_COLOR = "#ff9966"
WARING_BMI_COLOR = "#ffcc00"
GOOD_BMI_COLOR = "#339900"
TEXT_INPUT_FIELD_WIDTH = 50
CALENDAR_INPUT_WIDTH = 85
FEMALE_ICON = str(Path("icons/woman_female_avatar_icon_128.png").absolute())
MALE_ICON = str(Path("icons/man_avatar_male_icon_128.png").absolute())
ICON_BUTTON_SIZE = 42
ICON_BUTTON_ICON_SIZE = 40
GRID_ROW_MINIMUM_HEIGHT = 45
RESULTS_FONT_FAMILY = 'Helvetica'
RESULTS_FONT_SIZE = 16
BMR_TOOLTIP_METHOD = "Liczony metodą Mifflin-St Jeor"



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
        self.sex_button_group = QtWidgets.QButtonGroup()
        self.sex_label = QtWidgets.QLabel("Płeć:")
        self.sex_male_widget = QPushButton("m")
        self.sex_female_widget = QPushButton("f")
        self.birth_date_label = QtWidgets.QLabel("Podaj datę urodzenia:")
        self.birth_date_widget = QtWidgets.QDateEdit(calendarPopup=True)  # noqa
        self.weight_label = QtWidgets.QLabel("Podaj obecną wagę w kg:")
        self.weight_widget = QtWidgets.QLineEdit("50")
        self.height_label = QtWidgets.QLabel("Podaj wzrost w cm:")
        self.height_widget = QtWidgets.QLineEdit("150")
        self.BMI_label = QtWidgets.QLabel()
        self.BMI_widget = QtWidgets.QLabel()
        self.BMR_label = QtWidgets.QLabel()
        self.BMR_widget = QtWidgets.QLabel()
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
        # check how to set row height
        self.sex_male_widget.setFixedSize(ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)
        self.sex_male_widget.setIcon(QtGui.QIcon(MALE_ICON))
        self.sex_male_widget.setIconSize(QtCore.QSize(ICON_BUTTON_ICON_SIZE, ICON_BUTTON_ICON_SIZE))
        self.sex_male_widget.setCheckable(True)
        self.sex_female_widget.setFixedSize(ICON_BUTTON_SIZE, ICON_BUTTON_SIZE)
        self.sex_female_widget.setIcon(QtGui.QIcon(FEMALE_ICON))
        self.sex_female_widget.setIconSize(QtCore.QSize(ICON_BUTTON_ICON_SIZE, ICON_BUTTON_ICON_SIZE))
        self.sex_female_widget.setCheckable(True)
        self.sex_female_widget.setChecked(True)
        self.sex_button_group.addButton(self.sex_female_widget)
        self.sex_button_group.addButton(self.sex_male_widget)
        self.birth_date_widget.setDate(today)
        self.birth_date_widget.setMaximumDate(today)
        self.weight_widget.setValidator(self.onlyDouble)
        self.height_widget.setValidator(self.onlyInt)
        self.BMI_widget.setFont(QtGui.QFont(RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE))
        self.BMI_label.setFont(QtGui.QFont(RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE))
        self.BMR_label.setToolTip(BMR_TOOLTIP_METHOD)
        self.BMR_widget.setFont(QtGui.QFont(RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE))
        self.BMR_label.setFont(QtGui.QFont(RESULTS_FONT_FAMILY, RESULTS_FONT_SIZE))
        self.weight_widget.setFixedWidth(TEXT_INPUT_FIELD_WIDTH)
        self.height_widget.setFixedWidth(TEXT_INPUT_FIELD_WIDTH)
        self.birth_date_widget.setFixedWidth(CALENDAR_INPUT_WIDTH)

        window_layout.addWidget(self.sex_label, 0, 0)
        window_layout.addWidget(self.sex_female_widget, 0, 1)
        window_layout.addWidget(self.sex_male_widget, 0, 2)
        window_layout.addWidget(self.birth_date_label, 1, 0)
        window_layout.addWidget(self.birth_date_widget, 1, 1)

        window_layout.addWidget(self.weight_label, 2, 0)
        window_layout.addWidget(self.weight_widget, 2, 1)
        window_layout.addWidget(self.height_label, 3, 0)
        window_layout.addWidget(self.height_widget, 3, 1)
        window_layout.addWidget(self.calculate, 4, 1)
        window_layout.addWidget(self.BMI_label, 5, 0)
        window_layout.addWidget(self.BMI_widget, 6, 0)
        window_layout.addWidget(self.BMR_label, 5, 1)
        window_layout.addWidget(self.BMR_widget, 6, 1)
        window_layout.addWidget(self.description_widget, 7, 0, 1, 2)
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

        BMI = round((weight / height ** 2), 1)
        # BMR equation using Mifflin-St Jeor method
        BMR = int((9.99 * weight) + (6.25 * (height * 100)) - (4.92 * age))
        if self.sex_button_group.checkedButton().get_button_name() == "f":
            BMR -= 161
        else:
            BMR += 5

        BMI_value = f'<font color="{self.get_description(bmi_result=BMI).get("color", "green")}">' \
                       f'{str(BMI)}</font>'
        self.BMI_label.setText("BMI")
        self.BMI_widget.setText(BMI_value)

        self.BMR_label.setText("BMR")
        self.BMR_widget.setText(f'{str(BMR)} kcal')
        self.description_widget.setText(self.get_description(bmi_result=BMI).get("description", "brak opisu"))


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
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "wygłodzenie"
        elif 16 <= bmi_result <= 17:
            result["color"] = BAD_BMI_COLOR
            result["description"] = "wychudzenie (spowodowane często przez ciężką chorobę)"
        elif 17 <= bmi_result <= 18.5:
            result["color"] = WARING_BMI_COLOR
            result["description"] = "niedowaga"
        elif 18.5 <= bmi_result < 25:
            result["color"] = GOOD_BMI_COLOR
            result["description"] = "waga prawidłowa"
        elif 25 <= bmi_result < 30:
            result["color"] = WARING_BMI_COLOR
            result["description"] = "nadwaga"
        elif 30 <= bmi_result < 35:
            result["color"] = BAD_BMI_COLOR
            result["description"] = "I stopień otyłości"
        elif 35 <= bmi_result < 40:
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "II stopień otyłości"
        elif 40 <= bmi_result <= 720:
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "III stopień otyłości (otyłość skrajna)"
        else:
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Podano nieprawidłową wagę lub wzrost")  # noqa

        return result


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app_widget = AppWidget()
    app_widget.setWindowTitle(WINDOW_TITLE)
    app_widget.show()
    sys.exit(app.exec_())
