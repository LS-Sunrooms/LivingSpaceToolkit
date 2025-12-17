import pytest

from pytestqt import qtbot
from livingspacetoolkit.lib.toolkit_enums import Scenario

from livingspacetoolkit.main_window import MainWindow


@pytest.fixture
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    window.tabs_controller.set_to_default_state()
    return window


class TestStudioScenarioSelection:

    @pytest.mark.gui
    def test_scenario_1_selected(self, main_window):
        main_window.scenarios_view.radio1.click()

        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PITCH
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == True

    @pytest.mark.gui
    def test_scenario_2_selected(self, main_window):

        main_window.scenarios_view.radio2.click()

        assert main_window.toolkit_state.scenario == Scenario.WALL_HEIGHT_PEAK_HEIGHT
        assert main_window.tabs_view.studio_view.sunroom_roof.pitch.isEnabled() == False