#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <stdint.h>

long long comparison_count = 0;

double get_elapsed_time(clock_t start, clock_t end) {
    return (double)(end - start) / CLOCKS_PER_SEC;
}

int getMax(int arr[], int n) {

    int max = arr[0];

    for (int i = 1; i < n; i++) {
        comparison_count++;

        if (arr[i] > max)
            max = arr[i];
    }

    return max;
}

void countingSortForRadix(int arr[], int n, int exp) {

    int *output = (int*)malloc(n * sizeof(int));

    int count[10] = {0};

    for (int i = 0; i < n; i++)
        count[(arr[i] / exp) % 10]++;

    for (int i = 1; i < 10; i++)
        count[i] += count[i - 1];

    for (int i = n - 1; i >= 0; i--) {

        output[count[(arr[i] / exp) % 10] - 1] = arr[i];

        count[(arr[i] / exp) % 10]--;
    }

    for (int i = 0; i < n; i++)
        arr[i] = output[i];

    free(output);
}

void radixSort(int arr[], int n) {

    int max = getMax(arr, n);

    for (int exp = 1; max / exp > 0; exp *= 10)
        countingSortForRadix(arr, n, exp);
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

    radixSort(arr, n);

    end_time = clock();

    double elapsed = get_elapsed_time(start_time, end_time);

    fprintf(stderr, "TIME: %.9f\n", elapsed);
    fprintf(stderr, "COMPARISONS: %lld\n", comparison_count);

    free(arr);

    return 0;
}