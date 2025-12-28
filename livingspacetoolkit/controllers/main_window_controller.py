from livingspacetoolkit.logconf.log_config import logger
from livingspacetoolkit.views import ScenariosView, ResultsView, TabsView
from livingspacetoolkit.models.toolkit_state_model import ToolkitStateModel
from .studio_controller import StudioController
from .cathedral_controller import CathedralController
from livingspacetoolkit.lib.toolkit_enums import SunroomType


class MainWindowController:
    def __init__(self,
                 tabs_view: TabsView,
                 scenarios_view: ScenariosView,
                 results_view: ResultsView,
                 toolkit_state: ToolkitStateModel):
        self.tabs_view = tabs_view
        self.scenarios_view = scenarios_view
        self.results_view = results_view
        self.toolkit_state = toolkit_state

        # Controller for each tab
        self.studio_controller = StudioController(self.tabs_view.studio_view, self.toolkit_state)
        self.cathedral_controller = CathedralController(self.tabs_view.cathedral_view, self.toolkit_state)

        # Connect signals
        self.tabs_view.currentChanged.connect(self.handle_tab_change)
        self.scenarios_view.radio_group.buttonToggled.connect(self.handle_scenario_selected)
        self.results_view.calculate_button.clicked.connect(self.handle_results_button_click)

    def handle_tab_change(self) -> None:
        self.toolkit_state.default_state()
        self.toolkit_state.sunroom_type = SunroomType(self.tabs_view.currentIndex())
        self.results_view.results_view.clear()
        self.scenarios_view.default_state()
        self.set_to_default_state()
        logger.debug(f'The sunroom type, {SunroomType(self.tabs_view.currentIndex()).name}, has been selected.')

    def handle_scenario_selected(self) -> None:
        for button in self.scenarios_view.scenario_dict.keys():
            if button.isChecked():
                self.toolkit_state.scenario = self.scenarios_view.scenario_dict[button]
                logger.info(f"{self.scenarios_view.scenario_dict[button].name} has been selected as the scenario.")
        self.update_to_scenario()
        self.results_view.calculate_button.setEnabled(True)

    def handle_results_button_click(self) -> None:
        # TODO: Button press actually does calculations using calculations model
        try:
            logger.debug("Checking if all fields are filled for selected scenario.")
            self.toolkit_state.check_calculation_ready()
        except TypeError as err:
            self.tabs_view.show_warning(str(err))
            logger.warning(err)
        self.results_view.update_text("Button Pressed.\nNew line added.")

    def set_to_default_state(self) -> None:
        self.studio_controller.set_to_default()
        self.cathedral_controller.set_to_default()
        self.results_view.default_state()

    def update_to_scenario(self) -> None:
        self.results_view.results_view.clear()
        match self.toolkit_state.sunroom_type:
            case SunroomType.STUDIO:
                self.studio_controller.update_to_scenario()
            case SunroomType.CATHEDRAL:
                self.cathedral_controller.update_to_scenario()
