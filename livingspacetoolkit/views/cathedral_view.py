import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy

from livingspacetoolkit.views.cathedral_roof_component import CathedralRoof
from livingspacetoolkit.views.cathedral_wall_height_component import CathedralWallHeight
from livingspacetoolkit.views.floor_plan_component import FloorPlan

logger = logging.getLogger(__name__)


class Cathedral(QWidget):
    def __init__(self):
        super().__init__()

        layout: QHBoxLayout = QHBoxLayout()
        layout_sub: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.sunroom_roof: CathedralRoof = CathedralRoof()
        self.sunroom_wall: CathedralWallHeight = CathedralWallHeight()
        self.sunroom_floor: FloorPlan = FloorPlan()

        layout_sub.addWidget(self.sunroom_wall)
        layout_sub.addSpacerItem(spacer)
        layout_sub.addWidget(self.sunroom_floor)

        layout.addWidget(self.sunroom_roof)
        layout.addLayout(layout_sub)

        self.setLayout(layout)