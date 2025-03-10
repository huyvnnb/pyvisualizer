from PySide6.QtCore import QTimer
from visualizer import SortVisualizer
from shape import Bar


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
        yield "highlight", high, Bar.compare_color  # Yield action highlight
        yield None  # Yield None để tiếp tục bước tiếp theo mà không có hành động

        i = low - 1
        for j in range(low, high):
            # Highlight bar[j] khi so sánh
            yield "compare", j  # Yield action compare
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

