import k_partition

sizes = ['medium']

k_partition.main('small', 135)

"""
for num in range(248, 261):
    k_partition.main('small', num)

for size in sizes:
    for num in range(1, 261):   # FROM small/medium/large 1 to 260
        k_partition.main(size, num)
"""