from PySide2 import QtWidgets

CRITICAL_BMI_COLOR = "#cc3300"
BAD_BMI_COLOR = "#ff9966"
WARING_BMI_COLOR = "#ffcc00"
GOOD_BMI_COLOR = "#339900"

class Equation:

    def __init__(self, weight: str, height: str, age: int = None, sex: str = None, tte: float = None):
        """
        Initialization method.
        :param weight: `str`
        :param height: `str`
        :param age: `int`
        :param sex: `str`
        :param tte: `float`
        """
        self.weight = weight.replace(",", ".")
        self.height = height
        self.age = age
        self.sex = sex
        self.tte = tte
        try:
            self.height = int(self.height)
            self.weight = float(self.weight)
        except ValueError:
            return QtWidgets.QMessageBox.critical(None, "Wystąpił błąd", "Wzrost/waga musi być liczbą")  # noqa

    def BMI(self) -> float:
        """
        Method returns BMI value.
        :return: `float`
        """

        return round((self.weight / (self.height / 100) ** 2), 1)

    def BMR(self) -> int:
        """
        Method returns BMR value.
        :return: `int`
        """
        BMR = int((9.99 * self.weight) + (6.25 * self.height) - (4.92 * self.age))
        if self.sex == "f":
            BMR -= 161
        else:
            BMR += 5
        return BMR
    
    def get_BMI_description(self) -> int | dict[str, str | None]:
        """Method that's return description of BMI result and color.

        :return: `dict` description and color message
        """

        result = {
            "color": None,
            "description": None,
        }
        if 3 <= self.BMI() < 16.0:
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "wygłodzenie"
        elif 16 <= self.BMI() <= 17:
            result["color"] = BAD_BMI_COLOR
            result["description"] = "wychudzenie (spowodowane często przez ciężką chorobę)"
        elif 17 <= self.BMI() <= 18.5:
            result["color"] = WARING_BMI_COLOR
            result["description"] = "niedowaga"
        elif 18.5 <= self.BMI() < 25:
            result["color"] = GOOD_BMI_COLOR
            result["description"] = "waga prawidłowa"
        elif 25 <= self.BMI() < 30:
            result["color"] = WARING_BMI_COLOR
            result["description"] = "nadwaga"
        elif 30 <= self.BMI() < 35:
            result["color"] = BAD_BMI_COLOR
            result["description"] = "I stopień otyłości"
        elif 35 <= self.BMI() < 40:
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "II stopień otyłości"
        elif 40 <= self.BMI() <= 720:
            result["color"] = CRITICAL_BMI_COLOR
            result["description"] = "III stopień otyłości (otyłość skrajna)"
        else:
            return QtWidgets.QMessageBox.critical(self, "Wystąpił błąd", "Podano nieprawidłową wagę lub wzrost")  # noqa

        return result

    def TTE(self):
        """Method that returns TTE"""
        return ceil(self.BMR() * self.tte)
