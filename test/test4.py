import sys, random, math
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit,
    QGraphicsView, QGraphicsScene, QLineEdit, QLabel, QGraphicsItem
)
from PySide6.QtGui import QBrush, QPen, QColor, QPainter, QPolygonF, QFont
from PySide6.QtCore import Qt, QPointF

# --- Lớp NodeCircle: Vẽ đỉnh dưới dạng hình tròn có nhãn ---
from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem


class NodeCircle(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, value="", color=QColor("skyblue"), *args, **kwargs):
        # Vẽ hình tròn với tâm tại (0,0) rồi dịch chuyển đến (x,y)
        super().__init__(-radius, -radius, 2*radius, 2*radius, *args, **kwargs)
        self.setPos(x, y)
        self.radius = radius
        self.value = value
        self.setBrush(QBrush(color))
        self.setPen(QPen(Qt.black))
        
        # Tạo QGraphicsTextItem để hiển thị nhãn node, căn giữa
        self.label = QGraphicsTextItem(value, self)
        font = QFont("Arial", 10)
        self.label.setFont(font)
        self.label.setDefaultTextColor(Qt.black)
        self.setFlags(QGraphicsItem.ItemIsMovable)
        # Đưa nhãn vào giữa node
        self.label.setPos(-self.label.boundingRect().width()/2,
                          -self.label.boundingRect().height()/2)
        
    def setRed(self):
        """Đổi màu của node thành đỏ."""
        self.setBrush(QBrush(QColor("red")))


# --- Lớp Edge: Vẽ cạnh giữa 2 node; nếu đồ thị có hướng thì vẽ thêm mũi tên ---
from PySide6.QtWidgets import QGraphicsLineItem

