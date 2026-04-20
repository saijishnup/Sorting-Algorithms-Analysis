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

int partition(int arr[], int low, int high) {

    int pivot = arr[high];
    int i = low - 1;

    for (int j = low; j <= high - 1; j++) {

        comparison_count++;

        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }

    swap(&arr[i + 1], &arr[high]);

    return i + 1;
}

void quickSortRandomPivot(int arr[], int low, int high) {

    if (low < high) {

        int random_index = low + rand() % (high - low + 1);

        swap(&arr[random_index], &arr[high]);

        int pi = partition(arr, low, high);

        quickSortRandomPivot(arr, low, pi - 1);
        quickSortRandomPivot(arr, pi + 1, high);
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

    srand(time(NULL));

    clock_t start_time, end_time;

    start_time = clock();

    quickSortRandomPivot(arr, 0, n - 1);

    end_time = clock();

    double elapsed = get_elapsed_time(start_time, end_time);

    fprintf(stderr, "TIME: %.9f\n", elapsed);
    fprintf(stderr, "COMPARISONS: %lld\n", comparison_count);

    free(arr);

    return 0;
}