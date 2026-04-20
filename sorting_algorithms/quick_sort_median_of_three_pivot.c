#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

long long comparison_count = 0;

double get_elapsed_time(clock_t start, clock_t end) {
    return (double)(end - start) / CLOCKS_PER_SEC;
}

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

int medianOfThree(int arr[], int low, int high) {

    int mid = low + (high - low) / 2;

    comparison_count++;
    if (arr[low] > arr[mid]) swap(&arr[low], &arr[mid]);

    comparison_count++;
    if (arr[low] > arr[high]) swap(&arr[low], &arr[high]);

    comparison_count++;
    if (arr[mid] > arr[high]) swap(&arr[mid], &arr[high]);

    return mid;
}

int partition(int arr[], int low, int high) {

    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j <= high - 1; j++) {

        comparison_count++;

        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    swap(&arr[i + 1], &arr[high]);

    return (i + 1);
}

void quickSortMedianOfThreePivot(int arr[], int low, int high) {

    if (low < high) {

        int median_index = medianOfThree(arr, low, high);

        swap(&arr[median_index], &arr[high]);

        int pi = partition(arr, low, high);

        quickSortMedianOfThreePivot(arr, low, pi - 1);
        quickSortMedianOfThreePivot(arr, pi + 1, high);
    }
}

int main() {

    int n;

    scanf("%d", &n);

    int *arr = (int *)malloc(n * sizeof(int));

    if (arr == NULL)
        return 1;

    for (int i = 0; i < n; i++)
        scanf("%d", &arr[i]);

    clock_t start_time, end_time;

    start_time = clock();

    quickSortMedianOfThreePivot(arr, 0, n - 1);

    end_time = clock();

    double elapsed = get_elapsed_time(start_time, end_time);

    fprintf(stderr, "TIME: %.9f\n", elapsed);
    fprintf(stderr, "COMPARISONS: %lld\n", comparison_count);

    free(arr);

    return 0;
}