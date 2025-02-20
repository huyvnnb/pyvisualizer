from PySide6.QtCore import QEventLoop, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout
from shape import Bar


class Visualizer(QWidget):
    def __init__(self, /):
        super().__init__()
        self.setFixedSize(600, 400)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.start_button = QPushButton("Start")

        self.speed = 1.0

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.start_button)
        self.setLayout(layout)


class SortVisualizer(Visualizer):
    def __init__(self, array):
        super().__init__()
        self.array = array
        self.loop = QEventLoop()

        self.bars = []
        self.create_bars()
        self.speed = 1.0
        self.start_button.clicked.connect(self.start_sorting)

    def start_sorting(self):
        pass

    def create_bars(self):
        max_value = max(self.array)
        bar_width = 40
        spacing = 10
        start_x = 50

        for i, value in enumerate(self.array):
            height = (value / max_value) * 200
            rect = Bar(start_x + i * (bar_width + spacing), 250 - height, bar_width, height)
            self.scene.addItem(rect)
            self.bars.append(rect)

    def swap_bars(self, i, j):
        self.array[i], self.array[j] = self.array[j], self.array[i]

        bar1 = QPropertyAnimation(self.bars[i], b"x_pos")
        bar2 = QPropertyAnimation(self.bars[j], b"x_pos")

        bar1.setDuration(1000 / self.speed)
        bar2.setDuration(1000 / self.speed)

        bar1.setEasingCurve(QEasingCurve.InOutQuad)
        bar2.setEasingCurve(QEasingCurve.InOutQuad)

        bar1.setEndValue(self.bars[j].x())
        bar2.setEndValue(self.bars[i].x())

        swap_group = QParallelAnimationGroup()
        swap_group.addAnimation(bar1)
        swap_group.addAnimation(bar2)

        swap_group.finished.connect(self.loop.quit)

        swap_group.start()
        self.loop.exec()

        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]


class GraphVisualizer(Visualizer):
    pass




