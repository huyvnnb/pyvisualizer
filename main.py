import sys

from algorithm import BubbleSort, QuickSort
from PySide6.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    array = [21, 42, 5, 42, 64, 12]
    print(array)
    window = QuickSort(array)
    window.show()

    app.exec()
