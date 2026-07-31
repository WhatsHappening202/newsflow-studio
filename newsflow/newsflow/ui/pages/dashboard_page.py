from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._create_ui()
        self.clear_project()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(35, 30, 35, 30)
        main_layout.setSpacing(20)

        title = QLabel("Project Dashboard")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "View the files and production status of the current project."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        project_frame = QFrame()
        project_frame.setObjectName("panel")
        project_frame.setFrameShape(QFrame.Shape.StyledPanel)

        project_layout = QGridLayout(project_frame)
        project_layout.setContentsMargins(20, 20, 20, 20)
        project_layout.setHorizontalSpacing(20)
        project_layout.setVerticalSpacing(12)

        project_name_title = QLabel("Project Name")
        project_name_title.setObjectName("fieldTitle")

        project_location_title = QLabel("Location")
        project_location_title.setObjectName("fieldTitle")

        self.project_name_label = QLabel()
        self.project_name_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.project_location_label = QLabel()
        self.project_location_label.setWordWrap(True)
        self.project_location_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        project_layout.addWidget(project_name_title, 0, 0)
        project_layout.addWidget(self.project_name_label, 0, 1)
        project_layout.addWidget(project_location_title, 1, 0)
        project_layout.addWidget(self.project_location_label, 1, 1)

        main_layout.addWidget(project_frame)

        status_title = QLabel("Production Status")
        status_title.setObjectName("sectionTitle")
        main_layout.addWidget(status_title)

        status_grid = QGridLayout()
        status_grid.setSpacing(15)

        self.script_status_card, self.script_status_label = (
            self._create_status_card("Script")
        )
        self.narration_status_card, self.narration_status_label = (
            self._create_status_card("Narration")
        )
        self.images_status_card, self.images_status_label = (
            self._create_status_card("Images")
        )
        self.videos_status_card, self.videos_status_label = (
            self._create_status_card("Videos")
        )
        self.exports_status_card, self.exports_status_label = (
            self._create_status_card("Exports")
        )

        status_grid.addWidget(self.script_status_card, 0, 0)
        status_grid.addWidget(self.narration_status_card, 0, 1)
        status_grid.addWidget(self.images_status_card, 1, 0)
        status_grid.addWidget(self.videos_status_card, 1, 1)
        status_grid.addWidget(self.exports_status_card, 2, 0, 1, 2)

        main_layout.addLayout(status_grid)

        self.empty_state_label = QLabel(
            "Create or open a project to view its dashboard."
        )
        self.empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state_label.setObjectName("emptyState")

        main_layout.addWidget(self.empty_state_label)
        main_layout.addStretch()

    def _create_status_card(
        self,
        title: str,
    ) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("statusCard")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setMinimumHeight(105)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 16)

        title_label = QLabel(title)
        title_label.setObjectName("cardTitle")

        value_label = QLabel()
        value_label.setWordWrap(True)
        value_label.setObjectName("cardValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()

        return card, value_label

    def set_project(
        self,
        project_name: str,
        project_location: str,
        status: dict[str, object] | None = None,
    ) -> None:
        self.project_name_label.setText(project_name)
        self.project_location_label.setText(project_location)
        self.empty_state_label.hide()

        if status is None:
            self._reset_status_labels()
            return

        script_files = status.get("script_files", [])
        narration_files = status.get("narration_files", [])
        image_count = status.get("image_count", 0)
        video_count = status.get("video_count", 0)
        export_count = status.get("export_count", 0)

        if isinstance(script_files, list) and script_files:
            script_names = [Path(file).name for file in script_files]
            self.script_status_label.setText(
                f"Ready — {len(script_names)} file(s)\n"
                + ", ".join(script_names)
            )
        else:
            self.script_status_label.setText("Not started")

        if isinstance(narration_files, list) and narration_files:
            narration_names = [Path(file).name for file in narration_files]
            self.narration_status_label.setText(
                f"Ready — {len(narration_names)} file(s)\n"
                + ", ".join(narration_names)
            )
        else:
            self.narration_status_label.setText("Not started")

        self.images_status_label.setText(
            f"{int(image_count)} imported"
        )
        self.videos_status_label.setText(
            f"{int(video_count)} imported"
        )
        self.exports_status_label.setText(
            f"{int(export_count)} completed export(s)"
        )

    def clear_project(self) -> None:
        self.project_name_label.setText("No project open")
        self.project_location_label.setText("—")
        self._reset_status_labels()
        self.empty_state_label.show()

    def _reset_status_labels(self) -> None:
        self.script_status_label.setText("Not started")
        self.narration_status_label.setText("Not started")
        self.images_status_label.setText("0 imported")
        self.videos_status_label.setText("0 imported")
        self.exports_status_label.setText("0 completed exports")
