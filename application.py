from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from window import SortingWindow,GraphWindow

if __name__ == "__main__":
    app = QApplication([])
    window = GraphWindow()
    window.show()
    app.exec()
