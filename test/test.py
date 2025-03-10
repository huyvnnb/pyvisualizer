from PySide6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QMainWindow, QPushButton
from PySide6.QtGui import QPen, QColor, QBrush, QLinearGradient
from PySide6.QtCore import Qt, QTimer, QPointF
import sys
import math
import heapq


class Node(QGraphicsEllipseItem):
    """ Định nghĩa Node (đỉnh) trong đồ thị """
    def __init__(self, x, y, name, radius=20):
        super().__init__(-radius, -radius, 2*radius, 2*radius)
        self.setBrush(Qt.white)
        self.setPen(QPen(Qt.black, 2))
        self.setZValue(1)
        self.radius = radius
        self.setPos(x, y)
        self.name = name
        self.text = QGraphicsTextItem(name, self)
        self.text.setPos(-radius / 2, -radius / 2)
        self.edges = []


class Edge(QGraphicsLineItem):
    """ Định nghĩa cạnh (Edge) có hiệu ứng tô màu """
    def __init__(self, nodeA, nodeB, weight, directed=False):
        super().__init__()
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.weight = weight
        self.directed = directed
        self.default_pen = QPen(Qt.black, 2)
        self.highlight_pen = QPen(Qt.blue, 4)
        self.setPen(self.default_pen)
        self.arrowSize = 10
        self.updatePosition()
        self.gradient_progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGradient)
        self.weight_text = QGraphicsTextItem(str(weight))
        self.weight_text.setPos((nodeA.pos().x() + nodeB.pos().x()) / 2,
                                (nodeA.pos().y() + nodeB.pos().y()) / 2)

    def updatePosition(self):
        """ Cập nhật vị trí cạnh để kết nối đúng các node """
        posA = self.nodeA.pos()
        posB = self.nodeB.pos()
        delta = posB - posA
        dist = math.hypot(delta.x(), delta.y())
        if dist == 0:
            new_start = posA
            new_end = posB
        else:
            unit = QPointF(delta.x() / dist, delta.y() / dist)
            new_start = posA + unit * self.nodeA.radius
            new_end = posB - unit * self.nodeB.radius
        self.setLine(new_start.x(), new_start.y(), new_end.x(), new_end.y())

    def startAnimation(self):
        """ Bắt đầu hiệu ứng tô màu cạnh """
        self.gradient_progress = 0
        self.timer.start(50)

    def updateGradient(self):
        """ Cập nhật hiệu ứng tô màu từ trái sang phải """
        if self.gradient_progress >= 1:
            self.timer.stop()
            return

        self.gradient_progress += 0.1
        line = self.line()
        gradient = QLinearGradient(line.p1(), line.p2())
        gradient.setColorAt(0, Qt.blue)
        gradient.setColorAt(self.gradient_progress, Qt.blue)
        gradient.setColorAt(1, Qt.black)
        pen = QPen(QBrush(gradient), 4)
        self.setPen(pen)

    def paint(self, painter, option, widget):
        """ Vẽ cạnh với hiệu ứng tô màu """
        self.updatePosition()
        painter.setPen(self.pen())
        painter.drawLine(self.line())


class GraphVisualizer(QMainWindow):
    """ Giao diện chính để mô phỏng thuật toán Dijkstra """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mô phỏng Dijkstra")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(0, 0, 800, 550)

        self.start_button = QPushButton("Run Dijkstra", self)
        self.start_button.setGeometry(350, 560, 100, 30)
        self.start_button.clicked.connect(self.runDijkstra)

        self.nodes = {}
        self.edges = []
        self.createGraph()

    def createGraph(self):
        """ Tạo đồ thị với các đỉnh và cạnh """
        positions = {
            "A": (100, 100), "B": (300, 100), "C": (500, 100),
            "D": (200, 300), "E": (400, 300), "F": (300, 500)
        }
        for name, (x, y) in positions.items():
            node = Node(x, y, name)
            self.scene.addItem(node)
            self.nodes[name] = node

        edges = [
            ("A", "B", 4), ("A", "D", 1), ("B", "C", 3),
            ("B", "E", 1), ("C", "F", 5), ("D", "E", 2),
            ("E", "F", 3)
        ]
        for node1, node2, weight in edges:
            edge = Edge(self.nodes[node1], self.nodes[node2], weight)
            self.scene.addItem(edge)
            self.scene.addItem(edge.weight_text)
            self.edges.append(edge)
            self.nodes[node1].edges.append(edge)
            self.nodes[node2].edges.append(edge)

    def runDijkstra(self):
        """ Chạy thuật toán Dijkstra từ node A """
        start_node = "A"
        distances = {node: float('inf') for node in self.nodes}
        distances[start_node] = 0
        pq = [(0, start_node)]
        prev = {}

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)

            for edge in self.nodes[curr_node].edges:
                neighbor = edge.nodeB if edge.nodeA.name == curr_node else edge.nodeA
                new_dist = curr_dist + edge.weight

                if new_dist < distances[neighbor.name]:
                    distances[neighbor.name] = new_dist
                    prev[neighbor.name] = (curr_node, edge)
                    heapq.heappush(pq, (new_dist, neighbor.name))

        # Highlight đường đi ngắn nhất
        node = "F"  # Đích
        while node in prev:
            prev_node, edge = prev[node]
            edge.startAnimation()
            node = prev_node


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphVisualizer()
    window.show()
    sys.exit(app.exec())
