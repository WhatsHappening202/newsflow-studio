from PySide6.QtWidgets import QListWidget


class NavigationPanel(QListWidget):
    def __init__(self):
        super().__init__()

        self.addItem("Dashboard")
        self.addItem("Projects")

        self.setCurrentRow(0)
        self.setMaximumWidth(200)