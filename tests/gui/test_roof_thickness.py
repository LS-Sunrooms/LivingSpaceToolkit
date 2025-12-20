import pytest

from livingspacetoolkit.lib.toolkit_enums import LengthType
from livingspacetoolkit.lib import ToolkitLength


class TestStudioThickness:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_6inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '6"'
        # Act: Set Roof Type to EcoGreen and Thickness to 6"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(0)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_8inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '8.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 8"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(1)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_10inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '10.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 10"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(2)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_12inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '12.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 12"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(3)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_aluminum_thickness_3inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '3"'
        # Act: Set Roof Type to EcoGreen and Thickness to 3"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_al.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(0)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_aluminum_thickness_6inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(0)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '6"'
        # Act: Set Roof Type to EcoGreen and Thickness to 6"
        main_window.tabs_view.studio_view.sunroom_roof.roofing_type.radio_al.click()
        main_window.tabs_view.studio_view.sunroom_roof.thickness_combo.setCurrentIndex(1)
        # Assert
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == False
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.studio_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected
        

class TestCathedralThickness:

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_6inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '6"'
        # Act: Set Roof Type to EcoGreen and Thickness to 6"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(0)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_8inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '8.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 8"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(1)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_10inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '10.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 10"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(2)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_eco_green_thickness_12inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '12.25"'
        # Act: Set Roof Type to EcoGreen and Thickness to 12"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_eco.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(3)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == False
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_aluminum_thickness_3inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '3"'
        # Act: Set Roof Type to EcoGreen and Thickness to 3"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_al.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(0)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected

    @pytest.mark.gui
    @pytest.mark.integration
    def test_aluminum_thickness_6inch(self, main_window):
        # Arrange: Set tab to studio and scenario to WALL_HEIGHT_PITCH so that pitch is enabled. Set expected.
        main_window.tabs_view.setCurrentIndex(1)
        main_window.scenarios_view.radio1.click()
        # Expected length
        expected = ToolkitLength(LengthType.THICKNESS)
        expected.length = '6"'
        # Act: Set Roof Type to EcoGreen and Thickness to 6"
        main_window.tabs_view.cathedral_view.sunroom_roof.roofing_type.radio_al.click()
        main_window.tabs_view.cathedral_view.sunroom_roof.thickness_combo.setCurrentIndex(1)
        # Assert
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut1.isChecked() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut2.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.end_cuts.radio_endcut3.isEnabled() == False
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isEnabled() == True
        assert main_window.tabs_view.cathedral_view.sunroom_roof.fascia.isChecked() == True
        assert main_window.toolkit_state.thickness == expected