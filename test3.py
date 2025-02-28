from PySide6.QtCore import QRectF, Property, QTimer, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QAbstractAnimation
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsObject, QWidget, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout, QApplication
import sys

class Bar(QGraphicsObject):
    success_color = QColor("#00F060")  # Màu xanh lá khi hoàn thành
    compare_color = QColor("#F6D57A")  # Màu vàng khi đang so sánh
    default_color = QColor("deepskyblue")  # Màu mặc định

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.setPos(x, y)
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

    def set_highlight(self, highlight, color=None):
        """
        Thay đổi màu thanh khi đang xét.
        - Nếu `highlight` là True, đổi sang màu `color` (hoặc mặc định `compare_color` nếu không truyền).
        - Nếu `highlight` là False, trả về màu mặc định.
        """
        if highlight:
            self.color = color if color else self.compare_color
        else:
            self.color = self.default_color
        self.update()  # Vẽ lại


class Visualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.start_button = QPushButton("Start")

        self.speed = 4.0

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.start_button)
        self.setLayout(layout)


class SortVisualizer(Visualizer):
    def __init__(self, array):
        super().__init__()
        self.array = array
        self.bars = []
        self.animations = []  # Danh sách giữ các animation để tránh bị thu gom rác
        self.create_bars()
        self.start_button.clicked.connect(self.start_sorting)

    def start_sorting(self):
        pass  # sẽ override ở lớp kế thừa

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
        # Hoán đổi trong mảng
        self.array[i], self.array[j] = self.array[j], self.array[i]

        # Tạo animation di chuyển
        bar1 = QPropertyAnimation(self.bars[i], b"x_pos")
        bar2 = QPropertyAnimation(self.bars[j], b"x_pos")

        duration = 1000 / self.speed
        bar1.setDuration(duration)
        bar2.setDuration(duration)

        bar1.setEasingCurve(QEasingCurve.InOutQuad)
        bar2.setEasingCurve(QEasingCurve.InOutQuad)

        bar1.setEndValue(self.bars[j].x())
        bar2.setEndValue(self.bars[i].x())

        swap_group = QParallelAnimationGroup()
        swap_group.addAnimation(bar1)
        swap_group.addAnimation(bar2)

        # Hoán đổi thanh trong danh sách bars
        self.bars[i], self.bars[j] = self.bars[j], self.bars[i]

        # Lưu lại animation để tránh bị thu gom rác
        self.animations.append(swap_group)
        # Sau khi animation hoàn thành, loại bỏ khỏi danh sách
        swap_group.finished.connect(lambda: self.animations.remove(swap_group))
        swap_group.start()

    def stop_sorting(self):
        # Dừng mọi animation nếu cần
        for bar in self.bars:
            animations = bar.findChildren(QAbstractAnimation)
            for animation in animations:
                animation.stop()


class QuickSort(SortVisualizer):
    def __init__(self, array):
        super().__init__(array)
        self.gen = None  # Sẽ lưu trữ generator

    def start_sorting(self):
        """
        - Vô hiệu hóa nút Start để tránh nhấn lại khi đang chạy.
        - Tạo generator cho quicksort toàn bộ mảng.
        - Bắt đầu chạy từng bước bằng next_step().
        """
        self.start_button.setEnabled(False)
        self.gen = self.quicksort_generator(0, len(self.array) - 1)
        self.next_step()

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

    def quicksort_generator(self, low, high):
        """
        Triển khai QuickSort dưới dạng generator.
        Mỗi thao tác chính sẽ `yield` để báo cho giao diện cập nhật.
        """
        if low < high:
            pivot_index = yield from self.partition_generator(low, high)
            # Gọi đệ quy cho phần bên trái
            yield from self.quicksort_generator(low, pivot_index - 1)
            # Gọi đệ quy cho phần bên phải
            yield from self.quicksort_generator(pivot_index + 1, high)
        else:
            # Nếu đoạn [low..high] chỉ có 1 phần tử, đánh dấu xanh lá (đã sắp xếp xong)
            if 0 <= low < len(self.bars):
                yield ("highlight", low, Bar.success_color)  # Yield action highlight
            yield None  # Yield None để tiếp tục bước tiếp theo mà không có hành động

    def partition_generator(self, low, high):
        """
        Hàm partition, cũng dưới dạng generator.
        - Mỗi lần so sánh/hoán đổi, ta `yield` để hiển thị trực quan.
        """
        pivot_value = self.array[high]
        # Highlight pivot bằng màu so sánh
        yield ("highlight", high, Bar.compare_color)  # Yield action highlight
        yield None  # Yield None để tiếp tục bước tiếp theo mà không có hành động

        i = low - 1
        for j in range(low, high):
            # Highlight bar[j] khi so sánh
            yield ("compare", j)  # Yield action compare
            yield None  # Để giao diện kịp update

            if self.array[j] < pivot_value:
                i += 1
                yield ("swap", i, j)  # Yield action swap
                yield None  # Sau khi hoán đổi

            # Tắt highlight bar[j]
            yield ("reset_highlight", j)  # Yield action reset_highlight
            yield None

        # Đưa pivot vào vị trí chính xác (i+1)
        yield ("swap", i + 1, high)  # Yield action swap
        yield None
        # Tắt highlight pivot cũ
        yield ("reset_highlight", high)  # Yield action reset_highlight
        yield None
        # Đánh dấu pivot mới là màu xanh (đã xong)
        yield ("highlight", i + 1, Bar.success_color)  # Yield action highlight
        yield None

        return i + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    array = [9, 8, 7, 6, 10]
    print(array)
    window = QuickSort(array)
    window.show()
    sys.exit(app.exec())
