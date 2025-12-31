import time

def bubbleSort(arr, draw_func, delay):
    n = len(arr)
    while True:
        swap = False
        for i in range(n - 1):
            draw_func(arr, [i, i + 1])
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swap = True
            time.sleep(delay)

        if not swap:
            break
        n -= 1
        draw_func(arr, [])
        
    draw_func(arr, range(len(arr)), True)
    return arr