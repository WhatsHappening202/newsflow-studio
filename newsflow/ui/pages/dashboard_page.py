from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from newsflow.services.system_service import SystemService


class MetricCard(QFrame):
    def __init__(
        self,
        title: str,
        value: str = "0",
        subtitle: str = "",
    ) -> None:
        super().__init__()

        self.setObjectName("metricCard")
        self.setMinimumHeight(105)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 15, 18, 15)
        layout.setSpacing(5)

        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")

        self.value_label = QLabel(value)
        self.value_label.setObjectName("metricValue")

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("metricSubtitle")
        self.subtitle_label.setWordWrap(True)

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


class ProductionCard(QFrame):
    def __init__(
        self,
        title: str,
        icon: str,
    ) -> None:
        super().__init__()

        self.setObjectName("productionCard")
        self.setMinimumHeight(125)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(7)

        header_layout = QHBoxLayout()

        title_label = QLabel(f"{icon}  {title}")
        title_label.setObjectName("productionTitle")

        self.status_badge = QLabel("NOT STARTED")
        self.status_badge.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.status_badge)

        self.detail_label = QLabel()
        self.detail_label.setObjectName("productionDetail")
        self.detail_label.setWordWrap(True)

        layout.addLayout(header_layout)
        layout.addWidget(self.detail_label)
        layout.addStretch()

        self.set_status(
            "Not started",
            "No files found",
            "inactive",
        )

    def set_status(
        self,
        status: str,
        detail: str,
        state: str,
    ) -> None:
        self.status_badge.setText(status.upper())
        self.detail_label.setText(detail)

        styles = {
            "complete": (
                "background-color: #173D2A;"
                "color: #5CFF9D;"
                "border: 1px solid #39FF88;"
            ),
            "attention": (
                "background-color: #3D3214;"
                "color: #FFE66D;"
                "border: 1px solid #FACC15;"
            ),
            "missing": (
                "background-color: #451B25;"
                "color: #FF718B;"
                "border: 1px solid #EF4444;"
            ),
            "inactive": (
                "background-color: #30303A;"
                "color: #A8A8B2;"
                "border: 1px solid #454551;"
            ),
        }

        badge_style = styles.get(
            state,
            styles["inactive"],
        )

        self.status_badge.setStyleSheet(
            f"""
            QLabel {{
                {badge_style}
                border-radius: 8px;
                font-size: 10px;
                font-weight: 800;
                padding: 5px 9px;
            }}
            """
        )


class QuickActionButton(QPushButton):
    def __init__(
        self,
        icon: str,
        title: str,
        subtitle: str,
    ) -> None:
        super().__init__()

        self.setObjectName("quickActionButton")
        self.setMinimumHeight(82)
        self.setText(
            f"{icon}  {title}\n"
            f"     {subtitle}"
        )


