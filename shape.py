from PySide6.QtCore import QRectF, Property
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsObject


class Bar(QGraphicsObject):
    success_color = QColor("#00F060")
    compare_color = QColor("#F6D57A")
    default_color = QColor("deepskyblue")

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.setPos(x, y)
        self.color = self.default_color  # Màu hiện tại

    # Override: return QRectF
    def boundingRect(self):
        return self.rect

    # Draw object
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


class Node(QGraphicsObject):
    pass
