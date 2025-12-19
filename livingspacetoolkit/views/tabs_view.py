import logging

from PySide6.QtWidgets import QTabWidget

from .studio_view import StudioView
from .cathedral_view import CathedralView

logger = logging.getLogger(name="livingspacetoolkit")


class TabsView(QTabWidget):
    def __init__(self):
        super().__init__()

        self.studio_view = StudioView()
        self.cathedral_view = CathedralView()

        self.addTab(self.studio_view, "Studio")
        self.addTab(self.cathedral_view, "Cathedral")
        self.setMinimumSize(600, 400)
