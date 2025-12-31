import time

def selectionSort(arr, draw_func, delay):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            draw_func(arr, [j, min_idx])
            if arr[j] < arr[min_idx]:
                min_idx = j
            time.sleep(delay)

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        draw_func(arr, [i, min_idx])
        time.sleep(delay)

    draw_func(arr, range(len(arr)), True)
    return arr
