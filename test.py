import sys
from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsObject, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import (
    QPropertyAnimation, QEventLoop, Qt, Property,
    QSequentialAnimationGroup, QRectF, QParallelAnimationGroup,
    QEasingCurve, QTimer
)
import random


class AnimatedBar(QGraphicsObject):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.setPos(x, y)
        self.default_color = QColor("deepskyblue")  # Màu mặc định
        self.color = self.default_color  # Màu hiện tại

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(self.rect)

    def get_x_pos(self):
        return self.x()

    def set_x_pos(self, value):
        self.setX(value)

    x_pos = Property(float, get_x_pos, set_x_pos)

    def set_highlight(self, highlight, color="#F6D57A"):
        """Thay đổi màu khi đang xét"""
        self.color = color if highlight else self.default_color
        self.update()  # Vẽ lại


class BubbleSortVisualizer(QWidget):
    def __init__(self, array):
        super().__init__()
        self.setWindowTitle("Bubble Sort Visualization")
        self.setFixedSize(600, 400)
        self.loop = QEventLoop()

        self.array = array
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.start_button = QPushButton("Start")

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.bars = []
        self.create_bars()
        self.start_button.clicked.connect(self.start_sorting)

    def create_bars(self):
        max_value = max(self.array)
        bar_width = 40
        spacing = 10
        start_x = 50

        for i, value in enumerate(self.array):
            height = (value / max_value) * 100
            bar = AnimatedBar(start_x + i * (bar_width + spacing), 250 - height, bar_width, height)
            self.scene.addItem(bar)
            self.bars.append(bar)

    def swap_bars(self, j):
        """Hoán đổi hai cột tại vị trí j và j+1"""
        self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]

        anim1 = QPropertyAnimation(self.bars[j], b"x_pos")
        anim2 = QPropertyAnimation(self.bars[j + 1], b"x_pos")

        anim1.setDuration(1000)
        anim2.setDuration(1000)
        anim1.setEasingCurve(QEasingCurve.InOutQuad)
        anim2.setEasingCurve(QEasingCurve.InOutQuad)

        anim1.setEndValue(self.bars[j + 1].x())
        anim2.setEndValue(self.bars[j].x())

        swap_group = QParallelAnimationGroup()
        swap_group.addAnimation(anim1)
        swap_group.addAnimation(anim2)
        swap_group.finished.connect(self.loop.quit)

        swap_group.start()
        self.loop.exec()

        self.bars[j], self.bars[j + 1] = self.bars[j + 1], self.bars[j]

    def start_sorting(self):
        self.start_button.setEnabled(False)
        for i in range(len(self.bars) - 1):
            for j in range(len(self.bars) - 1 - i):
                self.bars[j].set_highlight(True)
                self.bars[j + 1].set_highlight(True)

                QTimer.singleShot(700, self.loop.quit)  # Đợi để thấy highlight
                self.loop.exec()

                if self.array[j] > self.array[j + 1]:
                    self.swap_bars(j)

                self.bars[j].set_highlight(False)
                self.bars[j + 1].set_highlight(False)

            self.bars[len(self.bars) - 1 - i].set_highlight(True, "#00F060")

        self.bars[0].set_highlight(True, "#00F060")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    array = [random.randint(1, 50) for _ in range(5)]  # Mảng giá trị ban đầu
    print(array)
    window = BubbleSortVisualizer(array)
    window.show()
    sys.exit(app.exec())
