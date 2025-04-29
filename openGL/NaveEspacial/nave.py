import math
import glfw
import random
from OpenGL.GL import *

NUM_ESTRELAS = 500
NUM_METEOROS = 5
ACELERACAO = 0.0001  
VEL_MAX = 0.02       
VEL_ROT = 0.6    
DES = 0.98        
VEL_PROJ = 0.03  
DEE_METEORO = 0.98
VEL_METEORO = 0.002  

pos_estrelas = []
teclas = {}
px, py = 0.0, 0.0
vx, vy = 0.0, 0.0
ang = 0.0
projeteis = []
meteoros = []
base_tri = 0.07
radius = 0.05

def iniciar_jogo():
    global pos_estrelas, teclas, meteoros
    pos_estrelas = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(NUM_ESTRELAS)]
    teclas = {glfw.KEY_UP: False, glfw.KEY_DOWN: False, glfw.KEY_LEFT: False, glfw.KEY_RIGHT: False, glfw.KEY_SPACE: False}
    meteoros = [(random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-VEL_METEORO, VEL_METEORO), random.uniform(-VEL_METEORO, VEL_METEORO)) for _ in range(NUM_METEOROS)]

def desenhar_fundo_e_nave():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1, 1, 1)
    glPointSize(2)
    glBegin(GL_POINTS)
    for x, y in pos_estrelas:
        glVertex2f(x, y)
    glEnd()
    desenhar_nave()
    desenhar_projetil()
    desenhar_meteoros()

def desenhar_nave():
    global base_tri
    ponta_tri = 0.21
    glPushMatrix()
    glTranslatef(px, py, 0)
    glRotatef(ang, 0, 0, 1)
    glBegin(GL_TRIANGLES)
    glColor3f(0, 1, 0)
    glVertex2f(-base_tri, 0)
    glVertex2f(base_tri, 0)
    glVertex2f(0, ponta_tri)
    glEnd()
    glBegin(GL_QUADS)
    glColor3f(1, 0, 1)
    glVertex2f(-base_tri, 0)
    glVertex2f(base_tri, 0)
    glVertex2f(base_tri, -0.21)
    glVertex2f(-base_tri, -0.21)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(1, 0, 0)
    glVertex2f(base_tri, -0.21)
    glVertex2f(0.14, -0.21)
    glVertex2f(base_tri, -0.14)
    glEnd()
    glBegin(GL_TRIANGLES)
    glColor3f(0, 0, 1)
    glVertex2f(-base_tri, -0.21)
    glVertex2f(-0.14, -0.21)
    glVertex2f(-base_tri, -0.14)
    glEnd()
    glPopMatrix()

def teclado(window, key, scancode, action, mods):
    if key in teclas:
        teclas[key] = (action != glfw.PRESS)

def atualizar_jogo():
    global px, py, vx, vy, ang, projeteis, meteoros
    ang += (VEL_ROT if teclas[glfw.KEY_LEFT] else -VEL_ROT) if teclas[glfw.KEY_LEFT] or teclas[glfw.KEY_RIGHT] else 0
    if teclas[glfw.KEY_UP]:
        rad = math.radians(ang + 90)
        vx += math.cos(rad) * ACELERACAO
        vy += math.sin(rad) * ACELERACAO
    velocidade = math.sqrt(vx**2 + vy**2)
    if velocidade > VEL_MAX:
        escala = VEL_MAX / velocidade
        vx *= escala
        vy *= escala
    px += vx
    py += vy
    vx *= DES
    vy *= DES
    if px > 1: px = -1
    if px < -1: px = 1
    if py > 1: py = -1
    if py < -1: py = 1
    if teclas[glfw.KEY_SPACE]:
        disparar_projetil()
    atualizar_projetis()
    atualizar_meteoros()

def disparar_projetil():
    rad = math.radians(ang + 90)
    vel_proj_x = math.cos(rad) * VEL_PROJ
    vel_proj_y = math.sin(rad) * VEL_PROJ
    projeteis.append([px + math.cos(rad) * 0.01, py + math.sin(rad) * 0.01, vel_proj_x, vel_proj_y])

def atualizar_projetis():
    global projeteis
    for proj in list(projeteis):
        proj[0] += proj[2]
        proj[1] += proj[3]
        if abs(proj[0]) > 1 or abs(proj[1]) > 1:
            projeteis.remove(proj)

def desenhar_projetil():
    glColor3f(1, 0, 1)
    for proj in projeteis:
        glPushMatrix()
        glTranslatef(proj[0], proj[1], 0)
        glBegin(GL_QUADS)
        glVertex2f(-0.02, -0.02)
        glVertex2f(0.02, -0.02)
        glVertex2f(0.02, 0.02)
        glVertex2f(-0.02, 0.02)
        glEnd()
        glPopMatrix()

def atualizar_meteoros():
    global meteoros
    for i in range(len(meteoros)):
        meteoros[i] = (meteoros[i][0] + meteoros[i][2], meteoros[i][1] + meteoros[i][3], meteoros[i][2], meteoros[i][3])
        if abs(meteoros[i][0]) > 1 or abs(meteoros[i][1]) > 1:
            meteoros[i] = (random.uniform(-1, 1), random.uniform(-1, 1), random.uniform(-VEL_METEORO, VEL_METEORO), random.uniform(-VEL_METEORO, VEL_METEORO))

def desenhar_meteoros():
    global radius
    glColor3f(0.5, 0.5, 0.5)
    for meteor in meteoros:
        num_segments = 10
        for i in range(num_segments):
            angle1 = 2 * math.pi * i / num_segments
            angle2 = 2 * math.pi * (i + 1) / num_segments
            glBegin(GL_TRIANGLES)
            glVertex2f(meteor[0], meteor[1])
            glVertex2f(meteor[0] + radius * math.cos(angle1), meteor[1] + radius * math.sin(angle1))
            glVertex2f(meteor[0] + radius * math.cos(angle2), meteor[1] + radius * math.sin(angle2))
            glEnd()

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

def checarColisao(quad_x, quad_y, s_tam, cx, cy, raio):
    metade = s_tam / 2
    x_prox = clamp(cx, quad_x - metade, quad_x + metade)
    y_prox = clamp(cy, quad_y - metade, quad_y + metade)    
    distance = math.hypot(x_prox - cx, y_prox - cy)
    return distance < raio

def verificarColisao(vx, vy):
    return checarColisao(vx, vy, base_tri, meteoros[0], meteoros[1], radius)

def main():
    if not glfw.init():
        return
    janela = glfw.create_window(600, 600, "Teste GLFW", None, None)
    glfw.make_context_current(janela)
    glfw.set_key_callback(janela, teclado)
    iniciar_jogo()
    while not glfw.window_should_close(janela):
        glClear(GL_COLOR_BUFFER_BIT)
        atualizar_jogo()
        desenhar_fundo_e_nave()
        glfw.swap_buffers(janela)
        glfw.poll_events()
    glfw.terminate()

if __name__ == "__main__":
    main()
