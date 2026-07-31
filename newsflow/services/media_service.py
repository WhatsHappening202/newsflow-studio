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
    def list_images(
        project: Project,
    ) -> list[Path]:
        return MediaService._list_files(
            MediaService.get_images_folder(project),
            MediaService.IMAGE_EXTENSIONS,
        )

    @staticmethod
    def list_videos(
        project: Project,
    ) -> list[Path]:
        return MediaService._list_files(
            MediaService.get_videos_folder(project),
            MediaService.VIDEO_EXTENSIONS,
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

            if not source.exists() or not source.is_file():
                continue

            target = MediaService._unique_destination(
                destination / source.name
            )

            shutil.copy2(
                source,
                target,
            )

            copied += 1

        return copied

    @staticmethod
    def _list_files(
        folder: Path,
        extensions: set[str],
    ) -> list[Path]:
        if not folder.exists():
            return []

        return sorted(
            (
                file
                for file in folder.iterdir()
                if (
                    file.is_file()
                    and file.suffix.lower() in extensions
                )
            ),
            key=lambda file: file.name.lower(),
        )

    @staticmethod
    def _unique_destination(
        destination: Path,
    ) -> Path:
        if not destination.exists():
            return destination

        counter = 2

        while True:
            candidate = destination.with_name(
                f"{destination.stem}_{counter}"
                f"{destination.suffix}"
            )

            if not candidate.exists():
                return candidate

            counter += 1