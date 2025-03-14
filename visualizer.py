from PySide6.QtCore import QEventLoop, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QAbstractAnimation, \
    QTimer
from PySide6.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout
from shape import Bar


class Visualizer(QWidget):
    def __init__(self, /):
        super().__init__()
        self.setFixedSize(600, 400)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.start_button = QPushButton("Start")

        self.speed = 1.5

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
        self.animations = []
        self.create_bars()
        self.start_button.clicked.connect(self.start_sorting)
        self.gen = None

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

        bar1.setDuration(500 / self.speed)
        bar2.setDuration(500 / self.speed)

        bar1.setEasingCurve(QEasingCurve.InOutQuad)
        bar2.setEasingCurve(QEasingCurve.InOutQuad)

        bar1.setEndValue(self.bars[j].x())
        bar2.setEndValue(self.bars[i].x())

        swap_group = QParallelAnimationGroup()
        swap_group.addAnimation(bar1)
        swap_group.addAnimation(bar2)

        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]

        self.animations.append(swap_group)
        swap_group.finished.connect(lambda: self.animations.remove(swap_group))
        swap_group.start()

        # swap_group.finished.connect(self.loop.quit)
        #
        # swap_group.start()
        # self.loop.exec()

    def stop_sorting(self):
        for bar in self.bars:
            animations = bar.findChildren(QAbstractAnimation)
            for animation in animations:
                animation.stop()

    def next_step(self):
        """
        Thực hiện 1 "bước" (step) của generator.
        Sau đó, lên lịch cho bước kế tiếp qua QTimer.singleShot.
        """
        try:
            action = next(self.gen)  # Nhận hành động tiếp theo từ generator
            if action:  # Kiểm tra nếu có action trả về
                action_type = action[0]
                params = action[1:]

                if action_type == "compare":
                    j = params[0]
                    self.bars[j].set_highlight(True, Bar.compare_color)
                elif action_type == "swap":
                    i, j = params
                    self.swap_bars(i, j)
                elif action_type == "highlight":
                    index, color = params
                    self.bars[index].set_highlight(True, color)
                elif action_type == "reset_highlight":
                    index = params[0]
                    self.bars[index].set_highlight(False)

            # Điều chỉnh delay theo ý muốn. 300 // self.speed chỉ là ví dụ.
            QTimer.singleShot(int(300 // self.speed), self.next_step)
        except StopIteration:
            # Khi generator kết thúc, kích hoạt lại nút Start.
            self.start_button.setEnabled(True)


class GraphVisualizer(Visualizer):
    pass




