import logging

from PySide6.QtWidgets import QWidget, QLineEdit, QComboBox, QVBoxLayout, QCheckBox, QSpacerItem, QSizePolicy, QLabel
from PySide6.QtCore import QSize

from .roof_end_cuts_view import RoofEndCutsView
from .roof_pitch_view import RoofPitchView
from .roofing_type_view import RoofingTypeView
from livingspacetoolkit.lib.toolkit_enums import SunroomType
from livingspacetoolkit.utils.helpers import set_strikethrough

logger = logging.getLogger(name="livingspacetoolkit")


class StudioRoofView(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()
        spacer: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.pitch: RoofPitchView = RoofPitchView("Pitch")
        self.overhang_edit: QLineEdit = QLineEdit()
        self.roofing_type: RoofingTypeView = RoofingTypeView()
        self.thickness_combo: QComboBox = QComboBox()
        self.end_cuts: RoofEndCutsView = RoofEndCutsView()
        self.fascia: QCheckBox = QCheckBox()

        self.overhang_edit.setPlaceholderText("0' or 0\"")
        self.overhang_edit.setMinimumSize(QSize(145, 35))
        self.fascia.setText("Fascia")

        layout.addWidget(QLabel("Pitch"))
        layout.addWidget(self.pitch)
        layout.addWidget(QLabel("Overhang"))
        layout.addWidget(self.overhang_edit)
        layout.addWidget(QLabel("Roofing Type"))
        layout.addWidget(self.roofing_type)
        layout.addWidget(QLabel("Thickness"))
        layout.addWidget(self.thickness_combo)
        layout.addWidget(QLabel("End Cuts"))
        layout.addWidget(self.end_cuts)
        layout.addWidget(self.fascia)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)

    def default_state(self) -> None:
        self.pitch.default_state(SunroomType.STUDIO)
        self.overhang_edit.clear()
        self.overhang_edit.setEnabled(False)
        self.roofing_type.default_state()
        self.thickness_combo.clear()
        self.thickness_combo.setEnabled(False)
        self.end_cuts.default_state()
        set_strikethrough(self.fascia, True)
        self.fascia.setChecked(False)
        self.fascia.setEnabled(False)

    def enable_except_pitch(self) -> None:
        self.overhang_edit.clear()
        self.overhang_edit.setEnabled(True)
        self.roofing_type.enabled_state()
        self.thickness_combo.clear()
        self.thickness_combo.setEnabled(True)
        self.end_cuts.enabled_state()
        set_strikethrough(self.fascia, False)