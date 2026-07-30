from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("NewsFlow Studio")
        title.setStyleSheet(
            """
            font-size: 32px;
            font-weight: bold;
            """
        )

        subtitle = QLabel("AI-assisted video production workspace")
        subtitle.setStyleSheet("font-size: 16px;")

        new_project_button = QPushButton("New Project")
        open_project_button = QPushButton("Open Project")

        recent_projects = QLabel("Recent Projects")
        recent_projects.setStyleSheet(
            """
            font-size: 20px;
            font-weight: bold;
            margin-top: 25px;
            """
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(new_project_button)
        layout.addWidget(open_project_button)
        layout.addWidget(recent_projects)

        self.setLayout(layout)