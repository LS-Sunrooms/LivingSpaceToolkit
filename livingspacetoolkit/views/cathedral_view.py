import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from livingspacetoolkit.views.cathedral_roof_component import CathedralRoof
from livingspacetoolkit.views.cathedral_wall_height_component import CathedralWallHeight
from livingspacetoolkit.views.floor_plan_component import FloorPlan

logger = logging.getLogger(__name__)


class Cathedral(QWidget):
    def __init__(self):
        super().__init__()

        layout_main: QHBoxLayout = QHBoxLayout()
        layout_sub: QVBoxLayout = QVBoxLayout()

        self.cathedral_roof: CathedralRoof = CathedralRoof()
        self.cathedral_wall: CathedralWallHeight = CathedralWallHeight()
        self.cathedral_floor: FloorPlan = FloorPlan()

        layout_sub.addWidget(self.cathedral_wall)
        layout_sub.addWidget(self.cathedral_floor)

        layout_main.addWidget(self.cathedral_roof)
        layout_main.addLayout(layout_sub)

        self.setLayout(layout_main)