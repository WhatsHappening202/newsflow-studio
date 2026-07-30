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

from newsflow.services.project_service import ProjectService
from newsflow.ui.dialogs.new_project_dialog import NewProjectDialog
from newsflow.ui.pages.dashboard_page import DashboardPage
from newsflow.ui.pages.projects_page import ProjectsPage
from newsflow.ui.widgets.navigation_panel import NavigationPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NewsFlow Studio")
        self.resize(1200, 800)

        self.current_project = None

        self._create_actions()
        self._create_menu_bar()
        self._create_toolbar()
        self._create_ui()
        self._create_status_bar()

    def _create_actions(self) -> None:
        self.new_project_action = QAction("New Project", self)
        self.new_project_action.setShortcut("Ctrl+N")
        self.new_project_action.triggered.connect(self._new_project)

        self.open_project_action = QAction("Open Project", self)
        self.open_project_action.setShortcut("Ctrl+O")
        self.open_project_action.triggered.connect(self._open_project)

        self.exit_action = QAction("Exit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)

        self.about_action = QAction("About NewsFlow Studio", self)
        self.about_action.triggered.connect(self._show_about)

    def _create_menu_bar(self) -> None:
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_project_action)
        file_menu.addAction(self.open_project_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        project_menu = self.menuBar().addMenu("&Project")
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

        self.addToolBar(toolbar)

    def _create_ui(self) -> None:
        central_widget = QWidget()
        layout = QHBoxLayout()

        self.navigation = NavigationPanel()

        self.page_stack = QStackedWidget()
        self.dashboard = DashboardPage()
        self.projects_page = ProjectsPage()

        self.page_stack.addWidget(self.dashboard)
        self.page_stack.addWidget(self.projects_page)

        self.navigation.currentRowChanged.connect(self._change_page)

        layout.addWidget(self.navigation)
        layout.addWidget(self.page_stack, 1)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _change_page(self, index: int) -> None:
        if 0 <= index < self.page_stack.count():
            self.page_stack.setCurrentIndex(index)

    def _create_status_bar(self) -> None:
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")
        self.setStatusBar(status_bar)

    def _new_project(self) -> None:
        dialog = NewProjectDialog(self)

        if dialog.exec() == QDialog.Accepted:
            project = dialog.created_project

            if project is not None:
                self.current_project = project
                self.setWindowTitle(f"NewsFlow Studio — {project.name}")
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
            project = ProjectService.load_project(project_folder)
        except Exception as error:
            QMessageBox.critical(
                self,
                "Could Not Open Project",
                str(error),
            )
            return

        self.current_project = project
        self.setWindowTitle(f"NewsFlow Studio — {project.name}")
        self.statusBar().showMessage(
            f'Project "{project.name}" opened successfully',
            5000,
        )

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NewsFlow Studio",
            "NewsFlow Studio\nVersion 0.2.0\n\n"
            "AI-assisted video production for documentary and news creators.",
        )


def apply_application_style(app: QApplication) -> None:
    app.setStyle("Fusion")