from pathlib import Path

from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from newsflow.models.project import Project
from newsflow.services.project_service import ProjectService


class NewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.created_project = None

        self.setWindowTitle("New Project")
        self.setMinimumWidth(550)

        main_layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.name_edit = QLineEdit()
        self.description_edit = QLineEdit()

        self.location_edit = QLineEdit()
        self.browse_button = QPushButton("Browse...")

        location_layout = QHBoxLayout()
        location_layout.addWidget(self.location_edit)
        location_layout.addWidget(self.browse_button)

        form_layout.addRow("Project Name:", self.name_edit)
        form_layout.addRow("Description:", self.description_edit)
        form_layout.addRow("Location:", location_layout)
        from newsflow.services.recent_projects_service import RecentProjectsService
        main_layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create Project")
        self.cancel_button = QPushButton("Cancel")

        button_layout.addStretch()
        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        self.browse_button.clicked.connect(self._browse_for_location)
        self.create_button.clicked.connect(self._create_project)
        self.cancel_button.clicked.connect(self.reject)

    def _browse_for_location(self) -> None:
        selected_folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Project Location",
            str(Path.home()),
        )

        if selected_folder:
            self.location_edit.setText(selected_folder)

    def _create_project(self) -> None:
        name = self.name_edit.text().strip()
        description = self.description_edit.text().strip()
        location = self.location_edit.text().strip()

        if not name:
            QMessageBox.warning(
                self,
                "Missing Project Name",
                "Please enter a project name.",
            )
            return

        if not location:
            QMessageBox.warning(
                self,
                "Missing Location",
                "Please choose a location for the project.",
            )
            return

        project = Project(
            name=name,
            description=description,
            location=location,
        )

        try:
            ProjectService.create_project(project)
            RecentProjectsService.add_project(project)
        except OSError as error:
            QMessageBox.critical(
                self,
                "Project Creation Failed",
                f"NewsFlow Studio could not create the project.\n\n{error}",
            )
            return

        self.created_project = project

        project_path = Path(project.location) / project.name

        QMessageBox.information(
        self,
        "Project Created",
        (
            f'The project "{project.name}" was created successfully.\n\n'
            f"Saved at:\n{project_path}"
        ),
)