from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
from shape import Bar


class BubbleSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.start_button.setEnabled(False)

        self.gen = self.bubble_sort()
        self.next_step()
        # self.start_button.setEnabled(True)

    def bubble_sort(self):
        for i in range(len(self.bars) - 1):
            for j in range(len(self.bars) - 1 - i):
                yield "compare", j
                yield "compare", j+1

                # self.bars[j].set_highlight(True)
                # self.bars[j+1].set_highlight(True)

                if self.array[j] > self.array[j + 1]:
                    yield "swap", j, j + 1
                    # self.swap_bars(j, j+1)

                yield "reset_highlight", j
                yield "reset_highlight", j+1
                # self.bars[j].set_highlight(False)
                # self.bars[j + 1].set_highlight(False)

            yield "highlight", len(self.bars) - 1 - i, Bar.success_color
            yield None
            #self.bars[len(self.bars) - 1 - i].set_highlight(True, Bar.success_color)

        yield "highlight", 0, Bar.success_color
        yield None
        #self.bars[0].set_highlight(True, Bar.success_color)
