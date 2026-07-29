//-----------------------------------------------------------------------
//                      SELECTION SORT
//-----------------------------------------------------------------------

#include <iostream>
using namespace std;

// Selection Func
void selectionSort(int arr[], int n)
{
    for(int i = 0; i < n - 1; i++)
    {
        // Assume the smallest element is at index i
        int minindex = i;

        for(int j = i + 1; j < n; j++)
        {
            if(arr[j] < arr[minindex])
            {
                minindex = j;
            }
        }

        // Move the smallest element to element i
        if(minindex != i)
        {
            swap(arr[i], arr[minindex]);
        }
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
    selectionSort(arr, n);

    cout << " AFTER SORTING : ";
    printArray(arr, n);

    return 0;
}