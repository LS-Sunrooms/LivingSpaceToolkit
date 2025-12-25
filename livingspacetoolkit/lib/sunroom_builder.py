import logging
from math import sin, cos, tan, atan, atan2, pi
from math import floor as m_floor
from math import ceil as m_ceil

from .toolkit_enums import Scenario, EndCutType, LengthType
from .base_scenario_class import ScenarioSelector
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel

logger = logging.getLogger(name="livingspacetoolkit")


class SunroomBuilder:
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model
        self.scenario = ScenarioSelector(self.toolkit_state_model).identify_scenario()

    def angled(self, pitch) -> float:
        """
        Calculates the angled thickness given pitch and the panel thickness. Pitch has to be in radians.
        :param pitch: float
        :return: float
        """
        angle = None
        try:
            angle = self.toolkit_state_model.thickness.length * (sin(pi / 2) / sin(pi / 2 - pitch))
        except ZeroDivisionError as err:
            logger.exception(err)
        return angle

    def calculate_drip_edge(self, soffit, pitch):
        """
        Returns the drip edge height given the soffit and angled thickness. Returns in units of inches.

        :param soffit: float: Soffit height in inches
        :param pitch: float: Pitch in radians
        :return:
        """
        angled_thickness = self.angled(pitch=pitch)
        if self.toolkit_state_model.end_cuts == EndCutType.PLUMB_CUT_TOP_BOTTOM:
            drip_edge = soffit + angled_thickness
        else:
            drip_edge = soffit + self.toolkit_state_model.thickness.length * cos(pitch)
        return drip_edge

    def estimate_drip_from_peak(self, estimate_pitch, pitched_wall_length):
        """
        This method is used to help estimate the pitch. Since I forgot how to do numerical methods this will have to do. All
        lengths must be in inches, the estimated pitch in radians, and this assumes you are cycling through a list of
        pitches.
        :param estimate_pitch: float: The estimated pitch of the room in radians
        :param pitched_wall_length: float: The length of the pitched-side wall in inches
        :return: float: Returns the drip edge height in inches
        """
        wall_height = (self.toolkit_state_model.wall_heights[LengthType.PEAK_HEIGHT].length
                       - pitched_wall_length * tan(estimate_pitch))
        soffit = wall_height - self.toolkit_state_model.overhang.length * tan(estimate_pitch)

        drip_edge = self.calculate_drip_edge(soffit, estimate_pitch)
        return drip_edge

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

    def _calculate_panel_length(self, pitch, pitched_wall):
        max_panel_length = False
        panel_tolerance = False
        if self.toolkit_state_model.end_cuts == EndCutType.UNCUT_TOP_BOTTOM:
            p_length = (pitched_wall + self.toolkit_state_model.overhang.length) / cos(pitch)
        else:
            p_bottom = (pitched_wall + self.toolkit_state_model.overhang.length) / (cos(pitch))
            p_top = (pitched_wall + self.toolkit_state_model.overhang.length +
                     self.toolkit_state_model.thickness.length * sin(pitch)) / cos(pitch)
            p_length = max(p_bottom, p_top)
        if p_length % 12 <= 1:  # This checks to see if the panel length is a maximum 1 inch past the nearest foot
            panel_tolerance = True
            # Returns panel length (in inches) rounded down to nearest foot and adds the 1 inch tolerance
            # CORRECTION: We will NOT add 1 inch. Just round down instead
            # panel_length = mfloor(p_length / 12) * 12 + 1
            panel_length = m_floor(p_length / 12) * 12
        else:
            panel_length = m_ceil(p_length / 12) * 12  # Returns panel length (in inches) rounded up to nearest foot
        if panel_length > 288:
            max_panel_length = True
            panel_length /= 2
        return {'Panel Length': panel_length, 'Max Length Check': max_panel_length, 'Panel Tolerance': panel_tolerance}