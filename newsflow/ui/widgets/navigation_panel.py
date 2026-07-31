from PySide6.QtWidgets import QListWidget


class NavigationPanel(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumWidth(220)
        self.setMaximumWidth(250)

        self.addItem("🏠  Dashboard")
        self.addItem("📁  Project")
        self.addItem("✍️  Script")
        self.addItem("🎙️  Narration")
        self.addItem("🖼️  Images")
        self.addItem("🎥  Videos")
        self.addItem("🎬  NewsFlow Director")
        self.addItem("🎞️  Timeline")
        self.addItem("📤  Export")
        self.addItem("⚙️  Settings")

        self.setCurrentRow(0)

        self.setStyleSheet(
            """
            QListWidget {
                background-color: #202026;
                border: none;
                border-right: 1px solid #3C3C46;
                color: #F5F5F5;
                font-size: 15px;
                padding: 10px;
                outline: none;
            }

            QListWidget::item {
                min-height: 42px;
                padding-left: 8px;
                border-radius: 6px;
                margin-bottom: 3px;
            }

            QListWidget::item:hover {
                background-color: #33333D;
                color: #FFFFFF;
            }

            QListWidget::item:selected {
                background-color: #39FF88;
                color: #101412;
                font-weight: bold;
                border-left: 4px solid #9BFFBF;
            }

            QListWidget::item:selected:!active {
                background-color: #39FF88;
                color: #101412;
                font-weight: bold;
                border-left: 4px solid #9BFFBF;
            }
            """
        )