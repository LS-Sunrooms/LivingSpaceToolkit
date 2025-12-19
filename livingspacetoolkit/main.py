import livingspacetoolkit.logconf.log_config
import logging

from PySide6.QtWidgets import QApplication

from livingspacetoolkit.main_window import MainWindow
from livingspacetoolkit.theme_manager import apply_theme
import livingspacetoolkit.Resource.resources_rc

logger = logging.getLogger(name="livingspacetoolkit")


def main():
    logger.info("Starting LivingSpace Toolkit…")
    app = QApplication([])
    apply_theme(app)
    window = MainWindow()
    window.show()
    window.tabs_controller.set_to_default_state()
    app.exec()

if __name__ == "__main__":
    main()
