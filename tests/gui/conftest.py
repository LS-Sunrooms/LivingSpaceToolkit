import pytest, pytestqt

from PySide6.QtWidgets import QMessageBox

from livingspacetoolkit.main_window import MainWindow


@pytest.fixture()
def main_window(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.tabs_controller.set_to_default_state()
    return window

@pytest.fixture()
def mock_warning(monkeypatch):
    calls = {}

    def fake_warning(parent, title, text, buttons=QMessageBox.StandardButton.Ok):
        calls["parent"] = parent
        calls["title"] = title
        calls["text"] = text
        calls["buttons"] = buttons
        return QMessageBox.StandardButton.Ok

    monkeypatch.setattr(QMessageBox, "warning", fake_warning)
    return calls