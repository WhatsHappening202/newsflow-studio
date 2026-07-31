import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


class ScriptService:
    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".markdown",
    }

    SCRIPT_FOLDER_NAMES = (
        "script",
        "scripts",
    )

    CURRENT_SCRIPT_FILENAME = "current_script.txt"
    METADATA_FILENAME = "script_metadata.json"

    @classmethod
    def import_script(
        cls,
        source_path: str | Path,
        project_path: str | Path,
    ) -> tuple[str, Path]:
        source = Path(source_path)
        project_root = Path(project_path)

        if not source.exists() or not source.is_file():
            raise FileNotFoundError(
                f"Script file does not exist:\n{source}"
            )

        if source.suffix.lower() not in cls.SUPPORTED_EXTENSIONS:
            raise ValueError(
                "Unsupported script format. "
                "Please select a TXT or Markdown file."
            )

        text = cls.read_text_file(source)
        script_folder = cls.get_script_folder(project_root)

        originals_folder = script_folder / "originals"
        originals_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        copied_source = cls._unique_destination(
            originals_folder / source.name
        )

        shutil.copy2(source, copied_source)

        current_script_path = (
            script_folder
            / cls.CURRENT_SCRIPT_FILENAME
        )

        current_script_path.write_text(
            text,
            encoding="utf-8",
        )

        cls._write_metadata(
            script_folder=script_folder,
            original_filename=source.name,
            imported_copy=copied_source.name,
        )

        return text, current_script_path

    @classmethod
    def save_script(
        cls,
        text: str,
        project_path: str | Path,
    ) -> Path:
        project_root = Path(project_path)
        script_folder = cls.get_script_folder(
            project_root
        )

        script_path = (
            script_folder
            / cls.CURRENT_SCRIPT_FILENAME
        )

        script_path.write_text(
            text,
            encoding="utf-8",
        )

        cls._update_saved_time(script_folder)

        return script_path

    @classmethod
    def load_script(
        cls,
        project_path: str | Path,
    ) -> tuple[str, Path | None]:
        project_root = Path(project_path)
        script_folder = cls.get_script_folder(
            project_root
        )

        current_script_path = (
            script_folder
            / cls.CURRENT_SCRIPT_FILENAME
        )

        if current_script_path.exists():
            return (
                cls.read_text_file(
                    current_script_path
                ),
                current_script_path,
            )

        candidates = sorted(
            path
            for path in script_folder.iterdir()
            if (
                path.is_file()
                and path.suffix.lower()
                in cls.SUPPORTED_EXTENSIONS
            )
        )

        if not candidates:
            return "", None

        first_script = candidates[0]

        return (
            cls.read_text_file(first_script),
            first_script,
        )

    @classmethod
    def get_script_folder(
        cls,
        project_path: str | Path,
    ) -> Path:
        project_root = Path(project_path)

        for folder_name in cls.SCRIPT_FOLDER_NAMES:
            candidate = project_root / folder_name

            if candidate.exists():
                candidate.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                return candidate

        script_folder = (
            project_root
            / cls.SCRIPT_FOLDER_NAMES[0]
        )

        script_folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        return script_folder

    @staticmethod
    def read_text_file(
        file_path: str | Path,
    ) -> str:
        path = Path(file_path)

        encodings = (
            "utf-8-sig",
            "utf-8",
            "cp1252",
        )

        for encoding in encodings:
            try:
                return path.read_text(
                    encoding=encoding
                )
            except UnicodeDecodeError:
                continue

        raise ValueError(
            "NewsFlow Studio could not determine "
            "the script file's text encoding."
        )

    @classmethod
    def _write_metadata(
        cls,
        script_folder: Path,
        original_filename: str,
        imported_copy: str,
    ) -> None:
        now = datetime.now().isoformat(
            timespec="seconds"
        )

        metadata: dict[str, Any] = {
            "original_filename": original_filename,
            "imported_copy": imported_copy,
            "imported_at": now,
            "last_saved_at": now,
        }

        metadata_path = (
            script_folder
            / cls.METADATA_FILENAME
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
            ),
            encoding="utf-8",
        )

    @classmethod
    def _update_saved_time(
        cls,
        script_folder: Path,
    ) -> None:
        metadata_path = (
            script_folder
            / cls.METADATA_FILENAME
        )

        metadata: dict[str, Any] = {}

        if metadata_path.exists():
            try:
                metadata = json.loads(
                    metadata_path.read_text(
                        encoding="utf-8"
                    )
                )
            except (
                json.JSONDecodeError,
                OSError,
            ):
                metadata = {}

        metadata["last_saved_at"] = (
            datetime.now().isoformat(
                timespec="seconds"
            )
        )

        metadata_path.write_text(
            json.dumps(
                metadata,
                indent=2,
            ),
            encoding="utf-8",
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