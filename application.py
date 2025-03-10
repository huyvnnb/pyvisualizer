from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from window import SortingWindow


if __name__ == "__main__":
    app = QApplication([])
    window = SortingWindow()
    window.show()
    app.exec()
