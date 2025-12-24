import logging
from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil

from .base_scenario_class import BaseScenarioClass
from .toolkit_enums import Scenario
from livingspacetoolkit.models import ToolkitStateModel

logger = logging.getLogger(name="livingspacetoolkit")


class WallHeightPitch(BaseScenarioClass):
    def __init__(self, toolkit_state_model: ToolkitStateModel) -> None:
        self.toolkit_state_model = toolkit_state_model

    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        logger.debug(f"Selecting {scenario.name} class for calculations.")
        return scenario == Scenario.WALL_HEIGHT_PITCH