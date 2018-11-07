import numpy
import copy

def translate(matrix, dx, dy, dz):
    #Translate using row-major form matrix multiplication
    transform = numpy.identity(4)
    transform[3,0] = dx
    transform[3,1] = dy
    transform[3,2] = dz
    for i in range(len(matrix[:,0])):
        matrix[i,:] = numpy.matmul(matrix[i,:], transform)

def dilate(matrix, k):
    transform = numpy.identity(4)
    for i in range(3):
        transform[i,i] = k
    transform[3,3] = 1
    for i in range(len(matrix[:,0])):
        matrix[i,:] = numpy.matmul(matrix[i,:], transform)

def rotate(matrix, deg, a, b):
    print("rotate")

def reflect(matrix, param):
    print("reflect")

def shear(matrix, param, k):
    not_error = True
    transform = numpy.identity(4)
    x = 0
    y = 0
    z = 0
    if param == "x":
        x = k
    elif param == "y":
        y = k
    elif param == "z":
        z = k
    else:
        print("Error, parameter salah")
        not_error = False

    if not_error:
        transform[1,0], transform[2,0] = x
        transform[0,1], transforn[2,1] = y
        transform[0,2], transform[1,2] = z

def stretch(matrix, param, k):
    print("stretch")

def custom(matrix, a, b, c, d):
    print("custom")

def multiple(matrix, n):
    print("multiple")

def reset(matrix_original, matrix_calculation):
    matrix_calculation = copy.deepcopy(matrix.original)
