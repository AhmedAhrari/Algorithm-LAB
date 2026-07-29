//--------------------------------------------------------------------------
//                      INSERTION SORT
//--------------------------------------------------------------------------

#include <iostream>
using namespace std;

// Insertion Func
void insertionSort(int arr[], int n)
{
    // Start from the second element (since we consider the first element to be a sorted section of size 1)
    for(int i = 1; i < n; i++)
    {
        int key = arr[i];   // The element we want to place in the right place
        int j = i - 1;
        
        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            j--;
        }

        arr[j + 1] = key;
        
    }
}


void printArray(int arr[], int size)
{
    for(int i = 0; i < size; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}


// Main Program
int main()
{
    int arr[] = {64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90};
    int n = sizeof(arr) / sizeof(arr[0]);

    cout << " BEFORE SORTING : ";
    printArray(arr, n);

    insertionSort(arr, n);

    cout << " AFTER SORTING  : ";
    printArray(arr, n);

    return 0;
}

