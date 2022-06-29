import sys
from pathlib import Path

from PySide2 import QtCore, QtWidgets, QtGui
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Equations import Equation
from Overrides.QPushButton import QPushButton

WINDOW_WIDTH = 330
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Kalkulator dietetyczny"

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
tte_items = [
                {"name": "1,2", "value": 1.2, "description": "osoba chora leżąca w łóżku"},
                {"name": "1,25", "value": 1.25, "description": "pracownika biurowey, osoba o bardzo niskiej "
                                                               "aktywności fizycznej związanej tylko z obowiązkami "
                                                               "domowymi."},
                {"name": "1,5", "value": 1.5, "description": "pracownik biurowy, który trenuje ok. 3 razy w tygodniu "
                                                             "przez co najmniej godzinę."},
                {"name": "1,75", "value": 1.75, "description": "osoba prowadząca aktywny tryb życia."},
                {"name": "2", "value": 2, "description": "sportowiec trenujący co najmniej 6 godzin tygodniowo lub"
                                                         " osoba, która wykonuje bardzo ciężką pracę fizyczną."},
            ]


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
        self.BMI_label = QtWidgets.QLabel()
        self.BMI_widget = QtWidgets.QLabel()
        self.TEE_label = QtWidgets.QLabel("Aktywność fizyczna:")
        self.TEE_widget = QtWidgets.QComboBox()
        self.TTE_description_table = QtWidgets.QTableWidget(len(tte_items), 2, self)
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
        self.add_tte_items(tte_items, self.TEE_widget)
        self.generate_description_table(tte_items, self.TTE_description_table)
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
        window_layout.addWidget(self.TEE_label, 4, 0)
        window_layout.addWidget(self.TEE_widget, 4, 1)
        window_layout.addWidget(self.calculate, 5, 1)
        window_layout.addWidget(self.TTE_description_table, 6, 0, 1, 3)
        window_layout.addWidget(self.BMI_label, 7, 0)
        window_layout.addWidget(self.BMI_widget, 8, 0)
        window_layout.addWidget(self.BMR_label, 7, 1)
        window_layout.addWidget(self.BMR_widget, 8, 1)
        window_layout.addWidget(self.description_widget, 9, 0, 1, 2)
        self.calculate.clicked.connect(lambda: self.calculate_results())

        return window_layout

    def calculate_results(self):
        birthdate = self.birth_date_widget.date().toPython()
        age = (relativedelta(datetime.today().date(), birthdate)).years
        calculation = Equation(weight=self.weight_widget.text(),
                               height=self.height_widget.text(),
                               sex=self.sex_button_group.checkedButton().get_button_name(),
                               age=age,
                               tte=self.TEE_widget.currentData())


        BMI_value = f'<font color="{calculation.get_BMI_description().get("color", "green")}">' \
                    f'{str(calculation.BMI())}</font>'
        self.BMI_label.setText("BMI")
        self.BMI_widget.setText(BMI_value)

        self.BMR_label.setText("BMR")
        self.BMR_widget.setText(f'{str(calculation.BMR())} kcal')
        self.description_widget.setText(calculation.get_BMI_description().get("description", "brak opisu"))
        print(calculation.TTE())


    def add_tte_items(self, items: list[dict], widget: QtWidgets.QComboBox):
        if type(items) not in [list, tuple]:
            raise ValueError(f"Items detected typ: {type(items)}. Items must be a `list` or `tuple`.")
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Nieprawidłowy typ wartości listy.")  # noqa
        for item in items:
            widget.addItem(item["name"], item["value"])

    def generate_description_table(self, rows: list[dict], table: QtWidgets.QTableWidget):
        if type(rows) not in [list, tuple]:
            raise ValueError(f"Items detected typ: {type(rows)}. Items must be a `list` or `tuple`.")
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Nieprawidłowy typ wartości listy.")  # noqa

        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setFocusPolicy(QtCore.Qt.NoFocus)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.setHorizontalHeaderLabels(["Warość", "Opis"])
        table.setColumnWidth(0, 56)
        table.setColumnWidth(1, 250)
        row_number = 0
        table_height = 0

        for row in rows:
            table.setItem(row_number, 0, QtWidgets.QTableWidgetItem(row["name"]))
            table.setItem(row_number, 1, QtWidgets.QTableWidgetItem(row["description"]))
            row_number += 1

        table.resizeRowsToContents()

        for row in range(table.rowCount()):
            table_height += table.rowHeight(row) + 0.5

        table_height += table.horizontalHeader().height()
        table.setFixedHeight(table_height)
        table.verticalHeader().hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    app_widget = AppWidget()
    app_widget.setWindowTitle(WINDOW_TITLE)
    app_widget.show()
    sys.exit(app.exec_())
