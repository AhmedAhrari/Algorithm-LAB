#----------------------------------------------------------------------
#                   INSERTION SORT 
#----------------------------------------------------------------------

def insertion_sort(arr):
    n = len(arr)
    
    # Start From Second Element
    for i in range(1, n):
        key = arr[i]        
        j = i - 1           
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        
        arr[j + 1] = key



def print_array(arr):
    print(" ".join(map(str, arr)))


# Main Program
if __name__ == "__main__":
    arr = [64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90]
    
    print("BEFORE SORTING :", end=" ")
    print_array(arr)
    
    insertion_sort(arr)
    
    print("AFTER SORTING  :", end=" ")
    print_array(arr)