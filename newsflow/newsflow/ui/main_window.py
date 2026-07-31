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

from newsflow.models.project import Project
from newsflow.services.project_service import ProjectService
from newsflow.ui.dialogs.new_project_dialog import NewProjectDialog
from newsflow.ui.pages.dashboard_page import DashboardPage
from newsflow.ui.pages.media_library_page import MediaLibraryPage
from newsflow.ui.pages.projects_page import ProjectsPage
from newsflow.ui.widgets.navigation_panel import NavigationPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("NewsFlow Studio")
        self.resize(1200, 800)
        self.setMinimumSize(980, 650)

        self.current_project: Project | None = None

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

        self.refresh_action = QAction("Refresh Project", self)
        self.refresh_action.setShortcut("F5")
        self.refresh_action.triggered.connect(
            self._refresh_current_project
        )

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
        toolbar.setObjectName("mainToolbar")

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
        self.navigation.addItem("Media Library")

        self.page_stack = QStackedWidget()
        self.dashboard = DashboardPage()
        self.projects_page = ProjectsPage()
        self.media_library_page = MediaLibraryPage()

        self.page_stack.addWidget(self.dashboard)
        self.page_stack.addWidget(self.projects_page)
        self.page_stack.addWidget(self.media_library_page)

        self.navigation.currentRowChanged.connect(self._change_page)
        self.media_library_page.media_changed.connect(
            self._refresh_current_project
        )

        layout.addWidget(self.navigation)
        layout.addWidget(self.page_stack, 1)

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

        if dialog.exec() == QDialog.DialogCode.Accepted:
            project = dialog.created_project

            if project is not None:
                self._set_current_project(project)
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
        except (OSError, ValueError, TypeError) as error:
            QMessageBox.critical(
                self,
                "Could Not Open Project",
                str(error),
            )
            return

        self._set_current_project(project)

        self.statusBar().showMessage(
            f'Project "{project.name}" opened successfully',
            5000,
        )

    def _set_current_project(self, project: Project) -> None:
        self.current_project = project
        ProjectService.ensure_project_structure(project)

        self.media_library_page.set_project(project)
        self._refresh_current_project()

        self.setWindowTitle(
            f"NewsFlow Studio — {project.name}"
        )

    def _refresh_current_project(self) -> None:
        if self.current_project is None:
            self.statusBar().showMessage(
                "No project is currently open",
                3000,
            )
            return

        try:
            status = ProjectService.get_project_status(
                self.current_project
            )

            self.dashboard.set_project(
                self.current_project.name,
                str(status["project_path"]),
                status,
            )

            self.media_library_page.refresh()

            self.statusBar().showMessage(
                "Project refreshed",
                3000,
            )
        except OSError as error:
            QMessageBox.critical(
                self,
                "Refresh Failed",
                str(error),
            )

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About NewsFlow Studio",
            "NewsFlow Studio\nVersion 0.4.0\n\n"
            "AI-assisted video production for documentary "
            "and news creators.",
        )


def apply_application_style(app: QApplication) -> None:
    app.setStyle("Fusion")

    app.setStyleSheet(
        """
        QMainWindow,
        QWidget {
            background-color: #17191d;
            color: #e9edf1;
            font-family: "Segoe UI";
            font-size: 10pt;
        }

        QMenuBar,
        QMenu,
        QToolBar,
        QStatusBar {
            background-color: #202329;
            color: #e9edf1;
        }

        QMenuBar::item:selected,
        QMenu::item:selected {
            background-color: #343943;
        }

        QToolBar {
            border-bottom: 1px solid #343943;
            spacing: 6px;
            padding: 5px;
        }

        QLabel#pageTitle {
            font-size: 25pt;
            font-weight: 700;
        }

        QLabel#pageSubtitle {
            color: #aeb6c2;
            font-size: 11pt;
        }

        QLabel#sectionTitle {
            font-size: 16pt;
            font-weight: 700;
            margin-top: 8px;
        }

        QLabel#fieldTitle,
        QLabel#cardTitle {
            font-weight: 700;
        }

        QLabel#cardValue {
            color: #cbd2dc;
        }

        QLabel#emptyState {
            color: #929aa6;
            font-size: 11pt;
            margin-top: 20px;
        }

        QFrame#panel,
        QFrame#statusCard {
            background-color: #22262c;
            border: 1px solid #343943;
            border-radius: 8px;
        }

        QPushButton {
            background-color: #2d6cdf;
            border: none;
            border-radius: 5px;
            color: white;
            font-weight: 600;
            padding: 8px 14px;
        }

        QPushButton:hover {
            background-color: #3b7af0;
        }

        QPushButton:pressed {
            background-color: #245bbd;
        }

        QPushButton:disabled {
            background-color: #3a3e46;
            color: #7f8792;
        }

        QListWidget,
        QTabWidget::pane {
            background-color: #1d2025;
            border: 1px solid #343943;
            border-radius: 6px;
        }

        QListWidget::item {
            border-radius: 5px;
            padding: 6px;
        }

        QListWidget::item:selected {
            background-color: #2d6cdf;
        }

        QTabBar::tab {
            background-color: #252930;
            border: 1px solid #343943;
            padding: 8px 18px;
        }

        QTabBar::tab:selected {
            background-color: #2d6cdf;
        }

        QScrollBar:vertical {
            background: #1d2025;
            width: 12px;
        }

        QScrollBar::handle:vertical {
            background: #4a505b;
            border-radius: 6px;
            min-height: 24px;
        }
        """
    )
