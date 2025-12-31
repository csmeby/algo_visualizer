import time

def partition(arr, low, high, draw_func, delay):
    i = (low - 1)
    pivot = arr[high]

    for j in range(low, high):
        draw_func(arr, [j, high])
        
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_func(arr, [i, j])
            time.sleep(delay)

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    draw_func(arr, [i + 1, high])
    time.sleep(delay)
    return (i + 1)

def quickSort(arr, draw_func, delay, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low < high:
        pi = partition(arr, low, high, draw_func, delay)

        quickSort(arr, draw_func, delay, low, pi - 1)
        quickSort(arr, draw_func, delay, pi + 1, high)

    if low == 0 and high == len(arr) - 1:
        draw_func(arr, range(len(arr)), True)
    
    return arr