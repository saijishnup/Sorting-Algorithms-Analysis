#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

long long comparison_count = 0;

double get_elapsed_time(clock_t start, clock_t end) {
    return (double)(end - start) / CLOCKS_PER_SEC;
}

void insertionSort(int arr[], int n) {
    int i, key, j;
    
    for (i = 1; i < n; i++) {
        key = arr[i];
        j = i - 1;
        
        while (j >= 0 && (comparison_count++, arr[j] > key)) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}

int main() {

    int n;
    scanf("%d", &n);

    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) {
        return 1;
    }

    for (int i = 0; i < n; i++) {
        scanf("%d", &arr[i]);
    }

    clock_t start_time, end_time;

    start_time = clock();

    insertionSort(arr, n);

    end_time = clock();

    double elapsed = get_elapsed_time(start_time, end_time);

    fprintf(stderr, "TIME: %.9f\n", elapsed);
    fprintf(stderr, "COMPARISONS: %lld\n", comparison_count);

    free(arr);

    return 0;
}