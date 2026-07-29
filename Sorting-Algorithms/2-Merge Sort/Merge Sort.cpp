//---------------------------------------------------------------------
//                      MERGE SORT
//---------------------------------------------------------------------

#include <iostream>
#include <vector>
using namespace std;

void merge(vector<int>& arr, int left, int mid, int right)
{
    int n1 = mid - left + 1;    // Left Half
    int n2 = right - mid;       // Right Half


    vector<int> leftArr(n1), rightArr(n2);

    for(int i = 0; i < n1; i++)
        leftArr[i] = arr[left + i];
    for(int j = 0; j < n2; j++)
        rightArr[j] = arr[mid + 1 + j];


    // Start 3 Andis for all 3 Arrays
    int i = 0;          // In leftArr
    int j = 0;          // In rightArr
    int k = left;       // Main Array


    // Merge two temporary arrays in ascending order
    while (i < n1 && j < n2)
    {
        if(leftArr[i] <= rightArr[j])
        {
            arr[k] = leftArr[i];
            i++;
        }

        else
        {
            arr[k] = rightArr[j];
            j++;
        }
        k++;
    }

    // Copy the remaining elements of leftArr (if any)
    while (i < n1)
    {
        arr[k] = leftArr[i];
        i++;
        k++;
    }

    // Copy the remaining elements of rightArr (if any)
    while (j < n2)
    {
        arr[k] = rightArr[j];
        j++;
        k++;
    }
}


// Main Merge Sort Func
void mergeSort(vector<int>& arr, int left, int right)
{
    if(left >= right)
        return;

    int mid = left + (right - left) / 2;    // Protected From Buffering

    // Recursive division
    mergeSort(arr, left, mid);
    mergeSort(arr, mid + 1, right);

    // Merging Two Half Sorted
    merge(arr, left, mid, right);

}


void printArray(const vector<int>& arr)
{
    for(int num : arr)
        cout << num << " ";
    cout << endl;
}


int main()
{
    vector<int> arr = {64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90};

    cout << " BEFORE SORTING : ";
    printArray(arr);

    mergeSort(arr, 0, arr.size() - 1);

    cout << " AFTER SORTED : ";
    printArray(arr);

    return 0;
}
