# Constant for Theoretical Amdahl's Law
THEORETICAL_SEQUENTIAL_FRACTION = 0.1

# Theoretical Speedup = 1 / (f + (1 - f) / P)
def calculate_theoretical_speedup(workers, f=THEORETICAL_SEQUENTIAL_FRACTION):
    if workers <= 0:
        return 0
    return 1 / (f + (1 - f) / workers)

# Actual Speedup = T(1) / T(N)
def calculate_actual_speedup(t_sequential, t_parallel):
    if t_parallel == 0:
        return 0
    return t_sequential / t_parallel

# Calculate Parallel Fraction P = (1/S_actual - 1) / (1/N - 1)
def calculate_parallel_fraction(actual_speedup, workers):
    if workers <= 1:
        return 1.0  

    if actual_speedup == 0:
        return 0

    numerator = (1.0 / actual_speedup) - 1.0
    denominator = (1.0 / workers) - 1.0
    
    return numerator / denominator

# Efficiency = Speedup / Workers
def calculate_efficiency(speedup, workers):
    if workers <= 0:
        return 0
    return speedup / workers
