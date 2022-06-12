from copy import copy

class MinHeap:

    class EmptyHeapError(Exception):
        pass

    def __init__(self, list_in=None):
        if list_in is None:
            self._heap_list = [None]
            self._size = 0
        else:
            self._heap_list = copy.deepcopy(list_in)
            self._size = len(list_in)
            self._heap_list.insert(0, 0)
            self._order_heap()

    @property
    def size(self):
        return self._size


    def insert(self, data):
        self._heap_list.append(None)
        self._size += 1
        child_index = self._size
        while child_index > 1 and data < self._heap_list[child_index // 2]:
            self._heap_list[child_index] = self._heap_list[child_index // 2]
            child_index = child_index // 2
        self._heap_list[child_index] = data


    def _percolate_down(self, hole):
        while hole * 2 <= self._size:
            minimum_child = self._find_minimum_child(hole)
            if self._heap_list[hole] > self._heap_list[minimum_child]:
                saved_off_value = self._heap_list[hole]
                self._heap_list[hole] = self._heap_list[minimum_child]
                self._heap_list[minimum_child] = saved_off_value
            hole = minimum_child


    def _find_minimum_child(self, hole):
        left_child_index  = hole*2
        right_child_index = hole*2 + 1

        if right_child_index > self._size:
            return left_child_index

        elif self._heap_list[left_child_index] < self._heap_list[right_child_index]:
            return left_child_index
        else:
            return right_child_index


    def remove(self):
        if self._size == 0:
            raise MinHeap.EmptyHeapError
        return_value = self._heap_list[1]
        self._heap_list[1] = self._heap_list[self._size]
        self._size -= 1
        self._heap_list.pop()
        if self._size > 0:
            self._percolate_down(1)
        return return_value

    def _order_heap(self):
        for i in range(self._size // 2, 0, -1):
            self._percolate_down(i)