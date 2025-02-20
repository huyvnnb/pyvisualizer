from PySide6.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QVBoxLayout, QLineEdit, \
    QHBoxLayout
from PySide6.QtGui import QPixmap

# Import các thuật toán (giả sử chúng đã được định nghĩa)
from algorithm import BubbleSort, InsertionSort, MergeSort


class SortingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sorting Algorithm Selector")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Thêm phần nhập array
        self.input_layout = QHBoxLayout()
        self.array_input = QLineEdit()
        self.array_input.setPlaceholderText("Enter numbers separated by commas")
        self.input_layout.addWidget(QLabel("Array: "))
        self.input_layout.addWidget(self.array_input)
        self.layout.addLayout(self.input_layout)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.algorithms = {
            "Bubble Sort": "BubbleSort",
            "Insertion Sort": "InsertionSort",
            "Merge Sort": "MergeSort"
        }

        self.create_ui()

    def create_ui(self):
        row, col = 0, 0
        for name, algo_class in self.algorithms.items():
            widget = self.create_algorithm_widget(name, algo_class)
            self.grid_layout.addWidget(widget, row, col)
            col += 1
            if col > 1:  # Giới hạn 2 cột mỗi hàng
                col = 0
                row += 1

    def create_algorithm_widget(self, name, algo_class):
        widget = QWidget()
        layout = QVBoxLayout()

        # Ảnh minh họa (giả sử đã có ảnh trong thư mục images)
        image_label = QLabel()
        pixmap = QPixmap(f"images/sort.png")
        image_label.setPixmap(pixmap.scaled(100, 100))

        # Nút chọn thuật toán
        button = QPushButton(name)
        button.clicked.connect(lambda: self.run_algorithm(algo_class))

        layout.addWidget(image_label)
        layout.addWidget(button)
        widget.setLayout(layout)
        return widget

    def run_algorithm(self, algo_class):
        array_str = self.array_input.text()
        try:
            array = [int(x.strip()) for x in array_str.split(",")]
            algorithm_class = globals()[algo_class]  # Lấy class từ tên
            algorithm = algorithm_class(array)
            algorithm.start_sorting()  # Gọi phương thức chạy thuật toán
        except ValueError:
            print("Invalid input! Please enter numbers separated by commas.")
        except KeyError:
            print(f"Algorithm {algo_class} not found!")


if __name__ == "__main__":
    app = QApplication([])
    window = SortingApp()
    window.show()
    app.exec()
