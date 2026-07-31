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