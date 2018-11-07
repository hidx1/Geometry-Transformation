import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import numpy
import copy
import _thread
import sys
import time
import queue
from calculation import *
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
q = queue.Queue()
numpy.set_printoptions(suppress=True)

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

verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
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

surfaces = (
    (0,1,2,3),
    (3,2,7,6),
    (6,7,5,4),
    (4,5,1,0),
    (1,5,7,2),
    (4,0,3,6)
    )

def Cube(): #Draw cube
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(verticies[vertex])
    glEnd()

    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
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

def IdentityMat44():
    return numpy.matrix(numpy.identity(4), copy=False, dtype='float32')

def threadedConsole(q): #Thread to switch between pygame window and command shell
    global consoling
    consoling = True
    while True:
        command = input(">>> ").split(" ")
        q.put(command)

def CreateMatrix(pasangan_point, matrix): #Fill matrix with user's input
    print("Masukkan nilai point:")
    for i in range(pasangan_point):
        matrix[i][0], matrix[i][1] = input().split(",")
        matrix[i][3] = 1

# --------------------- INTERFACE AWAL ---------------------------------------
bintang = "***************************************************\n"
welcome = "**Selamat Datang di Program Transformasi Geometri**\n"
msg = "Program ini digunakan untuk visualisasi transformasi\ngeometri terhadap objek 2D/3D. Untuk memulai\nprogram, pilih mode yang ingin dijalankan.\n"
def typing(str): #Simulated typing
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.0075)
typing(bintang)
typing(welcome)
typing(bintang)
print(msg)

#Choose between 2D/3D
pilihan = input("Mode yang ingin dijalankan (2D/3D): ")
while(not pilihan == "2D" and not pilihan == "3D"):
    pilihan = input("Input salah. Pilih antara 2D/3D: ")
print()

#Ask and create matrix based on user's input if choice is 2D
if(pilihan == "2D"):
    pasangan_point = int(input("Masukkan jumlah pasangan/tuple point: "))
    matrix = numpy.zeros((pasangan_point, 4)) #Bentuk matrix 3 * pasangan_point
    CreateMatrix(pasangan_point, matrix)
    print()
    print("Matrix yang dihasilkan: ")
    print(matrix)
    print()
else:
    matrix = numpy.zeros((8, 4))
    matrix = numpy.matrix([[1, -1, -1, 1],
                           [1, 1, -1, 1],
                           [-1, 1, -1, 1],
                           [-1, -1, -1, 1],
                           [1, -1, 1, 1],
                           [1, 1, 1, 1],
                           [-1, -1, 1, 1],
                           [-1, 1, 1, 1]])

matrix_result = copy.deepcopy(matrix)

view_mat = IdentityMat44()

# --------------------- Pygame Window ---------------------------------------
pygame.init() #Initialize pygame window
pygame.display.set_caption('Transformasi Geometri ' + str(pilihan)) #Set pygame window name
display = (800,600) #Create pygame window with 800 x 600 resolution
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

view_mat = IdentityMat44()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0, 0, -15)
glGetFloatv(GL_MODELVIEW_MATRIX, view_mat) #ngisi view_mat dengan matrix di stack modelview
glLoadIdentity()

consoling = False
tx = 0
ty = 0
tz = 0
ry = 0
rx = 0
command = [""] * 5 #Initialize list command with empty string

while True:
    command[0] = ""
    #Bagian command
    if not q.empty():
        command = q.get()

    if command[0] == "translate":
        dx = int(command[1])
        dy = int(command[2])
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.1,ty,tz)
        glMultMatrixf(view_mat)
        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPopMatrix()
        #tx=0.1
    elif command[0] == "dilate":
        k = int(command[1])
        dilate(matrix_result, k)
    elif command[0] == "rotate":
        deg = command[1]
        a = command[2]
        b = command[3]
        rotate(matrix_result, deg, a, b)
    elif command[0] == "reflect":
        param = command[1]
        reflect(matrix_result, param)
    elif command[0] == "shear":
        param = command[1]
        k = command[2]
        shear(matrix_result, param, k)
    elif command[0] == "stretch":
        param = command[1]
        k = command[2]
        stretch(matrix_result, param, k)
    elif command[0] == "custom":
        a = command[1]
        b = command[2]
        c = command[3]
        d = command[4]
        custom(matrix_result, a, b, c, d)
    elif command[0] == "multiple":
        n = command[1]
        multiple(matrix, n)
    elif command[0] == "reset":
        matrix_result = copy.deepcopy(matrix)
    elif command[0] == "exit":
        sys.exit(0)

    if not consoling: #If not in pygame window, switch Thread to command shell
            _thread.start_new_thread(threadedConsole,(q,))

    #Event in pygame window
    events = pygame.event.get()
    for event in events:
        #If Esc key is pressed, exit program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #If keyboard key is pressed down
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if   event.key == pygame.K_p:
                print("Printing matrix...")
                print(matrix_result)
                print()
                sys.stdout.write(">>> ")
                sys.stdout.flush()
            if   event.key == pygame.K_a:     tx =  0.1 #if key a is pressed
            elif event.key == pygame.K_d:     tx = -0.1 #if key d is pressed
            elif event.key == pygame.K_q:     ty = -0.1 #if key q is pressed
            elif event.key == pygame.K_e:     ty =  0.1 #if key e is pressed
            elif event.key == pygame.K_w:     tz =  0.1 #if key w is pressed
            elif event.key == pygame.K_s:     tz = -0.1 #if key s is pressed
            elif event.key == pygame.K_RIGHT: ry =  1.0 #if right anchor key is pressed
            elif event.key == pygame.K_LEFT:  ry = -1.0 #if left anchor key is pressed
            elif event.key == pygame.K_UP:    rx = -1.0 #if up anchor key is pressed
            elif event.key == pygame.K_DOWN:  rx =  1.0 #if down anchor key is pressed

        #If keyboard key is let go
        elif event.type == pygame.KEYUP:
            if   event.key == pygame.K_a     and tx > 0: tx = 0
            elif event.key == pygame.K_d     and tx < 0: tx = 0
            elif event.key == pygame.K_q     and ty < 0: ty = 0
            elif event.key == pygame.K_e     and ty > 0: ty = 0
            elif event.key == pygame.K_w     and tz > 0: tz = 0
            elif event.key == pygame.K_s     and tz < 0: tz = 0
            elif event.key == pygame.K_RIGHT and ry > 0: ry = 0.0
            elif event.key == pygame.K_LEFT  and ry < 0: ry = 0.0
            elif event.key == pygame.K_UP    and rx < 0: rx = 0.0
            elif event.key == pygame.K_DOWN  and rx > 0: rx = 0.0

    glPushMatrix()
    glLoadIdentity()
    glTranslatef(tx,ty,tz)
    glRotatef(ry, 0, 1, 0)
    glRotatef(rx, 1, 0, 0)
    glMultMatrixf(view_mat)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    Axis()
    Cube()
    #Axis()
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
