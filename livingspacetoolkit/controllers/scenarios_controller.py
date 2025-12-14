import logging

from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.controllers.tabs_controller import TabsController
from livingspacetoolkit.models.toolkit_state_model import ToolkitState

logger = logging.getLogger(__name__)


class ScenarioController:
    def __init__(self,
                 view: ScenariosView,
                 tabs_controller: TabsController,
                 toolkit_state: ToolkitState):
        self.view = view
        self.tabs_controller = tabs_controller
        self.toolkit_state = toolkit_state

        # Connect signals
        self.view.radio_group.buttonToggled.connect(self.handle_scenario_selected)


    def handle_scenario_selected(self) -> None:
        for button in self.view.scenario_dict.keys():
            if button.isChecked():
                self.toolkit_state.scenario = self.view.scenario_dict[button]
                logger.info(f"{self.view.scenario_dict[button].name} has been selected as the scenario.")
        self.tabs_controller.update_to_scenario()

    def default_state(self) -> None:
        self.view.default_state()