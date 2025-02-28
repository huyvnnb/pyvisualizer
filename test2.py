from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsObject
from PySide6.QtGui import QPainter, QBrush, QColor, QFont
from PySide6.QtCore import QRectF, Property
import sys

class Node(QGraphicsObject):
    def __init__(self, x, y, radius, value=None):
        super().__init__()
        self.radius = radius
        self.rect = QRectF(-radius, -radius, 2 * radius, 2 * radius)  # Hình tròn có tâm (0,0)
        self.setPos(x, y)
        self.default_color = QColor("deepskyblue")
        self.color = self.default_color
        self.value = value  # Giá trị hiển thị trong node
        # self.setFlag(QGraphicsObject.ItemIsMovable)

    def boundingRect(self):
        return self.rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawEllipse(self.rect)  # Vẽ hình tròn

        if self.value is not None:
            painter.setPen(QColor("black"))
            painter.setFont(QFont("Arial", 14))
            painter.drawText(self.rect, 0x84, str(self.value))  # 0x84 = Qt.AlignCenter

    def set_highlight(self, highlight, color="#F6D57A"):
        """Thay đổi màu khi đang xét"""
        self.color = QColor(color) if highlight else self.default_color
        self.update()


# Tạo ứng dụng
app = QApplication(sys.argv)

# Tạo Scene và View
scene = QGraphicsScene()
view = QGraphicsView(scene)
view.setRenderHint(QPainter.Antialiasing)

# Thêm các Node hình tròn vào Scene
scene.addItem(Node(50, 50, 30, "A"))
scene.addItem(Node(150, 100, 40, "B"))
scene.addItem(Node(250, 200, 50, "C"))

# Hiển thị
view.show()
sys.exit(app.exec())
