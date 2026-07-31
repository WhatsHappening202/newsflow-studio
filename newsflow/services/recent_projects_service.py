import json
from pathlib import Path

from newsflow.models.project import Project


class RecentProjectsService:
    APP_FOLDER = Path.home() / ".newsflow"
    RECENTS_FILE = APP_FOLDER / "recent_projects.json"

    @classmethod
    def _ensure_file(cls):
        cls.APP_FOLDER.mkdir(exist_ok=True)

        if not cls.RECENTS_FILE.exists():
            cls.RECENTS_FILE.write_text(
                "[]",
                encoding="utf-8",
            )

    @classmethod
    def get_recent_projects(cls):
        cls._ensure_file()

        with open(cls.RECENTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    @classmethod
    def add_project(cls, project: Project):
        cls._ensure_file()

        project_path = str(Path(project.location) / project.name)

        projects = cls.get_recent_projects()

        projects = [
            p
            for p in projects
            if p["path"] != project_path
        ]

        projects.insert(
            0,
            {
                "name": project.name,
                "path": project_path,
            },
        )

        projects = projects[:20]

        with open(
            cls.RECENTS_FILE,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(projects, file, indent=4)