import time

def insertionSort(arr, draw_func, delay):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            draw_func(arr, [j, j + 1])
            arr[j+1] = arr[j]
            j -= 1
            time.sleep(delay)
        
        arr[j+1] = key
        draw_func(arr, [i, j + 1])
        time.sleep(delay)

    draw_func(arr, range(len(arr)), True)
    return arr