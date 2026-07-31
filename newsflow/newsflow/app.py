import sys

from PySide6.QtWidgets import QApplication

from newsflow.ui.main_window import MainWindow, apply_application_style


def run() -> None:
    app = QApplication(sys.argv)

    app.setApplicationName("NewsFlow Studio")
    app.setOrganizationName("NewsFlow")

    apply_application_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
