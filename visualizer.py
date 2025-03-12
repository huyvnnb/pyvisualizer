import math
from random import random
from PySide6 import QtGui
from PySide6.QtCore import QEventLoop, QLineF, QPointF, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QAbstractAnimation, \
    QTimer, Qt
from PySide6.QtWidgets import QFrame, QGraphicsEllipseItem, QGraphicsItem, QGraphicsLineItem, QGraphicsTextItem, QMessageBox, QTextEdit, QWidget, QGraphicsScene, QGraphicsView, QPushButton, QVBoxLayout
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

# --- File: visualizer.py ---
import random
import math
from PySide6.QtCore import QPointF
from PySide6.QtGui import QColor, QPen, QPolygonF
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsItem

class GraphVisualizer(QGraphicsView):
    def __init__(self, parent=None):
        # Tạo một QGraphicsScene và gán cho QGraphicsView
        self._scene = QGraphicsScene()
        super().__init__(self._scene, parent)
        self.setScene(self._scene)
        self.nodeItems = {}  # Mapping: vertex (int) -> NodeCircle
        self.setFixedSize(800,600)

    def buildGraph(self, dske):
        """
        dske: dict kiểu {vertex (int): [(neighbor, cost), ...], ...}
        Vẽ đồ thị lên scene và trả về danh sách kề dạng {NodeCircle: [Edge, ...]}
        """
        self._scene.clear()

        # --- Bước 1: Xác định tập hợp các đỉnh ---
        nodes_set = set(dske.keys())
        for neighbors in dske.values():
            for v, cost in neighbors:
                nodes_set.add(v)
        nodes = list(nodes_set)

        # --- Bước 2: Khởi tạo vị trí ngẫu nhiên ---
        width, height = 1000, 800
        positions = {}
        for node in nodes:
            x = random.uniform(-width/2, width/2)
            y = random.uniform(-height/2, height/2)
            positions[node] = QPointF(x, y)

        # --- Bước 3: Tính layout với force-directed ---
        n = len(nodes)
        area = width * height
        k = math.sqrt(area / (n + 1))
        iterations = 100
        disp = {node: QPointF(0, 0) for node in nodes}
        temperature = width / 10.0

        for _ in range(iterations):
            for node in nodes:
                disp[node] = QPointF(0, 0)
            for i in range(n):
                for j in range(i + 1, n):
                    u = nodes[i]
                    v = nodes[j]
                    delta = positions[u] - positions[v]
                    dist = math.hypot(delta.x(), delta.y())
                    if dist == 0:
                        dist = 0.01
                    force = k * k / dist
                    direction = QPointF(delta.x() / dist, delta.y() / dist)
                    disp[u] += direction * force
                    disp[v] -= direction * force
            for u, neighbors in dske.items():
                for v, cost in neighbors:
                    delta = positions[u] - positions[v]
                    dist = math.hypot(delta.x(), delta.y())
                    if dist == 0:
                        dist = 0.01
                    force = (dist * dist) / k
                    direction = QPointF(delta.x() / dist, delta.y() / dist)
                    disp[u] -= direction * force
                    disp[v] += direction * force
            for node in nodes:
                d = disp[node]
                d_len = math.hypot(d.x(), d.y())
                if d_len > 0:
                    factor = min(d_len, temperature) / d_len
                    positions[node] += d * factor
            temperature *= 0.95

        # --- Bước 4: Tạo NodeCircle và thêm vào scene ---
        self.nodeItems = {}
        for node in nodes:
            pos = positions[node]
            nodeItem = NodeCircle(pos.x(), pos.y(), 20, node, QColor("skyblue"))
            self._scene.addItem(nodeItem)
            self.nodeItems[node] = nodeItem

        # --- Bước 5: Tạo Edge và xây dựng danh sách kề dạng {NodeCircle: [Edge, ...]} ---
        adjacency = {}
        for nodeItem in self.nodeItems.values():
            adjacency[nodeItem] = []

        for u, neighbors in dske.items():
            for v, cost in neighbors:
                if u in self.nodeItems and v in self.nodeItems:
                    edgeItem = Edge(self.nodeItems[u], self.nodeItems[v], cost, directed=True)
                    self._scene.addItem(edgeItem)
                    adjacency[self.nodeItems[u]].append(edgeItem)

        return adjacency
    def updateStatus(self, queue, costs):
        """
        Hiển thị trạng thái của thuật toán:
          - Queue hiện tại: danh sách các tuple (chi phí, đỉnh)
          - Bảng khoảng cách: mapping từ đỉnh đến khoảng cách (hiển thị '∞' nếu khoảng cách là vô hạn)
        """
        status_str = "Queue: " + ", ".join(f"({cost:.1f}, {vertex})" for cost, vertex in queue)
        status_str += "\nDistances: " + ", ".join(
            f"{vertex}: {cost if cost != float('inf') else '∞'}" for vertex, cost in costs.items()
        )
        if not hasattr(self, "statusText"):
            self.statusText = QGraphicsTextItem()
            self.statusText.setDefaultTextColor(QColor("black"))
            self._scene.addItem(self.statusText)
            self.statusText.setPos(20, 20)
        self.statusText.setPlainText(status_str)


