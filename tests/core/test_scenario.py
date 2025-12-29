import pytest
from math import sin, cos, tan, atan, pi
from typing import Dict

from livingspacetoolkit.lib import *
from livingspacetoolkit.models import ToolkitStateModel
from livingspacetoolkit.lib.toolkit_enums import Scenario, SunroomSide, RoofingType, SunroomType, EndCutType
from livingspacetoolkit.lib.toolkit_length import LengthType


def calculate_hypotenuse(opposite: float, pitch: float) -> float:
    if pitch == pi / 2:
        raise ZeroDivisionError("The pitch is 90 degrees?")
    return opposite * (sin(pi / 2) / sin(pi / 2 - pitch))

def calculate_triangle_height(angle_1: float, angle_2: float, base_length: float) -> float:
    return base_length * sin(angle_1) * sin(angle_2) / sin(pi - angle_1 - angle_2)


class TestStudioScenarios:

    @pytest.fixture(scope="module")
    def studio_test_data(self) -> Dict[str, float]:
        pitch = atan(10/12)
        overhang = 10
        thickness = 6
        b_wall_height = 120
        floor_walls = 120
        soffit_h = b_wall_height - overhang * tan(pitch)
        peak_h = b_wall_height + floor_walls * tan(pitch)
        max_h = peak_h + thickness * sin(pi/2)/sin(pi/2 - pitch)
        drip_edge = soffit_h + thickness * cos(pitch)
        data = {
            "pitch": pitch,
            "overhang": overhang,
            "thickness": thickness,
            "b_wall_height": b_wall_height,
            "floor_walls": floor_walls,
            "soffit_height": soffit_h,
            "peak_height": peak_h,
            "max_height": max_h,
            "drip_edge": drip_edge
        }
        return data

    @pytest.mark.integration
    def test_wall_height_pitch(self, studio_test_data):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = studio_test_data['overhang']
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = studio_test_data["thickness"]
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = studio_test_data['b_wall_height']
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = studio_test_data['floor_walls']
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = studio_test_data['floor_walls']
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = studio_test_data['floor_walls']
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        assert scenario.__class__.__name__ == "WallHeightPitch"
        assert toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == studio_test_data['peak_height']
        assert toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == studio_test_data['max_height']
        assert toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.SOFFIT_HEIGHT)].length == studio_test_data['soffit_height']
        assert toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length == studio_test_data['drip_edge']
        assert toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length == studio_test_data['floor_walls']
        assert toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length == studio_test_data['floor_walls']

    @pytest.mark.integration
    def test_wall_height_peak_height(self):
        pass

    @pytest.mark.integration
    def test_max_height_pitch(self):
        pass

    @pytest.mark.integration
    def test_soffit_height_peak_height(self):
        pass

    @pytest.mark.integration
    def test_soffit_height_pitch(self):
        pass

    @pytest.mark.integration
    def test_drip_edge_peak_height(self):
        pass

    @pytest.mark.integration
    def test_drip_edge_pitch(self):
        pass

class TestCathedralScenarios:

    @pytest.fixture(scope="module")
    def cathedral_test_data(self) -> Dict[str, float]:
        post_width = 3.25
        a_pitch = atan(10 / 12)
        c_pitch = atan(10 / 12)
        overhang = 10
        thickness = 6
        a_wall_height = 120
        c_wall_height = 120
        floor_walls = 120
        a_soffit_h = a_wall_height - overhang * tan(a_pitch)
        c_soffit_h = c_wall_height - overhang * tan(c_pitch)
        peak_h = calculate_triangle_height(a_pitch, c_pitch, floor_walls)
        peak_h += max(a_wall_height, c_wall_height)
        fenevision_peak = peak_h - calculate_triangle_height(a_pitch, c_pitch, post_width)
        max_h = (fenevision_peak + max(calculate_hypotenuse(thickness, a_pitch),
                                      calculate_hypotenuse(thickness, c_pitch)) +
                 calculate_triangle_height(a_pitch, c_pitch, post_width))
        a_drip_edge = a_soffit_h + thickness * cos(a_pitch)
        c_drip_edge = c_soffit_h + thickness * cos(c_pitch)
        data = {
            "a_pitch": a_pitch,
            "c_pitch": c_pitch,
            "overhang": overhang,
            "thickness": thickness,
            "a_wall_height": a_wall_height,
            "c_wall_height": c_wall_height,
            "floor_walls": floor_walls,
            "a_soffit_height": a_soffit_h,
            "c_soffit_height": c_soffit_h,
            "peak_height": fenevision_peak,
            "max_height": max_h,
            "a_drip_edge": a_drip_edge,
            "c_drip_edge": c_drip_edge,
        }
        return data

    @pytest.mark.integration
    def test_wall_height_pitch(self, cathedral_test_data):
        # Arrange
        toolkit_state = ToolkitStateModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = cathedral_test_data['overhang']
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = cathedral_test_data["thickness"]
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = cathedral_test_data[
            'a_wall_height']
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = cathedral_test_data[
            'c_wall_height']
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = cathedral_test_data['floor_walls']
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = cathedral_test_data['floor_walls']
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = cathedral_test_data['floor_walls']
        scenario = ScenarioSelector(toolkit_state).identify_scenario()
        # Act
        scenario.calculate_sunroom_properties()
        # Assert
        assert scenario.__class__.__name__ == "WallHeightPitch"
        assert toolkit_state.wall_heights[(None, LengthType.PEAK_HEIGHT)].length == cathedral_test_data['peak_height']
        assert toolkit_state.wall_heights[(None, LengthType.MAX_HEIGHT)].length == cathedral_test_data['max_height']
        assert toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.SOFFIT_HEIGHT)].length == cathedral_test_data[
            'a_soffit_height']
        assert toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.SOFFIT_HEIGHT)].length == cathedral_test_data[
            'c_soffit_height']
        assert (toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length ==
                cathedral_test_data['a_drip_edge'])
        assert toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.DRIP_EDGE_HEIGHT)].length == \
               cathedral_test_data['c_drip_edge']
        assert toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length == cathedral_test_data[
            'floor_walls']
        assert toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length == cathedral_test_data[
            'floor_walls']

    @pytest.mark.integration
    def test_wall_height_peak_height(self):
        pass

    @pytest.mark.integration
    def test_max_height_pitch(self):
        pass

    @pytest.mark.integration
    def test_soffit_height_peak_height(self):
        pass

    @pytest.mark.integration
    def test_soffit_height_pitch(self):
        pass

    @pytest.mark.integration
    def test_drip_edge_peak_height(self):
        pass

    @pytest.mark.integration
    def test_drip_edge_pitch(self):
        pass