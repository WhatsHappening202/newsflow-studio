from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from newsflow.services.media_service import MediaService


class MediaLibraryPage(QWidget):
    def __init__(self):
        super().__init__()

        self.project = None

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Media Library")
        title.setStyleSheet(
            """
            font-size:30px;
            font-weight:bold;
            """
        )

        layout.addWidget(title)

        button_layout = QVBoxLayout()

        self.import_images_button = QPushButton(
            "Import Images"
        )

        self.import_images_button.clicked.connect(
            self.import_images
        )

        button_layout.addWidget(
            self.import_images_button
        )

        self.image_count = QLabel("Images: 0")

        button_layout.addWidget(
            self.image_count
        )

        layout.addLayout(button_layout)

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.grid = QGridLayout(self.container)

        self.scroll.setWidget(self.container)

        layout.addWidget(self.scroll)

    def set_project(self, project):

        self.project = project

        self.refresh()

    def refresh(self):

        while self.grid.count():

            item = self.grid.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        if self.project is None:
            self.image_count.setText("Images: 0")
            return

        folder = MediaService.get_images_folder(
            self.project
        )

        images = sorted(folder.iterdir())

        self.image_count.setText(
            f"Images: {len(images)}"
        )

        row = 0
        col = 0

        for image in images:

            pixmap = QPixmap(str(image))

            pixmap = pixmap.scaled(
                180,
                120,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )

            thumb = QLabel()

            thumb.setPixmap(pixmap)

            name = QLabel(image.name)

            wrapper = QWidget()

            v = QVBoxLayout(wrapper)

            v.addWidget(thumb)

            v.addWidget(name)

            self.grid.addWidget(
                wrapper,
                row,
                col,
            )

            col += 1

            if col == 4:
                col = 0
                row += 1

    def import_images(self):

        if self.project is None:
            return

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Images",
            "",
            "Images (*.jpg *.jpeg *.png *.bmp *.webp)",
        )

        if not files:
            return

        MediaService.import_images(
            self.project,
            files,
        )

        self.refresh()