from PySide6.QtCore import QTimer

from visualizer import SortVisualizer
from shape import Bar


class InsertionSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)

    def start_sorting(self):
        self.start_button.setEnabled(False)

        self.bars[0].set_highlight(True, Bar.success_color)
        for i in range(1, len(self.bars)):
            key = self.array[i]
            j = i - 1

            self.bars[i].set_highlight(True)
            while j >= 0 and self.array[j] > key:

                self.swap_bars(j, j+1)
                j = j - 1

            self.bars[j+1].set_highlight(True, Bar.success_color)
            QTimer.singleShot(700 / self.speed, self.loop.quit)  # Đợi để thấy highlight
            self.loop.exec()
