import sys

from PySide6.QtWidgets import QApplication

from newsflow.ui.main_window import (
    MainWindow,
    apply_application_style,
)
from newsflow.ui.theme.stylesheet import (
    application_stylesheet,
)


def run() -> None:
    app = QApplication(sys.argv)

    app.setApplicationName("NewsFlow Studio")
    app.setOrganizationName("NewsFlow")

    apply_application_style(app)

    app.setStyleSheet(
        application_stylesheet()
    )

    window = MainWindow()
    window.show()

    sys.exit(app.exec())