import random

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QGridLayout, QLineEdit, \
    QLabel

from algorithm import BubbleSort, InsertionSort, QuickSort
from visualizer import SortVisualizer


class SortingWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Algorithm Visualizer")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Lưới chọn thuật toán
        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        # Nhập mảng
        self.input_layout = QHBoxLayout()
        self.array_input = QLineEdit()
        self.random_button = QPushButton("Randomize")
        array_label = QLabel("Array: ")
        self.array_input.setPlaceholderText("Enter numbers separated by commas")

        self.random_button.clicked.connect(self.generate_random_array)

        self.input_layout.addWidget(array_label)
        self.input_layout.addWidget(self.array_input)
        self.input_layout.addWidget(self.random_button)

        self.layout.addLayout(self.input_layout)

        # Khu vực chứa widget thuật toán (Căn giữa)
        self.center_layout = QHBoxLayout()
        self.layout.addLayout(self.center_layout)

        # QStackedWidget để chuyển đổi giữa các thuật toán
        self.stacked_widget = QStackedWidget()
        self.center_layout.addWidget(self.stacked_widget, alignment= Qt.AlignCenter)

        # Danh sách thuật toán
        self.algorithms = ["Bubble Sort", "Insertion Sort", "Quick Sort"]
        self.algorithm_widgets = {}
        self.selected_button = None
        self.create_ui()

    def create_ui(self):
        """Tạo UI với các thuật toán trong lưới"""
        cols = 3  # Giới hạn số cột
        row, col = 0, 0
        for name in self.algorithms:
            self.add_algorithm(name, row, col)
            col += 1
            if col >= cols:  # Nếu quá số cột, xuống dòng
                col = 0
                row += 1

    def add_algorithm(self, name, row, col):
        """Thêm thuật toán vào giao diện với vị trí hàng/cột"""
        button = QPushButton(name)
        button.clicked.connect(lambda: self.show_algorithm_widget(name, button))
        self.grid_layout.addWidget(button, row, col)

        # Thêm placeholder cho thuật toán này
        self.algorithm_widgets[name] = None
        self.stacked_widget.addWidget(QWidget())  # Placeholder

    def show_algorithm_widget(self, name, button):
        """Hiển thị giao diện của thuật toán, căn giữa"""
        self.stop_sorting()

        if self.selected_button:
            self.selected_button.setStyleSheet("")

        # button.setStyleSheet("background-color: #FF5733; color: white; font-weight: bold;")  # Đổi màu
        button.setStyleSheet("""
            QPushButton {
                background-color: #FF5733;
                color: white;
                font-weight: bold;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #E04D2B; /* Màu hover dịu hơn */
            }
            QPushButton:pressed {
                background-color: #C44124; /* Màu khi nhấn */
            }
        """)
        self.selected_button = button

        array = self.get_array_from_input()
        if array is None:
            return

        if self.algorithm_widgets[name] is not None:
            old_widget = self.algorithm_widgets[name]
            self.stacked_widget.removeWidget(old_widget)
            old_widget.deleteLater()

        widget = AlgorithmFactory.create_algorithm(name, array)
        widget.setFixedSize(500, 400)
        self.algorithm_widgets[name] = widget
        self.stacked_widget.addWidget(widget)
        self.stacked_widget.setCurrentWidget(widget)

    def get_array_from_input(self):
        """Lấy mảng từ input"""
        array_str = self.array_input.text()
        try:
            return [int(x.strip()) for x in array_str.split(",")]
        except ValueError:
            print("Invalid input! Please enter numbers separated by commas.")
            return None

    def generate_random_array(self):
        random_sample = random.sample(range(1, 50), 7)
        self.array_input.setText(", ".join(map(str, random_sample)))

    def stop_sorting(self):
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, SortVisualizer):
            current_widget.stop_sorting()


class AlgorithmFactory:
    @staticmethod
    def create_algorithm(name, array):
        algorithms = {
            "Bubble Sort": BubbleSort,
            "Insertion Sort": InsertionSort,
            "Quick Sort": QuickSort
        }

        if name in algorithms:
            return algorithms[name](array)
        else:
            raise ValueError(f"Algorithm '{name}' not found")
