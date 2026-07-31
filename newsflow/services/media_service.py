import shutil
from pathlib import Path

from newsflow.models.project import Project


class MediaService:
    IMAGE_EXTENSIONS = {
        ".jpg",
        ".jpeg",
        ".png",
        ".bmp",
        ".webp",
        ".gif",
    }

    VIDEO_EXTENSIONS = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".m4v",
    }

    @staticmethod
    def get_images_folder(project: Project) -> Path:
        return (
            Path(project.location)
            / project.name
            / "media"
            / "images"
        )

    @staticmethod
    def get_videos_folder(project: Project) -> Path:
        return (
            Path(project.location)
            / project.name
            / "media"
            / "videos"
        )

    @staticmethod
    def import_images(
        project: Project,
        files: list[str],
    ) -> int:
        return MediaService._copy_files(
            files,
            MediaService.get_images_folder(project),
        )

    @staticmethod
    def import_videos(
        project: Project,
        files: list[str],
    ) -> int:
        return MediaService._copy_files(
            files,
            MediaService.get_videos_folder(project),
        )

    @staticmethod
    def _copy_files(
        files: list[str],
        destination: Path,
    ) -> int:

        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        copied = 0

        for file in files:

            source = Path(file)

            if not source.exists():
                continue

            target = destination / source.name

            if target.exists():
                continue

            shutil.copy2(
                source,
                target,
            )

            copied += 1

        return copied