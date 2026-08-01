//=================================================
//              HEAP SORT
//=================================================

#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// n = Heap Length
// heapify function: preserve the maximum heap property in the root subtree i
void heapify(vector<int>& arr, int n, int i)
{
    int largest = i;    // Meaning ==> Root is Biggest
    int left = 2 * i + 1;   // Left child index
    int right = 2 * i + 2;  // Right child index


    // If Left child Bigger than Right child
    if(left < n && arr[left] > arr[largest])
        largest = left;

    // If Right child Bigger than Left child

    if (right < n && arr[right] > arr[largest])
        largest = right;

    // If the right child is greater than the largest current
    if(largest != i)
    {
        swap(arr[i], arr[largest]);
        heapify(arr, n, largest);       // Heapify on Subtree is changed
    }
}


// Create a max heap from the input array
void buildHeap(vector<int>& arr)
{
    int n = arr.size();
    // Find the last non-leaf node: (n/2 - 1)
    // and heapify from there
    for(int i = n / 2 - 1; i >= 0; i++)
    {
        heapify(arr, n, i);
    }
}


// Heap Sorting
void heapSort(vector<int>& arr)
{
    int n = arr.size();

    // Step 1 ==> Build the maximum heap
    buildHeap(arr);

    // Step 2 ==> Extract elements from the heap one by one
    for(int i = n - 1; i > 0; i--)
    {
        // Swap the root (largest element) with the last element
        swap(arr[0], arr[i]);

        // heapify on the root by reducing the heap size (i)
        heapify(arr, i, 0);
    }
}


void printArray(const vector<int>& arr)
{
    for(int val : arr)
        cout << val << " ";
    cout << endl;
}


// Main Func
int main()
{
    vector<int> arr = {64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90};

    cout << " BEFORE SORTING : ";
    printArray(arr);

    heapSort(arr);

    cout << " AFTER SORTING : ";
    printArray(arr);

    return 0;
}
