import pytest

from livingspacetoolkit.lib.toolkit_enums import Scenario


class TestStudioScenarioSelection:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_wall_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PITCH
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_wall_height_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio2.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PEAK_HEIGHT
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio3.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.MAX_HEIGHT_PITCH
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio4.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio5.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.SOFFIT_HEIGHT_PITCH
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio6.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.DRIP_EDGE_PEAK_HEIGHT
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == True
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio7.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.DRIP_EDGE_PITCH
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.b_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_label.font().strikeOut() == True
        assert main_window.tabs_view.studio_view.sunroom_wall.soffit_height_edit.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == False
        assert main_window.tabs_view.studio_view.sunroom_wall.drip_edge_height_edit.isEnabled() == True
        # Check floor UI changes
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''


class TestCathedralScenarioSelection:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_wall_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PITCH
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_wall_height_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio2.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PEAK_HEIGHT
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_max_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio3.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.MAX_HEIGHT_PITCH
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio4.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.SOFFIT_HEIGHT_PEAK_HEIGHT
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_soffit_height_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio5.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.SOFFIT_HEIGHT_PITCH
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == False
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_and_peak_height_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio6.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.DRIP_EDGE_PEAK_HEIGHT
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == True
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''

    @pytest.mark.gui
    @pytest.mark.integration
    def test_drip_edge_and_pitch_selected(self, main_window):
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio7.click()

        # Check roof UI changes
        assert main_window.toolkit_state.scenario == Scenario.DRIP_EDGE_PITCH
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.pitch_c.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.overhang_edit.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        # Check wall UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.peak_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.max_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.a_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.c_wall_height_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_a_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_label.font().strikeOut() == True
        assert main_window.tabs_view.cathedral_view.sunroom_wall.soffit_height_c_edit.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_label.font().strikeOut() == False
        assert main_window.tabs_view.cathedral_view.sunroom_wall.drip_edge_height_edit.isEnabled() == True
        # Check floor UI changes
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_a.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_b.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_floor.wall_c.isEnabled() == True
        # Check results UI Changes
        assert main_window.results_view.calculate_button.isEnabled() == True
        assert main_window.results_view.results_view.toPlainText() == ''