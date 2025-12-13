import logging

from PySide6.QtWidgets import QTabWidget

from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.views.results_view import Results
from livingspacetoolkit.views.studio_view import Studio
from livingspacetoolkit.views.cathedral_view import Cathedral

logger = logging.getLogger(__name__)


class ResultsController:
    def __init__(self,
                 view: Results,
                 main_tab: QTabWidget,
                 scenario: ScenariosView = None,
                 studio: Studio = None,
                 cathedral: Cathedral = None):
        self.view = view
        self.main_tab = main_tab
        self.scenario = scenario
        self.studio = studio
        self.cathedral = cathedral

        # Connect signals
        self.view.calculate_button.clicked.connect(self.handle_button_click)


    def handle_button_click(self):
        self.view.update_text(f"Button Pressed on tab {self.main_tab.currentIndex()}.\n"
                              f"Scenario is:")