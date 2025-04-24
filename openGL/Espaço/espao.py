import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

def initialize_window():
    if not glfw.init():
        raise Exception("GLFW não pode ser iniciado")
    
    window = glfw.create_window(800, 600, "Sol, Terra, Lua e Rotação", None, None)
    
    glfw.make_context_current(window)
    
    return window

def draw_circle(radius, num_segments):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex2f(x, y)
    glEnd()

def draw_earth(radius):
    glColor3f(0.0, 0.0, 1.0)
    draw_circle(radius, 50)

def draw_sun():
    glColor3f(1.0, 1.0, 0.0)
    draw_circle(1.0, 50)

def draw_moon():
    glColor3f(0.8, 0.8, 0.8)
    draw_circle(0.3, 50)

def draw_scene(rotation_angle, earth_angle):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -10.0)

    glPushMatrix()
    draw_sun()
    glPopMatrix()

    glPushMatrix()
    x_earth = 5.0 * math.cos(earth_angle)
    y_earth = 3.0 * math.sin(earth_angle)
    glTranslatef(x_earth, y_earth, 0.0)
    glRotatef(rotation_angle, 0.0, 0.0, 1.0)
    draw_earth(0.6)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(x_earth + 1.5, y_earth, 0.0)
    draw_moon()
    glPopMatrix()

def main():
    window = initialize_window()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 800/600, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    earth_angle = 0.0
    rotation_angle = 0.0
    while not glfw.window_should_close(window):
        glfw.poll_events()
        draw_scene(rotation_angle, earth_angle)
        rotation_angle += 0.1
        earth_angle += 0.002
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
