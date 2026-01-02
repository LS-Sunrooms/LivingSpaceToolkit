from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QGridLayout
from PySide6.QtGui import QPixmap, QIcon

from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.views import ScenariosView, ResultsView, TabsView
from livingspacetoolkit.controllers.main_window_controller import MainWindowController
from livingspacetoolkit.models.toolkit_state_model import ToolkitStateModel


class MainWindow(QMainWindow):
    """Uses views to assemble main window."""
    def __init__(self):
        super().__init__()

        central_widget = QWidget()

        self.setWindowTitle("LivingSpace Toolkit")
        self.setWindowIcon(QIcon(":/LivingSpace/LivingSpace_Icon"))

        self.logo: QLabel = QLabel()
        logo_image: QPixmap = QPixmap(":/LivingSpace/LivingSpace_Logo")
        self.logo.setPixmap(logo_image)

        # === Models ===
        self.toolkit_state = ToolkitStateModel()

        # === Views ===
        self.scenarios_view = ScenariosView()
        self.results_view = ResultsView()
        self.tabs_view = TabsView()

        # === Controllers ===
        self.tabs_controller = MainWindowController(self.tabs_view, self.scenarios_view, self.results_view,
                                                    self.toolkit_state)

        layout: QGridLayout = QGridLayout()

        layout.addWidget(self.logo, 0, 0, 1, 2)
        layout.addWidget(self.scenarios_view, 1, 0, 1, 2)
        layout.addWidget(self.tabs_view, 2, 0)
        layout.addWidget(self.results_view, 2, 1)

        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setMaximumSize(QSize(1150, 1200))
        self.setMinimumSize(QSize(1150, 1200))
