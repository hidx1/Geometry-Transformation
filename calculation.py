import numpy
import copy

def ConvertTo2D(matrix):
    matrix_result = numpy.zeros((len(matrix[:,0]), 2))
    for i in range(len(matrix[:,0])):
        for j in range(2):
            matrix_result[i][j] = matrix[i][j]
    return matrix_result

def translate(matrix, dx, dy, dz):
    for i in range(len(matrix[:,0])):
        matrix[i][0] += dx
        matrix[i][1] += dy
        matrix[i][2] += dz
    return matrix

def dilate(matrix, k):
    for i in range(len(matrix[:,0])):
        for j in range(3):
            matrix[i][j] *= k
    return matrix

def rotate(matrix, dim, deg, a, b):
    print("rotate")

def reflect(matrix, dim, param):
    if dim == 2:
        if param == "x":
            transform = numpy.array([[1,0],
                                      [0,-1]])
        elif param == "y":
            transform = numpy.array([[-1,0],
                                      [0,1]])
        elif param == "y=x":
            transform = numpy.array([[0,1],
                                      [1,0]])
        elif param == "y=-x":
            transform = numpy.array([[0,-1],
                                      [-1,0]])
        elif param == "(a,b)":
            print("dsaxcz")
    elif dim == 3:
        print("sadas")

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
        transform[1,0] = x
        transform[2,0] = x
        transform[0,1] = y
        transform[2,1] = y
        transform[0,2] = z
        transform[1,2] = z
    for i in range(len(matrix[:,0])):
        matrix[i,:] = numpy.matmul(matrix[i,:], transform)

def stretch(matrix, dim, param, k):
    not_error = True
    x = 1
    y = 1
    z = 1

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
        if dim == 2:
            #transform = numpy.array([[x,0,0],
            #                        [0,y,0],
            #                        [0,0,1]])
            transform = numpy.array([[1,k],
                                     [0,1]])
            matrix_temp = ConvertTo2D(matrix)
            matrix_temp = numpy.matmul(matrix_temp, transform)
            for i in range(len(matrix[:,0])):
                for j in range(2):
                    matrix[i][j] = matrix_temp[i][j]
            return matrix
        #return numpy.matmul(matrix, transform)

def custom(matrix, dim, a, b, c, d, e, f, g, h, i):
    if dim == 2:
        #Linear transformation for 2D
        matrix_temp = ConvertTo2D(matrix) #Create temporary N x 2 matrix
        #Create 2 x 2 transformation matrix
        transform = numpy.array([[a,b],
                                  [c,d]])
        #Matrix multiplication between matrix_temp and transform
        matrix_temp = numpy.matmul(matrix_temp, transform)
        #Copy x and y element from N x 2 matrix to N x 4 matrix
        for i in range(len(matrix[:,0])):
            for j in range(2):
                matrix[i][j] = matrix_temp[i][j]
        return matrix
    else:
        #Linear transformation for 3D
        #Create 3 x 3 transformation matrix
        transform = numpy.array([[a,b,c],
                                  [d,e,f],
                                  [g,h,i]])
        return numpy.matmul(matrix, transform)

def multiple(matrix, dim, n):
    print("multiple")
