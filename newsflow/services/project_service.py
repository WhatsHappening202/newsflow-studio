import json
from dataclasses import asdict
from pathlib import Path

from newsflow.models.project import Project


class ProjectService:
    @staticmethod
    def create_project(project: Project) -> None:
        project_path = Path(project.location) / project.name

        project_path.mkdir(parents=True, exist_ok=True)

        (project_path / "scripts").mkdir(exist_ok=True)
        (project_path / "narration").mkdir(exist_ok=True)

        media = project_path / "media"
        media.mkdir(exist_ok=True)

        (media / "images").mkdir(exist_ok=True)
        (media / "videos").mkdir(exist_ok=True)

        (project_path / "exports").mkdir(exist_ok=True)

        with open(project_path / "project.json", "w") as file:
            json.dump(asdict(project), file, indent=4)