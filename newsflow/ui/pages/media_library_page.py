from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class MediaLibraryPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title = QLabel("Media Library")
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        title.setStyleSheet(
            """
            font-size: 30px;
            font-weight: bold;
            """
        )

        description = QLabel(
            "This is where imported images and video clips will appear."
        )

        description.setStyleSheet(
            """
            font-size: 15px;
            """
        )

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addStretch()