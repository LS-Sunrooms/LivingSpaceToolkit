from PySide6.QtWidgets import QTabWidget, QMessageBox

from livingspacetoolkit.logconf.log_config import logger
from .studio_view import StudioView
from .cathedral_view import CathedralView


class TabsView(QTabWidget):
    def __init__(self):
        super().__init__()

        self.studio_view = StudioView()
        self.cathedral_view = CathedralView()

        self.addTab(self.studio_view, "Studio")
        self.addTab(self.cathedral_view, "Cathedral")
        self.setMinimumSize(600, 400)

    def show_warning(self, message: str) -> None:
        QMessageBox.warning(self, "WARNING", message, QMessageBox.StandardButton.Ok)
