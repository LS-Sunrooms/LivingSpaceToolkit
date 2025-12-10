import logging

from PySide6.QtWidgets import QGroupBox, QRadioButton, QHBoxLayout, QGridLayout, QLabel, QLineEdit
from PySide6.QtCore import Qt

logger = logging.getLogger(__name__)

class RoofPitch(QGroupBox):
    def __init__(self, label_text: str = ""):
        super().__init__()

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.radio_ratio: QRadioButton = QRadioButton()
        self.radio_ratio.setObjectName("radio_ratio")
        self.radio_ratio.setChecked(False)
        self.radio_ratio.setEnabled(True)
        self.radio_ratio.setText("Ratio")

        self.radio_angle: QRadioButton = QRadioButton()
        self.radio_angle.setObjectName("radio_angle")
        self.radio_angle.setChecked(False)
        self.radio_angle.setEnabled(True)
        self.radio_angle.setText("Angle")

        self.pitch_input: QLineEdit = QLineEdit()
        self.pitch_input.setObjectName("pitch_input")
        self.pitch_input.setEnabled(True)
        self.pitch_input.setPlaceholderText("0 in. or 0deg.")

        self.pitch_input_label: QLabel = QLabel("/12 in.")
        self.pitch_input_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        layout_ratio: QHBoxLayout = QHBoxLayout()
        layout_ratio.addWidget(self.radio_ratio)
        layout_ratio.addWidget(self.radio_angle)

        layout_main: QGridLayout = QGridLayout()
        layout_main.addWidget(label, 0, 0)
        layout_main.addLayout(layout_ratio, 1, 0)
        layout_main.addWidget(self.pitch_input, 2, 0)
        layout_main.addWidget(self.pitch_input_label, 2, 1)

        self.setLayout(layout_main)
