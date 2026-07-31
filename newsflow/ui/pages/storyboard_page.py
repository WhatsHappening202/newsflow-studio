from __future__ import annotations

from functools import partial

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from newsflow.models.storyboard import (
    Storyboard,
    StoryboardScene,
)


class SummaryMetric(QFrame):
    def __init__(
        self,
        title: str,
        value: str = "0",
        subtitle: str = "",
    ) -> None:
        super().__init__()

        self.setObjectName("directorMetric")
        self.setMinimumHeight(92)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(3)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            color: #AFAFBB;
            font-size: 11px;
            font-weight: 700;
            """
        )

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 23px;
            font-weight: 800;
            """
        )

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setStyleSheet(
            """
            color: #8E8E9A;
            font-size: 11px;
            """
        )

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)
        layout.addWidget(self.subtitle_label)
        layout.addStretch()

    def set_content(
        self,
        value: str,
        subtitle: str = "",
    ) -> None:
        self.value_label.setText(value)
        self.subtitle_label.setText(subtitle)


class KeywordChip(QLabel):
    def __init__(self, keyword: str) -> None:
        super().__init__(keyword)

        self.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.setStyleSheet(
            """
            QLabel {
                background-color: #2A1835;
                color: #E5B5FF;
                border: 1px solid #7B2CBF;
                border-radius: 9px;
                font-size: 11px;
                font-weight: 700;
                padding: 4px 9px;
            }
            """
        )


