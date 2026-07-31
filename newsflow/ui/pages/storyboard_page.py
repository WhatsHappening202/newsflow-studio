from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from newsflow.models.storyboard import (
    Storyboard,
    StoryboardScene,
)


class StoryboardSceneCard(QFrame):
    def __init__(
        self,
        scene: StoryboardScene,
    ) -> None:
        super().__init__()

        self.scene = scene

        self.setFrameShape(
            QFrame.Shape.StyledPanel
        )
        self.setMinimumHeight(190)
        self.setStyleSheet(
            """
            StoryboardSceneCard {
                border: 1px solid #b8b8b8;
                border-radius: 8px;
                background-color: rgba(255, 255, 255, 10);
            }
            """
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )
        layout.setSpacing(10)

        header_layout = QGridLayout()

        scene_title = QLabel(
            f"Scene {scene.number}"
        )
        scene_title.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            """
        )

        duration_label = QLabel(
            self._format_duration(
                scene.duration_seconds
            )
        )
        duration_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )
        duration_label.setStyleSheet(
            """
            font-size: 15px;
            font-weight: bold;
            """
        )

        header_layout.addWidget(
            scene_title,
            0,
            0,
        )
        header_layout.addWidget(
            duration_label,
            0,
            1,
        )

        details_label = QLabel(
            f"{scene.word_count} words"
        )
        details_label.setStyleSheet(
            """
            font-size: 12px;
            color: #777777;
            """
        )

        keyword_title = QLabel("Keywords")
        keyword_title.setStyleSheet(
            """
            font-size: 13px;
            font-weight: bold;
            """
        )

        keyword_text = (
            " • ".join(scene.keywords)
            if scene.keywords
            else "No keywords detected"
        )

        keyword_label = QLabel(keyword_text)
        keyword_label.setWordWrap(True)

        narration_title = QLabel(
            "Narration Preview"
        )
        narration_title.setStyleSheet(
            """
            font-size: 13px;
            font-weight: bold;
            """
        )

        narration_label = QLabel(
            self._create_preview(scene.text)
        )
        narration_label.setWordWrap(True)
        narration_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        status_label = QLabel("Needs Media")
        status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        status_label.setStyleSheet(
            """
            font-size: 12px;
            font-weight: bold;
            color: #8a5a00;
            background-color: #ffe7a3;
            border-radius: 5px;
            padding: 5px 10px;
            """
        )

        layout.addLayout(header_layout)
        layout.addWidget(details_label)
        layout.addWidget(keyword_title)
        layout.addWidget(keyword_label)
        layout.addWidget(narration_title)
        layout.addWidget(narration_label)
        layout.addStretch()
        layout.addWidget(status_label)

    @staticmethod
    def _format_duration(
        seconds: int,
    ) -> str:
        minutes, remaining_seconds = divmod(
            max(0, seconds),
            60,
        )

        return (
            f"{minutes}:"
            f"{remaining_seconds:02d}"
        )

    @staticmethod
    def _create_preview(
        text: str,
        maximum_length: int = 260,
    ) -> str:
        cleaned_text = " ".join(
            text.split()
        )

        if len(cleaned_text) <= maximum_length:
            return cleaned_text

        return (
            cleaned_text[:maximum_length]
            .rstrip()
            + "..."
        )


class StoryboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.storyboard: Storyboard | None = None

        self._create_ui()
        self.clear_storyboard()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            30,
            26,
            30,
            26,
        )
        main_layout.setSpacing(16)

        title = QLabel("NewsFlow Director")
        title.setStyleSheet(
            """
            font-size: 30px;
            font-weight: bold;
            """
        )

        subtitle = QLabel(
            "Review automatically detected scenes, "
            "estimated durations, narration, and visual keywords."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            """
            font-size: 15px;
            """
        )

        self.summary_label = QLabel()
        self.summary_label.setStyleSheet(
            """
            font-size: 14px;
            font-weight: bold;
            """
        )

        self.scene_list = QListWidget()
        self.scene_list.setSpacing(10)
        self.scene_list.setSelectionMode(
            QListWidget.SelectionMode.NoSelection
        )
        self.scene_list.setFocusPolicy(
            Qt.FocusPolicy.NoFocus
        )

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )
        scroll_area.setWidget(
            self.scene_list
        )

        self.empty_state_label = QLabel(
            "Import or write a script to generate "
            "a storyboard."
        )
        self.empty_state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.empty_state_label.setStyleSheet(
            """
            font-size: 16px;
            margin-top: 40px;
            """
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(
            self.summary_label
        )
        main_layout.addWidget(
            self.empty_state_label
        )
        main_layout.addWidget(
            scroll_area,
            1,
        )

    def load_storyboard(
        self,
        storyboard: Storyboard,
    ) -> None:
        self.storyboard = storyboard
        self.scene_list.clear()

        for scene in storyboard.scenes:
            card = StoryboardSceneCard(scene)

            item = QListWidgetItem()
            item.setSizeHint(
                card.sizeHint()
            )

            self.scene_list.addItem(item)
            self.scene_list.setItemWidget(
                item,
                card,
            )

        if storyboard.scenes:
            self.empty_state_label.hide()

            total_minutes, total_seconds = divmod(
                storyboard.total_duration,
                60,
            )

            self.summary_label.setText(
                (
                    f"{storyboard.scene_count} scenes  •  "
                    f"{storyboard.total_words:,} words  •  "
                    f"Estimated duration "
                    f"{total_minutes}:{total_seconds:02d}"
                )
            )
        else:
            self.clear_storyboard()

    def clear_storyboard(self) -> None:
        self.storyboard = None
        self.scene_list.clear()
        self.summary_label.setText(
            "No storyboard generated"
        )
        self.empty_state_label.show()