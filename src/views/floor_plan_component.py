import logging

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout
from PySide6.QtGui import QPixmap

import Resource.resources_rc


logger = logging.getLogger(__name__)

class FloorPlan(QWidget):
    def __init__(self):
        super().__init__()

        layout_main: QHBoxLayout = QHBoxLayout()
        layout_wall: QVBoxLayout = QVBoxLayout()

        self.wall_a: QLineEdit = QLineEdit()
        self.wall_b: QLineEdit = QLineEdit()
        self.wall_c: QLineEdit = QLineEdit()

        self.wall_a.setPlaceholderText("0' or 0\"")
        self.wall_a.setMaximumSize(QSize(85, 30))
        self.wall_b.setPlaceholderText("0' or 0\"")
        self.wall_b.setMaximumSize(QSize(85, 30))
        self.wall_c.setPlaceholderText("0' or 0\"")
        self.wall_c.setMaximumSize(QSize(85, 30))

        label_a: QLabel = QLabel("A Wall")
        label_b: QLabel = QLabel("B Wall")
        label_c: QLabel = QLabel("C Wall")

        layout_wall.addWidget(label_a)
        layout_wall.addWidget(self.wall_a)
        layout_wall.addWidget(label_b)
        layout_wall.addWidget(self.wall_b)
        layout_wall.addWidget(label_c)
        layout_wall.addWidget(self.wall_c)
        layout_wall.setAlignment(Qt.AlignmentFlag.AlignCenter)

        floor_image: QLabel = QLabel()
        floor_image.setPixmap( QPixmap(":/LivingSpace/LivingSpace_FloorPlan"))

        layout_main.addLayout(layout_wall)
        layout_main.addWidget(floor_image)
        self.setLayout(layout_main)
