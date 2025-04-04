import glfw
from OpenGL.GL import *

pos_x = 0
pos_y = 0
rotate = 0
frente1 = 0.3
frente2 = 0

def inicio():
    glClearColor(0,0,0,1)

def desenha():
    glClear(GL_COLOR_BUFFER_BIT)
    global pos_x, pos_y, rotate
    glPushMatrix()
    glTranslatef(pos_x,pos_y,0)
    glRotatef(rotate,0,0,1)
    glBegin(GL_TRIANGLES)
    glVertex2f(-0.1,0)
    glVertex2f(0.1,0)
    glVertex2f(frente2,frente1)
    glEnd()
    glFlush()
    glPopMatrix()
  

def teclado(window, key, scancode, action, mods):
    global pos_x, pos_y,rotate, frente2, frente1
    if action == glfw.PRESS or action == glfw.REPEAT:
        
        if pos_x >= 0.75:
            pos_x = 0.75
        if pos_x <= -0.75:
            pos_x = -0.75
        if key == glfw.KEY_W:
            print(rotate)
            if(rotate == -360):
                rotate = 0
            if(rotate == 0):
                pos_y +=0.1
            if(rotate == -30):
                pos_y +=0.1
                pos_x +=0.1
            if(rotate == -60):
                pos_y +=0.1
                pos_x +=0.1
            if(rotate == -90):
                pos_x +=0.1
            if(rotate == -120):
                pos_y -=0.1
                pos_x +=0.1
            if(rotate == -150):
                pos_y -=0.1
                pos_x +=0.1
            if(rotate == -180):
                pos_y -=0.1
            if(rotate == -210):
                pos_y -=0.1
                pos_x -=0.1
            if(rotate == -240):
                pos_y -=0.1
                pos_x -=0.1
            if(rotate == -270):
                pos_x -=0.1
            if(rotate == -300):
                pos_y +=0.1
                pos_x -=0.1
            if(rotate == -330):
                pos_y +=0.1
                pos_x -=0.1
            if(rotate == -360):
                pos_y +=0.1
            
        if key == glfw.KEY_A:
            pos_x -= 0.1
        if key == glfw.KEY_S:
            pos_y -= 0.1
        if key == glfw.KEY_D:
            pos_x += 0.1
        if key == glfw.KEY_LEFT:
            rotate -= 30
        if key == glfw.KEY_RIGHT:
            rotate += 30
        

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



