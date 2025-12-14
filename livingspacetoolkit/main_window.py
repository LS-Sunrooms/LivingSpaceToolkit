import logging

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout
from PySide6.QtGui import QPixmap, QIcon

import livingspacetoolkit.Resource.resources_rc
from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.views.results_view import Results
from livingspacetoolkit.views.tabs_view import TabsView
from livingspacetoolkit.controllers.results_controller import ResultsController
from livingspacetoolkit.controllers.scenarios_controller import ScenarioController
from livingspacetoolkit.controllers.tabs_controller import TabsController
from livingspacetoolkit.models.toolkit_state_model import ToolkitState


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
        self.toolkit_state = ToolkitState()

        # === Views ===
        self.scenarios_view = ScenariosView()
        self.results_view = Results()
        self.tabs_view = TabsView()

        # === Controllers ===
        self.tabs_controller = TabsController(self.tabs_view, self.scenarios_view,self.results_view, self.toolkit_state)
        self.results_controller = ResultsController(self.results_view, self.toolkit_state)
        self.scenario_controller = ScenarioController(self.scenarios_view, self.tabs_controller, self.toolkit_state)

        layout: QGridLayout = QGridLayout()

        layout.addWidget(self.logo, 0, 0, 1, 2)
        layout.addWidget(self.scenarios_view, 1, 0, 1, 2)
        layout.addWidget(self.tabs_view, 2, 0)
        layout.addWidget(self.results_view, 2, 1)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setMaximumSize(QSize(1150, 1200))
        self.setMinimumSize(QSize(1150, 1200))
