import contextlib
with contextlib.redirect_stdout(None):
    import pygame
import pygame
import numpy
import _thread
import sys
import time
import queue
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
q = queue.Queue()
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

def Cube():
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

def Axis():
    glEnd()
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

def threadedConsole(q):
    global consoling
    consoling = True
    while True:
        command = input("INPUT: ")
        q.put(command)

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
pilihan = input("Mode yang ingin dijalankan (2D/3D): ") #Choose between 2D/3D
while(not pilihan == "2D" and not pilihan == "3D"):
    pilihan = input("Input salah. Pilih antara 2D/3D: ")
print()

view_mat = IdentityMat44()

# --------------------- Pygame Window ---------------------------------------
pygame.init()
pygame.display.set_caption('Transformasi Geometri ' + str(pilihan))
display = (800,600)
screen = pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

glMatrixMode(GL_PROJECTION)
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

view_mat = IdentityMat44()
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()
glTranslatef(0, 0, -15)
glGetFloatv(GL_MODELVIEW_MATRIX, view_mat) #ngisi view_mat dengan matrix di stack modelview
glLoadIdentity()

aturan = 0
consoling = False
tx = 0
ty = 0
tz = 0
ry = 0
rx = 0
while True:
    
    
    command = ""
    #Bagian command
    if not q.empty():
        command = q.get()
    if command == "move":
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.1,ty,tz)
        glMultMatrixf(view_mat)
        glGetFloatv(GL_MODELVIEW_MATRIX, view_mat)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPopMatrix()
        #tx=0.1
        print("moved")
        
        
    if not consoling:
            _thread.start_new_thread(threadedConsole,(q,))
            
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

            if   event.key == pygame.K_a:     tx =  0.1
            elif event.key == pygame.K_d:     tx = -0.1
            elif event.key == pygame.K_q:     ty = -0.1
            elif event.key == pygame.K_e:     ty =  0.1
            elif event.key == pygame.K_w:     tz =  0.1
            elif event.key == pygame.K_s:     tz = -0.1
            elif event.key == pygame.K_RIGHT: ry =  1.0
            elif event.key == pygame.K_LEFT:  ry = -1.0
            elif event.key == pygame.K_UP:    rx = -1.0
            elif event.key == pygame.K_DOWN:  rx =  1.0
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
    Cube()
    Axis()
    glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)