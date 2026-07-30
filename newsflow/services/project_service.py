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

        media_path = project_path / "media"
        media_path.mkdir(exist_ok=True)

        (media_path / "images").mkdir(exist_ok=True)
        (media_path / "videos").mkdir(exist_ok=True)

        (project_path / "exports").mkdir(exist_ok=True)

        with open(
            project_path / "project.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(asdict(project), file, indent=4)

    @staticmethod
    def load_project(project_folder: str) -> Project:
        project_path = Path(project_folder)
        project_file = project_path / "project.json"

        if not project_file.exists():
            raise FileNotFoundError(
                f"No project.json file was found in:\n{project_path}"
            )

        with open(project_file, "r", encoding="utf-8") as file:
            project_data = json.load(file)

        return Project(**project_data)

    @staticmethod
    def get_project_status(project: Project) -> dict[str, object]:
        project_path = Path(project.location) / project.name

        scripts_path = project_path / "scripts"
        narration_path = project_path / "narration"
        images_path = project_path / "media" / "images"
        videos_path = project_path / "media" / "videos"
        exports_path = project_path / "exports"

        script_files = ProjectService._get_files(
            scripts_path,
            {".txt", ".docx", ".pdf", ".md"},
        )

        narration_files = ProjectService._get_files(
            narration_path,
            {".mp3", ".wav", ".m4a", ".aac"},
        )

        image_files = ProjectService._get_files(
            images_path,
            {".jpg", ".jpeg", ".png", ".webp", ".bmp"},
        )

        video_files = ProjectService._get_files(
            videos_path,
            {".mp4", ".mov", ".avi", ".mkv", ".webm"},
        )

        export_files = ProjectService._get_files(
            exports_path,
            {".mp4", ".mov", ".mkv"},
        )

        return {
            "project_path": str(project_path),
            "script_files": script_files,
            "narration_files": narration_files,
            "image_count": len(image_files),
            "video_count": len(video_files),
            "export_count": len(export_files),
        }

    @staticmethod
    def _get_files(
        folder: Path,
        extensions: set[str],
    ) -> list[Path]:
        if not folder.exists():
            return []

        return [
            file
            for file in folder.iterdir()
            if file.is_file() and file.suffix.lower() in extensions
        ]