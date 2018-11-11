from OpenGL.GL import *
from OpenGL.GLU import *
colors = (
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

verticies = [
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, -1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
    ]

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

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def Cube(vertexMatrix): #Draw cube
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(vertexMatrix[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            #print(verticies[vertex])
            # print(type(verticies[vertex]))
            glVertex3fv(vertexMatrix[vertex])
    glEnd()

def Axis(): #Draw x, y, z axes
    glBegin(GL_LINES)
    glColor3f(1, 0, 0)
    glVertex3f(-50, 0, 0)
    glVertex3f(50, 0, 0)

    glColor3f(0, 1, 0)
    glVertex3f(0, -50, 0)
    glVertex3f(0, 50, 0)

    glColor3f(0, 0, 1)
    glVertex3f(0, 0, -50)
    glVertex3f(0, 0, 50)
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
    glColor3f(0, 1, 0)
    for i in range(0,len(matrix)):
        glVertex3fv(matrix[i % len(matrix)])
    glEnd()