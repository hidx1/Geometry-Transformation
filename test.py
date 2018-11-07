from calculation import *
import numpy
import copy

matrix = numpy.zeros((3, 4))

def CreateMatrix(x, matrix): #Fill matrix with user's input
    print("Masukkan nilai point:")
    for i in range(x):
        matrix[i][0], matrix[i][1] = input().split(",")
        matrix[i][3] = 1

CreateMatrix(3, matrix)
print(matrix)

matrix_result = copy.deepcopy(matrix)

translate(matrix_result, 10, 2, 0)
print(matrix_result)

matrix_result = copy.deepcopy(matrix)

dilate(matrix_result, 3)
print(matrix_result)

matrix_result = copy.deepcopy(matrix)