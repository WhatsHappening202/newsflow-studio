from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class WorkflowPage(QWidget):
    def __init__(
        self,
        title: str,
        description: str,
    ) -> None:
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 30)
        layout.setSpacing(20)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            font-size: 30px;
            font-weight: bold;
            """
        )

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(
            """
            font-size: 15px;
            """
        )

        coming_soon_label = QLabel(
            "This workspace will be developed in an upcoming milestone."
        )
        coming_soon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        coming_soon_label.setStyleSheet(
            """
            font-size: 16px;
            margin-top: 50px;
            """
        )

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addWidget(coming_soon_label)
        layout.addStretch()