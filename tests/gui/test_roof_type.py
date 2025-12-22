import pytest

from livingspacetoolkit.lib.toolkit_enums import RoofingType, SunroomType


class TestEndCuts:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_studio_end_cut_selection(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Select roofing type
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        # Check initial state
        assert main_window.toolkit_state.sunroom_type == SunroomType.STUDIO
        assert main_window.toolkit_state.roofing_type == RoofingType.ECO_GREEN
        # Change roof type
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_al.click()
        assert main_window.toolkit_state.roofing_type == RoofingType.ALUMINUM

    @pytest.mark.gui
    @pytest.mark.integration
    def test_cathedral_end_cut_selection(self, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Select roofing type
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        # Check initial state
        assert main_window.toolkit_state.sunroom_type == SunroomType.CATHEDRAL
        assert main_window.toolkit_state.roofing_type == RoofingType.ECO_GREEN
        # Change roof type
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_al.click()
        assert main_window.toolkit_state.roofing_type == RoofingType.ALUMINUM