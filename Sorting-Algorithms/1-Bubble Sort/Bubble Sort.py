#----------------------------------------------------
#               BUBBLE SORT
#----------------------------------------------------

"""
        Bubble Sort ==> Sorting In-Place array
"""
def bubble_sort(arr):
    n = len(arr)
    
    # Traverse the entire array
    for i in range(n - 1):
        swapped = False     # Optimizing Flag
        
        # Compare adjacent elements to the end of the unsorted section
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                temp = arr[j]
                arr[j] = arr[j + 1]
                arr[j + 1] = temp
                swapped = True
                
        if not swapped:
            break
        
def print_array(arr):
    for val in arr:
        print(val, end = " ")
    print()
    
# The Main Program
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]
    
    print(" BEFORE SORTING : ", end = " ")
    print_array(arr)
    
    bubble_sort(arr)
    
    print(" AFTER SORTING : ", end = " ")
    print_array(arr)