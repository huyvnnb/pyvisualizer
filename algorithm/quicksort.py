from PySide6.QtCore import QTimer
from visualizer import SortVisualizer

class QuickSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)
        self.stack = [(0, len(self.array) - 1)]
        self.timer = QTimer()
        self.timer.timeout.connect(self.sort_step)

    def start_sorting(self):
        self.timer.start(100)  # Mỗi bước chạy sau 100ms

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.swap_bars(i, j)

        self.swap_bars(i + 1, high)
        return i + 1

    def sort_step(self):
        if not self.stack:
            self.timer.stop()
            return

        low, high = self.stack.pop()
        if low < high:
            pivot = self.partition(low, high)
            self.stack.append((low, pivot - 1))  
            self.stack.append((pivot + 1, high))  
