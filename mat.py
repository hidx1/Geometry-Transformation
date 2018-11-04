import numpy
import math
#belum dikerjakan : reflect,custom

def multiple(mat1, mat2):
    #untuk multiplikasi di 'rotate'

    try:
        temp = numpy.matmul(mat1, mat2) #matmul = matrix product of 2 arrays
        return temp
    except Exception as e:
        print(str(e))

def translate(dx=0, dy=0, dz=0, dim=2):
    #dim=dimension
    #rtype : matrix
    
    transform = numpy.identity(dim+1,dtype=int)

    try:
        dx = float(dx)
        dy = float(dy)
        dz = float(dz)
    except Exception as e:
        print(str(e))
        return transform
    
    if dim == 2: #2D
        transform = numpy.array([1, 0, dx],
                                [0, 1, dy],
                                [0, 0, 1])
    elif dim == 3: #3D
        transform = numpy.array([1, 0, 0, dx],
                                [0, 1, 0, dy],
                                [0, 0, 1, dz],
                                [0, 0, 0, 1])
    else:
        print("dimensi 2/3")
    
    return transform

def dilate(scale=1, dim=2): 
    #scale : int/float
    #rtype : matrix

    transform = numpy.identity(dim+1, dtype=int)
    s = float(scale)

    if dim == 2: #2D
        transform = numpy.array([s, 0, 0],
                                [0, s, 0],
                                [0, 0, 1])
    elif dim == 3: #3D
        transform = numpy.array([s, 0, 0, 0],
                                [0, s, 0, 0],
                                [0, 0, s, 0],
                                [0, 0, 0, 1])
    else:
        print("dimensi 2/3")

    return transform

def rotate(degree=0, x=0, y=0, z=0, dim=2, axis='x'):
    #degree : derajat perputaran (int/float)
    #x : poros [x]
    #y : poros [y]
    #z : poros [z]
    #axis : char, axis rotasi 3D
    #rtype : matrix

    transform = numpy.identity(dim+1, dtype=int)

    cos = math.cos(math.radians(float(degree)))
    sin = math.sin(math.radians(float(degree)))
    poros = False #apakah poros berubah

    try:
        x = float(x)
        y = float(y)
        z = float(z)
    
    except Exception as e:
        print(str(e))
    
    #inisialisasi transform sebelum dan sesudah translasi
    belum = transform
    sudah = transform

    if x != 0 or y != 0 or z != 0: #kasus poros tidak di (0,0,0)
        poros = True
        belum = translate(-x, -y, -z, dim=dim)
        sudah = translate(x, y, z, dim=dim)

    if dim == 2: #2D
        transform = numpy.array([cos, -sin, 0],
                                [sin, cos, 0],
                                [0, 0, 1])

    elif dim == 3: #3D
        axis = axis.strip().lower() #cari axis, lower krn paramnya dipake huruf kecil

        #rotasi sesuai axis
        if axis == "x":
            transform = numpy.array([1, 0, 0, 0],
                                    [0, cos, -sin, 0],
                                    [0, sin, cos, 0],
                                    [0, 0, 0, 1])
        elif axis == "y":
            transform = numpy.array([cos, 0, sin, 0],
                                    [0, 1, 0, 0],
                                    [-sin, 0, cos, 0],
                                    [0, 0, 0, 1])
        elif axis == "z":
            transform = numpy.array([cos, -sin, 0, 0],
                                    [sin, cos, 0, 0],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1])
        else:
            print("error")

    else:
        print("dimensi 2/3")

    if poros:
        transform = multiple(transform, belum)
        transform = multiple(sudah, transform)
    return transform

def shear(axis, scale=1, dim=2):
    #axis : char
    #scale : faktor shear
    #rtype : matrix

    axis = axis.strip().lower()
    found = True
    transform = numpy.identity(dim+1, dtype=int)

    try:
        scale = float(scale)
    except Exception as e:
        print(str(e))
        return transform

    x = 0
    y = 0
    z = 0

    if axis == "x":
        x = scale
    elif axis == "y":
        y = scale
    elif axis == "z":
        z = scale
    else:
        print("error")
        found = False

    if found:
        if dim == 2: #2D
            transform = numpy.array([1, x, 0],
                                    [y, 1, 0],
                                    [0, 0, 1])
        elif dim == 3: #3D
            transform = numpy.array([1, y, z, 0],
                                    [x, 1, z, 0],
                                    [x, y, 1, 0],
                                    [0, 0, 0, 1])
        else:
            print("dimensi 2/3")
        
def stretch(axis, scale=1, dim=2):
    
    axis = axis.strip().lower()
    found = True
    transform = numpy.identity(dim+1, dtype=int)

    try:
        scale = float(scale)
    except Exception as e:
        print(str(e))
        return transform

    x = 1
    y = 1
    z = 1

    if axis == "x":
        x = scale
    elif axis == "y":
        y = scale
    elif axis == "z":
        z = scale
    else:
        print("error")
        found = False

    if found:
        if dim == 2: #2D
            transform = numpy.array([x, 0, 0],
                                    [0, y, 0],
                                    [0, 0, 1])
        elif dim == 3: #3D
            transform = numpy.array([x, 0, 0, 0],
                                    [0, y, 0, 0],
                                    [0, 0, z, 0],
                                    [0, 0, 0, 1])
        else:
            print("dimensi 2/3")
    return transform