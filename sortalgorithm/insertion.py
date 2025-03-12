from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
from shape import Bar


class InsertionSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.start_button.setEnabled(False)
        self.gen = self.insertion_sort()
        self.next_step()

    def insertion_sort(self):
        yield "highlight", 0, Bar.success_color
        yield None
        # self.bars[0].set_highlight(True, Bar.success_color)
        for i in range(1, len(self.bars)):
            key = self.array[i]
            j = i - 1

            yield "compare", i
            yield None
            #self.bars[i].set_highlight(True)
            while j >= 0 and self.array[j] > key:
                yield "swap", j, j+1
                yield None
                #self.swap_bars(j, j + 1)
                j = j - 1

            yield "highlight", j+1, Bar.success_color
            yield None
            #self.bars[j + 1].set_highlight(True, Bar.success_color)
