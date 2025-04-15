import math
import glfw
import random
from OpenGL.GL import *

num_stars = 100
stars_pos = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(num_stars)]
pos_x = 0
pos_y = 0
mov = 0.01
ang = 0
base_trian = 0.1
ponta_tri = 0.3

def inicio():
    glClearColor(0,0,0,1)

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)
    glBegin(GL_POINTS)
    glColor3f(0.5,1,1)
    for y, x in stars_pos:
        glVertex2f(x, y)
    glEnd()
    global pos_x, pos_y, ang, base_trian, ponta_tri
    glPushMatrix()
    glTranslatef(pos_x,pos_y,0)
    glRotatef(ang,0,0,1)
    glBegin(GL_TRIANGLES)
    glColor3f(0,1,0)
    glVertex2f(-base_trian,0)
    glVertex2f(base_trian,0)
    glVertex2f(0,ponta_tri)
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(1,0,1)
    glVertex2f(-base_trian, 0)
    glVertex2f(base_trian,0)
    glVertex2f(base_trian,-0.30)
    glVertex2f(-base_trian,-0.30)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1,0,0)
    glVertex2f(base_trian,-0.30)
    glVertex2f(0.20,-0.30)
    glVertex2f(base_trian,-0.20)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0,0,1)
    glVertex2f(-base_trian,-0.30)
    glVertex2f(-0.20,-0.30)
    glVertex2f(-base_trian,-0.20)
    glEnd()
    glPopMatrix()
    
    glFlush()
    
  

def teclado(window, key, scancode, action, mods):
    global pos_x, pos_y, ang, mov, aceleracao, base_trian
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        
        if pos_y > 1 :
            pos_y = -1
        if pos_x > 1 :
            pos_x = -1
        if pos_y < -1 :
            pos_y = 1
        if pos_x < -1 :
            pos_x = 1
        if key == glfw.KEY_UP:  
            mov += 0.001
            if mov > 0.2 :
                mov = 0.2
            rot = math.radians(ang+90)
            pos_x += math.cos(rot) * mov 
            pos_y += math.sin(rot) * mov            
        elif key == glfw.KEY_DOWN:
            mov += 0.001
            if mov > 0.2 :
                mov = 0.2
            rot = math.radians(ang+90)
            pos_x -= math.cos(rot) * mov
            pos_y -= math.sin(rot) * mov
        elif key == glfw.KEY_LEFT:
            ang += 10
        elif key == glfw.KEY_RIGHT:
            ang -= 10
    if action == glfw.RELEASE :
        mov = 0.01
       
def main() : 
    glfw.init()
    window = glfw.create_window(600,600,"Teste GLFW", None, None)
    glfw.make_context_current(window)
    glfw.set_key_callback(window,teclado)

    inicio()

    while glfw.window_should_close(window) == False:
        glClear(GL_COLOR_BUFFER_BIT)
        desenha()
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()    

if __name__=="__main__":
    main()



