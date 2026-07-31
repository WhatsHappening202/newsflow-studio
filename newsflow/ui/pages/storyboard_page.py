from PySide6.QtWidgets import (
    QLabel,
    QListWidget,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from newsflow.models.storyboard import Storyboard


class StoryboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.storyboard = None

        layout = QVBoxLayout(self)

        title = QLabel("NewsFlow Director")
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
        """)

        subtitle = QLabel(
            "Automatically analyze your script into scenes."
        )

        self.scene_list = QListWidget()

        self.scene_text = QTextEdit()
        self.scene_text.setReadOnly(True)

        splitter = QSplitter()

        splitter.addWidget(self.scene_list)
        splitter.addWidget(self.scene_text)

        splitter.setStretchFactor(1, 1)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(splitter)

        self.scene_list.currentRowChanged.connect(
            self._scene_changed
        )

    def load_storyboard(
        self,
        storyboard: Storyboard,
    ):

        self.storyboard = storyboard

        self.scene_list.clear()

        for scene in storyboard.scenes:

            self.scene_list.addItem(
                f"Scene {scene.number}"
            )

        if storyboard.scenes:
            self.scene_list.setCurrentRow(0)

    def _scene_changed(
        self,
        row: int,
    ):

        if (
            self.storyboard is None
            or row < 0
        ):
            return

        scene = self.storyboard.scenes[row]

        self.scene_text.setPlainText(
            f"""Scene {scene.number}

Duration:
{scene.duration_seconds} seconds

Words:
{scene.word_count}

Keywords:
{", ".join(scene.keywords)}

Narration

{scene.text}
"""
        )