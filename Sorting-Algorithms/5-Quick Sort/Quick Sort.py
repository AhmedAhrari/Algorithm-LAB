#---------------------------------------------------
#                   Quick Sort
#---------------------------------------------------
"""
Be sure to note that when executing each method,
put the codes of the previous method in comments (#)
or inside the docstring (""" """).
"""

# ============= The first method ==> Sorting within the same array ==============

def partition(arr, low, high):
    pivot = arr[high]          # Select the last element as the axis
    i = low - 1                # Index of the smaller areas

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]   
    
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1               # Return the pivot index


def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)        # Find the pivot location
        quick_sort(arr, low, pi - 1)          # Sort the left section
        quick_sort(arr, pi + 1, high)         # Sort left section Sort right section



def print_array(arr):
    print(" ".join(map(str, arr)))


# Main Program
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]

    print("BEFORE SORTING :", end=" ")
    print_array(arr)

    quick_sort(arr, 0, len(arr) - 1)

    print("AFTER SORTING  :", end=" ")
    print_array(arr)
    
    
    
    
# ============== Method 2: Pythonic and recursive version (returning a new array) ==================

def quick_sort_pythonic(arr):
    # Return End Condition
    if len(arr) <= 1:
        return arr

    pivot = arr[-1]   # Select axis (last element)

    # Split into two lists: less than or equal to pivot, and greater than pivot
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]

    # Combine sorted sections with pivot in the middle
    return quick_sort_pythonic(left) + [pivot] + quick_sort_pythonic(right)


# Main Program
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]

    print("BEFORE SORTING :", arr)
    
    sorted_arr = quick_sort_pythonic(arr)
    
    print("AFTER SORTING  :", sorted_arr)
    print("ORIGINAL ARRAY :", arr)  # The original array remains intact!
    
