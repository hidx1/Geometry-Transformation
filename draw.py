from OpenGL.GL import *
from OpenGL.GLU import *
from math import *
import numpy
warnaCube = (
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (0,1,0),
    (1,1,1),
    (0,1,1),
    (1,0,0),
    (0,1,0),
    (0,0,1),
    (1,0,0),
    (1,1,1),
    (0,1,1),
    )

edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

surfacesCube = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def Cube(vertexMatrix): #Draw cube
    glBegin(GL_QUADS)
    for surface in surfacesCube:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(warnaCube[x])
            glVertex3fv(vertexMatrix[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertexMatrix[vertex])
    glEnd()

def Axis(): #Draw x, y, z axes
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(-500, 0, 0)
    glVertex3f(500, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, -500, 0)
    glVertex3f(0, 500, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -500)
    glVertex3f(0, 0, 500)
    glEnd()

def Draw2D(matrix):
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for i in range(0,len(matrix)):
        #print(matrix[i % len(matrix)])
        glVertex3fv(matrix[i % len(matrix)])
        glVertex3fv(matrix[(i+1) % len(matrix)])
    glEnd()
    glBegin(GL_POLYGON)
    glColor3f(0.3, 0.5, 0)
    for i in range(0,len(matrix)):
        glVertex3fv(matrix[i % len(matrix)])
    glEnd()

def glTranslatefKw(tx,ty,tz):
        matrix = glGetFloatv(GL_MODELVIEW_MATRIX)
        matrix[3,0]+=tx
        matrix[3,1]+=ty
        matrix[3,2]+=tz
        glLoadMatrixf(matrix)

def glRotationfKw(angle,x,y,z):
        matori = glGetFloatv(GL_MODELVIEW_MATRIX)
        c = cos(radians(angle))
        s = sin(radians(angle))
        matrix=IdentityMat44()
        matrix[0,0]=x*x*(1-c)+c
        matrix[0,1]=x*y*(1-c)-z*s
        matrix[0,2]=x*z*(1-c)-y*s

        matrix[1,0]=y*x*(1-c)+z*s
        matrix[1,1]=y*y*(1-c)+c
        matrix[1,2]=y*z*(1-c)+x*s

        matrix[2,0]=x*z*(1-c)+y*s
        matrix[2,1]=y*z*(1-c)-x*s
        matrix[2,2]=z*z*(1-c)+c
        matori= numpy.mat(matrix)*numpy.mat(matori)
        glLoadMatrixf(matori)

def IdentityMat44():
    return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')