
import numpy
import sys
import time

if (len(sys.argv) != 2):
    print("usage: python %s N" % sys.argv[0])
    quit()

n = int(sys.argv[1])
a = numpy.zeros((n, n))  # Matrix A
b = numpy.zeros((n, n))  # Matrix B
c = numpy.zeros((n, n))  # Matrix C

# Initialize the matrices to some values.
for i in range(n):
    for j in range(n):
        a[i, j] = i * n + j
        b[i, j] = j * n + i
        c[i, j] = 0

begin = time.time()

# n = 2
# a = numpy.arange(1, 5).reshape((2, 2))
# b = numpy.arange(1, 5).reshape((2, 2))
# c = numpy.zeros((n, n))
######################################################
# Write code to calculate C = A * B                  #

# transpose b by switching row and col
b = [[row[i] for row in b] for i in range(n)]

# store the sum of each row * col to its corresponding position in c
c[:, :] = [[sum(x * y for x, y in zip(row_a, col_b))
            for col_b in b] for row_a in a]

# (without using numpy librarlies e.g., numpy.dot()) #
######################################################

end = time.time()
print("time: %.6f sec" % (end - begin))
print(c)
# Print C for debugging. Comment out the print before measuring the execution time.
total = 0
for i in range(n):
    for j in range(n):
        # print c[i, j]
        total += c[i, j]
# Print out the sum of all values in C.
# This should be 450 for N=3, 3680 for N=4, and 18250 for N=5.
print("sum: %.6f" % total)

total = numpy.sum(numpy.dot(a, numpy.transpose(b)))
print(f'Correct sum: {total}')
