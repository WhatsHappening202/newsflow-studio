from __future__ import annotations

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
from newsflow.services.media_match_service import (
    SceneMediaMatches,
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
        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )
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
    def __init__(
        self,
        keyword: str,
    ) -> None:
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
        matches: SceneMediaMatches,
    ) -> None:
        super().__init__()

        self.scene = scene
        self.matches = matches

        self.setObjectName("directorSceneCard")
        self.setMinimumHeight(310)
        self.setMinimumWidth(310)

        self._create_ui()

    def _create_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            18,
            16,
            18,
            16,
        )
        layout.setSpacing(9)

        header_layout = QHBoxLayout()

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

        status_label = QLabel(
            (
                "MEDIA FOUND"
                if self.matches.has_matches
                else "NEEDS MEDIA"
            )
        )
        status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        if self.matches.has_matches:
            status_label.setStyleSheet(
                """
                QLabel {
                    background-color: #173D2A;
                    color: #5CFF9D;
                    border: 1px solid #39FF88;
                    border-radius: 8px;
                    font-size: 10px;
                    font-weight: 800;
                    padding: 5px 9px;
                }
                """
            )
        else:
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

        for keyword in self.scene.keywords[:5]:
            keyword_layout.addWidget(
                KeywordChip(keyword)
            )

        if not self.scene.keywords:
            keyword_layout.addWidget(
                QLabel("No keywords detected")
            )

        keyword_layout.addStretch()

        narration_title = QLabel(
            "NARRATION PREVIEW"
        )
        narration_title.setStyleSheet(
            """
            color: #AFAFBB;
            font-size: 10px;
            font-weight: 800;
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
            """
        )

        media_title = QLabel(
            "MATCHED PROJECT MEDIA"
        )
        media_title.setStyleSheet(
            """
            color: #AFAFBB;
            font-size: 10px;
            font-weight: 800;
            """
        )

        media_summary = QLabel(
            (
                f"🖼  {self.matches.image_count} Images"
                f"     🎥  {self.matches.video_count} Videos"
            )
        )
        media_summary.setStyleSheet(
            """
            color: #B9B9C4;
            font-size: 11px;
            font-weight: 700;
            """
        )

        matched_names: list[str] = []

        matched_names.extend(
            match.filename
            for match in self.matches.image_matches[:2]
        )
        matched_names.extend(
            match.filename
            for match in self.matches.video_matches[:1]
        )

        matched_files_label = QLabel(
            (
                "\n".join(
                    f"• {name}"
                    for name in matched_names
                )
                if matched_names
                else "No matching filenames found"
            )
        )
        matched_files_label.setWordWrap(True)
        matched_files_label.setStyleSheet(
            """
            color: #8F8F9B;
            font-size: 10px;
            """
        )

        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        open_button = QPushButton("Open Scene")
        find_media_button = QPushButton(
            "View Matches"
        )
        prompt_button = QPushButton("AI Prompt")

        open_button.clicked.connect(
            lambda: self.open_requested.emit(
                self.scene.number
            )
        )
        find_media_button.clicked.connect(
            lambda: (
                self.find_media_requested.emit(
                    self.scene.number
                )
            )
        )
        prompt_button.clicked.connect(
            lambda: self.prompt_requested.emit(
                self.scene.number
            )
        )

        action_layout.addWidget(open_button)
        action_layout.addWidget(find_media_button)
        action_layout.addWidget(prompt_button)

        layout.addLayout(header_layout)
        layout.addLayout(metadata_layout)
        layout.addWidget(keywords_title)
        layout.addWidget(keyword_container)
        layout.addWidget(narration_title)
        layout.addWidget(narration_label)
        layout.addWidget(media_title)
        layout.addWidget(media_summary)
        layout.addWidget(matched_files_label)
        layout.addStretch()
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
        maximum_length: int = 200,
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
        self.media_matches: dict[
            int,
            SceneMediaMatches,
        ] = {}

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

        title = QLabel("NewsFlow Director")
        title.setStyleSheet(
            """
            color: #F8F8FA;
            font-size: 30px;
            font-weight: 800;
            """
        )

        subtitle = QLabel(
            "Automatically match project media "
            "to each production scene."
        )
        subtitle.setStyleSheet(
            """
            color: #A4A4AF;
            font-size: 14px;
            """
        )

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        summary_grid = QGridLayout()
        summary_grid.setSpacing(12)

        self.scenes_metric = SummaryMetric(
            "Scenes",
        )
        self.words_metric = SummaryMetric(
            "Words",
        )
        self.runtime_metric = SummaryMetric(
            "Runtime",
        )
        self.media_metric = SummaryMetric(
            "Media Coverage",
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

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout(
            self.cards_container
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
            "Import a script and project media "
            "to begin matching visuals."
        )
        self.empty_state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.empty_state_label.setStyleSheet(
            """
            color: #92929E;
            font-size: 15px;
            padding: 50px;
            """
        )

        main_layout.addWidget(
            self.empty_state_label
        )
        main_layout.addWidget(
            cards_scroll,
            1,
        )

        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)

        self.setStyleSheet(
            """
            #directorMetric {
                background-color: #24242C;
                border: 1px solid #3B3B46;
                border-radius: 12px;
            }

            #directorSceneCard {
                background-color: #202028;
                border: 1px solid #383843;
                border-radius: 12px;
            }

            #directorSceneCard:hover {
                border: 1px solid #B026FF;
                background-color: #2A2A34;
            }
            """
        )

    def load_storyboard(
        self,
        storyboard: Storyboard,
        media_matches: dict[
            int,
            SceneMediaMatches,
        ] | None = None,
        coverage_percentage: int = 0,
    ) -> None:
        self.storyboard = storyboard
        self.media_matches = (
            media_matches or {}
        )

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
            f"{coverage_percentage}%",
            "Scenes with filename matches",
        )

        for index, scene in enumerate(
            storyboard.scenes
        ):
            matches = self.media_matches.get(
                scene.number,
                SceneMediaMatches(
                    scene_number=scene.number,
                    image_matches=(),
                    video_matches=(),
                ),
            )

            card = StoryboardSceneCard(
                scene=scene,
                matches=matches,
            )

            card.open_requested.connect(
                self._open_scene
            )
            card.find_media_requested.connect(
                self._view_matches
            )
            card.prompt_requested.connect(
                self._generate_prompt
            )

            self.scene_cards.append(card)

            row = index // 2
            column = index % 2

            self.cards_grid.addWidget(
                card,
                row,
                column,
            )

    def clear_storyboard(self) -> None:
        self.storyboard = None
        self.media_matches = {}

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
            "No estimated runtime",
        )
        self.media_metric.set_content(
            "0%",
            "No media matched",
        )

        self.empty_state_label.show()

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
        scene = self._get_scene(scene_number)

        if scene is None:
            return

        QMessageBox.information(
            self,
            f"Scene {scene.number}",
            scene.text,
        )

    def _view_matches(
        self,
        scene_number: int,
    ) -> None:
        matches = self.media_matches.get(
            scene_number
        )

        if matches is None or not matches.has_matches:
            QMessageBox.information(
                self,
                "No Media Matches",
                (
                    "No filenames matched this "
                    "scene's keywords or narration."
                ),
            )
            return

        lines: list[str] = []

        if matches.image_matches:
            lines.append("IMAGES")

            for match in matches.image_matches:
                terms = ", ".join(
                    match.matched_terms
                )

                lines.append(
                    f"• {match.filename}\n"
                    f"  Score: {match.score} | "
                    f"Matched: {terms}"
                )

        if matches.video_matches:
            lines.append("")
            lines.append("VIDEOS")

            for match in matches.video_matches:
                terms = ", ".join(
                    match.matched_terms
                )

                lines.append(
                    f"• {match.filename}\n"
                    f"  Score: {match.score} | "
                    f"Matched: {terms}"
                )

        QMessageBox.information(
            self,
            f"Media Matches — Scene {scene_number}",
            "\n".join(lines),
        )

    def _generate_prompt(
        self,
        scene_number: int,
    ) -> None:
        scene = self._get_scene(scene_number)

        if scene is None:
            return

        keywords = (
            ", ".join(scene.keywords)
            if scene.keywords
            else "documentary scene"
        )

        prompt = (
            "Create a realistic documentary-style "
            f"visual representing: {keywords}. "
            "Cinematic lighting, professional "
            "composition, no text, 16:9."
        )

        QMessageBox.information(
            self,
            f"AI Prompt — Scene {scene_number}",
            prompt,
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