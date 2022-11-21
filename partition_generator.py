import k_partition

sizes = ['small', 'medium', 'large']

for size in sizes:
    for num in range(1, 261):
        for k in range (2, 101):
            k_partition.main(size, num, k)