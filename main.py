import contextlib
with contextlib.redirect_stdout(None): #prevent welcome message from pygame
    import pygame
import numpy
import copy
import _thread
import sys
import time
import queue
import math
import os
from calculation import *
from pygame.locals import *
from draw import *
from inputThread import *
from OpenGL.GL import *
from OpenGL.GLU import *

numpy.set_printoptions(suppress=True) #prevent scientific notation
global matrix_result
global q
global dim
q = queue.Queue()

def CreateVertexMatrix(pasangan_point, matrix): #Fill matrix with user's input
    print("Masukkan nilai point:")
    for i in range(pasangan_point):
        matrix[i][0], matrix[i][1] = map(float, input().split(","))
        matrix[i][0] /= 100
        matrix[i][1] /= 100

# --------------------- INTERFACE AWAL ---------------------------------------
os.system('cls')  # Clear screen for Windows
#os.system('clear') #Clear screen for Linux/OS X
print(" _      _                         _______                   __                           _   _             ")
time.sleep(0.075)
print("| |    (_)                       |__   __|                 / _|                         | | (_)            ")
time.sleep(0.075)
print("| |     _ _ __   ___  __ _ _ __     | |_ __ __ _ _ __  ___| |_ ___  _ __ _ __ ___   __ _| |_ _  ___  _ __  ")
time.sleep(0.075)
print("| |    | | '_ \ / _ \/ _` | '__|    | | '__/ _` | '_ \/ __|  _/ _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \ ")
time.sleep(0.075)
print("| |____| | | | |  __/ (_| | |       | | | | (_| | | | \__ \ || (_) | |  | | | | | | (_| | |_| | (_) | | | |")
time.sleep(0.075)
print("|______|_|_| |_|\___|\__,_|_|       |_|_|  \__,_|_| |_|___/_| \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|")
time.sleep(0.075)
print("______           ___  _____                    _   ____  _____     ____  _     _           _   ")
time.sleep(0.075)
print("|  ____|         |__ \\|  __ \\                  | | |___ \\|  __ \\   / __ \\| |   (_)         | |  ")
time.sleep(0.075)
print("| |__ ___  _ __     ) | |  | |   __ _ _ __   __| |   __) | |  | | | |  | | |__  _  ___  ___| |_ ")
time.sleep(0.075)
print("|  __/ _ \\| '__|   / /| |  | |  / _` | '_ \\ / _` |  |__ <| |  | | | |  | | '_ \\| |/ _ \\/ __| __|")
time.sleep(0.075)
print("| | | (_) | |     / /_| |__| | | (_| | | | | (_| |  ___) | |__| | | |__| | |_) | |  __/ (__| |_ ")
time.sleep(0.075)
print("|_|  \\___/|_|    |____|_____/   \\__,_|_| |_|\\__,_| |____/|_____/   \\____/|_.__/| |\\___|\\___|\\__|")
time.sleep(0.075)
print("                                                                              _/ |              ")
time.sleep(0.075)
print("                                                                             |__/               ")
time.sleep(2)
os.system('cls')  # Clear screen for Windows
#os.system('clear') #Clear screen for Linux/OS X
bintang = "***************************************************\n"
welcome = "**Selamat Datang di Program Transformasi Geometri**\n"
msg = "Program ini digunakan untuk visualisasi transformasi\nlinier terhadap objek 2D/3D. Untuk memulai\nprogram, pilih mode yang ingin dijalankan.\n"
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
print("Mode yang ingin dijalankan: ")
print("1. 2D Dimensi")
print("2. 3D Dimensi")
pilihan = int(input("Pilihan: "))
while(not pilihan == 1 and not pilihan == 2):
    pilihan = int(input("Input salah. Pilih antara 2D/3D: "))
print()

#Ask and create matrix based on user's input if choice is 2D
if(pilihan == 1):
    dim = 2
    pasangan_point = int(input("Masukkan jumlah pasangan point: "))
    matrix = numpy.zeros((pasangan_point, 3))
    CreateVertexMatrix(pasangan_point, matrix) #Bentuk matrix sebesar pasangan_point * 3
    print()
