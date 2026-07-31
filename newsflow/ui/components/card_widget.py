from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
)


class CardWidget(QFrame):
    def __init__(self):
        super().__init__()

        self.setObjectName("CardWidget")

        self.setMinimumHeight(120)

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )

        self.layout.setSpacing(12)
    