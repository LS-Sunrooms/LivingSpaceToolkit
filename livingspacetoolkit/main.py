# nuitka-project: --enable-plugin=pyside6
# nuitka-project: --mode=onefile
# nuitka-project: --windows-console-mode=disable
# nuitka-project: --windows-icon-from-ico=livingspacetoolkit/Resource/Livingspace_Sunrooms_icon.ico
# nuitka-project: --output-dir=output
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --output-filename=LivingspaceToolkit.exe
# nuitka-project-else:
#    nuitka-project: --output-filename=LivingspaceToolkit

from PySide6.QtWidgets import QApplication

from livingspacetoolkit.config.log_config import logger
from livingspacetoolkit.main_window import MainWindow
from livingspacetoolkit.theme_manager import apply_theme
import livingspacetoolkit.Resource.resources_rc


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
