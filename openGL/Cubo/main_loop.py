import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

from cube_rounded import draw_rounded_cube
from lighting import setup_lighting, update_moving_light, draw_lamp

WIDTH, HEIGHT = 800, 600

def run_render_loop():
    if not glfw.init():
        print("Erro ao iniciar GLFW")
        return
    window = glfw.create_window(WIDTH, HEIGHT, "Cubo Arredondado com Luz Giratória", None, None)
    if not window:
        glfw.terminate()
        print("Erro ao criar janela GLFW")
        return
    glfw.make_context_current(window)

    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / float(HEIGHT or 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    setup_lighting()

    angle = 0

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(5, 3, 2, 0, 0, 0, 0, 1, 0)

        # Atualiza posição da luz APÓS configurar a câmera
        lamp_pos = update_moving_light(angle)

        # Desenha o cubo arredondado
        draw_rounded_cube()

        # Desenha a esfera que representa a lâmpada emissora na posição da luz
        draw_lamp(position=lamp_pos[:3])

        glfw.swap_buffers(window)

        angle += 0.4
        if angle >= 360:
            angle -= 360

    glfw.terminate()