class Edge(QGraphicsLineItem):
    def __init__(self, nodeA, nodeB, directed=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.directed = directed
        self.pen = QPen(Qt.black, 2)
        self.setPen(self.pen)
        self.arrowSize = 10
        self.updatePosition()

    def updatePosition(self):
        posA = self.nodeA.pos()
        posB = self.nodeB.pos()
        # Tính vector từ nodeA đến nodeB
        delta = posB - posA
        dist = math.hypot(delta.x(), delta.y())
        if dist == 0:
            new_start = posA
            new_end = posB
        else:
            # Tính đơn vị vector theo hướng từ A đến B
            unit = QPointF(delta.x() / dist, delta.y() / dist)
            # Cắt bớt đoạn thẳng sao cho không vẽ vào trong node (bằng bán kính của node)
            new_start = posA + unit * self.nodeA.radius
            new_end = posB - unit * self.nodeB.radius
        self.setLine(new_start.x(), new_start.y(), new_end.x(), new_end.y())

    def paint(self, painter, option, widget):
        # Cập nhật vị trí cạnh trước khi vẽ
        self.updatePosition()
        painter.setPen(self.pen)
        painter.drawLine(self.line())
        
        # Nếu là đồ thị có hướng, vẽ mũi tên
        if self.directed:
            line = self.line()
            angle = math.atan2(-line.dy(), line.dx())
            p2 = line.p2()
            arrowP1 = p2 + QPointF(math.cos(angle + math.pi/6) * -self.arrowSize,
                                   -math.sin(angle + math.pi/6) * -self.arrowSize)
            arrowP2 = p2 + QPointF(math.cos(angle - math.pi/6) * -self.arrowSize,
                                   -math.sin(angle - math.pi/6) * -self.arrowSize)
            arrowHead = QPolygonF([p2, arrowP1, arrowP2])
            painter.setBrush(self.pen.color())
            painter.drawPolygon(arrowHead)

# --- Lớp GraphWidget: Hiển thị đồ thị trên QGraphicsScene ---
class GraphWidget(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.nodes = {}   # Lưu các NodeCircle theo id (nhãn)
        self.edges = []   # Lưu các Edge
        self.setRenderHint(QPainter.Antialiasing)

    def buildGraph(self, inputText, directed=False):
        # Xóa nội dung cũ
        self.scene.clear()
        self.nodes = {}
        self.edges = []
        
        # Phân tích dữ liệu: mỗi dòng chứa "u v" (u, v là nhãn của node)
        edges_input = []
        lines = inputText.strip().splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) < 2:
                continue
            u, v = parts[0], parts[1]
            edges_input.append((u, v))
        
        # Lấy tập các node từ dữ liệu cạnh
        node_ids = set()
        for u, v in edges_input:
            node_ids.add(u)
            node_ids.add(v)
        node_ids = list(node_ids)
        n = len(node_ids)
        
        # Khởi tạo vị trí ban đầu cho các node (trong vùng cố định)
        width, height = 400, 400
        positions = {}
        for node_id in node_ids:
            positions[node_id] = QPointF(random.uniform(-width/2, width/2),
                                         random.uniform(-height/2, height/2))
        
        # Thuật toán force-directed layout đơn giản
        iterations = 50
        area = width * height
        k = math.sqrt(area / n)
        disp = {node_id: QPointF(0, 0) for node_id in node_ids}
        
        for _ in range(iterations):
            for v in node_ids:
                disp[v] = QPointF(0, 0)
            # Lực đẩy giữa các node
            for i in range(n):
                for j in range(i+1, n):
                    u = node_ids[i]
                    v = node_ids[j]
                    delta = positions[u] - positions[v]
                    distance = math.hypot(delta.x(), delta.y()) + 0.01
                    force = k*k / distance
                    dx = delta.x() / distance * force
                    dy = delta.y() / distance * force
                    disp[u] += QPointF(dx, dy)
                    disp[v] -= QPointF(dx, dy)
            # Lực kéo giữa các node có cạnh nối
            for u, v in edges_input:
                delta = positions[u] - positions[v]
                distance = math.hypot(delta.x(), delta.y()) + 0.01
                force = distance*distance / k
                dx = delta.x() / distance * force
                dy = delta.y() / distance * force
                disp[u] -= QPointF(dx, dy)
                disp[v] += QPointF(dx, dy)
            # Cập nhật vị trí với bước nhảy bị giới hạn bởi "temperature"
            temperature = width / 10
            for v in node_ids:
                disp_vector = disp[v]
                disp_length = math.hypot(disp_vector.x(), disp_vector.y())
                if disp_length > 0:
                    factor = min(disp_length, temperature) / disp_length
                    positions[v] += disp_vector * factor
                positions[v].setX(min(width/2, max(-width/2, positions[v].x())))
                positions[v].setY(min(height/2, max(-height/2, positions[v].y())))
        
        # Tạo các NodeCircle với vị trí và nhãn
        for node_id in node_ids:
            pos = positions[node_id]
            nodeItem = NodeCircle(pos.x(), pos.y(), 20, value=node_id, color=QColor("skyblue"))
            self.scene.addItem(nodeItem)
            self.nodes[node_id] = nodeItem

        # Tạo các Edge và thêm vào scene
        for u, v in edges_input:
            nodeA = self.nodes[u]
            nodeB = self.nodes[v]
            edgeItem = Edge(nodeA, nodeB, directed=directed)
            self.scene.addItem(edgeItem)
            self.edges.append(edgeItem)

# --- Giao diện chính của ứng dụng ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vẽ đồ thị với mũi tên và đổi màu node")
        self.resize(800, 700)
        layout = QVBoxLayout(self)
        
        # 2 ô nhập liệu: một cho đồ thị có hướng, một cho đồ thị không hướng
        self.directedInput = QTextEdit()
        self.directedInput.setPlaceholderText("Nhập đồ thị có hướng (mỗi dòng: u v)")
        
        self.undirectedInput = QTextEdit()
        self.undirectedInput.setPlaceholderText("Nhập đồ thị không hướng (mỗi dòng: u v)")
        
        btnLayout = QHBoxLayout()
        self.btnDirected = QPushButton("Start Directed Graph")
        self.btnUndirected = QPushButton("Start Undirected Graph")
        btnLayout.addWidget(self.btnDirected)
        btnLayout.addWidget(self.btnUndirected)
        
        # QGraphicsView để hiển thị đồ thị
        self.graphView = GraphWidget()
        
        # Các điều khiển để đổi màu node thành đỏ
        colorLayout = QHBoxLayout()
        self.nodeIdInput = QLineEdit()
        self.nodeIdInput.setPlaceholderText("Nhập id node cần đổi màu")
        self.btnSetRed = QPushButton("Set Node Red")
        colorLayout.addWidget(QLabel("Node ID:"))
        colorLayout.addWidget(self.nodeIdInput)
        colorLayout.addWidget(self.btnSetRed)
        
        # Sắp xếp layout
        layout.addWidget(self.directedInput)
        layout.addWidget(self.btnDirected)
        layout.addWidget(self.undirectedInput)
        layout.addWidget(self.btnUndirected)
        layout.addWidget(self.graphView)
        layout.addLayout(colorLayout)
        
        # Kết nối sự kiện
        self.btnDirected.clicked.connect(self.startDirected)
        self.btnUndirected.clicked.connect(self.startUndirected)
        self.btnSetRed.clicked.connect(self.setNodeRed)
    
    def startDirected(self):
        inputText = self.directedInput.toPlainText()
        self.graphView.buildGraph(inputText, directed=True)
    
    def startUndirected(self):
        inputText = self.undirectedInput.toPlainText()
        self.graphView.buildGraph(inputText, directed=False)
    
    def setNodeRed(self):
        node_id = self.nodeIdInput.text().strip()
        if node_id in self.graphView.nodes:
            self.graphView.nodes[node_id].setRed()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
