import k_partition

# sizes = ['small', 'medium', 'large']
sizes = ['large']

for size in sizes:
    for num in range(179, 261):
        for k in range (2, 30):
            k_partition.main(size, num, k)
