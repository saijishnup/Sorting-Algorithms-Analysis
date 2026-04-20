# Sorting Algorithms in C

This directory contains implementations of various sorting algorithms in C.

## Available Algorithms

### 1. Bubble Sort (`bubble_sort.c`)
- **Time Complexity**: O(n²) average and worst case, O(n) best case
- **Space Complexity**: O(1)
- **Description**: Repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order.
- **Compile & Run**: `gcc bubble_sort.c -o bubble_sort && ./bubble_sort`

### 2. Selection Sort (`selection_sort.c`)
- **Time Complexity**: O(n²) in all cases
- **Space Complexity**: O(1)
- **Description**: Divides the input into a sorted and unsorted region, repeatedly selects the smallest element from the unsorted region.
- **Compile & Run**: `gcc selection_sort.c -o selection_sort && ./selection_sort`

### 3. Insertion Sort (`insertion_sort.c`)
- **Time Complexity**: O(n²) average and worst case, O(n) best case
- **Space Complexity**: O(1)
- **Description**: Builds the final sorted array one item at a time by inserting each element into its proper position.
- **Compile & Run**: `gcc insertion_sort.c -o insertion_sort && ./insertion_sort`

### 4. Merge Sort (`merge_sort.c`)
- **Time Complexity**: O(n log n) in all cases
- **Space Complexity**: O(n)
- **Description**: Divide and conquer algorithm that divides the array into halves, sorts them, and merges them back together.
- **Compile & Run**: `gcc merge_sort.c -o merge_sort && ./merge_sort`

### 5. Quick Sort (`quick_sort.c`)
- **Time Complexity**: O(n log n) average case, O(n²) worst case
- **Space Complexity**: O(log n)
- **Description**: Divide and conquer algorithm that picks a pivot element and partitions the array around it.
- **Compile & Run**: `gcc quick_sort.c -o quick_sort && ./quick_sort`

### 6. Heap Sort (`heap_sort.c`)
- **Time Complexity**: O(n log n) in all cases
- **Space Complexity**: O(1)
- **Description**: Uses a binary heap data structure to sort elements by building a max heap and repeatedly extracting the maximum.
- **Compile & Run**: `gcc heap_sort.c -o heap_sort && ./heap_sort`

### 7. Shell Sort (`shell_sort.c`)
- **Time Complexity**: O(n log n) to O(n²) depending on gap sequence
- **Space Complexity**: O(1)
- **Description**: Generalization of insertion sort that allows exchange of far apart elements.
- **Compile & Run**: `gcc shell_sort.c -o shell_sort && ./shell_sort`

### 8. Counting Sort (`counting_sort.c`)
- **Time Complexity**: O(n + k) where k is the range of input
- **Space Complexity**: O(k)
- **Description**: Non-comparison based sorting algorithm that counts the occurrences of each element.
- **Compile & Run**: `gcc counting_sort.c -o counting_sort && ./counting_sort`

### 9. Radix Sort (`radix_sort.c`)
- **Time Complexity**: O(d * (n + k)) where d is the number of digits
- **Space Complexity**: O(n + k)
- **Description**: Non-comparison based algorithm that sorts integers by processing individual digits.
- **Compile & Run**: `gcc radix_sort.c -o radix_sort && ./radix_sort`

### 10. Bucket Sort (`bucket_sort.c`)
- **Time Complexity**: O(n + k) average case, O(n²) worst case
- **Space Complexity**: O(n)
- **Description**: Distributes elements into buckets, sorts each bucket, and concatenates them.
- **Compile & Run**: `gcc bucket_sort.c -o bucket_sort && ./bucket_sort`

### 11. Randomized Quick Sort (`randomized_quick_sort.c`)
- **Time Complexity**: O(n log n) expected case
- **Space Complexity**: O(log n)
- **Description**: Variant of Quick Sort that randomly selects the pivot to avoid worst-case scenarios.
- **Compile & Run**: `gcc randomized_quick_sort.c -o randomized_quick_sort && ./randomized_quick_sort`

## Compilation

To compile all programs at once:
```bash
gcc bubble_sort.c -o bubble_sort
gcc selection_sort.c -o selection_sort
gcc insertion_sort.c -o insertion_sort
gcc merge_sort.c -o merge_sort
gcc quick_sort.c -o quick_sort
gcc heap_sort.c -o heap_sort
gcc shell_sort.c -o shell_sort
gcc counting_sort.c -o counting_sort
gcc radix_sort.c -o radix_sort
gcc bucket_sort.c -o bucket_sort
gcc randomized_quick_sort.c -o randomized_quick_sort
```

## Notes

- Each program includes a `main()` function with sample test data
- All programs print the original array and the sorted array
- Algorithms are implemented with standard C libraries (stdio.h, stdlib.h)
- Memory management is properly handled with malloc/free where needed
