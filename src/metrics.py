# Constant for Theoretical Amdahl's Law
THEORETICAL_SEQUENTIAL_FRACTION = 0.1

# Calculate the Theoretical Speedup using Amdahl's Law
# Formula: Speedup = 1 / (f + (1 - f) / P)
def calculate_theoretical_speedup(workers, f=THEORETICAL_SEQUENTIAL_FRACTION):

    if workers <= 0:
        return 0
    return 1 / (f + (1 - f) / workers)

# Calculate the user-observed (actual) speedup.
# Formula: Speedup = T(1) / T(N)
def calculate_actual_speedup(t_sequential, t_parallel):

    if t_parallel == 0:
        return 0
    return t_sequential / t_parallel
  
# Back-calculate the 'Parallel Fraction' (1 - f) usually denoted as 'p' from the observed speedup.
def calculate_parallel_fraction(actual_speedup, workers):

    if workers <= 1:
        return 1.0  

    if actual_speedup == 0:
        return 0

    numerator = (1.0 / actual_speedup) - 1.0
    denominator = (1.0 / workers) - 1.0
    
    return numerator / denominator

# Calculate the efficiency of the parallel execution. 
# Formula: Efficiency = Speedup / Workers
def calculate_efficiency(speedup, workers):

    if workers <= 0:
        return 0
    return speedup / workers
