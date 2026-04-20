import os
import subprocess
import time
import matplotlib.pyplot as plt
import re
import pandas as pd
import numpy as np
from scipy.stats import pearsonr


C_FILES = [
    "bubble_sort.c",
    "heap_sort.c",
    "insertion_sort.c",
    "merge_sort.c",
    "quick_sort_median_of_three_pivot.c",  # Using median of three pivot
    "radix_sort.c",
    "selection_sort.c",
]

# Quick Sort variants for analysis
QUICK_SORT_VARIANTS = [
    "quick_sort_first_pivot.c",  # Last element pivot
    "quick_sort_median_of_three_pivot.c",  # Median of three pivot
    "quick_sort_random_pivot.c",  # Random pivot
]

C_FILE_PATHS = [os.path.join("sorting_algorithms", f) for f in C_FILES]
QUICK_SORT_PATHS = [os.path.join("sorting_algorithms", f) for f in QUICK_SORT_VARIANTS]
EXECUTABLES_DIR = "executables"
TEST_DATA_DIR = "test_data"
OUTPUT_GRAPHS_DIR = "graphs"
OUTPUT_7_ALGOS_DIR = os.path.join(OUTPUT_GRAPHS_DIR, "7_sorting_algo_comparisons")
OUTPUT_QUICK_SORT_DIR = os.path.join(OUTPUT_GRAPHS_DIR, "quick_sort_analysis")
OUTPUT_CSV_DIR = os.path.join(OUTPUT_GRAPHS_DIR, "csv_data")
NUM_REPETITIONS = 7  # Number of times to run each experiment for averaging
# The maximum input size to consider for plotting. Adjust if needed.
MAX_PLOT_N = 100000 

# --- Helper Functions ---

