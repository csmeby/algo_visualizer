import time

def countingSort(arr, exp, draw_func, delay):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = arr[i] // exp
        count[index % 10] += 1
        draw_func(arr, [i])

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        draw_func(arr, [i])

    for i in range(n):
        arr[i] = output[i]
        draw_func(arr, [i])
        time.sleep(delay)

def radixSort(arr, draw_func, delay):
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        countingSort(arr, exp, draw_func, delay)
        exp *= 10
        
    draw_func(arr, range(len(arr)), True)
    return arr