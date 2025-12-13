import logging

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QTabWidget, QGridLayout
from PySide6.QtGui import QPixmap, QIcon

import livingspacetoolkit.Resource.resources_rc
from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.views.results_view import Results
from livingspacetoolkit.views.studio_view import Studio
from livingspacetoolkit.views.cathedral_view import Cathedral
from livingspacetoolkit.controllers.results_controller import ResultsController
from livingspacetoolkit.controllers.studio_controller import StudioController

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.setWindowTitle("LivingSpace Toolkit")
        self.setWindowIcon(QIcon(":/LivingSpace/LivingSpace_Icon"))

        self.logo: QLabel = QLabel()
        logo_image: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Logo")
        self.logo.setPixmap(logo_image)

        # === Models ===

        # === Views ===
        self.scenarios_view = ScenariosView()
        self.results_view = Results()
        self.studio_view = Studio()
        self.cathedral_view = Cathedral()

        tabs: QTabWidget = QTabWidget()
        tabs.addTab(self.studio_view, "Studio")
        tabs.addTab(self.cathedral_view, "Cathedral")
        tabs.setMinimumSize(600, 400)

        # === Controllers ===
        self.results_controller = ResultsController(self.results_view, tabs)
        self.studio_controller = StudioController(self.studio_view)

        layout: QGridLayout = QGridLayout()

        layout.addWidget(self.logo, 0, 0, 1, 2)
        layout.addWidget(self.scenarios_view, 1, 0, 1, 2)
        layout.addWidget(tabs, 2, 0)
        layout.addWidget(self.results_view, 2, 1)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setMaximumSize(QSize(1150, 1200))
        self.setMinimumSize(QSize(1150, 1200))