from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
from shape import Bar
import random


class QuickSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.start_button.setEnabled(False)
        self.quicksort_iterative()
        self.start_button.setEnabled(True)
        print("Sort successfully")

    def quicksort_iterative(self):
        stack = [(0, len(self.array) - 1)]  # Dùng stack để thay thế đệ quy

        while stack:
            low, high = stack.pop()

            if low < high:
                pivot = self.array[high]
                i = low - 1

                # Partition ngay trong vòng lặp này
                for j in range(low, high):
                    if self.array[j] < pivot:
                        i += 1
                        self.swap_bars(i, j)  # Swap animation
                        self.loop.exec()  # Dừng lại, đợi animation hoàn thành

                # Swap pivot về đúng vị trí
                self.swap_bars(i + 1, high)
                self.loop.exec()  # Đợi animation hoàn thành

                pivot_index = i + 1

                # Đẩy phạm vi chưa sắp xếp vào stack
                stack.append((low, pivot_index - 1))  # Bên trái pivot
                stack.append((pivot_index + 1, high))  # Bên phải pivot

    # def partition(self, low, high):
    #     for k in range(low, high+1):
    #         self.bars[k].set_highlight(True, Bar.range_color)
    #
    #     pivot = self.array[high]
    #     self.bars[high].set_highlight(True, Bar.success_color)
    #
    #     i = low - 1
    #
    #     for j in range(low, high):
    #         if self.array[j] < pivot:
    #             i += 1
    #             self.bars[i].set_highlight(True)
    #             self.bars[j].set_highlight(True)
    #
    #             self.swap_bars(i, j)
    #             self.loop.exec()
    #
    #             self.bars[i].set_highlight(False)
    #             self.bars[j].set_highlight(False)
    #
    #         self.bars[j].set_highlight(False)
    #
    #     self.swap_bars(i + 1, high)
    #     self.loop.exec()
    #     for k in range(low, high+1):
    #         self.bars[k].set_highlight(False)
    #
    #     return i + 1
    #
    # def quicksort(self):
    #     stack = [(0, len(self.array) - 1)]
    #
    #     while stack:
    #         low, high = stack.pop()
    #         print(f"Processing partition({low}, {high})")
    #         if low < high:
    #             pivot = self.partition(low, high)
    #             print(f"Pivot at index {pivot}, stack before push: {stack}")
    #             stack.append((low, pivot - 1))  # Đẩy phần bên trái vào stack
    #             stack.append((pivot + 1, high))
    #             print(f"Stack after push: {stack}")