import k_partition

sizes = ['small', 'medium', 'large']

for num in range(171, 261):
    for k in range(2, 30):
        k_partition.main('small', num, k)
"""
for size in sizes:
    for num in range(1, 261):
        for k in range (2, 30):
            k_partition.main(size, num, k)
"""