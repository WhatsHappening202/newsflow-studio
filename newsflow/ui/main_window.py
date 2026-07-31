from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from newsflow.controllers.project_controller import ProjectController
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
        self.resize(1350, 850)
        self.setMinimumSize(1050, 700)

        self._create_actions()
        self._create_pages()
        self._create_controller()
        self._create_ui()
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

        self.addAction(self.new_project_action)
        self.addAction(self.open_project_action)
        self.addAction(self.refresh_action)
        self.addAction(self.exit_action)

    def _create_pages(self) -> None:
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

    def _create_ui(self) -> None:
        central_widget = QWidget()
        central_widget.setObjectName("applicationShell")

        outer_layout = QVBoxLayout(central_widget)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        self.header = self._create_header()
        outer_layout.addWidget(self.header)

        workspace_widget = QWidget()
        workspace_layout = QHBoxLayout(workspace_widget)
        workspace_layout.setContentsMargins(0, 0, 0, 0)
        workspace_layout.setSpacing(0)

        self.navigation = NavigationPanel()
        self.navigation.currentRowChanged.connect(
            self._change_page
        )

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("mainWorkspace")

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

        workspace_layout.addWidget(self.navigation)
        workspace_layout.addWidget(self.page_stack, 1)

        outer_layout.addWidget(workspace_widget, 1)

        self.setCentralWidget(central_widget)

    def _create_header(self) -> QFrame:
        header = QFrame()
        header.setObjectName("applicationHeader")
        header.setFixedHeight(82)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(24, 12, 24, 12)
        layout.setSpacing(12)

        brand_layout = QVBoxLayout()
        brand_layout.setSpacing(1)

        brand_label = QLabel("NEWSFLOW STUDIO")
        brand_label.setObjectName("brandTitle")
        brand_label.setStyleSheet(
            """
            font-size: 21px;
            font-weight: 800;
            letter-spacing: 1px;
            color: #F5F5F5;
            """
        )

        tagline_label = QLabel(
            "Professional Documentary Production"
        )
        tagline_label.setObjectName("brandTagline")
        tagline_label.setStyleSheet(
            """
            font-size: 11px;
            color: #B8B8C2;
            """
        )

        brand_layout.addWidget(brand_label)
        brand_layout.addWidget(tagline_label)

        self.current_project_label = QLabel(
            "No project open"
        )
        self.current_project_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.current_project_label.setMinimumWidth(230)
        self.current_project_label.setStyleSheet(
            """
            background-color: #23232B;
            border: 1px solid #3C3C46;
            border-radius: 9px;
            color: #B8B8C2;
            font-size: 13px;
            padding: 9px 14px;
            """
        )

        self.new_project_button = QPushButton(
            "＋ New Project"
        )
        self.new_project_button.setToolTip(
            "Create a new NewsFlow project (Ctrl+N)"
        )
        self.new_project_button.clicked.connect(
            self._new_project
        )

        self.open_project_button = QPushButton(
            "📂 Open Project"
        )
        self.open_project_button.setToolTip(
            "Open an existing NewsFlow project (Ctrl+O)"
        )
        self.open_project_button.clicked.connect(
            self._open_project
        )

        self.refresh_button = QPushButton(
            "↻ Refresh"
        )
        self.refresh_button.setToolTip(
            "Refresh the current project (F5)"
        )
        self.refresh_button.clicked.connect(
            self._refresh_project
        )

        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(
            self._show_about
        )

        layout.addLayout(brand_layout)
        layout.addStretch()
        layout.addWidget(self.current_project_label)
        layout.addSpacing(8)
        layout.addWidget(self.new_project_button)
        layout.addWidget(self.open_project_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.about_button)

        return header

    def _change_page(self, index: int) -> None:
        if 0 <= index < self.page_stack.count():
            self.page_stack.setCurrentIndex(index)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar()
        status_bar.setObjectName("mainStatusBar")
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

        self.current_project_label.setText(
            project.name
        )
        self.current_project_label.setStyleSheet(
            """
            background-color: #25152F;
            border: 1px solid #B026FF;
            border-radius: 9px;
            color: #F5F5F5;
            font-size: 13px;
            font-weight: 700;
            padding: 9px 14px;
            """
        )

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
                "Version 0.7.0\n\n"
                "Professional Documentary Production\n\n"
                "AI-assisted video production for "
                "documentary and news creators."
            ),
        )


def apply_application_style(
    app: QApplication,
) -> None:
    app.setStyle("Fusion")