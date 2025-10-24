from typing import Generator
import random

FILE_PATH = "ml-1m/ratings.dat"



def get_sample(file_path: str) -> Generator[tuple[int, int], None, None]:
    #1::1193::5::978300760
    #UserID::Gender::Age::Occupation::Zip-code
    """
    UserID::MovieID::Rating::Timestamp

    - UserIDs range between 1 and 6040 
    - MovieIDs range between 1 and 3952
    - Ratings are made on a 5-star scale (whole-star ratings only)
    - Timestamp is represented in seconds since the epoch as returned by time(2)
    - Each user has at least 20 ratings

    Returns: Generator of tuples (UserID, MovieID)
    """
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            content = line.strip()
            if content:  
                parts = content.split("::")
                sample = (int(parts[0]), int(parts[1]))
                yield sample



# 2^16 should be larger than elements in the stream
binary_str_length = 16

def get_hash_function():
    a, b = random.randint(1, 100), random.randint(0, 100)
    def hash_function(x: int) -> int:
        return (a * x + b) % (2**binary_str_length)
    return hash_function


def trailing_zeros(n: int) -> int:
    """Count trailing zeros in binary representation of n"""

    # skip the '0b1' prefix (as mentioned in reference video)
    binary_str = bin(n)[3:]
    total_zeros = 0
    for char in reversed(binary_str):
        if char == '0':
            total_zeros += 1
        else:
            break
    return total_zeros

def median(values: list[float]) -> float:
    """Return the median of a list of numbers."""
    n = len(values)
    if n == 0:
        raise ValueError("median() arg is an empty sequence")
    sorted_vals = sorted(values)
    mid = n // 2
    if n % 2 == 1:
        return sorted_vals[mid]
    else:
        return (sorted_vals[mid - 1] + sorted_vals[mid]) / 2

NUM_REGISTERS = 8
hash_functions = [get_hash_function() for _ in range(NUM_REGISTERS)]
max_zeros_per_register = [0] * NUM_REGISTERS

for entry in get_sample(FILE_PATH):
    for i, hf in enumerate(hash_functions):
        hv = hf(entry[0])
        tz = trailing_zeros(hv)
        if tz > max_zeros_per_register[i]:
            max_zeros_per_register[i] = tz

print(max_zeros_per_register)

estimates = [2 ** r for r in max_zeros_per_register]
avg_est = median(estimates)

# Correction constant for FM 0.77351
estimate = avg_est / 0.77351

print("Estimated unique elements:", int(estimate))
