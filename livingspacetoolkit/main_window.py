import logging

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTabWidget
from PySide6.QtGui import QPixmap, QIcon

import livingspacetoolkit.Resource.resources_rc

from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.views.roof_pitch_component import RoofPitch
from livingspacetoolkit.views.roofing_type_component import RoofingType
from livingspacetoolkit.views.roof_end_cuts_component import RoofEndCuts
from livingspacetoolkit.views.floor_plan_component import FloorPlan
from livingspacetoolkit.views.results_view import Results
from livingspacetoolkit.views.studio_roof_component import StudioRoof
from livingspacetoolkit.views.studio_wall_height_component import StudioWallHeight
from livingspacetoolkit.views.studio_view import Studio

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.setWindowTitle("LivingSpace Toolkit")
        self.setWindowIcon(QIcon(":/LivingSpace/LivingSpace_Icon"))

        self.logo: QLabel = QLabel()
        logo_image: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Logo")
        self.logo.setPixmap(logo_image)

        self.scenarios = ScenariosView()
        self.roof_pitch = RoofPitch("Pitch")
        self.roofing_type = RoofingType()
        self.roof_end_cuts = RoofEndCuts()
        self.floor_plan = FloorPlan()
        self.results = Results()
        self.studio_roof = StudioRoof()
        self.studio_wall_height = StudioWallHeight()
        self.studio = Studio()

        tabs: QTabWidget = QTabWidget()
        tabs.addTab(self.studio, "Studio")

        layout: QVBoxLayout = QVBoxLayout()

        layout.addWidget(self.logo)
        layout.addWidget(self.scenarios)
        central_layout: QHBoxLayout = QHBoxLayout()
        central_layout.addWidget(tabs)
        central_layout.addWidget(self.results)
        layout.addLayout(central_layout)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setMaximumSize(QSize(1150, 1200))
        self.setMinimumSize(QSize(1150, 1200))