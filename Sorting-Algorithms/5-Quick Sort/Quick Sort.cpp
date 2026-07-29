//-------------------------------------------------------------------
//                  QUICK SORT
//-------------------------------------------------------------------

#include <iostream>
using namespace std;

// Partition function using Lomuto method
// Selects the last element of the array as the pivot
int partition(int arr[], int low, int high)
{
    int pivot = arr[high];   // select pivot (last element)
    int i = low - 1;        // Index of the smallest element

    // Check all elements except pivot
    for(int j = low; j < high; j++)
    {
        // If the current element is smaller than or equal to pivot
        if (arr[j] <= pivot)
        {
            i++;                     
            swap(arr[i], arr[j]);
        }
    }

    // Place the pivot in the right place (between the two sections)
    swap(arr[i + 1], arr[high]);
    return i + 1;                   
}


// Main Quick Sort Func (Recursive)
void quickSort(int arr[], int low, int high)
{
    if (low < high)
    {
        // Split the array and get the pivot index
        int pi = partition(arr, low, high);

        // Sort the left part (SMALLER)
        quickSort(arr, low, pi - 1);
        // Sort the right part (LARGER)
        quickSort(arr, pi + 1, high);
    }
}


void printArray(int arr[], int size)
{
    for (int i = 0; i < size; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}


    int main()
    {
        int arr[] = {64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90};
        int n = sizeof(arr) / sizeof(arr[0]);

        cout << " BEFORE SORTING : ";
        printArray(arr, n);

        quickSort(arr, 0, n - 1);

        cout << " AFTER SORTING  : ";
        printArray(arr, n);

        return 0;
    }