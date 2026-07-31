import os
import subprocess
from pathlib import Path


class SystemService:
    @staticmethod
    def open_folder(path: str | Path) -> None:
        folder = Path(path)

        if not folder.exists():
            raise FileNotFoundError(
                f"Folder not found:\n{folder}"
            )

        if os.name == "nt":
            os.startfile(folder)
        else:
            subprocess.run(
                ["xdg-open", str(folder)],
                check=False,
            )

    @staticmethod
    def open_project_folder(project_path: str | Path) -> None:
        SystemService.open_folder(project_path)

    @staticmethod
    def open_scripts_folder(project_path: str | Path) -> None:
        SystemService.open_folder(
            Path(project_path) / "scripts"
        )

    @staticmethod
    def open_images_folder(project_path: str | Path) -> None:
        SystemService.open_folder(
            Path(project_path)
            / "media"
            / "images"
        )

    @staticmethod
    def open_narration_folder(project_path: str | Path) -> None:
        SystemService.open_folder(
            Path(project_path)
            / "narration"
        )

    @staticmethod
    def open_exports_folder(project_path: str | Path) -> None:
        SystemService.open_folder(
            Path(project_path)
            / "exports"
        )