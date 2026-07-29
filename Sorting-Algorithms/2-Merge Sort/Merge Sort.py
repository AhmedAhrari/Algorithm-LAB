#--------------------------------------------------------------------------
#                       MERGE SORT
#--------------------------------------------------------------------------

def merge(arr, left, mid, right):
    n1 = mid - left + 1
    n2 = right - mid

    left_arr = [0] * n1
    right_arr = [0] * n2

    for i in range(n1):
        left_arr[i] = arr[left + i]
    for j in range(n2):
        right_arr[j] = arr[mid + 1 + j]

    i = 0       # In leftArr
    j = 0       # In rightArr
    k = left    # Main Array

    # Merge two temporary arrays
    while i < n1 and j < n2:
        if left_arr[i] <= right_arr[j]:
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1

    # Copy the remaining elements of leftArr (if any)
    while i < n1:
        arr[k] = left_arr[i]
        i += 1
        k += 1
    # Copy the remaining elements of rightArr (if any)
    while j < n2:
        arr[k] = right_arr[j]
        j += 1
        k += 1


def merge_sort(arr, left, right):
    if left >= right:
        return

    mid = (left + right) // 2

    # Recursive division
    merge_sort(arr, left, mid)
    merge_sort(arr, mid + 1, right)

    # Merging Two Half Sorted
    merge(arr, left, mid, right)



if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]
    print("BEFORE SORTING :", arr)

    merge_sort(arr, 0, len(arr) - 1)

    print("AFTER SORTED  :", arr)