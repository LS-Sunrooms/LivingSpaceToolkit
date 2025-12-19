import pytest, pytestqt

from livingspacetoolkit.main_window import MainWindow


@pytest.fixture()
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.tabs_controller.set_to_default_state()
    return window
