#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

long long comparison_count = 0;

double get_elapsed_time(clock_t start, clock_t end) {
    return (double)(end - start) / CLOCKS_PER_SEC;
}

void selectionSort(int arr[], int n) {

    int i, j, min_idx, temp;

    for (i = 0; i < n - 1; i++) {

        min_idx = i;

        for (j = i + 1; j < n; j++) {

            comparison_count++;

            if (arr[j] < arr[min_idx])
                min_idx = j;
        }

        if (min_idx != i) {

            temp = arr[min_idx];
            arr[min_idx] = arr[i];
            arr[i] = temp;
        }
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

    selectionSort(arr, n);

    end_time = clock();

    double elapsed = get_elapsed_time(start_time, end_time);

    fprintf(stderr, "TIME: %.9f\n", elapsed);
    fprintf(stderr, "COMPARISONS: %lld\n", comparison_count);

    free(arr);

    return 0;
}