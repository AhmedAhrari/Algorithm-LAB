//-------------------------------------------------
//              SHELL SORT
//-------------------------------------------------

#include <iostream>
#include <vector>
using namespace std;

// Shell Sort Func
void shellSort(vector<int>& arr)
{
    int n = arr.size();

    // Start with a large distance and gradually decrease it
    for(int gap = n / 2; gap > 0; gap /= 2)
    {
        // Perform insertion sort for each subarray with gap
        for(int i = gap; i < n; i++)
        {
            int temp = arr[i];
            int j = i;

            // Move elements at the same gap
            while (j >= gap && arr[j - gap] > temp)
            {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
            
        }
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

    shellSort(arr);

    cout << " AFTER SORTING : ";
    printArray(arr);

    return 0;
}