class StoryboardSceneCard(QFrame):
    open_requested = Signal(int)
    find_media_requested = Signal(int)
    prompt_requested = Signal(int)

    def __init__(
        self,
        scene: StoryboardScene,
    ) -> None:
        super().__init__()

        self.scene = scene

        self.setObjectName("directorSceneCard")
        self.setMinimumHeight(260)
        self.setMinimumWidth(300)

        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(8)

        scene_title = QLabel(
            f"🎬  Scene {self.scene.number}"
        )
        scene_title.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 17px;
            font-weight: 800;
            """
        )

        duration_label = QLabel(
            self._format_duration(
                self.scene.duration_seconds
            )
        )
        duration_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        duration_label.setStyleSheet(
            """
            QLabel {
                background-color: #24152E;
                color: #D98BFF;
                border: 1px solid #8A2BE2;
                border-radius: 8px;
                font-size: 12px;
                font-weight: 800;
                padding: 5px 9px;
            }
            """
        )

        header_layout.addWidget(scene_title)
        header_layout.addStretch()
        header_layout.addWidget(duration_label)

        metadata_layout = QHBoxLayout()

        word_label = QLabel(
            f"{self.scene.word_count:,} words"
        )
        word_label.setStyleSheet(
            """
            color: #9999A5;
            font-size: 11px;
            """
        )

        status_label = QLabel("NEEDS MEDIA")
        status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        status_label.setStyleSheet(
            """
            QLabel {
                background-color: #3B2B12;
                color: #FFE66D;
                border: 1px solid #FACC15;
                border-radius: 8px;
                font-size: 10px;
                font-weight: 800;
                padding: 5px 9px;
            }
            """
        )

        metadata_layout.addWidget(word_label)
        metadata_layout.addStretch()
        metadata_layout.addWidget(status_label)

        keywords_title = QLabel("VISUAL KEYWORDS")
        keywords_title.setStyleSheet(
            """
            color: #AFAFBB;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            """
        )

        keyword_container = QWidget()
        keyword_layout = QHBoxLayout(
            keyword_container
        )
        keyword_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        keyword_layout.setSpacing(6)

        if self.scene.keywords:
            for keyword in self.scene.keywords[:5]:
                keyword_layout.addWidget(
                    KeywordChip(keyword)
                )
        else:
            no_keywords = QLabel(
                "No keywords detected"
            )
            no_keywords.setStyleSheet(
                """
                color: #777783;
                font-size: 11px;
                font-style: italic;
                """
            )
            keyword_layout.addWidget(no_keywords)

        keyword_layout.addStretch()

        narration_title = QLabel(
            "NARRATION PREVIEW"
        )
        narration_title.setStyleSheet(
            """
            color: #AFAFBB;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            """
        )

        narration_label = QLabel(
            self._create_preview(
                self.scene.text
            )
        )
        narration_label.setWordWrap(True)
        narration_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        narration_label.setStyleSheet(
            """
            color: #D7D7DE;
            font-size: 12px;
            line-height: 1.35;
            """
        )

        media_layout = QHBoxLayout()
        media_layout.setSpacing(8)

        images_label = QLabel("🖼  0 Images")
        images_label.setStyleSheet(
            """
            color: #B9B9C4;
            font-size: 11px;
            """
        )

        videos_label = QLabel("🎥  0 Videos")
        videos_label.setStyleSheet(
            """
            color: #B9B9C4;
            font-size: 11px;
            """
        )

        media_layout.addWidget(images_label)
        media_layout.addWidget(videos_label)
        media_layout.addStretch()

        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        open_button = QPushButton("Open Scene")
        open_button.clicked.connect(
            lambda: self.open_requested.emit(
                self.scene.number
            )
        )

        find_media_button = QPushButton(
            "Find Media"
        )
        find_media_button.clicked.connect(
            lambda: (
                self.find_media_requested.emit(
                    self.scene.number
                )
            )
        )

        prompt_button = QPushButton(
            "AI Prompt"
        )
        prompt_button.clicked.connect(
            lambda: (
                self.prompt_requested.emit(
                    self.scene.number
                )
            )
        )

        for button in (
            open_button,
            find_media_button,
            prompt_button,
        ):
            button.setMinimumHeight(34)

        open_button.setStyleSheet(
            """
            QPushButton {
                background-color: #39FF88;
                color: #102018;
                border: none;
                border-radius: 7px;
                font-size: 11px;
                font-weight: 800;
                padding: 7px 12px;
            }

            QPushButton:hover {
                background-color: #72FFAA;
            }
            """
        )

        find_media_button.setStyleSheet(
            """
            QPushButton {
                background-color: #7B2CBF;
                color: white;
                border: none;
                border-radius: 7px;
                font-size: 11px;
                font-weight: 800;
                padding: 7px 12px;
            }

            QPushButton:hover {
                background-color: #A344E5;
            }
            """
        )

        prompt_button.setStyleSheet(
            """
            QPushButton {
                background-color: #2D2D37;
                color: #E6E6ED;
                border: 1px solid #4A4A57;
                border-radius: 7px;
                font-size: 11px;
                font-weight: 800;
                padding: 7px 12px;
            }

            QPushButton:hover {
                border: 1px solid #B026FF;
                color: white;
            }
            """
        )

        action_layout.addWidget(open_button)
        action_layout.addWidget(
            find_media_button
        )
        action_layout.addWidget(prompt_button)

        layout.addLayout(header_layout)
        layout.addLayout(metadata_layout)
        layout.addWidget(keywords_title)
        layout.addWidget(keyword_container)
        layout.addWidget(narration_title)
        layout.addWidget(narration_label)
        layout.addStretch()
        layout.addLayout(media_layout)
        layout.addLayout(action_layout)

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
        maximum_length: int = 240,
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


class DirectorAIPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self.setObjectName("directorAIPanel")
        self.setMinimumWidth(280)
        self.setMaximumWidth(340)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            18,
            18,
            18,
            18,
        )
        layout.setSpacing(12)

        title = QLabel("🤖  Director AI")
        title.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 18px;
            font-weight: 800;
            """
        )

        subtitle = QLabel(
            "Production guidance based on "
            "the current storyboard."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            """
            color: #9696A2;
            font-size: 11px;
            """
        )

        self.suggestion_label = QLabel()
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setStyleSheet(
            """
            QLabel {
                background-color: #25152F;
                color: #E9D5FF;
                border: 1px solid #6F2A91;
                border-radius: 10px;
                font-size: 12px;
                padding: 13px;
            }
            """
        )

        self.media_label = QLabel()
        self.media_label.setWordWrap(True)
        self.media_label.setStyleSheet(
            """
            QLabel {
                background-color: #1D2922;
                color: #A6FFCA;
                border: 1px solid #267549;
                border-radius: 10px;
                font-size: 12px;
                padding: 13px;
            }
            """
        )

        self.warning_label = QLabel()
        self.warning_label.setWordWrap(True)
        self.warning_label.setStyleSheet(
            """
            QLabel {
                background-color: #332912;
                color: #FFE788;
                border: 1px solid #806A22;
                border-radius: 10px;
                font-size: 12px;
                padding: 13px;
            }
            """
        )

        generate_button = QPushButton(
            "Generate Suggestions"
        )
        generate_button.clicked.connect(
            self._show_placeholder
        )

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(6)
        layout.addWidget(self.suggestion_label)
        layout.addWidget(self.media_label)
        layout.addWidget(self.warning_label)
        layout.addStretch()
        layout.addWidget(generate_button)

        self.update_summary(None)

    def update_summary(
        self,
        storyboard: Storyboard | None,
    ) -> None:
        if (
            storyboard is None
            or not storyboard.scenes
        ):
            self.suggestion_label.setText(
                "Import or write a script to "
                "receive production guidance."
            )
            self.media_label.setText(
                "No scenes are currently available "
                "for media matching."
            )
            self.warning_label.setText(
                "No production issues detected yet."
            )
            return

        long_scenes = sum(
            scene.duration_seconds > 45
            for scene in storyboard.scenes
        )

        self.suggestion_label.setText(
            (
                f"✓ {storyboard.scene_count} scenes "
                "were detected.\n\n"
                "Next recommendation: begin "
                "matching visuals to each scene."
            )
        )

        self.media_label.setText(
            (
                "Media matching has not started.\n\n"
                f"{storyboard.scene_count} scene(s) "
                "currently need visual coverage."
            )
        )

        if long_scenes:
            self.warning_label.setText(
                (
                    f"⚠ {long_scenes} scene(s) are "
                    "longer than 45 seconds and may "
                    "benefit from additional visuals."
                )
            )
        else:
            self.warning_label.setText(
                "✓ Scene lengths look balanced."
            )

    def _show_placeholder(self) -> None:
        QMessageBox.information(
            self,
            "Director AI",
            (
                "AI-powered production suggestions "
                "will be connected in an upcoming "
                "milestone."
            ),
        )


class StoryboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.storyboard: Storyboard | None = None
        self.scene_cards: list[
            StoryboardSceneCard
        ] = []

        self._create_ui()
        self.clear_storyboard()

    def _create_ui(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(
            QFrame.Shape.NoFrame
        )

        content = QWidget()
        main_layout = QVBoxLayout(content)
        main_layout.setContentsMargins(
            30,
            26,
            30,
            30,
        )
        main_layout.setSpacing(18)

        header_layout = QHBoxLayout()

        title_group = QVBoxLayout()
        title_group.setSpacing(3)

        title = QLabel("NewsFlow Director")
        title.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 30px;
            font-weight: 800;
            """
        )

        subtitle = QLabel(
            "Turn your script into a structured "
            "visual production plan."
        )
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(
            """
            color: #A4A4AF;
            font-size: 14px;
            """
        )

        title_group.addWidget(title)
        title_group.addWidget(subtitle)

        self.director_status_label = QLabel(
            "NO STORYBOARD"
        )
        self.director_status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.director_status_label.setStyleSheet(
            """
            QLabel {
                background-color: #30303A;
                color: #AAAAAF;
                border: 1px solid #454551;
                border-radius: 9px;
                font-size: 10px;
                font-weight: 800;
                padding: 7px 11px;
            }
            """
        )

        header_layout.addLayout(title_group)
        header_layout.addStretch()
        header_layout.addWidget(
            self.director_status_label
        )

        main_layout.addLayout(header_layout)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(12)

        self.scenes_metric = SummaryMetric(
            "Scenes",
            "0",
            "No scenes detected",
        )
        self.words_metric = SummaryMetric(
            "Words",
            "0",
            "No narration text",
        )
        self.runtime_metric = SummaryMetric(
            "Runtime",
            "0:00",
            "Estimated narration length",
        )
        self.media_metric = SummaryMetric(
            "Media Coverage",
            "0%",
            "No media matched",
        )

        summary_grid.addWidget(
            self.scenes_metric,
            0,
            0,
        )
        summary_grid.addWidget(
            self.words_metric,
            0,
            1,
        )
        summary_grid.addWidget(
            self.runtime_metric,
            0,
            2,
        )
        summary_grid.addWidget(
            self.media_metric,
            0,
            3,
        )

        main_layout.addLayout(summary_grid)

        workspace_layout = QHBoxLayout()
        workspace_layout.setSpacing(18)

        scenes_section = QFrame()
        scenes_section.setObjectName(
            "directorScenesSection"
        )

        scenes_layout = QVBoxLayout(
            scenes_section
        )
        scenes_layout.setContentsMargins(
            18,
            17,
            18,
            18,
        )
        scenes_layout.setSpacing(14)

        scenes_header = QHBoxLayout()

        scenes_title = QLabel(
            "Production Scenes"
        )
        scenes_title.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 18px;
            font-weight: 800;
            """
        )

        self.scene_count_label = QLabel(
            "0 scenes"
        )
        self.scene_count_label.setStyleSheet(
            """
            color: #9B9BA6;
            font-size: 11px;
            """
        )

        scenes_header.addWidget(scenes_title)
        scenes_header.addStretch()
        scenes_header.addWidget(
            self.scene_count_label
        )

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout(
            self.cards_container
        )
        self.cards_grid.setContentsMargins(
            0,
            0,
            0,
            0,
        )
        self.cards_grid.setSpacing(14)
        self.cards_grid.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        cards_scroll = QScrollArea()
        cards_scroll.setWidgetResizable(True)
        cards_scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )
        cards_scroll.setWidget(
            self.cards_container
        )

        self.empty_state_label = QLabel(
            "Import or write a script to generate "
            "your first production storyboard."
        )
        self.empty_state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.empty_state_label.setWordWrap(True)
        self.empty_state_label.setStyleSheet(
            """
            color: #92929E;
            font-size: 15px;
            padding: 50px;
            """
        )

        scenes_layout.addLayout(scenes_header)
        scenes_layout.addWidget(
            self.empty_state_label
        )
        scenes_layout.addWidget(
            cards_scroll,
            1,
        )

        self.ai_panel = DirectorAIPanel()

        workspace_layout.addWidget(
            scenes_section,
            1,
        )
        workspace_layout.addWidget(
            self.ai_panel
        )

        main_layout.addLayout(
            workspace_layout,
            1,
        )

        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)

        self.setStyleSheet(
            """
            #directorMetric,
            #directorScenesSection,
            #directorAIPanel {
                background-color: #24242C;
                border: 1px solid #3B3B46;
                border-radius: 12px;
            }

            #directorMetric:hover,
            #directorSceneCard:hover {
                border: 1px solid #B026FF;
                background-color: #2A2A34;
            }

            #directorSceneCard {
                background-color: #202028;
                border: 1px solid #383843;
                border-radius: 12px;
            }
            """
        )

    def load_storyboard(
        self,
        storyboard: Storyboard,
    ) -> None:
        self.storyboard = storyboard

        self._clear_scene_cards()

        if not storyboard.scenes:
            self.clear_storyboard()
            return

        self.empty_state_label.hide()

        total_minutes, total_seconds = divmod(
            storyboard.total_duration,
            60,
        )

        self.scenes_metric.set_content(
            f"{storyboard.scene_count:,}",
            "Production scenes detected",
        )
        self.words_metric.set_content(
            f"{storyboard.total_words:,}",
            "Total narration words",
        )
        self.runtime_metric.set_content(
            (
                f"{total_minutes}:"
                f"{total_seconds:02d}"
            ),
            "Estimated narration length",
        )
        self.media_metric.set_content(
            "0%",
            "Media matching not started",
        )

        self.scene_count_label.setText(
            f"{storyboard.scene_count} scenes"
        )

        self.director_status_label.setText(
            "STORYBOARD READY"
        )
        self.director_status_label.setStyleSheet(
            """
            QLabel {
                background-color: #173D2A;
                color: #5CFF9D;
                border: 1px solid #39FF88;
                border-radius: 9px;
                font-size: 10px;
                font-weight: 800;
                padding: 7px 11px;
            }
            """
        )

        columns = 2

        for index, scene in enumerate(
            storyboard.scenes
        ):
            card = StoryboardSceneCard(scene)

            card.open_requested.connect(
                self._open_scene
            )
            card.find_media_requested.connect(
                self._find_media
            )
            card.prompt_requested.connect(
                self._generate_prompt
            )

            self.scene_cards.append(card)

            row = index // columns
            column = index % columns

            self.cards_grid.addWidget(
                card,
                row,
                column,
            )

        self.ai_panel.update_summary(
            storyboard
        )

    def clear_storyboard(self) -> None:
        self.storyboard = None

        self._clear_scene_cards()

        self.scenes_metric.set_content(
            "0",
            "No scenes detected",
        )
        self.words_metric.set_content(
            "0",
            "No narration text",
        )
        self.runtime_metric.set_content(
            "0:00",
            "Estimated narration length",
        )
        self.media_metric.set_content(
            "0%",
            "No media matched",
        )

        self.scene_count_label.setText(
            "0 scenes"
        )

        self.director_status_label.setText(
            "NO STORYBOARD"
        )
        self.director_status_label.setStyleSheet(
            """
            QLabel {
                background-color: #30303A;
                color: #AAAAAF;
                border: 1px solid #454551;
                border-radius: 9px;
                font-size: 10px;
                font-weight: 800;
                padding: 7px 11px;
            }
            """
        )

        self.empty_state_label.show()
        self.ai_panel.update_summary(None)

    def _clear_scene_cards(self) -> None:
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.scene_cards.clear()

    def _open_scene(
        self,
        scene_number: int,
    ) -> None:
        scene = self._get_scene(
            scene_number
        )

        if scene is None:
            return

        QMessageBox.information(
            self,
            f"Scene {scene.number}",
            (
                f"Duration: "
                f"{StoryboardSceneCard._format_duration(scene.duration_seconds)}\n\n"
                f"Words: {scene.word_count}\n\n"
                f"Keywords:\n"
                f"{', '.join(scene.keywords) or 'None'}\n\n"
                f"Narration:\n\n{scene.text}"
            ),
        )

    def _find_media(
        self,
        scene_number: int,
    ) -> None:
        QMessageBox.information(
            self,
            "Find Media",
            (
                f"Media matching for Scene "
                f"{scene_number} will be added "
                "in the next production milestone."
            ),
        )

    def _generate_prompt(
        self,
        scene_number: int,
    ) -> None:
        scene = self._get_scene(
            scene_number
        )

        if scene is None:
            return

        keyword_text = (
            ", ".join(scene.keywords)
            if scene.keywords
            else "documentary visual"
        )

        suggested_prompt = (
            "Create a realistic documentary-style "
            f"visual representing: {keyword_text}. "
            "Cinematic composition, professional "
            "lighting, no text, 16:9."
        )

        QMessageBox.information(
            self,
            f"AI Prompt — Scene {scene_number}",
            suggested_prompt,
        )

    def _get_scene(
        self,
        scene_number: int,
    ) -> StoryboardScene | None:
        if self.storyboard is None:
            return None

        for scene in self.storyboard.scenes:
            if scene.number == scene_number:
                return scene

        return None