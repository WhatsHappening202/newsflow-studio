from pathlib import Path

from PySide6.QtCore import QObject, Signal

from newsflow.models.project import Project
from newsflow.models.storyboard import Storyboard
from newsflow.services.media_match_service import (
    MediaMatchService,
)
from newsflow.services.project_service import (
    ProjectService,
)
from newsflow.services.storyboard_service import (
    StoryboardService,
)
from newsflow.ui.pages.dashboard_page import (
    DashboardPage,
)
from newsflow.ui.pages.media_library_page import (
    MediaLibraryPage,
)
from newsflow.ui.pages.script_workspace import (
    ScriptWorkspace,
)
from newsflow.ui.pages.storyboard_page import (
    StoryboardPage,
)


class ProjectController(QObject):
    status_message = Signal(str, int)

    def __init__(
        self,
        dashboard: DashboardPage,
        script_page: ScriptWorkspace,
        images_page: MediaLibraryPage,
        storyboard_page: StoryboardPage,
    ) -> None:
        super().__init__()

        self.dashboard = dashboard
        self.script_page = script_page
        self.images_page = images_page
        self.storyboard_page = storyboard_page

        self.current_project: Project | None = None
        self.project_path: Path | None = None

    def set_project(
        self,
        project: Project,
    ) -> None:
        self.current_project = project
        self.project_path = (
            Path(project.location)
            / project.name
        )

        self.images_page.set_project(project)

        self.script_page.set_project(
            project,
            self.project_path,
        )

        self.refresh()

    def refresh(self) -> None:
        if (
            self.current_project is None
            or self.project_path is None
        ):
            self.status_message.emit(
                "No project is currently open",
                3000,
            )
            return

        status = ProjectService.get_project_status(
            self.current_project
        )

        self.dashboard.set_project(
            self.current_project.name,
            self.current_project.location,
            str(self.project_path),
            status,
        )

        self.script_page.refresh()
        self.images_page.refresh()
        self._refresh_storyboard()

        self.status_message.emit(
            "Project refreshed",
            3000,
        )

    def _refresh_storyboard(self) -> None:
        if self.current_project is None:
            return

        script_text = (
            self.script_page
            .script_editor
            .toPlainText()
        )

        if script_text.strip():
            storyboard = (
                StoryboardService.build_storyboard(
                    script_text
                )
            )
        else:
            storyboard = Storyboard(scenes=[])

        media_matches = (
            MediaMatchService.match_storyboard(
                storyboard=storyboard,
                project=self.current_project,
            )
        )

        coverage = (
            MediaMatchService.coverage_percentage(
                storyboard=storyboard,
                matches=media_matches,
            )
        )

        self.storyboard_page.load_storyboard(
            storyboard=storyboard,
            media_matches=media_matches,
            coverage_percentage=coverage,
        )