# --- Lớp Edge ---
class Edge(QGraphicsLineItem):
    def __init__(self, source, dest, cost=1, directed=True):
        super().__init__()
        self.source = source
        self.dest = dest
        self.cost = cost
        # Đảm bảo edge luôn là directed
        self.directed = True  
        self.setPen(QPen(QColor("black"), 2))
        self.adjust()

    def adjust(self):
        line = QLineF(self.source.pos(), self.dest.pos())
        r = 20  # Giả sử bán kính của NodeCircle là 20
        if line.length() == 0:
            return
        dx = line.dx() / line.length()
        dy = line.dy() / line.length()
        newP1 = line.p1() + QPointF(dx * r, dy * r)
        newP2 = line.p2() - QPointF(dx * r, dy * r)
        self.setLine(QLineF(newP1, newP2))

    def paint(self, painter, option, widget):
        self.adjust()
        line = self.line()
        if line.length() == 0:
            return
        painter.setPen(self.pen())
        painter.drawLine(line)

        # Vì đồ thị của bạn luôn là directed nên luôn vẽ mũi tên
        angle = math.atan2(-line.dy(), line.dx())
        arrowSize = 10
        p1 = line.p2() - QPointF(math.sin(angle + math.pi/3) * arrowSize,
                                  math.cos(angle + math.pi/3) * arrowSize)
        p2 = line.p2() - QPointF(math.sin(angle + math.pi - math.pi/3) * arrowSize,
                                  math.cos(angle + math.pi - math.pi/3) * arrowSize)
        arrowHead = QPolygonF([line.p2(), p1, p2])
        painter.setBrush(self.pen().color())
        painter.drawPolygon(arrowHead)

        # Vẽ trọng số cạnh tại vị trí giữa (có thể điều chỉnh offset nếu cần)
        midPoint = line.pointAt(0.5)
        offset = QPointF(0, -10)
        text = str(self.cost)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        painter.drawText(midPoint + offset, text)

    def set_highlight(self):
        self.setPen(QPen(QColor("red"), 3))

    def set_default(self):
        self.setPen(QPen(QColor("black"), 2))

# --- Lớp NodeCircle ---
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PySide6.QtCore import Qt

class NodeCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, value, color):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius)
        self.highlightColor = QColor(Qt.red)
        self.normalColor = color
        self.setPos(x, y)
        self.value = value
        self.setBrush(color)
        self.setPen(QPen(QColor("black")))
        self.textItem = QGraphicsTextItem(str(value), self)
        self.textItem.setPos(-radius/2, -radius/2)
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setCacheMode(QGraphicsItem.NoCache)

    def highlight(self):
        self.setBrush(self.highlightColor)

    def defau(self):
        self.setBrush(self.normalColor)
