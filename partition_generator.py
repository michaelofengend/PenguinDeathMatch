import k_partition

sizes = ['small', 'medium', 'large']

for size in sizes:
    for num in range(1, 261):   # FROM small/medium/large 1 to 260
        for k in range (2, 30): # FROM k = 2 to 29
            k_partition.main(size, num, k)
