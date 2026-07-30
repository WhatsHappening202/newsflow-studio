import sys

from PySide6.QtWidgets import QApplication

from newsflow.ui.main_window import MainWindow


def run() -> None:
    app = QApplication(sys.argv)

    app.setApplicationName("NewsFlow Studio")
    app.setOrganizationName("NewsFlow")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())