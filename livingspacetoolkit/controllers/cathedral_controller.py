import logging

from livingspacetoolkit.views.cathedral_view import CathedralView
from livingspacetoolkit.models.toolkit_state_model import ToolkitStateModel
from .base_sunroom_controller import BaseSunroomController
from livingspacetoolkit.lib.livingspacetoolkit_enums import PitchType, SunroomType, RoofingType, EndCutType, Scenario

logger = logging.getLogger(__name__)


class CathedralController(BaseSunroomController):
    def __init__(self, view: CathedralView, toolkit_state: ToolkitStateModel):
        self.view = view
        self.toolkit_state = toolkit_state

    def update_to_scenario(self):
        pass
