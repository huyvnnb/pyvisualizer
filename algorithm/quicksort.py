from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
import random


class QuickSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.quicksort()

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1

        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.swap_bars(i, j)

        self.swap_bars(i + 1, high)
        return i + 1

    def quicksort(self):
        stack = [(0, len(self.array) - 1)]

        while stack:
            low, high = stack.pop()
            if low < high:
                pivot = self.partition(low, high)
                stack.append((low, pivot - 1))  # Đẩy phần bên trái vào stack
                stack.append((pivot + 1, high))