# Constant for Amdahl's Law
SEQUENTIAL_FRACTION = 0.05

# Speedup = 1 / (f + (1 - f) / P)
def calculate_amdahl_speedup(workers, f=SEQUENTIAL_FRACTION):
    if workers <= 0:
        return 0
    return 1 / (f + (1 - f) / workers)

# Efficiency = Speedup / P
def calculate_efficiency(speedup, workers):
    if workers <= 0:
        return 0
    return speedup / workers