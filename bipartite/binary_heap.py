"""
    This class realise binary heap structure
    based on single dimension list
    child of vertex with index i has index 2*i + 1 and
    2*i + 2 accordingly
"""

class BinaryHeap:
    def __init__(self, values=None):
        if values is None:
            values = []
        self.heap_list = values
        self.__build_heap__()

    def get_heap_size(self):
        return len(self.heap_list)

    def add_element(self, value):
        heap_list = self.heap_list
        heap_list.append(value)
        start_index = self.get_heap_size() - 1
        parent_index = (self.get_heap_size() - 2) // 2

        while start_index > 0 and heap_list[parent_index] < heap_list[start_index]:
            heap_list[parent_index], heap_list[start_index] = heap_list[start_index], heap_list[parent_index]
            start_index = parent_index
            parent_index = (parent_index - 1) // 2


    """
        build heap with heapify method
        complexity of this method is O(N*log(N))
    """
    def __build_heap__(self):
        for i in range(self.get_heap_size() // 2 + 1, -1, -1):
            self.__heapify__(i)

    def __heapify__(self, index):
        heap_size = self.get_heap_size()
        heap_list = self.heap_list

        while True:
            left_child = 2 * index + 1
            right_child = 2 * index + 2
            largest = index

            if left_child < heap_size and heap_list[left_child] > heap_list[largest]:
                largest = left_child

            if right_child < heap_size and heap_list[right_child] > heap_list[largest]:
                largest = right_child

            if largest == index:
                break

            # replace
            heap_list[index], heap_list[largest] =\
                heap_list[largest], heap_list[index]

            index = largest

    def get_root(self):
        result = self.heap_list[0]
        self.heap_list[0] = self.heap_list[self.get_heap_size() - 1]
        self.heap_list.pop()
        # restore binary structure
        self.__heapify__(0)
        return result

## tests

if __name__ == '__main__':
    heap = BinaryHeap([0, 1, 2, 3, 4, 5])
    print(heap.get_heap_size())
    print(heap.heap_list)
    print(heap.get_root())
    print('################################')
    heap.get_root()
    print(heap.heap_list)
    heap.add_element(4)
    print(heap.heap_list)
    heap.add_element(5)
    print(heap.heap_list)

