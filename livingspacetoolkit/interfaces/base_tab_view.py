from typing import Protocol

from PySide6.QtWidgets import QWidget


class BaseTabView(Protocol):
    sunroom_roof: QWidget
    sunroom_wall: QWidget
    sunroom_floor: QWidget