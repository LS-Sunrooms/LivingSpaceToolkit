import logging

from livingspacetoolkit.views.tabs_view import TabsView
from livingspacetoolkit.views.scenarios_view import ScenariosView
from livingspacetoolkit.views.results_view import Results
from livingspacetoolkit.models.toolkit_state_model import ToolkitState
from livingspacetoolkit.controllers.studio_controller import StudioController
from livingspacetoolkit.controllers.cathedral_controller import CathedralController
from livingspacetoolkit.lib.livingspacetoolkit_enums import SunroomType

logger = logging.getLogger(__name__)


# TODO: Change to main controller. No need to have 3 controllers. Have one extra for each tab.
class TabsController:
    def __init__(self,
                 view: TabsView,
                 scenarios_view: ScenariosView,
                 results_view: Results,
                 toolkit_state: ToolkitState):
        self.view = view
        self.scenarios_view = scenarios_view
        self.results_view = results_view
        self.toolkit_state = toolkit_state

        self.studio_controller = StudioController(self.view.studio_view, self.toolkit_state)
        self.cathedral_controller = CathedralController(self.view.cathedral_view, self.toolkit_state)

        # Connect signals
        self.view.currentChanged.connect(self.handle_tab_change)

    def handle_tab_change(self) -> None:
        self.toolkit_state.sunroom_type = SunroomType(self.view.currentIndex())
        self.results_view.results_view.clear()
        self.scenarios_view.default_state()
        self.set_to_default_state()

        logging.info(f'The sunroom type, {SunroomType(self.view.currentIndex()).name}, has been selected.')

    def set_to_default_state(self) -> None:
        self.studio_controller.set_to_default()

    def update_to_scenario(self) -> None:
        self.results_view.results_view.clear()
        match self.toolkit_state.sunroom_type:
            case SunroomType.STUDIO:
                self.studio_controller.update_to_scenario()
            case SunroomType.CATHEDRAL:
                pass
