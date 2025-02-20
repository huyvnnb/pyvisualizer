from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
from shape import Bar


class BubbleSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.start_button.setEnabled(False)

        for i in range(len(self.bars) - 1):
            for j in range(len(self.bars) - 1 - i):
                self.bars[j].set_highlight(True)
                self.bars[j+1].set_highlight(True)

                QTimer.singleShot(700, self.loop.quit)  # Đợi để thấy highlight
                self.loop.exec()

                if self.array[j] > self.array[j + 1]:
                    self.swap_bars(j, j+1)

                self.bars[j].set_highlight(False)
                self.bars[j + 1].set_highlight(False)

            self.bars[len(self.bars) - 1 - i].set_highlight(True, Bar.success_color)

        self.bars[0].set_highlight(True, Bar.success_color)
