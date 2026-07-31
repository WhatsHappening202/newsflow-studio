from PySide6.QtWidgets import QListWidget


class NavigationPanel(QListWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setMinimumWidth(210)
        self.setMaximumWidth(240)

        self.addItem("🏠  Dashboard")
        self.addItem("📁  Project")
        self.addItem("✍️  Script")
        self.addItem("🎙️  Narration")
        self.addItem("🖼️  Images")
        self.addItem("🎥  Videos")
        self.addItem("🧠  AI Storyboard")
        self.addItem("🎬  Timeline")
        self.addItem("📤  Export")
        self.addItem("⚙️  Settings")

        self.setCurrentRow(0)

        self.setStyleSheet(
            """
            QListWidget {
                font-size: 15px;
                padding: 10px;
            }

            QListWidget::item {
                min-height: 42px;
                padding-left: 8px;
                border-radius: 6px;
            }

            QListWidget::item:hover {
                background-color: rgba(120, 120, 120, 60);
            }

            QListWidget::item:selected {
                background-color: #3367d6;
                color: white;
                font-weight: bold;
            }
            """
        )