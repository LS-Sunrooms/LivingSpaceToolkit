from math import tan

from livingspacetoolkit.logconf.log_config import logger
from .base_scenario_class import BaseScenarioClass
from .toolkit_enums import Scenario, LengthType, SunroomSide, SunroomType
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel


class DripEdgePitch(BaseScenarioClass):
    def __init__(self, toolkit_state_model: ToolkitStateModel, sunroom_model: SunroomModel) -> None:
        self.toolkit_state_model = toolkit_state_model
        self.sunroom_model = sunroom_model


    @staticmethod
    def scenario_condition(scenario: Scenario) -> bool:
        logger.debug(f"Selecting {scenario.name} class for calculations.")
        return scenario == Scenario.DRIP_EDGE_PITCH

    def calculate_sunroom_properties(self) -> None:
        match self.toolkit_state_model.sunroom_type:
            case SunroomType.STUDIO:
                # Gather variables
                flat_wall = max(self.toolkit_state_model.floor_walls[SunroomSide.A_SIDE],
                                self.toolkit_state_model.floor_walls[SunroomSide.C_SIDE]).length
                pitch_b_side = self.toolkit_state_model.pitch[SunroomSide.B_SIDE].pitch_value
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                drip_edge_b_side = self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE,
                                                                            LengthType.DRIP_EDGE_HEIGHT)].length
                # Calculate
                soffit_height_b_side = drip_edge_b_side - self.calculate_hypotenuse(thickness, pitch_b_side)
                wall_height_b_side = soffit_height_b_side + overhang * tan(pitch_b_side)
                peak_height = wall_height_b_side + flat_wall * tan(pitch_b_side)
                max_height = peak_height + self.calculate_hypotenuse(thickness, pitch_b_side)
                drip_edge_b_side = self.calculate_drip_edge(thickness, soffit_height_b_side, pitch_b_side)
                # Add calculated values to toolkit_state_model
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length = (
                    soffit_height_b_side)
                self.toolkit_state_model.wall_heights[(None, LengthType.PEAK_HEIGHT)].length = peak_height
                self.toolkit_state_model.wall_heights[(None, LengthType.MAX_HEIGHT)].length = max_height
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length = drip_edge_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.toolkit_state_model.wall_heights[
                    (SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = wall_height_b_side
                self.sunroom_model.gable_wall[SunroomSide.B_SIDE].length = flat_wall
            case SunroomType.CATHEDRAL:
                # Gather variables
                gabled_wall = self.toolkit_state_model.floor_walls[SunroomSide.B_SIDE].length
                pitch_a_side = self.toolkit_state_model.pitch[SunroomSide.A_SIDE].pitch_value
                pitch_c_side = self.toolkit_state_model.pitch[SunroomSide.C_SIDE].pitch_value
                overhang = self.toolkit_state_model.overhang.length
                thickness = self.toolkit_state_model.thickness.length
                drip_edge_a_side = self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE,
                                                                            LengthType.DRIP_EDGE_HEIGHT)].length
                drip_edge_c_side = self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE,
                                                                            LengthType.DRIP_EDGE_HEIGHT)].length
                # Calculate
                soffit_height_a_side = drip_edge_a_side - self.calculate_hypotenuse(thickness, pitch_a_side)
                soffit_height_c_side = drip_edge_c_side - self.calculate_hypotenuse(thickness, pitch_c_side)
                # I don't know why I chose the max between the two, but it's what the original calculations are.
                soffit = max(soffit_height_a_side, soffit_height_c_side)
                wall_height_a_side = soffit + overhang * tan(pitch_a_side)
                wall_height_c_side = soffit + overhang * tan(pitch_c_side)
                peak_height = (self.calculate_triangle_height(pitch_a_side, pitch_c_side, gabled_wall) +
                               max(wall_height_a_side, wall_height_c_side))
                half_gable_a_side = (peak_height - max(wall_height_a_side, wall_height_c_side)) / tan(pitch_a_side)
                half_gable_c_side = (peak_height - max(wall_height_a_side, wall_height_c_side)) / tan(pitch_c_side)
                fenevision_peak = peak_height - self.calculate_triangle_height(pitch_a_side, pitch_c_side,
                                                                               self.post_width)
                max_height = (fenevision_peak + max(self.calculate_hypotenuse(thickness, pitch_a_side),
                                                   self.calculate_hypotenuse(thickness, pitch_c_side)) +
                              self.calculate_triangle_height(pitch_a_side, pitch_c_side, self.post_width))
                drip_edge_a_side = self.calculate_drip_edge(thickness, soffit_height_a_side, pitch_a_side)
                drip_edge_c_side = self.calculate_drip_edge(thickness, soffit_height_c_side, pitch_c_side)
                # Add calculated values to toolkit_state_model
                self.toolkit_state_model.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_a_side)
                self.toolkit_state_model.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = (
                    wall_height_c_side)
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
                self.sunroom_model.gable_wall[SunroomSide.A_SIDE].length = half_gable_a_side
                self.sunroom_model.gable_wall[SunroomSide.C_SIDE].length = half_gable_c_side