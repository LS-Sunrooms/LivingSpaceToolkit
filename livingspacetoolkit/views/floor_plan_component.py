import logging

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QSpacerItem, QSizePolicy
from PySide6.QtGui import QPixmap

import livingspacetoolkit.Resource.resources_rc


logger = logging.getLogger(__name__)

class FloorPlan(QWidget):
    def __init__(self):
        super().__init__()

        layout_main: QHBoxLayout = QHBoxLayout()
        layout_wall: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.wall_a: QLineEdit = QLineEdit()
        self.wall_b: QLineEdit = QLineEdit()
        self.wall_c: QLineEdit = QLineEdit()

        self.wall_a.setPlaceholderText("0' or 0\"")
        self.wall_a.setMaximumSize(QSize(150, 40))
        self.wall_b.setPlaceholderText("0' or 0\"")
        self.wall_b.setMaximumSize(QSize(150, 40))
        self.wall_c.setPlaceholderText("0' or 0\"")
        self.wall_c.setMaximumSize(QSize(150, 40))

        label_a: QLabel = QLabel("A Wall")
        label_b: QLabel = QLabel("B Wall")
        label_c: QLabel = QLabel("C Wall")

        layout_wall.addSpacerItem(spacer)
        layout_wall.addWidget(label_a)
        layout_wall.addWidget(self.wall_a)
        layout_wall.addWidget(label_b)
        layout_wall.addWidget(self.wall_b)
        layout_wall.addWidget(label_c)
        layout_wall.addWidget(self.wall_c)
        layout_wall.addSpacerItem(spacer)
        layout_wall.setAlignment(Qt.AlignmentFlag.AlignLeft)

        floor_image: QLabel = QLabel()
        floor_image.setPixmap( QPixmap(":/LivingSpace/LivingSpace_FloorPlan"))

        layout_main.addLayout(layout_wall)
        layout_main.addWidget(floor_image)
        self.setLayout(layout_main)
