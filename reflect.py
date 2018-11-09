import numpy
import math
import mat

def reflect(target,dim=2):
    #target = titik pantul (string)
    #dim = dimensi
    #rtype : matrix

    transform = numpy.identity(dim+1,dtype=int)

    #mencari titik pantul
    target = "".join(target.split())
    target = target.strip().lower()

    def get(target):
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
        if target == "x":
            transform = numpy.array([1, 0, 0],
                                    [0, -1, 0],
                                    [0, 0, 1])
        elif target == "y":
            transform = numpy.array([-1, 0 ,0],
                                    [0, 1, 0],
                                    [0, 0, 1])
        elif target == "y=x":
            transform = numpy.array([0, 1, 0],
                                    [1, 0, 0],
                                    [0, 0, 1])
        elif target == "y=-x":
            transform = numpy.array([0, -1, 0],
                                    [-1, 0, 0],
                                    [0, 0, 1])
        else: #reflect berdasar titik
            get_point = get(target)
            if len(get_point) >= 2:

                #apakah titik sumbu dapat digunakan
                try:
                    get_point = [float(x) for x in get_point]
                    a = float(get_point[0])
                    b = float(get_point[1])
                except Exception as e:
                    print(str(e))
                    return transform

                #rumusnya reflect(x) = 2(poros x) - x
                #translasi -2(poros x) *(-1)
                transform = numpy.array([-1, 0, 2*a],
                                        [0, -1, 2*b],
                                        [0, 0, 1])
            else:
                print("error")
                return transform
    elif dim == 3: #3D
        if target == "xy":
            transform = numpy.array([1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,-1,0],
                                    [0,0,0,1])
        elif target == "yz":
            transform = numpy.array([-1,0,0,0],
                                    [0,1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1])
        elif target == "xz":
            transform = numpy.array([1,0,0,0],
                                    [0,-1,0,0],
                                    [0,0,1,0],
                                    [0,0,0,1])
        else:
            print("error")
        
        return transform

# command = "" #input
# global vertices

# command, param = mat.input_command()
# if "reflect" in command: #main.py line 220
#     try:
#         target = param[0]
#     except:
#         target = "(0,0)"

#     transform = reflect.reflect(target=target, dim=dim)
#     hasil = mat.multiple(transform,vertices)