import logging

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtGui import QPixmap


logger = logging.getLogger(__name__)


class StudioWallHeight(QWidget):
    def __init__(self):
        super().__init__()

        layout_heights: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        studio_image: QLabel = QLabel()
        pix: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Studio")
        studio_image.setPixmap(
            pix.scaled(360, 360, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        studio_image.setMinimumSize(QSize(500, 500))
        layout: QHBoxLayout = QHBoxLayout()

        self.peak_height_edit: QLineEdit = QLineEdit()
        self.max_height_edit: QLineEdit = QLineEdit()
        self.b_wall_height_edit: QLineEdit = QLineEdit()
        self.soffit_height_edit: QLineEdit = QLineEdit()
        self.drip_edge_height_edit: QLineEdit = QLineEdit()
        peak_height_label: QLabel = QLabel("Peak Height")
        max_height_label: QLabel = QLabel("Max Height")
        b_wall_height_label: QLabel = QLabel("B Wall Height")
        soffit_height_label: QLabel = QLabel("Soffit Height")
        drip_edge_height_label: QLabel = QLabel("Drip Edge Height")

        self.peak_height_edit.setPlaceholderText("0' or 0\"")
        self.peak_height_edit.setMaximumSize(QSize(150, 40))
        self.max_height_edit.setPlaceholderText("0' or 0\"")
        self.b_wall_height_edit.setPlaceholderText("0' or 0\"")
        self.soffit_height_edit.setPlaceholderText("0' or 0\"")
        self.drip_edge_height_edit.setPlaceholderText("0' or 0\"")

        layout_heights.addSpacerItem(spacer)
        layout_heights.addWidget(peak_height_label)
        layout_heights.addWidget(self.peak_height_edit)
        layout_heights.addWidget(max_height_label)
        layout_heights.addWidget(self.max_height_edit)
        layout_heights.addWidget(b_wall_height_label)
        layout_heights.addWidget(self.b_wall_height_edit)
        layout_heights.addWidget(soffit_height_label)
        layout_heights.addWidget(self.soffit_height_edit)
        layout_heights.addWidget(drip_edge_height_label)
        layout_heights.addWidget(self.drip_edge_height_edit)
        layout_heights.addSpacerItem(spacer)

        layout.addLayout(layout_heights)
        layout.addWidget(studio_image)

        self.setLayout(layout)