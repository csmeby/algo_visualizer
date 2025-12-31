import time

def merge(arr, left, mid, right, draw_func, delay):
    left_copy = arr[left:mid + 1]
    right_copy = arr[mid + 1:right + 1]

    left_idx, right_idx = 0, 0
    sorted_idx = left

    while left_idx < len(left_copy) and right_idx < len(right_copy):
        draw_func(arr, [left + left_idx, mid + 1 + right_idx])
        
        if left_copy[left_idx] <= right_copy[right_idx]:
            arr[sorted_idx] = left_copy[left_idx]
            left_idx += 1
        else:
            arr[sorted_idx] = right_copy[right_idx]
            right_idx += 1
        
        draw_func(arr, [sorted_idx])
        sorted_idx += 1
        time.sleep(delay)

    while left_idx < len(left_copy):
        arr[sorted_idx] = left_copy[left_idx]
        left_idx += 1
        sorted_idx += 1
        draw_func(arr, [sorted_idx])
        time.sleep(delay)

    while right_idx < len(right_copy):
        arr[sorted_idx] = right_copy[right_idx]
        right_idx += 1
        sorted_idx += 1
        draw_func(arr, [sorted_idx])
        time.sleep(delay)

def mergeSortAlgorithm(arr, left, right, draw_func, delay):
    if left < right:
        mid = (left + right) // 2
        mergeSortAlgorithm(arr, left, mid, draw_func, delay)
        mergeSortAlgorithm(arr, mid + 1, right, draw_func, delay)
        merge(arr, left, mid, right, draw_func, delay)

def mergeSort(arr, draw_func, delay):
    mergeSortAlgorithm(arr, 0, len(arr) - 1, draw_func, delay)
    draw_func(arr, range(len(arr)), True)
    return arr