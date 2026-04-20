import os
import random

def generate_data(n, data_type):
    if data_type == "random":
        return [random.randint(0, n * 2) for _ in range(n)]
    elif data_type == "sorted":
        return list(range(n))
    elif data_type == "reverse_sorted":
        return list(range(n - 1, -1, -1))
    else:
        raise ValueError("Invalid data_type. Choose from 'random', 'sorted', 'reverse_sorted'.")

def save_data_to_file(data, filename):
    with open(filename, "w") as f:
        for item in data:
            f.write(str(item) + "\n")

def main():
    input_sizes = [
        100,
        500,
        1000,
        5000,
        10000,
        25000,
        50000,
        75000,
        100000
    ]
    data_types = ["random", "sorted", "reverse_sorted"]
    output_dir = "test_data"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"Generating test data in '{output_dir}' directory...")

    for n in input_sizes:
        for dtype in data_types:
            print(f"  Generating n={n}, type={dtype}...")
            data = generate_data(n, dtype)
            filename = os.path.join(output_dir, f"n_{n}_{dtype}.txt")
            save_data_to_file(data, filename)
            print(f"    Saved to {filename}")

    print("Data generation complete.")

if __name__ == "__main__":
    main()
