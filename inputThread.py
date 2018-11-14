from calculation import *
import os

def windowInput(q,dim,matrix,matrix_result): #Thread to switch between pygame window and perintah shell
    while True:
        perintah = input(">>> ").split(" ")
        matrixOri = copy.deepcopy(matrix_result)
        matrix_result = copy.deepcopy(matrix_result)
        matrix_result = numpy.array(matrix_result, dtype = numpy.float64)
        if perintah[0] == "translate":
            dx = float(perintah[1])/100
            dy = float(perintah[2])/100
            if dim == 2:
                dz = 0
            else:
                dz = float(perintah[3])/100
            matrix_result = translate(matrix_result,dx,dy,dz)

        elif perintah[0] == "dilate":
            k = float(perintah[1])
            matrix_result = dilate(matrix_result, k)

        elif perintah[0] == "rotate":
            deg = numpy.float64(perintah[1])
            a = float(perintah[2])
            b = float(perintah[3])
            if dim == 2:
                c = 0
                axis = ""
            else:
                c = float(perintah[4])
                axis = perintah[5]
            for i in range(0,60):
                matrix_result = rotate(matrix_result, dim, numpy.float64(deg/60), a, b, c, axis)
                data = []
                data.append(matrix_result)
                data.append(1)
                q.put(data)

        elif perintah[0] == "reflect":
            param = perintah[1]
            matrix_result = reflect(matrix_result, dim, param)

        elif perintah[0] == "shear":
            param = perintah[1]
            k = float(perintah[2])
            if dim == 3:
                l = float(perintah[3])
            else:
                l = 0
            matrix_result = shear(matrix_result, dim, param, k, l)

        elif perintah[0] == "stretch":
            param = perintah[1]
            k = float(perintah[2])
            matrix_result = stretch(matrix_result, dim, param, k)

        elif perintah[0] == "custom":
            a = float(perintah[1])
            b = float(perintah[2])
            c = float(perintah[3])
            d = float(perintah[4])
            if dim == 2:
                e = 0
                f = 0
                g = 0
                h = 0
                i = 0
            else:
                e = float(perintah[5])
                f = float(perintah[6])
                g = float(perintah[7])
                h = float(perintah[8])
                i = float(perintah[9])
            matrix_result = custom(matrix_result, dim, a, b, c, d, e, f, g, h, i)

        elif perintah[0] == "multiple":
            n = int(perintah[1])
            matrix_result = multiple(matrix_result, dim, n)

        elif perintah[0] == "reset":
            matrix_result = copy.deepcopy(matrix)

        elif perintah[0] == "exit":
            os._exit(0)

        if perintah[0] != "rotate":
            for i in range(0,60):
                data = []
                data.append(differenceCalc(matrixOri, matrix_result, 60))
                data.append(0)
                q.put(data)
        matrixOri = matrix_result
