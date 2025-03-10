def quicksort(arr, low, high):
    if low < high:
        pivot_index = partition(arr, low, high)
        quicksort(arr, low, pivot_index - 1)  # Sắp xếp phần bên trái pivot
        quicksort(arr, pivot_index + 1, high)  # Sắp xếp phần bên phải pivot


def partition(arr, low, high):
    pivot = arr[high]  # Chọn pivot là phần tử cuối
    i = low - 1  # Vị trí phần tử nhỏ hơn pivot

    for j in range(low, high):
        if arr[j] < pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]  # Đổi chỗ phần tử nhỏ hơn pivot

    arr[i + 1], arr[high] = arr[high], arr[i + 1]  # Đặt pivot vào đúng vị trí
    return i + 1  # Trả về vị trí mới của pivot


# Chạy thử
arr = [8, 3, 1, 7, 0, 10, 2]
quicksort(arr, 0, len(arr) - 1)
print(arr)  # 👉 [0, 1, 2, 3, 7, 8, 10]
