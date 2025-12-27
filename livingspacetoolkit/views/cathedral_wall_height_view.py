import logging
from typing import Dict

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtGui import QPixmap

from livingspacetoolkit.utils.helpers import set_strikethrough
from livingspacetoolkit.lib.toolkit_enums import LengthType, SunroomSide

logger = logging.getLogger(name="livingspacetoolkit")


class CathedralWallHeightView(QWidget):
    def __init__(self):
        super().__init__()
        layout_heights: QVBoxLayout = QVBoxLayout()
        layout_img: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        cathedral_image: QLabel = QLabel()
        pix: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Cathedral")
        cathedral_image.setPixmap(
            pix.scaled(360, 360, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        cathedral_image.setMinimumSize(QSize(500, 500))
        layout: QHBoxLayout = QHBoxLayout()

        self.peak_height_edit: QLineEdit = QLineEdit()
        self.max_height_edit: QLineEdit = QLineEdit()
        self.a_wall_height_edit: QLineEdit = QLineEdit()
        self.c_wall_height_edit: QLineEdit = QLineEdit()
        self.soffit_height_a_edit: QLineEdit = QLineEdit()
        self.soffit_height_c_edit: QLineEdit = QLineEdit()
        self.drip_edge_height_edit: QLineEdit = QLineEdit()
        self.peak_height_label: QLabel = QLabel("Peak Height")
        self.max_height_label: QLabel = QLabel("Max Height")
        self.a_wall_height_label: QLabel = QLabel("A Wall Height")
        self.c_wall_height_label: QLabel = QLabel("C Wall Height")
        self.soffit_height_a_label: QLabel = QLabel("Soffit Height A Wall")
        self.soffit_height_c_label: QLabel = QLabel("Soffit Height C Wall")
        self.drip_edge_height_label: QLabel = QLabel("Drip Edge Height")

        self.wall_height_dict: Dict[tuple[SunroomSide | None, QLineEdit]] = {
            (None, LengthType.PEAK_HEIGHT): self.peak_height_edit,
            (None, LengthType.MAX_HEIGHT): self.max_height_edit,
            (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT): self.a_wall_height_edit,
            (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT): self.c_wall_height_edit,
            (SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT): self.soffit_height_a_edit,
            (SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT): self.soffit_height_c_edit,
            (None, LengthType.DRIP_EDGE_HEIGHT): self.drip_edge_height_edit
        }

        self.peak_height_edit.setPlaceholderText("0' or 0\"")
        self.peak_height_edit.setMaximumSize(QSize(150, 40))
        self.max_height_edit.setPlaceholderText("0' or 0\"")
        self.a_wall_height_edit.setPlaceholderText("0' or 0\"")
        self.c_wall_height_edit.setPlaceholderText("0' or 0\"")
        self.soffit_height_a_edit.setPlaceholderText("0' or 0\"")
        self.soffit_height_c_edit.setPlaceholderText("0' or 0\"")
        self.drip_edge_height_edit.setPlaceholderText("0' or 0\"")

        layout_heights.addWidget(self.peak_height_label)
        layout_heights.addWidget(self.peak_height_edit)
        layout_heights.addWidget(self.max_height_label)
        layout_heights.addWidget(self.max_height_edit)
        layout_heights.addWidget(self.a_wall_height_label)
        layout_heights.addWidget(self.a_wall_height_edit)
        layout_heights.addWidget(self.c_wall_height_label)
        layout_heights.addWidget(self.c_wall_height_edit)
        layout_heights.addWidget(self.soffit_height_a_label)
        layout_heights.addWidget(self.soffit_height_a_edit)
        layout_heights.addWidget(self.soffit_height_c_label)
        layout_heights.addWidget(self.soffit_height_c_edit)
        layout_heights.addWidget(self.drip_edge_height_label)
        layout_heights.addWidget(self.drip_edge_height_edit)
        layout_heights.addSpacerItem(spacer)

        layout_img.addWidget(cathedral_image)
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
        set_strikethrough(self.a_wall_height_label, True)
        self.a_wall_height_edit.clear()
        self.a_wall_height_edit.setEnabled(False)
        set_strikethrough(self.c_wall_height_label, True)
        self.c_wall_height_edit.clear()
        self.c_wall_height_edit.setEnabled(False)
        set_strikethrough(self.soffit_height_a_label, True)
        self.soffit_height_a_edit.clear()
        self.soffit_height_a_edit.setEnabled(False)
        set_strikethrough(self.soffit_height_c_label, True)
        self.soffit_height_c_edit.clear()
        self.soffit_height_c_edit.setEnabled(False)
        set_strikethrough(self.drip_edge_height_label, True)
        self.drip_edge_height_edit.clear()
        self.drip_edge_height_edit.setEnabled(False)
