#-----------------------------------------------------------------
#                   HEAP SORT
#-----------------------------------------------------------------

def heapify(arr, n, i):
    """
        heapify function ==> preserves the maximum heap property in the root subtree i.
        Assumes that the left and right subtrees are already heaps.
        arr: list of numbers
        n: heap size (number of valid elements in the array)
        i: index of the root of the subtree
    """
    largest = i          # Meaning ==> Root is Biggest
    left = 2 * i + 1     # Left child index
    right = 2 * i + 2    # Right child index

    # If Left child Bigger than Right child
    if left < n and arr[left] > arr[largest]:
        largest = left

    # If Right child Bigger than Left child
    if right < n and arr[right] > arr[largest]:
        largest = right

    # If the right child is greater than the largest current
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]   # Swap
        heapify(arr, n, largest)   #  Heapify on Subtree is changed

def build_heap(arr):
    
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

def heap_sort(arr):
    
    n = len(arr)

    # Step 1 ==> Build the maximum heap
    build_heap(arr)

    # Step 2 ==> Extract elements from the heap one by one
    for i in range(n - 1, 0, -1):
        # Swap the root (largest element) with the last element
        arr[0], arr[i] = arr[i], arr[0]
        # heapify on the root by reducing the heap size (i)
        heapify(arr, i, 0)


def print_array(arr):
    print(" ".join(map(str, arr)))

# Main
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]
    print(" BEFORE SORTING : ")
    print_array(arr)

    heap_sort(arr)

    print(" AFTER SORTING : ")
    print_array(arr)