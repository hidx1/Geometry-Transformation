import numpy
import copy
import sys
import math
def ConvertTo2D(matrix):
    matrix_result = numpy.zeros((len(matrix[:,0]), 2))
    for i in range(len(matrix[:,0])):
        for j in range(2):
            matrix_result[i][j] = matrix[i][j]
    return matrix_result

def animasi(matrix, matrixAnimasi):
    for i in range(0,len(matrix[:,0])):
        matrix[i][0] += matrixAnimasi[i][0]
        matrix[i][1] += matrixAnimasi[i][1]
        matrix[i][2] += matrixAnimasi[i][2]
    return matrix

def translate(matrix, dx, dy, dz):
    for i in range(len(matrix[:,0])):
        matrix[i][0] += dx
        matrix[i][1] += dy
        matrix[i][2] += dz
    return matrix

def dilate(matrixIn, factor):
    matrix=copy.deepcopy(matrixIn)
    k = float(factor)
    for i in range(len(matrix[:,0])):
        for j in range(3):
            matrix[i][j] *= k
    return matrix

def rotate(matrixIn, dim, deg, a, b):
    matrix = copy.deepcopy(matrixIn)
    c = cos(radians(deg))
    s = sin(radians(deg))
    base = numpy.array[[c,-1*s],
                       [s,c]]
    matrix = numpy.mat(base)*numpy.mat()
    print("rotate")

def reflect(matrixIn, dim, param):
    param = param.lower()
    #target = titik pantul (string)
    #dim = dimensi
    #rtype : matrix

    #mencari titik pantul
    matrix = copy.deepcopy(matrixIn)
    def get(param):
        #fungsi yang mengembalikan pencarian

        #mencari index dalam ( ) *cek komentar code di bawah
        start = target.find("(") + 1
        stop = target.rfind(")") #rfind == return highest param bleh bleh

        #boolean
        found = (stop - start) >= 1
        if found:
            output = target[start:stop]
            output = output.split(",")
            return output
        else:
            return []

    if dim == 2: #dimensi 2
        #mengembalikan matrix transformasi berdasar sumbu pantul
        if param == "x":
            transform = numpy.array([[1, 0, 0],
                                    [0, -1, 0],
                                    [0, 0, 1]])
        elif param == "y":
            transform = numpy.array([[-1, 0 ,0],
                                    [0, 1, 0],
                                    [0, 0, 1]])
        elif param == "y=x":
            transform = numpy.array([[0, 1, 0],
                                    [1, 0, 0],
                                    [0, 0, 1]])
        elif param == "y=-x":
            transform = numpy.array([[0, -1, 0],
                                    [-1, 0, 0],
                                    [0, 0, 1]])
        else: #reflect berdasar titik
            get_point = get(param)
            get_point = [float(x) for x in get_point]
            a = float(get_point[0])
            b = float(get_point[1])

            #rumusnya reflect(x) = 2(poros x) - x
            #translasi -2(poros x) *(-1)
            transform = numpy.array([[-1, 0, 2*a],
                                    [0, -1, 2*b],
                                    [0, 0, 1]])
    elif dim == 3: #3D
        if param in ("xy","yx") :
            transform = numpy.array([[1,0,0],
                                    [0,1,0],
                                    [0,0,-1]])
        elif param in ("yz","zy") :
            transform = numpy.array([[-1,0,0],
                                    [0,1,0],
                                    [0,0,1]])
        elif param in ("xz","zx") :
            transform = numpy.array([[1,0,0],
                                    [0,-1,0],
                                    [0,0,1]])
        
        # print(numpy.mat(matrix)*numpy.mat(transform))
    return numpy.array(numpy.mat(matrix)*numpy.mat(transform))

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

def multiple(matrix, dim, n):
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

def differenceCalc(matrixOri,matrixTarget,nFrame):
    #fungsi yang menghasilkan matrix yang berisi perubahan yang harus di push ke queue
    diffMatrix=[]
    for indexRow in range(0,len(matrixOri)):
        rowToAppend=[]
        for indexColumn in range(0,len(matrixOri[0])):
            rowToAppend.append(float((matrixTarget[indexRow][indexColumn]-matrixOri[indexRow][indexColumn])/nFrame))
        diffMatrix.append(rowToAppend)
    return numpy.array(diffMatrix)