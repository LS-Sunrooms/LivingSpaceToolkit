import logging

from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel

from livingspacetoolkit.views.roof_pitch_component import RoofPitch
from livingspacetoolkit.views.roofing_type_component import RoofingType
from livingspacetoolkit.views.roof_end_cuts_component import RoofEndCuts

logger = logging.getLogger(__name__)


class CathedralRoof(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.pitch_a: RoofPitch = RoofPitch("A Side Pitch")
        self.pitch_c: RoofPitch = RoofPitch("C Side Pitch")
        self.overhang_edit: QLineEdit = QLineEdit()
        self.roofing_type: RoofingType = RoofingType()
        self.thickness_combo: QComboBox = QComboBox()
        self.end_cuts: RoofEndCuts = RoofEndCuts()
        self.fascia: QCheckBox = QCheckBox()

        overhang_label: QLabel = QLabel("Overhang")
        thickness_label: QLabel = QLabel("Thickness")

        self.overhang_edit.setPlaceholderText("0' or 0\"")
        self.fascia.setText("Fascia")

        layout.addWidget(self.pitch_a)
        layout.addWidget(self.pitch_c)
        layout.addWidget(overhang_label)
        layout.addWidget(self.overhang_edit)
        layout.addWidget(self.roofing_type)
        layout.addWidget(thickness_label)
        layout.addWidget(self.thickness_combo)
        layout.addWidget(self.end_cuts)
        layout.addWidget(self.fascia)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)
