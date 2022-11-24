import k_partition

sizes = ['small', 'medium', 'large']

for size in sizes:
    for num in range(179, 260):   # FROM small/medium/large 1 to 260
        k_partition.main(size, num)