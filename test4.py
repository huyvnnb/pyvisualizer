# --- File: graphwindow.py ---
import random
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QGridLayout, QLineEdit, QLabel

from graphalgorithm import Dijkstra
from visualizer import GraphVisualizer

class GraphWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Graph Algorithm Visualizer")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Lưới chọn thuật toán
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        # Nhập mảng
        self.input_layout = QHBoxLayout()
        self.graph_input = QLineEdit()
        self.random_button = QPushButton("Randomize")
        graph_label = QLabel("Graph: ")
        self.graph_input.setPlaceholderText("Enter numbers separated by commas")

        self.random_button.clicked.connect(self.generate_random_graph)

        self.input_layout.addWidget(graph_label)
        self.input_layout.addWidget(self.graph_input)
        self.input_layout.addWidget(self.random_button)

        # Thêm nút Start Dijkstra
        self.start_button = QPushButton("Start Dijkstra")
        self.start_button.clicked.connect(self.start_dijkstra)
        self.input_layout.addWidget(self.start_button)

        self.layout.addLayout(self.input_layout)

        # Khu vực chứa widget thuật toán (Căn giữa)
        self.center_layout = QHBoxLayout()
        self.layout.addLayout(self.center_layout)

        # QStackedWidget để chuyển đổi giữa các thuật toán
        self.stacked_widget = QStackedWidget()
        self.center_layout.addWidget(self.stacked_widget, alignment=Qt.AlignCenter)

        # Danh sách thuật toán (placeholder)
        self.algorithms = ["Dijkstra", "Prim", "Topo Sort"]
        self.algorithm_widgets = {}
        self.selected_button = None
        self.create_ui()

        # Tạo và thêm GraphVisualizer vào stacked_widget
        self.graphvisualier = GraphVisualizer()
        self.stacked_widget.addWidget(self.graphvisualier)
        
        # Lưu dữ liệu danh sách kề (mapping NodeCircle -> [Edge, ...])
        self.graph_adjacent_object = {}
        self.dijkstra = Dijkstra()

    def create_ui(self):
        cols = 3
        row, col = 0, 0
        for name in self.algorithms:
            self.add_algorithm(name, row, col)
            col += 1
            if col >= cols:
                col = 0
                row += 1

    def add_algorithm(self, name, row, col):
        button = QPushButton(name)
        button.clicked.connect(lambda: self.show_algorithm_widget(name, button))
        self.grid_layout.addWidget(button, row, col)
        self.algorithm_widgets[name] = None
        self.stacked_widget.addWidget(QWidget())  # Placeholder

    def show_algorithm_widget(self, name, button):
        if self.selected_button:
            self.selected_button.setStyleSheet("")
        button.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E04D2B;
            }
            QPushButton:pressed {
                background-color: #C44124;
            }
        """)
        self.selected_button = button

        graph_adjacent = self.get_adjacent_list_from_input()
        # Xây dựng đồ thị trực quan; lưu mapping {NodeCircle: [Edge, ...]} vào graph_adjacent_object
        self.graph_adjacent_object = self.graphvisualier.buildGraph(graph_adjacent)
        self.stacked_widget.setCurrentWidget(self.graphvisualier)

    def get_adjacent_list_from_input(self):
        graph_str = self.graph_input.text().strip()
        adjacent_list = {}
        if not graph_str:
            return adjacent_list
        edges = graph_str.split(",")
        for edge in edges:
            parts = edge.strip().split()
            if len(parts) < 3:
                continue
            try:
                u = int(parts[0])
                v = int(parts[1])
                w = float(parts[2])
            except ValueError:
                continue
            if u not in adjacent_list:
                adjacent_list[u] = []
            if v not in adjacent_list:
                adjacent_list[v] = []
            adjacent_list[u].append((v, w))
        return adjacent_list

    def generate_random_graph(self):
        num_vertices = 7
        num_edges = 9
        vertices = list(range(1, num_vertices + 1))
        random.shuffle(vertices)
        edges = []
        existing_edges = set()
        for i in range(1, num_vertices):
            u = vertices[i - 1]
            v = vertices[i]
            weight = random.randint(1, 10)
            edges.append((u, v, weight))
            existing_edges.add((min(u, v), max(u, v)))
        while len(edges) < num_edges:
            u, v = random.sample(vertices, 2)
            edge_key = (min(u, v), max(u, v))
            if edge_key in existing_edges:
                continue
            weight = random.randint(1, 10)
            edges.append((u, v, weight))
            existing_edges.add(edge_key)
        edge_strs = [f"{u} {v} {w}" for u, v, w in edges]
        graph_str = ", ".join(edge_strs)
        self.graph_input.setText(graph_str)

    # --- Phần chạy thuật toán Dijkstra và animate các bước ---
    def start_dijkstra(self):
        dske = self.get_adjacent_list_from_input()
        if not dske:
            return
        # Chọn đỉnh xuất phát (ở đây dùng đỉnh đầu tiên)
        start_vertex = list(dske.keys())[0]
        self.steps = self.dijkstra.GetStep(dske, start_vertex)
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.timer.start(1000)  # 1 bước/giây

    def show_next_step(self):
        if self.step_index >= len(self.steps):
            self.timer.stop()
            return
        step = self.steps[self.step_index]
        costs = step['costs']
        current = step['current']

        # Reset màu cho tất cả các Node và Edge
        for node in self.graphvisualier.nodeItems.values():
            node.defau()
        for edges in self.graph_adjacent_object.values():
            for edge in edges:
                edge.set_default()

        # Highlight node đang được xử lý
        if current is not None and current in self.graphvisualier.nodeItems:
            currentNode = self.graphvisualier.nodeItems[current]
            currentNode.highlight()
            # Highlight các cạnh xuất phát từ node này (nếu có)
            if currentNode in self.graph_adjacent_object:
                for edge in self.graph_adjacent_object[currentNode]:
                    edge.set_highlight()
        # Sau khi update highlight cho Node và Edge, cập nhật trạng thái hiển thị:
        self.graphvisualier.updateStatus(step['queue'], step['costs'])

        # (Có thể cập nhật thêm thông tin hiển thị trạng thái queue, bảng costs, v.v.)

        self.step_index += 1
