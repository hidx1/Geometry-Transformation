from OpenGL.GL import*
from OpenGL.GLUT import*
from OpenGL.GLU import*
import glfw
import numpy as np
import sys
import time

# INTERFACE AWAL
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

def Cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

# MAIN FUNCTION
def main():

    #initialize GLFW
    if not glfw.init():
        return -1

    #Create windows mode window
    window = glfw.create_window(1024, 720, "Transformasi Geometri Objek " + str(pilihan), None, None)

    if not window:
        glfw.terminate()
        return -1

    #Make GLFW window's context current
    glfw.make_context_current(window)

    #Loop until window closes
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        #Poll and process events
        glfw.poll_events()
        #Swap front and back buffers
        glfw.swap_buffers(window)

    #Terminate GLFW window
    glfw.terminate()

if __name__ == "__main__":
    main()