def compile_c_code(c_file_path, output_executable_path):
    """Compiles a C source file into an executable."""
    print(f"Compiling {c_file_path}...")
    try:
        subprocess.run(
            ["gcc", c_file_path, "-o", output_executable_path, "-Wl,--stack=268435456"],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"Successfully compiled {c_file_path} to {output_executable_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error compiling {c_file_path}:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        exit(1)

def read_test_data(filepath):
    """Reads integers from a given test data file, one integer per line."""
    with open(filepath, 'r') as f:
        data = [int(line.strip()) for line in f if line.strip()] # Read all non-empty lines as integers
    return data

def run_benchmark(executable_path, data):
    """
    Runs the compiled C program with the given data, reads timing from C code.
    Input data is passed via stdin. Returns (time, comparisons).
    Time is measured inside C code using clock_gettime(), not Python subprocess overhead.
    """
    input_str = f"{len(data)}\n" + " ".join(map(str, data))
    
    try:
        process = subprocess.run(
            [executable_path],
            input=input_str,
            capture_output=True,
            text=True,
            check=True
        )
        
        timing = float('inf')
        comparisons = 0
        stderr_lines = process.stderr.strip().split('\n')
        for line in stderr_lines:
            if line.startswith("TIME:"):
                timing = float(line.split(":")[1].strip())
            elif line.startswith("COMPARISONS:"):
                comparisons = int(line.split(":")[1].strip())
        
        return timing, comparisons
    except subprocess.CalledProcessError as e:
        print(f"Error running {executable_path} with data size {len(data)}:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return float('inf'), 0 

def extract_n_and_type(filename):
    """Extracts N and data type (random, sorted, reverse_sorted) from a filename."""
    match = re.match(r"n_(\d+)_(\w+)\.txt", filename)
    if match:
        return int(match.group(1)), match.group(2)
    return None, None

def plot_results(results, plot_type, output_dir, metric="time"):
    """Generates and saves a plot for a specific case (best, worst, average)."""
    # ===== Linear Scale Plot =====
    plt.figure(figsize=(12, 7))
    
    for algo_name, data_points in results.items():
        # Sort data points by N for correct plotting
        data_points.sort(key=lambda x: x[0])
        ns = [dp[0] for dp in data_points if dp[0] <= MAX_PLOT_N]
        values = [dp[1] for dp in data_points if dp[0] <= MAX_PLOT_N]
        plt.plot(ns, values, marker='o', linestyle='-', label=algo_name, linewidth=2, markersize=6)

    plt.xlabel("Input Size (n)", fontsize=11)
    if metric == "time":
        plt.ylabel("Average Execution Time (s)", fontsize=11)
        plt.title(f"Sorting Algorithm Performance (Time): {plot_type} Case", fontsize=12, fontweight='bold')
    else:
        plt.ylabel("Number of Comparisons", fontsize=11)
        plt.title(f"Sorting Algorithm Performance (Comparisons): {plot_type} Case", fontsize=12, fontweight='bold')
    
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3)
    plt.xscale('log')  # Use log scale for x-axis if N values span a wide range
    plt.tight_layout()
    
    metric_suffix = "_time" if metric == "time" else "_comparisons"
    output_path = os.path.join(output_dir, f"sorting_algorithms_{plot_type.lower().replace(' ', '_')}_case{metric_suffix}.png")
    plt.savefig(output_path, dpi=150)
    print(f"Generated plot: {output_path}")
    plt.close()
    
    # ===== Logarithmic Scale Plot (Y-axis) - For better visibility =====
    plt.figure(figsize=(12, 7))
    
    for algo_name, data_points in results.items():
        # Sort data points by N for correct plotting
        data_points.sort(key=lambda x: x[0])
        ns = [dp[0] for dp in data_points if dp[0] <= MAX_PLOT_N]
        values = [dp[1] for dp in data_points if dp[0] <= MAX_PLOT_N]
        # Filter out zero or negative values for log scale
        filtered_ns = [n for n, v in zip(ns, values) if v > 0]
        filtered_values = [v for v in values if v > 0]
        if filtered_values:
            plt.plot(filtered_ns, filtered_values, marker='o', linestyle='-', label=algo_name, linewidth=2, markersize=6)

    plt.xlabel("Input Size (n)", fontsize=11)
    if metric == "time":
        plt.ylabel("Average Execution Time (s) - Log Scale", fontsize=11)
        plt.title(f"Sorting Algorithm Performance (Time) - Log Scale: {plot_type} Case", fontsize=12, fontweight='bold')
    else:
        plt.ylabel("Number of Comparisons - Log Scale", fontsize=11)
        plt.title(f"Sorting Algorithm Performance (Comparisons) - Log Scale: {plot_type} Case", fontsize=12, fontweight='bold')
    
    plt.legend(fontsize=10, loc='best')
    plt.grid(True, alpha=0.3, which='both')
    plt.xscale('log')
    plt.yscale('log')  # Logarithmic scale on Y-axis for better visibility
    plt.tight_layout()
    
    # Save with _log_scale suffix
    output_path_log = os.path.join(output_dir, f"sorting_algorithms_{plot_type.lower().replace(' ', '_')}_case{metric_suffix}_log_scale.png")
    plt.savefig(output_path_log, dpi=150)
    print(f"Generated plot: {output_path_log}")
    plt.close()

def plot_correlation(results, output_dir):
    """Generate correlation plots between time and comparisons for each algorithm."""
    plt.figure(figsize=(14, 10))
    
    num_algos = len(results)
    rows = (num_algos + 1) // 2
    cols = 2
    
    for idx, (algo_name, data_points) in enumerate(results.items(), 1):
        plt.subplot(rows, cols, idx)
        
        # Extract time and comparisons data
        times = [dp[1] for dp in data_points if dp[1] != float('inf')]
        comparisons = [dp[2] for dp in data_points if dp[1] != float('inf')]
        
        if len(times) > 1 and len(comparisons) > 1:
            # Calculate correlation coefficient
            corr, p_value = pearsonr(comparisons, times)
            
            # Plot scatter with trend line
            plt.scatter(comparisons, times, alpha=0.6, s=100, color='steelblue', edgecolors='black', linewidth=0.5)
            
            # Add trend line
            z = np.polyfit(comparisons, times, 1)
            p = np.poly1d(z)
            x_line = np.linspace(min(comparisons), max(comparisons), 100)
            plt.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Trend Line')
            
            plt.xlabel("Number of Comparisons", fontsize=10)
            plt.ylabel("Execution Time (s)", fontsize=10)
            title = f"{algo_name}\nCorrelation: {corr:.4f} (p={p_value:.4e})"
            plt.title(title, fontsize=10, fontweight='bold')
            plt.grid(True, alpha=0.3)
            # Add legend
            plt.legend(fontsize=9, loc='best')
    
    plt.tight_layout()
    output_path = os.path.join(output_dir, "time_vs_comparisons_correlation.png")
    plt.savefig(output_path, dpi=150)
    print(f"Generated correlation plot: {output_path}")
    plt.close()

# --- Main Execution ---
if __name__ == "__main__":
    # Create necessary directories
    os.makedirs(EXECUTABLES_DIR, exist_ok=True)
    os.makedirs(OUTPUT_GRAPHS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_7_ALGOS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_QUICK_SORT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_CSV_DIR, exist_ok=True)

    executables = {}
    for c_file in C_FILES:
        base_name = os.path.splitext(c_file)[0]
        executable_path = os.path.join(EXECUTABLES_DIR, base_name)
        compile_c_code(os.path.join("sorting_algorithms", c_file), executable_path)
        executables[base_name] = executable_path
    
    # Compile quick sort variants
    quick_sort_executables = {}
    for c_file in QUICK_SORT_VARIANTS:
        base_name = os.path.splitext(c_file)[0]
        executable_path = os.path.join(EXECUTABLES_DIR, base_name)
        compile_c_code(os.path.join("sorting_algorithms", c_file), executable_path)
        quick_sort_executables[base_name] = executable_path

    # Data structure: {algo: {data_type: [(n, time, comparisons), ...]}}
    all_results = {
        "bubble_sort": {"random": [], "sorted": [], "reverse_sorted": []},
        "heap_sort": {"random": [], "sorted": [], "reverse_sorted": []},
        "insertion_sort": {"random": [], "sorted": [], "reverse_sorted": []},
        "merge_sort": {"random": [], "sorted": [], "reverse_sorted": []},
        "quick_sort_median_of_three_pivot": {"random": [], "sorted": [], "reverse_sorted": []},
        "radix_sort": {"random": [], "sorted": [], "reverse_sorted": []},
        "selection_sort": {"random": [], "sorted": [], "reverse_sorted": []},
    }
    
    # Results for quick sort variants analysis
    quick_sort_results = {
        "quick_sort_first_pivot": {"random": [], "sorted": [], "reverse_sorted": []},
        "quick_sort_median_of_three_pivot": {"random": [], "sorted": [], "reverse_sorted": []},
        "quick_sort_random_pivot": {"random": [], "sorted": [], "reverse_sorted": []},
    }

    # Get all test data files
    test_data_files = [f for f in os.listdir(TEST_DATA_DIR) if f.endswith(".txt")]
    test_data_files.sort(key=lambda x: (extract_n_and_type(x)[0], extract_n_and_type(x)[1]))

    print("\nStarting benchmarking...")
    for data_file in test_data_files:
        n, data_type = extract_n_and_type(data_file)
        if n is None:
            continue
        
        data_filepath = os.path.join(TEST_DATA_DIR, data_file)
        original_data = read_test_data(data_filepath)
        
        print(f"Benchmarking N={n}, Type={data_type}...")

        for algo_base_name, executable_path in executables.items():
            total_time = 0
            total_comparisons = 0
            for _ in range(NUM_REPETITIONS):
                # Pass a copy of the data because C program might modify it
                time_taken, comparisons = run_benchmark(executable_path, list(original_data))
                total_time += time_taken
                total_comparisons += comparisons
            
            avg_time = total_time / NUM_REPETITIONS
            avg_comparisons = total_comparisons / NUM_REPETITIONS
            print(f"  {algo_base_name}: Time = {avg_time:.6f} s, Comparisons = {avg_comparisons:.0f}")
            
            # Store results as (n, time, comparisons)
            all_results[algo_base_name][data_type].append((n, avg_time, avg_comparisons))
        
        # Also benchmark quick sort variants separately
        for qs_variant, qs_executable_path in quick_sort_executables.items():
            total_time = 0
            total_comparisons = 0
            for _ in range(NUM_REPETITIONS):
                time_taken, comparisons = run_benchmark(qs_executable_path, list(original_data))
                total_time += time_taken
                total_comparisons += comparisons
            
            avg_time = total_time / NUM_REPETITIONS
            avg_comparisons = total_comparisons / NUM_REPETITIONS
            print(f"  {qs_variant}: Time = {avg_time:.6f} s, Comparisons = {avg_comparisons:.0f}")
            
            quick_sort_results[qs_variant][data_type].append((n, avg_time, avg_comparisons))

    print("\nBenchmarking complete. Generating plots...")

    # --- Plotting ---
    # Prepare plot data for time
    avg_case_time = {}
    worst_case_time = {}
    best_case_time = {}
    
    # Prepare plot data for comparisons
    avg_case_comp = {}
    worst_case_comp = {}
    best_case_comp = {}
    
    # Prepare data for correlation analysis
    correlation_data = {}
    
    for algo, types in all_results.items():
        # Format algorithm name for display
        display_name = algo.replace('_', ' ').title()
        if "Quick Sort Median Of Three Pivot" in display_name:
            display_name = "Quick Sort (Median of Three)"
        
        # Time plots - extract (n, time)
        avg_case_time[display_name] = [(n, t) for n, t, c in types["random"]]
        worst_case_time[display_name] = [(n, t) for n, t, c in types["reverse_sorted"]]
        best_case_time[display_name] = [(n, t) for n, t, c in types["sorted"]]
        
        # Comparison plots - extract (n, comparisons)
        avg_case_comp[display_name] = [(n, c) for n, t, c in types["random"]]
        worst_case_comp[display_name] = [(n, c) for n, t, c in types["reverse_sorted"]]
        best_case_comp[display_name] = [(n, c) for n, t, c in types["sorted"]]
        
        # Correlation data - combine all cases, extract (n, time, comparisons)
        all_cases = types["random"] + types["sorted"] + types["reverse_sorted"]
        correlation_data[display_name] = all_cases
    
    # Generate Time vs N plots in 7_sorting_algo_comparisons folder
    plot_results(avg_case_time, "Average Case (Random Input)", OUTPUT_7_ALGOS_DIR, metric="time")
    plot_results(worst_case_time, "Worst Case (Reverse Sorted Input)", OUTPUT_7_ALGOS_DIR, metric="time")
    plot_results(best_case_time, "Best Case (Sorted Input)", OUTPUT_7_ALGOS_DIR, metric="time")
    
    # Generate Comparisons vs N plots in 7_sorting_algo_comparisons folder
    plot_results(avg_case_comp, "Average Case (Random Input)", OUTPUT_7_ALGOS_DIR, metric="comparisons")
    plot_results(worst_case_comp, "Worst Case (Reverse Sorted Input)", OUTPUT_7_ALGOS_DIR, metric="comparisons")
    plot_results(best_case_comp, "Best Case (Sorted Input)", OUTPUT_7_ALGOS_DIR, metric="comparisons")
    
    # Generate correlation plot for 7 algorithms in 7_sorting_algo_comparisons folder
    plot_correlation(correlation_data, OUTPUT_7_ALGOS_DIR)
    
    # --- Quick Sort Variants Analysis ---
    print("\nGenerating QuickSort variant plots...")
    
    # Prepare quick sort variant plot data
    qs_avg_case_time = {}
    qs_worst_case_time = {}
    qs_best_case_time = {}
    
    qs_avg_case_comp = {}
    qs_worst_case_comp = {}
    qs_best_case_comp = {}
    
    for qs_algo, qs_types in quick_sort_results.items():
        # Format algorithm name for display
        display_name = qs_algo.replace('_', ' ').title()
        if "Median Of Three" in display_name:
            display_name = "Quick Sort (Median of Three)"
        elif qs_algo == "quick_sort_first_pivot":
            display_name = "Quick Sort (First Element Pivot)"
        elif "Random" in display_name:
            display_name = "Quick Sort (Random Pivot)"
        
        # Time plots
        qs_avg_case_time[display_name] = [(n, t) for n, t, c in qs_types["random"]]
        qs_worst_case_time[display_name] = [(n, t) for n, t, c in qs_types["reverse_sorted"]]
        qs_best_case_time[display_name] = [(n, t) for n, t, c in qs_types["sorted"]]
        
        # Comparison plots
        qs_avg_case_comp[display_name] = [(n, c) for n, t, c in qs_types["random"]]
        qs_worst_case_comp[display_name] = [(n, c) for n, t, c in qs_types["reverse_sorted"]]
        qs_best_case_comp[display_name] = [(n, c) for n, t, c in qs_types["sorted"]]
    
    # Generate Quick Sort Time vs N plots
    plot_results(qs_avg_case_time, "Average Case (Random Input)", OUTPUT_QUICK_SORT_DIR, metric="time")
    plot_results(qs_worst_case_time, "Worst Case (Reverse Sorted Input)", OUTPUT_QUICK_SORT_DIR, metric="time")
    plot_results(qs_best_case_time, "Best Case (Sorted Input)", OUTPUT_QUICK_SORT_DIR, metric="time")
    
    # Generate Quick Sort Comparisons vs N plots
    plot_results(qs_avg_case_comp, "Average Case (Random Input)", OUTPUT_QUICK_SORT_DIR, metric="comparisons")
    plot_results(qs_worst_case_comp, "Worst Case (Reverse Sorted Input)", OUTPUT_QUICK_SORT_DIR, metric="comparisons")
    plot_results(qs_best_case_comp, "Best Case (Sorted Input)", OUTPUT_QUICK_SORT_DIR, metric="comparisons")
    
    # Prepare correlation data for quick sort variants
    qs_correlation_data = {}
    for qs_algo, qs_types in quick_sort_results.items():
        display_name = qs_algo.replace('_', ' ').title()
        if "Median Of Three" in display_name:
            display_name = "Quick Sort (Median of Three)"
        elif qs_algo == "quick_sort_first_pivot":
            display_name = "Quick Sort (First Element Pivot)"
        elif "Random" in display_name:
            display_name = "Quick Sort (Random Pivot)"
        
        # Correlation data - combine all cases
        all_cases = qs_types["random"] + qs_types["sorted"] + qs_types["reverse_sorted"]
        qs_correlation_data[display_name] = all_cases
    
    # Generate correlation plot for quick sort variants
    plot_correlation(qs_correlation_data, OUTPUT_QUICK_SORT_DIR)

    print("\nAll plots generated successfully.")
    print(f"Results are in the '{OUTPUT_GRAPHS_DIR}' directory.")
    print(f"  - 7 sorting algorithm comparisons: '{OUTPUT_7_ALGOS_DIR}'")
    print(f"  - Quick sort analysis: '{OUTPUT_QUICK_SORT_DIR}'")
    print(f"  - CSV data: '{OUTPUT_CSV_DIR}'")
    
    print("\n--- Benchmarking Methodology ---")
    print(f"Each experiment was repeated {NUM_REPETITIONS} times, and the average execution time is reported.")
    print("Timing mechanism: C's `clock()` function from <time.h> is used to measure algorithm execution time.")
    print("Comparison counting: Instrumented C code tracks all element comparisons.")
    print("Input selection: Pre-generated test data from the 'test_data/' directory was used.")
    print("Same inputs were used for all sorting algorithms to ensure a fair comparison.")
    print("\nNote on Best/Worst Case Definitions:")
    print("  - Average Case: Represented by 'random' input data.")
    print("  - Worst Case: Represented by 'reverse_sorted' input data.")
    print("  - Best Case: Represented by 'sorted' input data.")
    print("\nCorrelation Analysis:")
    print("  The correlation plots show the relationship between the number of comparisons")
    print("  and execution time. A high correlation (close to 1.0) indicates that comparisons")
    print("  are a strong predictor of execution time for that algorithm.")

    # --- Generate Table ---
    print("\n--- Benchmarking Results Table ---")
    table_data = []
    for algo_key, types_data in all_results.items():
        # Format algorithm name
        algo_name = algo_key.replace('_', ' ').title()
        if "Quick Sort Median Of Three Pivot" in algo_name:
            algo_name = "Quick Sort (Median of Three)"
        
        for data_type, results_list in types_data.items():
            for n, avg_time, avg_comparisons in results_list:
                table_data.append({
                    "Algorithm": algo_name,
                    "Input Type": data_type.replace('_', ' ').title(),
                    "Input Size (N)": n,
                    "Average Time (s)": f"{avg_time:.6f}" if avg_time != float('inf') else "Crashed/Timeout",
                    "Average Comparisons": f"{avg_comparisons:.0f}" if avg_time != float('inf') else "N/A"
                })
    
    df = pd.DataFrame(table_data)
    df_sorted = df.sort_values(by=["Input Size (N)", "Input Type", "Algorithm"])
    print(df_sorted.to_string(index=False))

    # Save to CSV in csv_data folder
    csv_output_path = os.path.join(OUTPUT_CSV_DIR, "all_sorting_benchmark_results.csv")
    df_sorted.to_csv(csv_output_path, index=False)
    print(f"\nFull results table saved to {csv_output_path}")
    
    # --- Correlation Analysis Summary ---
    print("\n--- Correlation Analysis Summary ---")
    print("Algorithm                           | Correlation (r) | P-value")
    print("-" * 70)
    for algo_name, data_points in correlation_data.items():
        times = [dp[1] for dp in data_points if dp[1] != float('inf')]
        comparisons = [dp[2] for dp in data_points if dp[1] != float('inf')]
        
        if len(times) > 1 and len(comparisons) > 1:
            corr, p_value = pearsonr(comparisons, times)
            print(f"{algo_name:<35} | {corr:>15.4f} | {p_value:.4e}")
    
    print("\nInterpretation:")
    print("  r close to 1.0: Strong positive correlation (more comparisons → more time)")
    print("  r close to 0.0: Weak/no correlation")
    print("  p-value < 0.05: Statistically significant correlation")
    
    # --- Important Notes ---
    print("\n" + "="*80)
    print("IMPORTANT NOTES ON RESULTS")
    print("="*80)
    
    print("\n⚠️  TIMING MEASUREMENT:")
    print("  - Timing is measured INSIDE C code using clock() from <time.h>")
    print("  - The clock() function measures CPU time used by the program")
    print("  - Python is only used to run the executable and collect results")
    print("  - This avoids Python subprocess overhead affecting algorithm timing")
    
    print("\n⚠️  RADIX SORT 'COMPARISONS' NOTE:")
    print("  - Radix sort is a NON-COMPARATIVE sorting algorithm")
    print("  - It does NOT use element comparisons (like other algorithms)")
    print("  - The 'comparisons' count represents operations in getMax() function")
    print("  - This value (~n) is NOT comparable to other algorithms' comparisons")
    print("  - Use TIME metric, not COMPARISONS, to evaluate radix sort performance")
    
    print("\n✓ EXPECTED BEHAVIOR:")
    print("  - O(n²) algorithms: Bubble, Insertion, Selection Sort")
    print("  - O(n log n) algorithms: Heap, Merge, Quick Sort")
    print("  - O(n+k) algorithm: Radix Sort (where k is key range)")
    print("  - Best case optimized: Bubble & Insertion sort show O(n) for sorted input")
    print("="*80)