//-----------------------------------------------------
//                  BUBBLE SORT
//-----------------------------------------------------

#include <iostream>
#include <vector>
using namespace std;

void bubbleSort(vector<int>& arr)
{
    int n = arr.size();

    for( int i = 0 ; i < n - 1 ; i++ )
    {
        bool swapped = false;   // For Optimization

        for( int j = 0 ; j < n - i - 1 ; j++ )
        {
            if(arr[j] > arr[j+1])
            {
                //  SWAPPED
                swap(arr[j], arr[j+1]);
                swapped = true;
            }
        }

        if(!swapped)
        {
            break;
        }
    }
}


void printArray(const vector<int>& arr)
{
    for(int val : arr)
    {
        cout << val << " ";
    }
    cout << endl;
}


int main()
{
    vector<int> arr = {64, 45, 48, 87, 878, 78, 74, 13, 55, 44, 34, 25, 12, 22, 100, 210, 150, 124, 11, 90};

    cout << " BEFORE SORTING : ";
    printArray(arr);

    bubbleSort(arr);

    cout << " AFTER SORTING ";
    printArray(arr);

    return 0;
}
