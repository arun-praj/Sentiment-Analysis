
"""
    GUI tutorial : https://www.mfitzp.com/tutorials/creating-your-first-pyqt-window/
    date : 2021/7/13
"""

from PyQt5.QtWidgets import QApplication
import sys
from MainWindow import MainWindow

app = QApplication([])

window = MainWindow()
window.show()

app.exec()