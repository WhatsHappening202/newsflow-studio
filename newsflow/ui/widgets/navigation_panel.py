from PySide6.QtWidgets import QListWidget


class NavigationPanel(QListWidget):
    def __init__(self):
        super().__init__()

        self.setMaximumWidth(220)
        self.setMinimumWidth(180)

        self.addItem("🏠 Dashboard")
        self.addItem("📁 Projects")
        self.addItem("🖼️ Media Library")

        self.setCurrentRow(0)