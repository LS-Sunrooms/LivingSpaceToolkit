import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextBrowser, QSpacerItem, QSizePolicy

logger = logging.getLogger(__name__)

class Results(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()

        spacer_top: QSpacerItem = QSpacerItem(20, 40)
        spacer_bottom: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.calculate_button: QPushButton = QPushButton("Calculate")
        self.results_label: QLabel = QLabel()
        self.results_view: QTextBrowser = QTextBrowser()
        font: QFont = QFont("Noto Sans", 12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)

        self.results_label.setText("Results:")
        self.results_label.setFont(font)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.results_view.setMinimumSize(300, 850)

        layout.addSpacerItem(spacer_top)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.results_label)
        layout.addWidget(self.results_view)
        layout.addSpacerItem(spacer_bottom)
        self.setLayout(layout)
