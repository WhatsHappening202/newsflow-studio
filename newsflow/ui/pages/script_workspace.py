from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from newsflow.services.script_analyzer import (
    ScriptAnalyzer,
)
from newsflow.services.script_service import (
    ScriptService,
)


class StatisticCard(QFrame):
    def __init__(
        self,
        title: str,
        initial_value: str = "0",
    ) -> None:
        super().__init__()

        self.setFrameShape(
            QFrame.Shape.StyledPanel
        )

        self.setMinimumHeight(86)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet(
            """
            font-size: 12px;
            color: #777777;
            """
        )

        self.value_label = QLabel(initial_value)
        self.value_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: bold;
            """
        )

        layout.addWidget(title_label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)


class ScriptWorkspace(QWidget):
    status_message = Signal(str, int)

    def __init__(self) -> None:
        super().__init__()

        self.project = None
        self.project_path: Path | None = None
        self.current_script_path: Path | None = None
        self._loading_text = False
        self._has_unsaved_changes = False

        self._create_ui()
        self._update_statistics("")
        self._update_controls()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(
            28,
            24,
            28,
            24,
        )
        main_layout.setSpacing(16)

        header_layout = QHBoxLayout()

        title_section = QVBoxLayout()
        title_section.setSpacing(3)

        title_label = QLabel(
            "Script Workspace"
        )
        title_label.setStyleSheet(
            """
            font-size: 28px;
            font-weight: bold;
            """
        )

        self.filename_label = QLabel(
            "No script loaded"
        )
        self.filename_label.setStyleSheet(
            """
            font-size: 13px;
            color: #777777;
            """
        )

        title_section.addWidget(title_label)
        title_section.addWidget(
            self.filename_label
        )

        self.import_button = QPushButton(
            "Import Script"
        )
        self.import_button.clicked.connect(
            self._import_script
        )

        self.save_button = QPushButton(
            "Save Script"
        )
        self.save_button.clicked.connect(
            self._save_script
        )

        header_layout.addLayout(title_section)
        header_layout.addStretch()
        header_layout.addWidget(
            self.import_button
        )
        header_layout.addWidget(
            self.save_button
        )

        statistics_layout = QGridLayout()
        statistics_layout.setSpacing(10)

        self.word_card = StatisticCard(
            "Words"
        )
        self.character_card = StatisticCard(
            "Characters"
        )
        self.runtime_card = StatisticCard(
            "Estimated Runtime",
            "0:00",
        )
        self.scene_card = StatisticCard(
            "Estimated Scenes"
        )
        self.paragraph_card = StatisticCard(
            "Paragraphs"
        )
        self.sentence_card = StatisticCard(
            "Sentences"
        )

        statistics_layout.addWidget(
            self.word_card,
            0,
            0,
        )
        statistics_layout.addWidget(
            self.character_card,
            0,
            1,
        )
        statistics_layout.addWidget(
            self.runtime_card,
            0,
            2,
        )
        statistics_layout.addWidget(
            self.scene_card,
            0,
            3,
        )
        statistics_layout.addWidget(
            self.paragraph_card,
            1,
            0,
        )
        statistics_layout.addWidget(
            self.sentence_card,
            1,
            1,
        )

        preview_header = QHBoxLayout()

        preview_label = QLabel(
            "Script Editor"
        )
        preview_label.setStyleSheet(
            """
            font-size: 16px;
            font-weight: bold;
            """
        )

        self.change_status_label = QLabel(
            "Saved"
        )
        self.change_status_label.setStyleSheet(
            """
            font-size: 12px;
            color: #777777;
            """
        )

        preview_header.addWidget(preview_label)
        preview_header.addStretch()
        preview_header.addWidget(
            self.change_status_label
        )

        self.script_editor = QTextEdit()
        self.script_editor.setPlaceholderText(
            "Open a project and import a TXT or "
            "Markdown script to begin."
        )
        self.script_editor.setAcceptRichText(False)
        self.script_editor.textChanged.connect(
            self._handle_text_changed
        )

        self.workspace_status_label = QLabel(
            "Open or create a project to begin."
        )
        self.workspace_status_label.setStyleSheet(
            """
            font-size: 12px;
            color: #777777;
            """
        )

        main_layout.addLayout(header_layout)
        main_layout.addLayout(
            statistics_layout
        )
        main_layout.addLayout(preview_header)
        main_layout.addWidget(
            self.script_editor,
            1,
        )
        main_layout.addWidget(
            self.workspace_status_label
        )

    def set_project(
        self,
        project,
        project_path: str | Path,
    ) -> None:
        self.project = project
        self.project_path = Path(project_path)

        self._load_project_script()
        self._update_controls()

    def clear_project(self) -> None:
        self.project = None
        self.project_path = None
        self.current_script_path = None

        self._set_editor_text("")
        self.filename_label.setText(
            "No script loaded"
        )
        self.workspace_status_label.setText(
            "Open or create a project to begin."
        )

        self._has_unsaved_changes = False
        self._update_change_status()
        self._update_controls()

    def refresh(self) -> None:
        if self.project_path is None:
            return

        if self._has_unsaved_changes:
            return

        self._load_project_script()

    def _load_project_script(self) -> None:
        if self.project_path is None:
            return

        try:
            text, script_path = (
                ScriptService.load_script(
                    self.project_path
                )
            )
        except Exception as error:
            QMessageBox.warning(
                self,
                "Could Not Load Script",
                str(error),
            )
            return

        self.current_script_path = script_path
        self._set_editor_text(text)

        if script_path is None:
            self.filename_label.setText(
                "No script loaded"
            )
            self.workspace_status_label.setText(
                "No script has been imported "
                "for this project."
            )
        else:
            self.filename_label.setText(
                script_path.name
            )
            self.workspace_status_label.setText(
                f"Loaded from {script_path}"
            )

        self._has_unsaved_changes = False
        self._update_change_status()

    def _import_script(self) -> None:
        if self.project_path is None:
            QMessageBox.information(
                self,
                "Open a Project",
                "Create or open a project before "
                "importing a script.",
            )
            return

        source_path, _ = (
            QFileDialog.getOpenFileName(
                self,
                "Import Script",
                "",
                (
                    "Script Files "
                    "(*.txt *.md *.markdown);;"
                    "Text Files (*.txt);;"
                    "Markdown Files "
                    "(*.md *.markdown);;"
                    "All Files (*)"
                ),
            )
        )

        if not source_path:
            return

        try:
            text, saved_path = (
                ScriptService.import_script(
                    source_path,
                    self.project_path,
                )
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Could Not Import Script",
                str(error),
            )
            return

        self.current_script_path = saved_path
        self._set_editor_text(text)

        self.filename_label.setText(
            Path(source_path).name
        )
        self.workspace_status_label.setText(
            f"Script imported to {saved_path}"
        )

        self._has_unsaved_changes = False
        self._update_change_status()
        self._update_controls()

        self.status_message.emit(
            "Script imported successfully",
            5000,
        )

    def _save_script(self) -> None:
        if self.project_path is None:
            QMessageBox.information(
                self,
                "Open a Project",
                "Create or open a project before "
                "saving a script.",
            )
            return

        text = self.script_editor.toPlainText()

        if not text.strip():
            QMessageBox.information(
                self,
                "Empty Script",
                "Enter or import script text before "
                "saving.",
            )
            return

        try:
            saved_path = (
                ScriptService.save_script(
                    text,
                    self.project_path,
                )
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Could Not Save Script",
                str(error),
            )
            return

        self.current_script_path = saved_path
        self.filename_label.setText(
            saved_path.name
        )
        self.workspace_status_label.setText(
            f"Saved to {saved_path}"
        )

        self._has_unsaved_changes = False
        self._update_change_status()
        self._update_controls()

        self.status_message.emit(
            "Script saved",
            4000,
        )

    def _handle_text_changed(self) -> None:
        text = self.script_editor.toPlainText()
        self._update_statistics(text)

        if self._loading_text:
            return

        self._has_unsaved_changes = True
        self._update_change_status()
        self._update_controls()

    def _set_editor_text(
        self,
        text: str,
    ) -> None:
        self._loading_text = True
        self.script_editor.setPlainText(text)
        self._loading_text = False

        self._update_statistics(text)

    def _update_statistics(
        self,
        text: str,
    ) -> None:
        statistics = ScriptAnalyzer.analyze(text)

        self.word_card.set_value(
            f"{statistics.word_count:,}"
        )
        self.character_card.set_value(
            f"{statistics.character_count:,}"
        )
        self.runtime_card.set_value(
            statistics.estimated_runtime_display
        )
        self.scene_card.set_value(
            f"{statistics.scene_count:,}"
        )
        self.paragraph_card.set_value(
            f"{statistics.paragraph_count:,}"
        )
        self.sentence_card.set_value(
            f"{statistics.sentence_count:,}"
        )

    def _update_change_status(self) -> None:
        if self._has_unsaved_changes:
            self.change_status_label.setText(
                "Unsaved changes"
            )
            self.change_status_label.setStyleSheet(
                """
                font-size: 12px;
                color: #b36b00;
                font-weight: bold;
                """
            )
        else:
            self.change_status_label.setText(
                "Saved"
            )
            self.change_status_label.setStyleSheet(
                """
                font-size: 12px;
                color: #777777;
                """
            )

    def _update_controls(self) -> None:
        project_is_open = (
            self.project_path is not None
        )

        self.import_button.setEnabled(
            project_is_open
        )
        self.script_editor.setEnabled(
            project_is_open
        )

        has_text = bool(
            self.script_editor
            .toPlainText()
            .strip()
        )

        self.save_button.setEnabled(
            project_is_open
            and has_text
            and self._has_unsaved_changes
        )