from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, QMessageBox

from livingspacetoolkit.logconf.log_config import logger
from .floor_plan_view import FloorPlanView
from .studio_wall_height_view import StudioWallHeightView
from .studio_roof_view import StudioRoofView


class StudioView(QWidget):
    def __init__(self):
        super().__init__()

        layout: QHBoxLayout = QHBoxLayout()
        layout_sub: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.sunroom_roof: StudioRoofView = StudioRoofView()
        self.sunroom_wall: StudioWallHeightView = StudioWallHeightView()
        self.sunroom_floor: FloorPlanView = FloorPlanView()

        layout_sub.addWidget(self.sunroom_wall)
        layout_sub.addSpacerItem(spacer)
        layout_sub.addWidget(self.sunroom_floor)

        layout.addWidget(self.sunroom_roof)
        layout.addLayout(layout_sub)

        self.setLayout(layout)

    def show_warning(self, message: str) -> None:
        QMessageBox.warning(self, "WARNING", message, QMessageBox.StandardButton.Ok)