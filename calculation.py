import numpy
import copy
import math

def animasi(matrixIn, matrixAnimasi):
    matrix = copy.deepcopy(matrixIn)
    for i in range(0,len(matrix[:,0])):
        matrix[i][0] += matrixAnimasi[i][0]
        matrix[i][1] += matrixAnimasi[i][1]
        matrix[i][2] += matrixAnimasi[i][2]
    return matrix

def translate(matrixIn, dx, dy, dz):
    matrix = copy.deepcopy(matrixIn)
    for i in range(len(matrix[:,0])):
        matrix[i][0] += dx
        matrix[i][1] += dy
        matrix[i][2] += dz
    return matrix

def dilate(matrixIn, k):
    matrix = copy.deepcopy(matrixIn)
    for i in range(len(matrix[:,0])):
        for j in range(3):
            matrix[i][j] *= k
    return matrix

def rotate(matrixIn, dim, deg, a, b, c):
    matrix = copy.deepcopy(matrixIn)
    matrix = translate(matrix, a, b, c)
    transform = numpy.identity(3)

    cos = math.cos(math.radians(float(-deg)))
    sin = math.sin(math.radians(float(-deg)))

    if dim == 2: #2D
        transform = numpy.array([[cos, -sin, 0],
                                 [sin, cos, 0],
                                 [0, 0, 1]])

    matrix = numpy.matmul(matrix, transform)
    matrix = translate(matrix, -a, -b, -c)
    return matrix

def reflect(matrixIn, dim, param):
    matrix = copy.deepcopy(matrixIn)
    param = param.lower()
    #target = titik pantul (string)
    #dim = dimensi
    #rtype : matrix

    #mencari titik pantul
    #matrix = copy.deepcopy(matrixIn)
    def get(param):
        #fungsi yang mengembalikan pencarian

        #mencari index dalam ( ) *cek komentar code di bawah
        start = param.find("(") + 1
        stop = param.rfind(")") #rfind == return highest param bleh bleh

        #boolean
        found = (stop - start) >= 1
        if found:
            output = param[start:stop]
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

def shear(matrixIn, dim, param, k):
    matrix = copy.deepcopy(matrixIn)
    transform = numpy.identity(3)
    x = 0
    y = 0
    z = 0
    if param == "x":
        x = k
    elif param == "y":
        y = k
    else:
        z = k

    if dim == 2: #2D
        transform = numpy.array([[1, y, 0],
                                 [x, 1, 0],
                                 [0, 0, 1]])
        matrix = numpy.matmul(matrix, transform)
    else: #3D
        transform = numpy.array([[1, y, z],
                                 [x, 1, z],
                                 [x, y, 1]])
    matrix = numpy.matmul(matrix, transform)
    return matrix

def stretch(matrixIn, dim, param, k):
    matrix = copy.deepcopy(matrixIn)
    transform = numpy.identity(3)
    x = 1
    y = 1
    z = 1
    if param == "x":
        x = k
    elif param == "y":
        y = k
    else:
        z = k

    if dim == 2: #2D
        transform = numpy.array([[x, 0, 0],
                                 [0, y, 0],
                                 [0, 0, 1]])
    else: #3D
        transform = numpy.array([[x, 0, 0],
                                 [0, y, 0],
                                 [0, 0, z]])
    matrix = numpy.matmul(matrix, transform)
    return matrix

def custom(matrixIn, dim, a, b, c, d, e, f, g, h, i):
    matrix = copy.deepcopy(matrixIn)
    if dim == 2:
        transform = numpy.array([[d,b,0],
                                 [c,a,0],
                                 [0,0,1]])
    else:
        transform = numpy.array([[a,d,g],
                                 [b,e,h],
                                 [c,f,i]])
    return numpy.matmul(matrix, transform)

def multiple(matrixIn, dim, n):
    matrix = copy.deepcopy(matrixIn)
    print("Masukkan " + str(n) + " command(s): ")
    for i in range(n):
        command = input("Command " + str(i+1) + ": ").split(" ")
        if command[0] == "translate":
            dx = float(command[1])/100
            dy = float(command[2])/100
            if dim == 2:
                dz = 0
            else:
                dz = float(command[3])/100
            matrix = translate(matrix,dx,dy,dz)

        elif command[0] == "dilate":
            k = float(command[1])
            matrix = dilate(matrix, k)

        elif command[0] == "rotate":
            deg = float(command[1])
            a = float(command[2])
            b = float(command[3])
            if dim == 2:
                c = 0
            else:
                c = float(command[4])
            matrix = rotate(matrix, dim, deg, a, b, c)

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
    print()
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
