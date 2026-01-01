import pytest

from livingspacetoolkit.lib.toolkit_enums import SunroomSide, SunroomType, Scenario, RoofingType, LengthType, EndCutType
from livingspacetoolkit.models import ToolkitStateModel, SunroomModel
from livingspacetoolkit.lib import SunroomBuilder, ScenarioSelector


class TestStudioSunroomBuild:
    @pytest.mark.integration
    def test_wall_height_pitch_with_fascia(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 130
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.B_SIDE] == 180
        assert sunroom_model.roof_area[SunroomSide.B_SIDE] == 200
        assert sunroom_model.roof_panels[SunroomSide.B_SIDE] == 5
        assert sunroom_model.roof_panels_split[SunroomSide.B_SIDE] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["value"] == 12
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["value"] == 12
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["value"] == 160
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 172
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 186
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 186
        assert sunroom_model.armstrong_panels == 6

    @pytest.mark.integration
    def test_wall_height_pitch_without_fascia(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = False
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 130
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.B_SIDE] == 180
        assert sunroom_model.roof_area[SunroomSide.B_SIDE] == 200
        assert sunroom_model.roof_panels[SunroomSide.B_SIDE] == 5
        assert sunroom_model.roof_panels_split[SunroomSide.B_SIDE] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["value"] == 12
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["value"] == 12
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["value"] == 160
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 0
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 0
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 0
        assert sunroom_model.armstrong_panels == 6

    @pytest.mark.integration
    def test_wall_height_pitch_with_fascia_split(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.STUDIO
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.B_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.B_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 200
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 200
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 200
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.B_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.B_SIDE] == 276
        assert sunroom_model.roof_area[SunroomSide.B_SIDE] == 430
        assert sunroom_model.roof_panels[SunroomSide.B_SIDE] == 7
        assert sunroom_model.roof_panels_split[SunroomSide.B_SIDE] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.A_SIDE]["value"] == 12
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["long_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.C_SIDE]["value"] == 12
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["max_length"] == True
        assert sunroom_model.hang_rails[SunroomSide.B_SIDE]["value"] == 112
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == True
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 118
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == True
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 141
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == True
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 141
        assert sunroom_model.armstrong_panels == 14


class TestCathedralSunroomBuild:
    @pytest.mark.integration
    def test_wall_height_pitch_with_fascia(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.A_SIDE] == False
        assert sunroom_model.max_panel_length[SunroomSide.C_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.A_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.C_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.A_SIDE] == 96
        assert sunroom_model.panel_length[SunroomSide.C_SIDE] == 96
        assert (sunroom_model.roof_area[SunroomSide.A_SIDE] + sunroom_model.roof_area[SunroomSide.C_SIDE]) == 192
        assert sunroom_model.roof_panels[SunroomSide.A_SIDE] == 4.5
        assert sunroom_model.roof_panels[SunroomSide.C_SIDE] == 4.5
        assert sunroom_model.roof_panels_split[SunroomSide.A_SIDE] == True
        assert sunroom_model.roof_panels_split[SunroomSide.C_SIDE] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["long_check"] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["value"] == 24
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["value"] == 96
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["value"] == 96
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 102
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][1] == 102
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 150
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 150
        assert sunroom_model.armstrong_panels == 6

    @pytest.mark.integration
    def test_wall_height_pitch_without_fascia(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = False
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 120
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 120
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.A_SIDE] == False
        assert sunroom_model.max_panel_length[SunroomSide.C_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.A_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.C_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.A_SIDE] == 96
        assert sunroom_model.panel_length[SunroomSide.C_SIDE] == 96
        assert (sunroom_model.roof_area[SunroomSide.A_SIDE] + sunroom_model.roof_area[SunroomSide.C_SIDE]) == 192
        assert sunroom_model.roof_panels[SunroomSide.A_SIDE] == 4.5
        assert sunroom_model.roof_panels[SunroomSide.C_SIDE] == 4.5
        assert sunroom_model.roof_panels_split[SunroomSide.A_SIDE] == True
        assert sunroom_model.roof_panels_split[SunroomSide.C_SIDE] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["long_check"] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["value"] == 24
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["value"] == 96
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["value"] == 96
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 0
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][1] == 0
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 0
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 0
        assert sunroom_model.armstrong_panels == 6

    @pytest.mark.integration
    def test_wall_height_pitch_with_fascia_split(self):
        # Arrange
        toolkit_state = ToolkitStateModel()
        sunroom_model = SunroomModel()
        toolkit_state.sunroom_type = SunroomType.CATHEDRAL
        toolkit_state.scenario = Scenario.WALL_HEIGHT_PITCH
        toolkit_state.pitch[SunroomSide.A_SIDE].pitch_value = '10'
        toolkit_state.pitch[SunroomSide.C_SIDE].pitch_value = '10'
        toolkit_state.overhang.length = 12
        toolkit_state.roofing_type = RoofingType.ECO_GREEN
        toolkit_state.thickness.length = 6
        toolkit_state.end_cuts = EndCutType.UNCUT_TOP_BOTTOM
        toolkit_state.fascia = True
        toolkit_state.wall_heights[(SunroomSide.A_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.wall_heights[(SunroomSide.C_SIDE, LengthType.WALL_HEIGHT)].length = 120
        toolkit_state.floor_walls[SunroomSide.A_SIDE].length = 250
        toolkit_state.floor_walls[SunroomSide.B_SIDE].length = 500
        toolkit_state.floor_walls[SunroomSide.C_SIDE].length = 250
        scenario = ScenarioSelector(toolkit_state).identify_scenario(sunroom_model)
        scenario.calculate_sunroom_properties()
        builder = SunroomBuilder(toolkit_state, sunroom_model)
        # Act
        builder.build_roof_components()
        # Assert
        assert sunroom_model.max_panel_length[SunroomSide.A_SIDE] == True
        assert sunroom_model.max_panel_length[SunroomSide.C_SIDE] == True
        assert sunroom_model.panel_tolerance[SunroomSide.A_SIDE] == False
        assert sunroom_model.panel_tolerance[SunroomSide.C_SIDE] == False
        assert sunroom_model.panel_length[SunroomSide.A_SIDE] == 174
        assert sunroom_model.panel_length[SunroomSide.C_SIDE] == 174
        assert (sunroom_model.roof_area[SunroomSide.A_SIDE] + sunroom_model.roof_area[SunroomSide.C_SIDE]) == 1316
        assert sunroom_model.roof_panels[SunroomSide.A_SIDE] == 8.5
        assert sunroom_model.roof_panels[SunroomSide.C_SIDE] == 8.5
        assert sunroom_model.roof_panels_split[SunroomSide.A_SIDE] == True
        assert sunroom_model.roof_panels_split[SunroomSide.C_SIDE] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["short_check"] == False
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["long_check"] == True
        assert sunroom_model.roof_overhang[SunroomSide.B_SIDE]["value"] == 22
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.A_SIDE]["value"] == 96
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["max_length"] == False
        assert sunroom_model.hang_rails[SunroomSide.C_SIDE]["value"] == 96
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][0] == 180
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["max_length"] == False
        assert sunroom_model.fascia[SunroomSide.B_SIDE]["value"][1] == 180
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["max_length"] == True
        assert sunroom_model.fascia[SunroomSide.A_SIDE]["value"][0] == 139
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["max_length"] == True
        assert sunroom_model.fascia[SunroomSide.C_SIDE]["value"][0] == 139
        assert sunroom_model.armstrong_panels == 44