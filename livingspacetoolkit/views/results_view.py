import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QTextEdit

logger = logging.getLogger(name="livingspacetoolkit")


class ResultsView(QWidget):
    def __init__(self):
        super().__init__()

        layout: QVBoxLayout = QVBoxLayout()

        spacer_top: QSpacerItem = QSpacerItem(20, 40)
        spacer_bottom: QSpacerItem = QSpacerItem(20, 40, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.calculate_button: QPushButton = QPushButton("Calculate")
        self.results_label: QLabel = QLabel()
        self.results_view: QTextEdit = QTextEdit()
        self.results_view.setReadOnly(True)
        self.results_view.setPlaceholderText("Waiting on selection...")
        font: QFont = QFont("Noto Sans", 12)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)

        self.results_label.setText("ResultsView:")
        self.results_label.setFont(font)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.results_view.setMinimumSize(300, 850)

        layout.addSpacerItem(spacer_top)
        layout.addWidget(self.calculate_button)
        layout.addWidget(self.results_label)
        layout.addWidget(self.results_view)
        layout.addSpacerItem(spacer_bottom)
        self.setLayout(layout)

    def default_state(self) -> None:
        logger.debug("Setting results to default state.")
        self.results_view.clear()
        self.calculate_button.setEnabled(False)

    def update_text(self, text: str) -> None:
        self.results_view.setText(text)