class DashboardPage(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.project_folder: str | None = None

        self._create_ui()
        self.clear_project()

    def _create_ui(self) -> None:
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)

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
        main_layout.setSpacing(20)

        header_layout = QHBoxLayout()

        title_group = QVBoxLayout()
        title_group.setSpacing(3)

        title = QLabel("Project Dashboard")
        title.setObjectName("dashboardTitle")

        subtitle = QLabel(
            "Your production command center"
        )
        subtitle.setObjectName("dashboardSubtitle")

        title_group.addWidget(title)
        title_group.addWidget(subtitle)

        self.project_status_label = QLabel(
            "NO PROJECT OPEN"
        )
        self.project_status_label.setObjectName(
            "projectStatusBadge"
        )

        header_layout.addLayout(title_group)
        header_layout.addStretch()
        header_layout.addWidget(
            self.project_status_label
        )

        main_layout.addLayout(header_layout)

        self.project_overview = QFrame()
        self.project_overview.setObjectName(
            "projectOverviewCard"
        )

        overview_layout = QGridLayout(
            self.project_overview
        )
        overview_layout.setContentsMargins(
            22,
            18,
            22,
            18,
        )
        overview_layout.setHorizontalSpacing(18)
        overview_layout.setVerticalSpacing(10)

        project_heading = QLabel(
            "CURRENT PROJECT"
        )
        project_heading.setObjectName(
            "smallSectionLabel"
        )

        self.project_name_label = QLabel()
        self.project_name_label.setObjectName(
            "currentProjectName"
        )

        location_heading = QLabel("Location")
        location_heading.setObjectName("fieldLabel")

        folder_heading = QLabel("Project Folder")
        folder_heading.setObjectName("fieldLabel")

        self.project_location_label = QLabel()
        self.project_location_label.setWordWrap(True)
        self.project_location_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.project_folder_label = QLabel()
        self.project_folder_label.setWordWrap(True)
        self.project_folder_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        overview_layout.addWidget(
            project_heading,
            0,
            0,
            1,
            2,
        )
        overview_layout.addWidget(
            self.project_name_label,
            1,
            0,
            1,
            2,
        )
        overview_layout.addWidget(
            location_heading,
            2,
            0,
        )
        overview_layout.addWidget(
            self.project_location_label,
            2,
            1,
        )
        overview_layout.addWidget(
            folder_heading,
            3,
            0,
        )
        overview_layout.addWidget(
            self.project_folder_label,
            3,
            1,
        )

        main_layout.addWidget(self.project_overview)

        metrics_layout = QGridLayout()
        metrics_layout.setSpacing(12)

        self.scripts_metric = MetricCard(
            "Scripts",
            "0",
            "No script imported",
        )
        self.narration_metric = MetricCard(
            "Narration",
            "0",
            "No narration imported",
        )
        self.images_metric = MetricCard(
            "Images",
            "0",
            "No images imported",
        )
        self.videos_metric = MetricCard(
            "Videos",
            "0",
            "No videos imported",
        )
        self.exports_metric = MetricCard(
            "Exports",
            "0",
            "No completed exports",
        )

        metrics_layout.addWidget(
            self.scripts_metric,
            0,
            0,
        )
        metrics_layout.addWidget(
            self.narration_metric,
            0,
            1,
        )
        metrics_layout.addWidget(
            self.images_metric,
            0,
            2,
        )
        metrics_layout.addWidget(
            self.videos_metric,
            0,
            3,
        )
        metrics_layout.addWidget(
            self.exports_metric,
            0,
            4,
        )

        main_layout.addLayout(metrics_layout)

        dashboard_grid = QGridLayout()
        dashboard_grid.setSpacing(18)

        production_section = QFrame()
        production_section.setObjectName(
            "dashboardSection"
        )

        production_layout = QVBoxLayout(
            production_section
        )
        production_layout.setContentsMargins(
            20,
            18,
            20,
            20,
        )
        production_layout.setSpacing(14)

        production_title = QLabel(
            "Production Status"
        )
        production_title.setObjectName(
            "dashboardSectionTitle"
        )

        status_grid = QGridLayout()
        status_grid.setSpacing(12)

        self.script_card = ProductionCard(
            "Script",
            "📄",
        )
        self.narration_card = ProductionCard(
            "Narration",
            "🎙",
        )
        self.media_card = ProductionCard(
            "Media",
            "🖼",
        )
        self.export_card = ProductionCard(
            "Export",
            "📤",
        )

        status_grid.addWidget(
            self.script_card,
            0,
            0,
        )
        status_grid.addWidget(
            self.narration_card,
            0,
            1,
        )
        status_grid.addWidget(
            self.media_card,
            1,
            0,
        )
        status_grid.addWidget(
            self.export_card,
            1,
            1,
        )

        production_layout.addWidget(
            production_title
        )
        production_layout.addLayout(status_grid)

        health_section = QFrame()
        health_section.setObjectName(
            "dashboardSection"
        )
        health_section.setMinimumWidth(300)

        health_layout = QVBoxLayout(health_section)
        health_layout.setContentsMargins(
            22,
            18,
            22,
            20,
        )
        health_layout.setSpacing(13)

        health_title = QLabel("Production Health")
        health_title.setObjectName(
            "dashboardSectionTitle"
        )

        self.health_percentage_label = QLabel("0%")
        self.health_percentage_label.setObjectName(
            "healthPercentage"
        )
        self.health_percentage_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.health_message_label = QLabel(
            "Open a project to begin"
        )
        self.health_message_label.setObjectName(
            "healthMessage"
        )
        self.health_message_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.health_message_label.setWordWrap(True)

        self.health_progress = QProgressBar()
        self.health_progress.setRange(0, 100)
        self.health_progress.setValue(0)
        self.health_progress.setTextVisible(False)
        self.health_progress.setObjectName(
            "healthProgress"
        )

        self.next_step_title = QLabel("NEXT STEP")
        self.next_step_title.setObjectName(
            "smallSectionLabel"
        )

        self.next_step_label = QLabel(
            "Create or open a project"
        )
        self.next_step_label.setObjectName(
            "nextStepLabel"
        )
        self.next_step_label.setWordWrap(True)

        health_layout.addWidget(health_title)
        health_layout.addStretch()
        health_layout.addWidget(
            self.health_percentage_label
        )
        health_layout.addWidget(
            self.health_message_label
        )
        health_layout.addWidget(
            self.health_progress
        )
        health_layout.addSpacing(8)
        health_layout.addWidget(
            self.next_step_title
        )
        health_layout.addWidget(
            self.next_step_label
        )
        health_layout.addStretch()

        dashboard_grid.addWidget(
            production_section,
            0,
            0,
        )
        dashboard_grid.addWidget(
            health_section,
            0,
            1,
        )
        dashboard_grid.setColumnStretch(0, 3)
        dashboard_grid.setColumnStretch(1, 1)

        main_layout.addLayout(dashboard_grid)

        actions_section = QFrame()
        actions_section.setObjectName(
            "dashboardSection"
        )

        actions_layout = QVBoxLayout(actions_section)
        actions_layout.setContentsMargins(
            20,
            18,
            20,
            20,
        )
        actions_layout.setSpacing(14)

        actions_title = QLabel("Quick Actions")
        actions_title.setObjectName(
            "dashboardSectionTitle"
        )

        action_grid = QGridLayout()
        action_grid.setSpacing(12)

        self.open_project_button = QuickActionButton(
            "📂",
            "Project Folder",
            "Open the main project directory",
        )
        self.open_scripts_button = QuickActionButton(
            "📄",
            "Scripts Folder",
            "View imported and saved scripts",
        )
        self.open_images_button = QuickActionButton(
            "🖼",
            "Images Folder",
            "Browse project images",
        )
        self.open_narration_button = QuickActionButton(
            "🎙",
            "Narration Folder",
            "View narration and audio files",
        )
        self.open_exports_button = QuickActionButton(
            "📤",
            "Exports Folder",
            "Open completed video exports",
        )

        self.open_project_button.clicked.connect(
            self._open_project_folder
        )
        self.open_scripts_button.clicked.connect(
            self._open_scripts_folder
        )
        self.open_images_button.clicked.connect(
            self._open_images_folder
        )
        self.open_narration_button.clicked.connect(
            self._open_narration_folder
        )
        self.open_exports_button.clicked.connect(
            self._open_exports_folder
        )

        action_grid.addWidget(
            self.open_project_button,
            0,
            0,
        )
        action_grid.addWidget(
            self.open_scripts_button,
            0,
            1,
        )
        action_grid.addWidget(
            self.open_images_button,
            0,
            2,
        )
        action_grid.addWidget(
            self.open_narration_button,
            1,
            0,
        )
        action_grid.addWidget(
            self.open_exports_button,
            1,
            1,
        )

        actions_layout.addWidget(actions_title)
        actions_layout.addLayout(action_grid)

        main_layout.addWidget(actions_section)

        self.empty_state_label = QLabel(
            "Create or open a project to activate "
            "your production dashboard."
        )
        self.empty_state_label.setObjectName(
            "dashboardEmptyState"
        )
        self.empty_state_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            self.empty_state_label
        )
        main_layout.addStretch()

        scroll_area.setWidget(content)
        page_layout.addWidget(scroll_area)

    def set_project(
        self,
        project_name: str,
        project_location: str,
        project_folder: str,
        status: dict[str, object] | None = None,
    ) -> None:
        self.project_folder = project_folder

        self.project_name_label.setText(project_name)
        self.project_location_label.setText(
            project_location
        )
        self.project_folder_label.setText(
            project_folder
        )

        self.project_status_label.setText(
            "ACTIVE PROJECT"
        )
        self.empty_state_label.hide()

        self._set_action_buttons_enabled(True)

        if status is None:
            self._reset_dashboard_status()
            return

        script_files = status.get(
            "script_files",
            [],
        )
        narration_files = status.get(
            "narration_files",
            [],
        )

        image_count = self._safe_integer(
            status.get("image_count", 0)
        )
        video_count = self._safe_integer(
            status.get("video_count", 0)
        )
        export_count = self._safe_integer(
            status.get("export_count", 0)
        )

        script_count = (
            len(script_files)
            if isinstance(script_files, list)
            else 0
        )
        narration_count = (
            len(narration_files)
            if isinstance(narration_files, list)
            else 0
        )

        self.scripts_metric.set_content(
            str(script_count),
            (
                "Script ready"
                if script_count
                else "No script imported"
            ),
        )
        self.narration_metric.set_content(
            str(narration_count),
            (
                "Narration ready"
                if narration_count
                else "No narration imported"
            ),
        )
        self.images_metric.set_content(
            f"{image_count:,}",
            (
                "Images available"
                if image_count
                else "No images imported"
            ),
        )
        self.videos_metric.set_content(
            f"{video_count:,}",
            (
                "Video clips available"
                if video_count
                else "No videos imported"
            ),
        )
        self.exports_metric.set_content(
            f"{export_count:,}",
            (
                "Completed export available"
                if export_count
                else "No completed exports"
            ),
        )

        if script_count:
            script_names = [
                Path(file).name
                for file in script_files
            ]

            self.script_card.set_status(
                "Ready",
                "Imported: "
                + ", ".join(script_names[:3]),
                "complete",
            )
        else:
            self.script_card.set_status(
                "Missing",
                "Import or create a script",
                "missing",
            )

        if narration_count:
            narration_names = [
                Path(file).name
                for file in narration_files
            ]

            self.narration_card.set_status(
                "Ready",
                "Imported: "
                + ", ".join(narration_names[:3]),
                "complete",
            )
        else:
            self.narration_card.set_status(
                "Needed",
                "Import narration audio",
                "attention",
            )

        total_media = image_count + video_count

        if total_media:
            self.media_card.set_status(
                "In Progress",
                (
                    f"{image_count:,} images and "
                    f"{video_count:,} video clips"
                ),
                "complete",
            )
        else:
            self.media_card.set_status(
                "Missing",
                "Import images or video clips",
                "missing",
            )

        if export_count:
            self.export_card.set_status(
                "Complete",
                f"{export_count} exported video(s)",
                "complete",
            )
        else:
            self.export_card.set_status(
                "Not Started",
                "No finished export",
                "inactive",
            )

        completed_stages = sum(
            (
                script_count > 0,
                narration_count > 0,
                total_media > 0,
                export_count > 0,
            )
        )

        health = round(
            completed_stages / 4 * 100
        )

        self._set_health(
            health=health,
            script_ready=script_count > 0,
            narration_ready=narration_count > 0,
            media_ready=total_media > 0,
            export_ready=export_count > 0,
        )

    def clear_project(self) -> None:
        self.project_folder = None

        self.project_name_label.setText(
            "No project open"
        )
        self.project_location_label.setText("—")
        self.project_folder_label.setText("—")
        self.project_status_label.setText(
            "NO PROJECT OPEN"
        )

        self._reset_dashboard_status()
        self._set_action_buttons_enabled(False)
        self.empty_state_label.show()

    def _reset_dashboard_status(self) -> None:
        self.scripts_metric.set_content(
            "0",
            "No script imported",
        )
        self.narration_metric.set_content(
            "0",
            "No narration imported",
        )
        self.images_metric.set_content(
            "0",
            "No images imported",
        )
        self.videos_metric.set_content(
            "0",
            "No videos imported",
        )
        self.exports_metric.set_content(
            "0",
            "No completed exports",
        )

        self.script_card.set_status(
            "Not Started",
            "No script found",
            "inactive",
        )
        self.narration_card.set_status(
            "Not Started",
            "No narration found",
            "inactive",
        )
        self.media_card.set_status(
            "Not Started",
            "No media found",
            "inactive",
        )
        self.export_card.set_status(
            "Not Started",
            "No export found",
            "inactive",
        )

        self.health_percentage_label.setText("0%")
        self.health_message_label.setText(
            "Open a project to begin"
        )
        self.health_progress.setValue(0)
        self.next_step_label.setText(
            "Create or open a project"
        )

    def _set_health(
        self,
        health: int,
        script_ready: bool,
        narration_ready: bool,
        media_ready: bool,
        export_ready: bool,
    ) -> None:
        self.health_percentage_label.setText(
            f"{health}%"
        )
        self.health_progress.setValue(health)

        if export_ready:
            message = "Production complete"
            next_step = (
                "Review or open the exported video"
            )
        elif not script_ready:
            message = "Needs attention"
            next_step = (
                "Import or create the project script"
            )
        elif not narration_ready:
            message = "Production underway"
            next_step = "Import narration audio"
        elif not media_ready:
            message = "Production underway"
            next_step = (
                "Import images and video clips"
            )
        else:
            message = "Ready for assembly"
            next_step = (
                "Build the timeline and export"
            )

        self.health_message_label.setText(message)
        self.next_step_label.setText(next_step)

    def _set_action_buttons_enabled(
        self,
        enabled: bool,
    ) -> None:
        buttons = (
            self.open_project_button,
            self.open_scripts_button,
            self.open_images_button,
            self.open_narration_button,
            self.open_exports_button,
        )

        for button in buttons:
            button.setEnabled(enabled)

    def _open_project_folder(self) -> None:
        self._open_folder_action(
            SystemService.open_project_folder
        )

    def _open_scripts_folder(self) -> None:
        self._open_folder_action(
            SystemService.open_scripts_folder
        )

    def _open_images_folder(self) -> None:
        self._open_folder_action(
            SystemService.open_images_folder
        )

    def _open_narration_folder(self) -> None:
        self._open_folder_action(
            SystemService.open_narration_folder
        )

    def _open_exports_folder(self) -> None:
        self._open_folder_action(
            SystemService.open_exports_folder
        )

    def _open_folder_action(
        self,
        action,
    ) -> None:
        if not self.project_folder:
            return

        try:
            action(self.project_folder)
        except OSError as error:
            QMessageBox.critical(
                self,
                "Could Not Open Folder",
                str(error),
            )

    @staticmethod
    def _safe_integer(value: object) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0