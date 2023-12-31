from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QRect

from papasGuideria.resources.ResourceManager import ResourceManager


class CustomImageLabel(QLabel):
    """A custom image label to be displayed."""

    def __init__(self, image_name: str, parent=None):
        super().__init__(parent)
        image_path = ResourceManager.get_image(image_name)

        self.original_pixmap = QPixmap()
        if not self.original_pixmap.load(image_path):
            print(f"Image not found. ({image_path})")
        self.setPixmap(self.original_pixmap)

    def resize_image(self, width: int = -1, height: int = -1):
        """
        Resizes the image to the given lengths exactly, ignoring the original aspect ratio.\n
        If width is negative (by default), the new width will keep the aspect ratio following the new height given.\n
        If height is negative (by default), the new height will keep the aspect ratio following the new width given.\n
        If both are negative, nothing will happen.
        """
        if width < 0 and height < 0:
            return

        if width < 0:
            scale_factor = height / self.original_pixmap.height()
            width = self.original_pixmap.width() * scale_factor
        elif height < 0:
            scale_factor = width / self.original_pixmap.width()
            height = self.original_pixmap.height() * scale_factor

        resized_pixmap = self.pixmap().scaled(int(width), int(height), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(resized_pixmap)

    def resize_image_keep_aspect(self, width: int, height: int):
        """Resizes the image to the given pixel lengths, keeping the aspect ratio."""
        resized_pixmap = self.original_pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(resized_pixmap)

    def resize_by_scale_factor(self, scale_factor: float):
        """Resizes the image by the given scale factor."""
        width = int(self.original_pixmap.width() * scale_factor)
        height = int(self.original_pixmap.height() * scale_factor)
        resized_pixmap = self.original_pixmap.scaled(width, height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(resized_pixmap)

    def greyscale(self, is_greyscale: bool):
        """Sets the image as greyscale or normal colours."""
        if is_greyscale:
            image = QPixmap.toImage(self.pixmap())
            greyscale_image = image.convertToFormat(QImage.Format_Grayscale8)
            grey_pixmap = QPixmap.fromImage(greyscale_image)
            self.setPixmap(grey_pixmap)
        else:
            self.setPixmap(self.original_pixmap)

    def crop(self, width: int, height: int, offset_x: int = 0, offset_y: int = 0):
        """Crops the image to the desired size."""
        crop_rect = QRect(offset_x, offset_y, width, height)
        self.setPixmap(self.pixmap().copy(crop_rect))
