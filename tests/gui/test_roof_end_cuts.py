import pytest

from livingspacetoolkit.lib.toolkit_enums import EndCutType, SunroomType


class TestEndCuts:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_studio_end_cut_selection(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Select roofing type to enable end cuts
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        # Check initial state
        assert main_window.toolkit_state.sunroom_type == SunroomType.STUDIO
        assert main_window.toolkit_state.end_cuts == EndCutType.UNCUT_TOP_BOTTOM
        # Check plumb cut top and bottom
        main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.click()
        assert main_window.toolkit_state.end_cuts == EndCutType.PLUMB_CUT_TOP_BOTTOM
        # Check plumb cut top only
        main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.click()
        assert main_window.toolkit_state.end_cuts == EndCutType.PLUMB_CUT_TOP

    @pytest.mark.gui
    @pytest.mark.integration
    def test_cathedral_end_cut_selection(self, main_window):
        # Arrange: Set tab to cathedral and scenario to WALL_HEIGHT_PITCH.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Select roofing type to enable end cuts
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        # Check initial state
        assert main_window.toolkit_state.sunroom_type == SunroomType.CATHEDRAL
        assert main_window.toolkit_state.end_cuts == EndCutType.UNCUT_TOP_BOTTOM
        # Check plumb cut top and bottom
        main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.click()
        assert main_window.toolkit_state.end_cuts == EndCutType.PLUMB_CUT_TOP_BOTTOM
        # Check plumb cut top only
        main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.click()
        assert main_window.toolkit_state.end_cuts == EndCutType.PLUMB_CUT_TOP