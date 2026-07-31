from pathlib import Path

from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QAbstractItemView,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from newsflow.models.project import Project
from newsflow.services.project_service import ProjectService


class MediaLibraryPage(QWidget):
    media_changed = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.current_project: Project | None = None

        self._create_ui()
        self.clear_project()

    def _create_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(35, 30, 35, 30)
        main_layout.setSpacing(18)

        title = QLabel("Media Library")
        title.setObjectName("pageTitle")

        subtitle = QLabel(
            "Import and organize the images and video clips used "
            "in the current project."
        )
        subtitle.setObjectName("pageSubtitle")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        button_layout = QHBoxLayout()

        self.import_images_button = QPushButton("Import Images")
        self.import_images_button.clicked.connect(self._import_images)

        self.import_videos_button = QPushButton("Import Videos")
        self.import_videos_button.clicked.connect(self._import_videos)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh)

        button_layout.addWidget(self.import_images_button)
        button_layout.addWidget(self.import_videos_button)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_button)

        main_layout.addLayout(button_layout)

        self.tabs = QTabWidget()

        self.images_list = self._create_media_list()
        self.videos_list = self._create_media_list()

        self.tabs.addTab(self.images_list, "Images (0)")
        self.tabs.addTab(self.videos_list, "Videos (0)")

        main_layout.addWidget(self.tabs, 1)

        self.empty_state_label = QLabel(
            "Create or open a project before importing media."
        )
        self.empty_state_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.empty_state_label.setObjectName("emptyState")
        main_layout.addWidget(self.empty_state_label)

    def _create_media_list(self) -> QListWidget:
        media_list = QListWidget()
        media_list.setViewMode(QListWidget.ViewMode.IconMode)
        media_list.setResizeMode(QListWidget.ResizeMode.Adjust)
        media_list.setMovement(QListWidget.Movement.Static)
        media_list.setIconSize(QSize(160, 100))
        media_list.setGridSize(QSize(190, 145))
        media_list.setSpacing(10)
        media_list.setWordWrap(True)
        media_list.setSelectionMode(
            QAbstractItemView.SelectionMode.ExtendedSelection
        )
        return media_list

    def set_project(self, project: Project) -> None:
        self.current_project = project
        self.import_images_button.setEnabled(True)
        self.import_videos_button.setEnabled(True)
        self.refresh_button.setEnabled(True)
        self.tabs.setEnabled(True)
        self.empty_state_label.hide()
        self.refresh()

    def clear_project(self) -> None:
        self.current_project = None
        self.images_list.clear()
        self.videos_list.clear()
        self.tabs.setTabText(0, "Images (0)")
        self.tabs.setTabText(1, "Videos (0)")
        self.import_images_button.setEnabled(False)
        self.import_videos_button.setEnabled(False)
        self.refresh_button.setEnabled(False)
        self.tabs.setEnabled(False)
        self.empty_state_label.show()

    def refresh(self) -> None:
        if self.current_project is None:
            self.clear_project()
            return

        status = ProjectService.get_project_status(
            self.current_project
        )

        image_files = status.get("image_files", [])
        video_files = status.get("video_files", [])

        self._populate_images(
            image_files if isinstance(image_files, list) else []
        )
        self._populate_videos(
            video_files if isinstance(video_files, list) else []
        )

        self.tabs.setTabText(
            0,
            f"Images ({self.images_list.count()})",
        )
        self.tabs.setTabText(
            1,
            f"Videos ({self.videos_list.count()})",
        )

    def _populate_images(self, files: list[Path]) -> None:
        self.images_list.clear()

        for file_path in files:
            path = Path(file_path)
            pixmap = QPixmap(str(path))

            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    160,
                    100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            item = QListWidgetItem(QIcon(pixmap), path.name)
            item.setToolTip(str(path))
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            self.images_list.addItem(item)

    def _populate_videos(self, files: list[Path]) -> None:
        self.videos_list.clear()
        video_icon = self.style().standardIcon(
            self.style().StandardPixmap.SP_MediaPlay
        )

        for file_path in files:
            path = Path(file_path)
            item = QListWidgetItem(video_icon, path.name)
            item.setToolTip(str(path))
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            self.videos_list.addItem(item)

    def _import_images(self) -> None:
        if self.current_project is None:
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Images",
            "",
            (
                "Image Files "
                "(*.jpg *.jpeg *.png *.webp *.bmp *.gif)"
            ),
        )

        if files:
            self._import_files(files, "images")

    def _import_videos(self) -> None:
        if self.current_project is None:
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Videos",
            "",
            (
                "Video Files "
                "(*.mp4 *.mov *.avi *.mkv *.webm *.m4v)"
            ),
        )

        if files:
            self._import_files(files, "videos")

    def _import_files(
        self,
        files: list[str],
        media_type: str,
    ) -> None:
        if self.current_project is None:
            return

        result = ProjectService.import_media(
            self.current_project,
            files,
            media_type,
        )

        imported = result.get("imported", [])
        skipped = result.get("skipped", [])
        errors = result.get("errors", [])

        self.refresh()
        self.media_changed.emit()

        message_parts = [
            f"Imported: {len(imported)}",
            f"Duplicates skipped: {len(skipped)}",
        ]

        if errors:
            message_parts.append(
                "Errors:\n" + "\n".join(str(error) for error in errors)
            )

        QMessageBox.information(
            self,
            "Media Import Complete",
            "\n\n".join(message_parts),
        )
