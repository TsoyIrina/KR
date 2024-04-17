import sys

from PyQt6.QtWidgets import QApplication, QWidget

from controls.main_control import MainControl

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setStyle("windows")
    window = QWidget()
    control = MainControl(window)
    window.show()
    status = app.exec()
    sys.exit(status)
