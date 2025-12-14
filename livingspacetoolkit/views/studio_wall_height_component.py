import logging

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtGui import QPixmap

from livingspacetoolkit.utils.helpers import set_strikethrough

logger = logging.getLogger(__name__)


class StudioWallHeight(QWidget):
    def __init__(self):
        super().__init__()

        layout_heights: QVBoxLayout = QVBoxLayout()
        layout_img: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        studio_image: QLabel = QLabel()
        pix: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Studio")
        studio_image.setPixmap(
            pix.scaled(360, 360, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        studio_image.setMinimumSize(QSize(500, 500))
        layout: QHBoxLayout = QHBoxLayout()

        self.peak_height_edit: QLineEdit = QLineEdit()
        self.max_height_edit: QLineEdit = QLineEdit()
        self.soffit_height_edit: QLineEdit = QLineEdit()
        self.drip_edge_height_edit: QLineEdit = QLineEdit()
        self.peak_height_label: QLabel = QLabel("Peak Height")
        self.max_height_label: QLabel = QLabel("Max Height")
        self.b_wall_height_label: QLabel = QLabel("B Wall Height")
        self.soffit_height_label: QLabel = QLabel("Soffit Height")
        self.b_wall_height_edit: QLineEdit = QLineEdit()
        self.drip_edge_height_label: QLabel = QLabel("Drip Edge Height")
        self.peak_height_edit.setPlaceholderText("0' or 0\"")

        self.peak_height_edit.setMinimumSize(QSize(145, 35))
        self.max_height_edit.setPlaceholderText("0' or 0\"")
        self.b_wall_height_edit.setPlaceholderText("0' or 0\"")
        self.soffit_height_edit.setPlaceholderText("0' or 0\"")
        self.drip_edge_height_edit.setPlaceholderText("0' or 0\"")

        layout_heights.addWidget(self.peak_height_label)
        layout_heights.addWidget(self.peak_height_edit)
        layout_heights.addWidget(self.max_height_label)
        layout_heights.addWidget(self.max_height_edit)
        layout_heights.addWidget(self.b_wall_height_label)
        layout_heights.addWidget(self.b_wall_height_edit)
        layout_heights.addWidget(self.soffit_height_label)
        layout_heights.addWidget(self.soffit_height_edit)
        layout_heights.addWidget(self.drip_edge_height_label)
        layout_heights.addWidget(self.drip_edge_height_edit)
        layout_heights.addSpacerItem(spacer)

        layout_img.addWidget(studio_image)
        layout_img.addSpacerItem(spacer)

        layout.addLayout(layout_heights)
        layout.addLayout(layout_img)

        self.setLayout(layout)

    def default_state(self) -> None:
        set_strikethrough(self.peak_height_label, True)
        self.peak_height_edit.clear()
        self.peak_height_edit.setEnabled(False)
        set_strikethrough(self.max_height_label, True)
        self.max_height_edit.clear()
        self.max_height_edit.setEnabled(False)
        set_strikethrough(self.b_wall_height_label, True)
        self.b_wall_height_edit.clear()
        self.b_wall_height_edit.setEnabled(False)
        set_strikethrough( self.soffit_height_label, True)
        self.soffit_height_edit.clear()
        self.soffit_height_edit.setEnabled(False)
        set_strikethrough(self.drip_edge_height_label, True)
        self.drip_edge_height_edit.clear()
        self.drip_edge_height_edit.setEnabled(False)