else:
    dim = 3
    matrix = numpy.array([[1.0, -1.0, -1.0], #matrix for cube
                           [1.0, 1.0, -1.0],
                           [-1.0, 1.0, -1.0],
                           [-1.0, -1.0, -1.0],
                           [1.0, -1.0, 1.0],
                           [1.0, 1.0, 1.0],
                           [-1.0, -1.0, 1.0],
                           [-1.0, 1.0, 1.0]])

matrix_result = copy.deepcopy(matrix)

view_mat = IdentityMat44()

# --------------------- Pygame Window and glView Initialization ----------------
pygame.init() #Initialize pygame window
pygame.display.set_caption('Transformasi Geometri ' + str(dim) + 'D') #Set pygame window name
display = (800,600) #Create pygame window with 800 x 600 resolution
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)

gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
view_mat = IdentityMat44()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0, 0, -15)
glGetFloatv(GL_MODELVIEW_MATRIX, view_mat) #ngisi view_mat dengan matrix di stack modelview
glLoadIdentity()

_thread.start_new_thread(windowInput,(q,dim,matrix,matrix_result,)) #New thread Initialization

tx = 0
ty = 0
tz = 0
rx = 0
ry = 0
rz = 0

while True:
    #Bagian command
    if not q.empty():
        command = q.get()
        if command[1] == 0:
            matrix_result = animasi(matrix_result, command[0]) #animate the object
        else:
            matrix_result = command[0]

    #Event in pygame window
    events = pygame.event.get()
    for event in events:
        #If Esc key is pressed, exit program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        #If keyboard key is pressed down
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: #press esc to exit program
                pygame.quit()
                quit()

            if   event.key == pygame.K_p: #press p key to print current matrix
                print("Printing matrix...")
                print(matrix_result)
                print()
                sys.stdout.write(">>> ")
                sys.stdout.flush()

            if   event.key == pygame.K_a:     tx =  0.1 #if key a is pressed
            elif event.key == pygame.K_d:     tx = -0.1 #if key d is pressed
            elif event.key == pygame.K_q:     ty =  0.1 #if key q is pressed
            elif event.key == pygame.K_e:     ty = -0.1 #if key e is pressed
            elif event.key == pygame.K_w:     tz =  0.1 #if key w is pressed
            elif event.key == pygame.K_s:     tz = -0.1 #if key s is pressed
            elif event.key == pygame.K_UP:    rx = -1.0 #if up anchor key is pressed
            elif event.key == pygame.K_DOWN:  rx =  1.0 #if down anchor key is pressed
            elif event.key == pygame.K_RIGHT: ry =  1.0 #if right anchor key is pressed
            elif event.key == pygame.K_LEFT:  ry = -1.0 #if left anchor key is pressed
            elif event.key == pygame.K_c:     rz = -1.0 #if key c is pressed
            elif event.key == pygame.K_x:     rz =  1.0 #if key x is pressed

        #If keyboard key is let go
        elif event.type == pygame.KEYUP:
            if   event.key == pygame.K_a     and tx > 0: tx = 0
            elif event.key == pygame.K_d     and tx < 0: tx = 0
            elif event.key == pygame.K_q     and ty > 0: ty = 0
            elif event.key == pygame.K_e     and ty < 0: ty = 0
            elif event.key == pygame.K_w     and tz > 0: tz = 0
            elif event.key == pygame.K_s     and tz < 0: tz = 0
            elif event.key == pygame.K_RIGHT and ry > 0: ry = 0.0
            elif event.key == pygame.K_LEFT  and ry < 0: ry = 0.0
            elif event.key == pygame.K_UP    and rx < 0: rx = 0.0
            elif event.key == pygame.K_DOWN  and rx > 0: rx = 0.0
            elif event.key == pygame.K_c     and rz < 0: rz = 0.0
            elif event.key == pygame.K_x     and rz > 0: rz = 0.0

    glPushMatrix()
    glLoadIdentity()

    #Camera manipulation
    CameraTranslate(tx,ty,tz) #translate by tx, ty, tz
    CameraRotation(rx, 1, 0, 0) #rotate camera
    CameraRotation(ry, 0, 1, 0)
    CameraRotation(rz, 0, 0, 1)

    glMultMatrixf(view_mat)
    glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    if dim == 2: #if 2D, draw 2D object
        Draw2D(matrix_result)
    else: #if 3D, draw cube
        Cube(matrix_result)
    Axis(dim) #draw axis based on object's dimension
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(math.floor(1000/75))
