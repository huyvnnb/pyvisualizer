# --- File: dijkstra.py ---
import heapq

class Dijkstra:
    def __init__(self):
        pass

    def GetStep(self, dske, dinhbatdau):
        """
        Trả về một danh sách các bước, mỗi bước là một dictionary gồm:
            'queue': trạng thái của priority queue (list các tuple (chi phí, đỉnh))
            'costs': dictionary lưu chi phí ngắn nhất từ đỉnh bắt đầu tới mỗi đỉnh
            'current': đỉnh vừa được xử lý (None nếu không có)
        """
        # Khởi tạo bảng chi phí
        costs = {vertex: float('inf') for vertex in dske}
        costs[dinhbatdau] = 0

        # Priority queue 
        pq = [(0, dinhbatdau)]
        heapq.heapify(pq)

        steps = []
        # Lưu trạng thái ban đầu
        steps.append({
            'queue': list(pq),
            'costs': costs.copy(),
            'current': None
        })

        while pq:
            current_cost, current_vertex = heapq.heappop(pq)
            if current_cost > costs[current_vertex]:
                steps.append({
                    'queue': list(pq),
                    'costs': costs.copy(),
                    'current': None
                })
                continue

            current = current_vertex
            for neighbor, weight in dske.get(current_vertex, []):
                if costs[current_vertex] + weight < costs[neighbor]:
                    costs[neighbor] = costs[current_vertex] + weight
                    heapq.heappush(pq, (costs[neighbor], neighbor))
            steps.append({
                'queue': list(pq),
                'costs': costs.copy(),
                'current': current
            })

        return steps
