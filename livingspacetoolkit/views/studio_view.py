import logging

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from livingspacetoolkit.views.studio_roof_component import StudioRoof
from livingspacetoolkit.views.studio_wall_height_component import StudioWallHeight
from livingspacetoolkit.views.floor_plan_component import FloorPlan

class Studio(QWidget):
    def __init__(self):
        super().__init__()

        layout_main: QHBoxLayout = QHBoxLayout()
        layout_sub: QVBoxLayout = QVBoxLayout()

        self.studio_roof: StudioRoof = StudioRoof()
        self.studio_wall: StudioWallHeight = StudioWallHeight()
        self.studio_floor: FloorPlan = FloorPlan()

        layout_sub.addWidget(self.studio_wall)
        layout_sub.addWidget(self.studio_floor)

        layout_main.addWidget(self.studio_roof)
        layout_main.addLayout(layout_sub)

        self.setLayout(layout_main)