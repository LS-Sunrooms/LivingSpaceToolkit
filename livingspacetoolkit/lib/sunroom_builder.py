from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil

from livingspacetoolkit.logconf.log_config import logger
from .toolkit_enums import Scenario, EndCutType, LengthType
from .toolkit_length import ToolkitLength
from .base_scenario_class import ScenarioSelector
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel



class SunroomBuilder:
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model
        self.scenario = ScenarioSelector(self.toolkit_state_model).identify_scenario()

    @staticmethod
    def calculate_armstrong_panels(pitch, pitched_wall, unpitched_wall):
        """
        Calculates the number of armstrong boxes for the roof.
        :param pitch: float: The pitch of the roof in radians
        :param pitched_wall: float: The length of the pitched wall in inches
        :param unpitched_wall: float: The length of the unpitched wall in inches
        :return:
        """
        rake_length = pitched_wall / cos(pitch)
        armstrong_area = rake_length * unpitched_wall / 144  # To get area in sq. ft.
        return m_ceil((armstrong_area + (armstrong_area * 0.1)) / 29)

    def _calculate_panel_length(self, pitch, pitched_wall, overhang, thickness):
        max_panel_length = False
        panel_tolerance = False
        panel_length = ToolkitLength(LengthType.PANEL)
        if self.toolkit_state_model.end_cuts == EndCutType.UNCUT_TOP_BOTTOM:
            p_length = (pitched_wall + overhang) / cos(pitch)
        else:
            p_bottom = (pitched_wall + overhang) / cos(pitch)
            p_top = (pitched_wall + overhang + thickness * sin(pitch)) / cos(pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1 inch past the nearest foot
            panel_tolerance = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1 inch tolerance
            # CORRECTION: We will NOT add 1 inch. Just round down instead
            # panel_length = mfloor(p_length / 12) * 12 + 1
            value = m_floor(p_length / 12) * 12
        else:
            # Returns panel length (in inches) rounded up to nearest foot
            value = m_ceil(p_length / 12) * 12
        try:
            panel_length.length = value
        except ValueError as err:
            logger.warning(err)
            max_panel_length = True
            panel_length.length = value/2
        return {'Panel Length': panel_length, 'Max Length Check': max_panel_length, 'Panel Tolerance': panel_tolerance}