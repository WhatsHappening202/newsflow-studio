from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ProjectsPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Projects")
        title.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            """
        )

        message = QLabel("Project Manager coming soon...")
        message.setStyleSheet("font-size: 16px;")

        layout.addWidget(title)
        layout.addWidget(message)

        self.setLayout(layout)