from math import tan

from .base_scenario_class import BaseScenarioClass
from .toolkit_enums import Scenario, LengthType, SunroomSide, SunroomType
from livingspacetoolkit.logconf.log_config import logger
from livingspacetoolkit.models import ToolkitStateModel


class WallHeightPitch(BaseScenarioClass):
    def __init__(self, toolkit_state_model: ToolkitStateModel) -> None:
        self.toolkit_state_model = toolkit_state_model

    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        logger.debug(f"Selecting {scenario.name} class for calculations.")
        return scenario == Scenario.WALL_HEIGHT_PITCH

    def calculate_sunroom_properties(self) -> None:
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                # Gather variables
                flat_wall = max(self.toolkit_state_model.floor_walls[SunroomSide.A_SIDE],
                                self.toolkit_state_model.floor_walls[SunroomSide.C_SIDE]).length
                pitch_b_side = self.toolkit_state_model.pitch[SunroomSide.B_SIDE].pitch_value
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                wall_height_b_side = self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE,
                                                                            LengthType.WALL_HEIGHT)].length
                # Calculate
                soffit_height_b_side = wall_height_b_side - overhang * tan(pitch_b_side)
                peak_height = wall_height_b_side + flat_wall * tan(pitch_b_side)
                max_height = peak_height + self.calculate_hypotenuse(thickness, pitch_b_side)
                drip_edge = self.calculate_drip_edge(thickness, soffit_height_b_side, pitch_b_side)
                # Add calculated values to toolkit_state_model
                self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_b_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = peak_height
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = drip_edge
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
            case SunroomType.CATHEDRAL:
                # Gather variables
                gabled_wall = self.toolkit_state_model.floor_walls[SunroomSide.B_SIDE].length
                pitch_a_side = self.toolkit_state_model.pitch[SunroomSide.A_SIDE].pitch_value
                pitch_c_side = self.toolkit_state_model.pitch[SunroomSide.C_SIDE].pitch_value
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                wall_height_a_side = self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE,
                                                                            LengthType.WALL_HEIGHT)].length
                wall_height_c_side = self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE,
                                                                            LengthType.WALL_HEIGHT)].length
                # Calculate
                soffit_height_a_side = wall_height_a_side - overhang * tan(pitch_a_side)
                soffit_height_c_side = wall_height_c_side - overhang * tan(pitch_c_side)
                peak = self.calculate_triangle_height(pitch_a_side, pitch_c_side, gabled_wall)
                peak += max(wall_height_a_side, wall_height_c_side)
                fenevision_peak = peak - self.calculate_triangle_height(pitch_a_side, pitch_c_side, self.post_width)
                max_height = (fenevision_peak + max(self.calculate_hypotenuse(thickness, pitch_a_side),
                                         self.calculate_hypotenuse(thickness, pitch_c_side)) +
                                     self.calculate_triangle_height(pitch_a_side, pitch_c_side, self.post_width))
                drip_edge_a_side = self.calculate_drip_edge(thickness, soffit_height_a_side, pitch_a_side)
                drip_edge_c_side = self.calculate_drip_edge(thickness, soffit_height_c_side, pitch_c_side)
                # Add calculated values to toolkit_state_model
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_c_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = fenevision_peak
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = (
                    drip_edge_c_side)