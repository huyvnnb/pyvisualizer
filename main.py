import sys

from algorithm import BubbleSort
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    array = [9,8,7,6,5]
    print(array)
    window = BubbleSort(array)
    window.show()

    app.exec()
