from PySide6.QtCore import QRectF, Property
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QGraphicsObject


class Bar(QGraphicsObject):
    success_color = QColor("#00F060")

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = QRectF(0, 0, width, height)
        self.setPos(x, y)
        self.default_color = QColor("deepskyblue")  # Màu mặc định
        self.color = self.default_color  # Màu hiện tại
        # self._iterate_color = ""

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

    def set_highlight(self, highlight, color="#F6D57A"):
        """Thay đổi màu khi đang xét"""
        self.color = color if highlight else self.default_color
        self.update()  # Vẽ lại


class Node(QGraphicsObject):
    pass
