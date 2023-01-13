import sys
import numpy as np

filename = sys.argv

with open(filename[1]) as f:
    lines = f.readlines()

    nums = [int(line) for line in lines]

print(f'Statistics Summary')
print(f'Mean: {np.mean(nums)}')
print(f'Std: {np.std(nums)}')
print(f'Min: {min(nums)}')
print(f'Max: {max(nums)}')
