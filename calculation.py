import numpy
import copy
import sys

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
        matrix_temp = ConvertTo2D(matrix)
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
        else:
            print("zczcda")
    elif dim == 3:
        print("sadas")
    matrix_temp = numpy.matmul(matrix_temp, transform)
    for i in range(len(matrix[:,0])):
        for j in range(2):
            matrix[i][j] = matrix_temp[i][j]
    return matrix

def shear(matrix, dim, param, k):
    not_error = True
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
        if dim == 2:
            transform = numpy.array([[1, y, 0],
                                     [x, 1, 0],
                                     [0, 0, 1]])
            return numpy.matmul(matrix, transform)

def stretch(matrix, dim, param, k):
    if param == "x" or param == "y" or param == "z":
        if dim == 2:
            if param == "x":
                transform = numpy.array([[1,0],
                                         [k,1]])
            elif param == "y":
                transform = numpy.array([[0,1],
                                         [1,k]])
            matrix_temp = ConvertTo2D(matrix)
            matrix_temp = numpy.matmul(matrix_temp, transform)
            for i in range(len(matrix[:,0])):
                for j in range(2):
                    matrix[i][j] = matrix_temp[i][j]
            return matrix
    else:
        print("Parameter salah")

def custom(matrix, dim, a, b, c, d, e, f, g, h, i):
    if dim == 2:
        #Linear transformation for 2D
        matrix_temp = ConvertTo2D(matrix) #Create temporary N x 2 matrix
        #Create 2 x 2 transformation matrix
        transform = numpy.array([[d,b],
                                 [c,a]])
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
        transform = numpy.array([[a,d,g],
                                 [b,e,h],
                                 [c,f,i]])
        return numpy.matmul(matrix, transform)

def multiple(matrix, dim, n, consoling):
    sys.stdout.write("Masukkan " + str(n) + " command(s): ")
    sys.stdout.flush()
    for i in range(n):
        command = input("Command " + str(i+1) + ": ").split(" ")
        if command[0] == "translate":
            dx = float(command[1])
            dy = float(command[2])
            if dim == 2:
                dz = 0
            else:
                dz = float(command[3])
            matrix = translate(matrix,dx,dy,dz)

        elif command[0] == "dilate":
            k = float(command[1])
            matrix = dilate(matrix, k)

        elif command[0] == "rotate":
            deg = float(command[1])
            a = float(command[2])
            b = float(command[3])
            matrix = rotate(matrix, deg, a, b)

        elif command[0] == "reflect":
            param = command[1]
            matrix = reflect(matrix, dim, param)

        elif command[0] == "shear":
            param = command[1]
            k = float(command[2])
            matrix = shear(matrix, dim, param, k)

        elif command[0] == "stretch":
            param = command[1]
            k = float(command[2])
            matrix = stretch(matrix, dim, param, k)

        elif command[0] == "custom":
            a = float(command[1])
            b = float(command[2])
            c = float(command[3])
            d = float(command[4])
            if dim == 2:
                e = 0
                f = 0
                g = 0
                h = 0
                i = 0
            else:
                e = float(command[5])
                f = float(command[6])
                g = float(command[7])
                h = float(command[8])
                i = float(command[9])
            matrix = custom(matrix, dim, a, b, c, d, e, f, g, h, i)
    return matrix
