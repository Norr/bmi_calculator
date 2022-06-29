from PySide2 import QtWidgets


class QPushButton(QtWidgets.QPushButton):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def get_button_name(self):
        return self.name