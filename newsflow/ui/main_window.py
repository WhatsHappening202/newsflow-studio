from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QStatusBar,
    QToolBar,
    QWidget,
)

from newsflow.controllers.project_controller import (
    ProjectController,
)
from newsflow.services.project_service import ProjectService
from newsflow.ui.dialogs.new_project_dialog import NewProjectDialog
from newsflow.ui.pages.dashboard_page import DashboardPage
from newsflow.ui.pages.media_library_page import MediaLibraryPage
from newsflow.ui.pages.projects_page import ProjectsPage
from newsflow.ui.pages.script_workspace import ScriptWorkspace
from newsflow.ui.pages.storyboard_page import StoryboardPage
from newsflow.ui.pages.workflow_page import WorkflowPage
from newsflow.ui.widgets.navigation_panel import NavigationPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NewsFlow Studio")
        self.resize(1200, 800)
        self.setMinimumSize(980, 650)

        self._create_actions()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_ui()
        self._create_controller()
        self._create_status_bar()

    def _create_actions(self) -> None:
        self.new_project_action = QAction(
            "New Project",
            self,
        )
        self.new_project_action.setShortcut("Ctrl+N")
        self.new_project_action.triggered.connect(
            self._new_project
        )

        self.open_project_action = QAction(
            "Open Project",
            self,
        )
        self.open_project_action.setShortcut("Ctrl+O")
        self.open_project_action.triggered.connect(
            self._open_project
        )

        self.refresh_action = QAction(
            "Refresh Project",
            self,
        )
        self.refresh_action.setShortcut("F5")
        self.refresh_action.triggered.connect(
            self._refresh_project
        )

        self.exit_action = QAction(
            "Exit",
            self,
        )
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(
            self.close
        )

        self.about_action = QAction(
            "About NewsFlow Studio",
            self,
        )
        self.about_action.triggered.connect(
            self._show_about
        )

    def _create_menu_bar(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        project_menu = self.menuBar().addMenu("&Project")
        project_menu.addAction(self.refresh_action)
        project_menu.addSeparator()
        project_menu.addAction("Project Settings")

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")

        tools_menu = self.menuBar().addMenu("&Tools")
        tools_menu.addAction("Preferences")

        help_menu = self.menuBar().addMenu("&Help")
        help_menu.addAction(self.about_action)

    def _create_toolbar(self) -> None:
        toolbar = QToolBar("Main Toolbar")
        toolbar.setMovable(False)

        toolbar.addAction(self.new_project_action)
        toolbar.addAction(self.open_project_action)
        toolbar.addSeparator()
        toolbar.addAction(self.refresh_action)

        self.addToolBar(toolbar)

    def _create_ui(self) -> None:
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.navigation = NavigationPanel()
        self.page_stack = QStackedWidget()

        self.dashboard = DashboardPage()
        self.projects_page = ProjectsPage()

        self.script_page = ScriptWorkspace()
        self.script_page.status_message.connect(
            self._show_status_message
        )

        self.narration_page = WorkflowPage(
            "Narration Workspace",
            "Import narration, review audio duration, and "
            "synchronize narration with the script.",
        )

        self.images_page = MediaLibraryPage()

        self.videos_page = WorkflowPage(
            "Video Library",
            "Import, preview, organize, and manage video clips "
            "for the current production.",
        )

        self.storyboard_page = StoryboardPage()

        self.timeline_page = WorkflowPage(
            "Timeline Builder",
            "Arrange narration, images, video clips, and "
            "transitions into the final production timeline.",
        )

        self.export_page = WorkflowPage(
            "Export",
            "Choose video settings and render the finished "
            "production.",
        )

        self.settings_page = WorkflowPage(
            "Settings",
            "Configure application preferences, project defaults, "
            "and channel templates.",
        )

        self.page_stack.addWidget(self.dashboard)
        self.page_stack.addWidget(self.projects_page)
        self.page_stack.addWidget(self.script_page)
        self.page_stack.addWidget(self.narration_page)
        self.page_stack.addWidget(self.images_page)
        self.page_stack.addWidget(self.videos_page)
        self.page_stack.addWidget(self.storyboard_page)
        self.page_stack.addWidget(self.timeline_page)
        self.page_stack.addWidget(self.export_page)
        self.page_stack.addWidget(self.settings_page)

        self.navigation.currentRowChanged.connect(
            self._change_page
        )

        layout.addWidget(self.navigation)
        layout.addWidget(self.page_stack, 1)

        self.setCentralWidget(central_widget)

    def _create_controller(self) -> None:
        self.project_controller = ProjectController(
            dashboard=self.dashboard,
            script_page=self.script_page,
            images_page=self.images_page,
            storyboard_page=self.storyboard_page,
        )

        self.project_controller.status_message.connect(
            self._show_status_message
        )

    def _change_page(self, index: int) -> None:
        if 0 <= index < self.page_stack.count():
            self.page_stack.setCurrentIndex(index)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def _new_project(self) -> None:
        dialog = NewProjectDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        project = dialog.created_project

        if project is None:
            return

        try:
            self._set_current_project(project)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Could Not Open New Project",
                str(error),
            )
            return

        self.statusBar().showMessage(
            f'Project "{project.name}" created successfully',
            5000,
        )

    def _open_project(self) -> None:
        project_folder = QFileDialog.getExistingDirectory(
            self,
            "Open NewsFlow Project",
        )

        if not project_folder:
            return

        try:
            project = ProjectService.load_project(
                project_folder
            )

            self._set_current_project(project)

        except Exception as error:
            QMessageBox.critical(
                self,
                "Could Not Open Project",
                str(error),
            )
            return

        self.statusBar().showMessage(
            f'Project "{project.name}" opened successfully',
            5000,
        )

    def _set_current_project(self, project) -> None:
        self.project_controller.set_project(project)

        self.setWindowTitle(
            f"NewsFlow Studio — {project.name}"
        )

    def _refresh_project(self) -> None:
        try:
            self.project_controller.refresh()
        except Exception as error:
            QMessageBox.critical(
                self,
                "Project Refresh Failed",
                str(error),
            )

    def _show_status_message(
        self,
        message: str,
        duration: int,
    ) -> None:
        self.statusBar().showMessage(
            message,
            duration,
        )

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NewsFlow Studio",
            (
                "NewsFlow Studio\n"
                "Version 0.6.0\n\n"
                "AI-assisted video production for "
                "documentary and news creators."
            ),
        )


def apply_application_style(
    app: QApplication,
) -> None:
    app.setStyle("Fusion")