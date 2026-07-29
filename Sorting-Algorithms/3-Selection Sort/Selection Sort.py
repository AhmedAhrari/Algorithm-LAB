#---------------------------------------------------------------------------
#                       SELECTION SORT
#---------------------------------------------------------------------------

def selection_sort(arr):
    n = len(arr)
    
    # Move on the boundary between the ordered and unordered section
    for i in range(n - 1):
        # Assume the smallest element is at index i
        min_index = i
        
        # Find the smallest element in the unordered part
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        
        # Swap the smallest element with the first element of the unordered section (i)
        if min_index != i:
            arr[i], arr[min_index] = arr[min_index], arr[i]  # Change in 0ne line



def print_array(arr):
    print(" ".join(map(str, arr)))


# Main Program
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]
    
    print("BEFORE SORTING :", end=" ")
    print_array(arr)
    
    selection_sort(arr)
    
    print("AFTER SORTING :", end=" ")
    print_array(arr)