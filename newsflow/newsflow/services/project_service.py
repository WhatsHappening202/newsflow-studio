import hashlib
import json
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from newsflow.models.project import Project


class ProjectService:
    IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}
    VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}
    SCRIPT_EXTENSIONS = {".txt", ".docx", ".pdf", ".md"}
    NARRATION_EXTENSIONS = {".mp3", ".wav", ".m4a", ".aac"}
    EXPORT_EXTENSIONS = {".mp4", ".mov", ".mkv"}

    @staticmethod
    def get_project_path(project: Project) -> Path:
        return Path(project.location) / project.name

    @staticmethod
    def create_project(project: Project) -> None:
        project_path = ProjectService.get_project_path(project)
        ProjectService.ensure_project_structure(project)

        with open(
            project_path / "project.json",
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(asdict(project), file, indent=4)

    @staticmethod
    def ensure_project_structure(project: Project) -> None:
        project_path = ProjectService.get_project_path(project)

        folders = (
            project_path,
            project_path / "scripts",
            project_path / "narration",
            project_path / "media",
            project_path / "media" / "images",
            project_path / "media" / "videos",
            project_path / "exports",
        )

        for folder in folders:
            folder.mkdir(parents=True, exist_ok=True)

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

        project = Project(**project_data)
        ProjectService.ensure_project_structure(project)
        return project

    @staticmethod
    def get_project_status(project: Project) -> dict[str, object]:
        ProjectService.ensure_project_structure(project)
        project_path = ProjectService.get_project_path(project)

        script_files = ProjectService._get_files(
            project_path / "scripts",
            ProjectService.SCRIPT_EXTENSIONS,
        )

        narration_files = ProjectService._get_files(
            project_path / "narration",
            ProjectService.NARRATION_EXTENSIONS,
        )

        image_files = ProjectService._get_files(
            project_path / "media" / "images",
            ProjectService.IMAGE_EXTENSIONS,
        )

        video_files = ProjectService._get_files(
            project_path / "media" / "videos",
            ProjectService.VIDEO_EXTENSIONS,
        )

        export_files = ProjectService._get_files(
            project_path / "exports",
            ProjectService.EXPORT_EXTENSIONS,
        )

        return {
            "project_path": str(project_path),
            "script_files": script_files,
            "narration_files": narration_files,
            "image_files": image_files,
            "video_files": video_files,
            "export_files": export_files,
            "image_count": len(image_files),
            "video_count": len(video_files),
            "export_count": len(export_files),
        }

    @staticmethod
    def import_media(
        project: Project,
        source_files: Iterable[str],
        media_type: str,
    ) -> dict[str, object]:
        ProjectService.ensure_project_structure(project)

        if media_type == "images":
            allowed_extensions = ProjectService.IMAGE_EXTENSIONS
        elif media_type == "videos":
            allowed_extensions = ProjectService.VIDEO_EXTENSIONS
        else:
            raise ValueError("media_type must be either 'images' or 'videos'.")

        destination_folder = (
            ProjectService.get_project_path(project)
            / "media"
            / media_type
        )

        existing_hashes = {
            ProjectService._calculate_file_hash(file)
            for file in ProjectService._get_files(
                destination_folder,
                allowed_extensions,
            )
        }

        imported: list[Path] = []
        skipped: list[Path] = []
        errors: list[str] = []

        for source_value in source_files:
            source = Path(source_value)

            try:
                if not source.exists() or not source.is_file():
                    errors.append(f"File not found: {source}")
                    continue

                if source.suffix.lower() not in allowed_extensions:
                    errors.append(f"Unsupported file type: {source.name}")
                    continue

                source_hash = ProjectService._calculate_file_hash(source)

                if source_hash in existing_hashes:
                    skipped.append(source)
                    continue

                destination = ProjectService._unique_destination(
                    destination_folder,
                    source.name,
                )

                shutil.copy2(source, destination)
                imported.append(destination)
                existing_hashes.add(source_hash)

            except OSError as error:
                errors.append(f"{source.name}: {error}")

        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
        }

    @staticmethod
    def _unique_destination(
        folder: Path,
        filename: str,
    ) -> Path:
        original = Path(filename)
        destination = folder / original.name

        if not destination.exists():
            return destination

        counter = 2

        while True:
            candidate = folder / (
                f"{original.stem}_{counter}{original.suffix}"
            )

            if not candidate.exists():
                return candidate

            counter += 1

    @staticmethod
    def _calculate_file_hash(file_path: Path) -> str:
        digest = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)

        return digest.hexdigest()

    @staticmethod
    def _get_files(
        folder: Path,
        extensions: set[str],
    ) -> list[Path]:
        if not folder.exists():
            return []

        return sorted(
            (
                file
                for file in folder.iterdir()
                if file.is_file()
                and file.suffix.lower() in extensions
            ),
            key=lambda file: file.name.lower(),
        )
