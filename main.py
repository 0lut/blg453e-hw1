from gui import GUI
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = GUI()
    sys.exit(app.exec_())
