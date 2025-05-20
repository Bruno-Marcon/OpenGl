import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

width, height = 800, 600

pos_cubo = [0.0, 0.0, 0.0]
angulo_rotacao = 0.0
pos_luz = [3.0, 2.5, 0.0]

mouse_ativo = False
ultimo_x, ultimo_y = 0, 0

luz_ambiente_ativa = True

def desenharCubinhoFace(tam_face, espessura):
    metade = tam_face / 2
    metade_esp = espessura / 2
    glBegin(GL_QUADS)
    # Frente
    glNormal3f(0,0,1)
    glVertex3f(-metade, -metade, metade_esp)
    glVertex3f(metade, -metade, metade_esp)
    glVertex3f(metade, metade, metade_esp)
    glVertex3f(-metade, metade, metade_esp)
    # Atrás
    glNormal3f(0,0,-1)
    glVertex3f(-metade, -metade, -metade_esp)
    glVertex3f(metade, -metade, -metade_esp)
    glVertex3f(metade, metade, -metade_esp)
    glVertex3f(-metade, metade, -metade_esp)
    # Direita
    glNormal3f(1,0,0)
    glVertex3f(metade, -metade, -metade_esp)
    glVertex3f(metade, metade, -metade_esp)
    glVertex3f(metade, metade, metade_esp)
    glVertex3f(metade, -metade, metade_esp)
    # Esquerda
    glNormal3f(-1,0,0)
    glVertex3f(-metade, -metade, -metade_esp)
    glVertex3f(-metade, metade, -metade_esp)
    glVertex3f(-metade, metade, metade_esp)
    glVertex3f(-metade, -metade, metade_esp)
    # Cima
    glNormal3f(0,1,0)
    glVertex3f(-metade, metade, -metade_esp)
    glVertex3f(metade, metade, -metade_esp)
    glVertex3f(metade, metade, metade_esp)
    glVertex3f(-metade, metade, metade_esp)
    # Baixo
    glNormal3f(0,-1,0)
    glVertex3f(-metade, -metade, -metade_esp)
    glVertex3f(metade, -metade, -metade_esp)
    glVertex3f(metade, -metade, metade_esp)
    glVertex3f(-metade, -metade, metade_esp)
    glEnd()

def desenharCilindroEntre(p1, p2, raio, segmentos=16):
    dir_vec = [p2[i] - p1[i] for i in range(3)]
    altura = math.sqrt(sum([c**2 for c in dir_vec]))
    if altura == 0:
        return
    dir_norm = [c / altura for c in dir_vec]

    glPushMatrix()
    glTranslatef(*p1)

    up = [0, 0, 1]
    axis = (up[1]*dir_norm[2] - up[2]*dir_norm[1],
            up[2]*dir_norm[0] - up[0]*dir_norm[2],
            up[0]*dir_norm[1] - up[1]*dir_norm[0])
    angle = math.acos(max(min(sum([up[i]*dir_norm[i] for i in range(3)]),1),-1)) * (180.0 / math.pi)

    if abs(angle) > 0.0001 and (axis[0] != 0 or axis[1] != 0 or axis[2] != 0):
        glRotatef(angle, *axis)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, raio, raio, altura, segmentos, 1)
    gluDeleteQuadric(quad)

    glPopMatrix()

def desenharEsfera(pos, raio, segmentos=16):
    glPushMatrix()
    glTranslatef(*pos)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, raio, segmentos, segmentos)
    gluDeleteQuadric(quad)
    glPopMatrix()

def desenharCuboArredondado(tam=2.0, raio=0.2):
    tam_meio = tam / 2
    face_tam = tam - 2*raio

    mat_amb = [0.3, 0.3, 0.3, 1.0]
    mat_diff = [0.8, 0.8, 0.8, 1.0]
    mat_spec = [1.0, 1.0, 1.0, 1.0]
    shininess = [100.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_amb)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diff)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_spec)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

    glPushMatrix()
    glTranslatef(0, 0, tam_meio - raio/2)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -tam_meio + raio/2)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(tam_meio - raio/2, 0, 0)
    glRotatef(90, 0,1,0)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    # Aqui está a correção para a chamada glTranslatef com 3 argumentos
    glPushMatrix()
    glTranslatef(-tam_meio + raio/2, 0, 0)
    glRotatef(90, 0,1,0)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, tam_meio - raio/2, 0)
    glRotatef(90, 1,0,0)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -tam_meio + raio/2, 0)
    glRotatef(90, 1,0,0)
    desenharCubinhoFace(face_tam, raio)
    glPopMatrix()

    arestas = [
        [(tam_meio - raio, tam_meio - raio, -tam_meio + raio), (tam_meio - raio, tam_meio - raio, tam_meio - raio)],
        [(-tam_meio + raio, tam_meio - raio, -tam_meio + raio), (-tam_meio + raio, tam_meio - raio, tam_meio - raio)],
        [(tam_meio - raio, -tam_meio + raio, -tam_meio + raio), (tam_meio - raio, -tam_meio + raio, tam_meio - raio)],
        [(-tam_meio + raio, -tam_meio + raio, -tam_meio + raio), (-tam_meio + raio, -tam_meio + raio, tam_meio - raio)],

        [(-tam_meio + raio, tam_meio - raio, tam_meio - raio), (tam_meio - raio, tam_meio - raio, tam_meio - raio)],
        [(-tam_meio + raio, -tam_meio + raio, tam_meio - raio), (tam_meio - raio, -tam_meio + raio, tam_meio - raio)],
        [(-tam_meio + raio, tam_meio - raio, -tam_meio + raio), (tam_meio - raio, tam_meio - raio, -tam_meio + raio)],
        [(-tam_meio + raio, -tam_meio + raio, -tam_meio + raio), (tam_meio - raio, -tam_meio + raio, -tam_meio + raio)],

        [(tam_meio - raio, -tam_meio + raio, -tam_meio + raio), (tam_meio - raio, tam_meio - raio, -tam_meio + raio)],
        [(-tam_meio + raio, -tam_meio + raio, -tam_meio + raio), (-tam_meio + raio, tam_meio - raio, -tam_meio + raio)],
        [(tam_meio - raio, -tam_meio + raio, tam_meio - raio), (tam_meio - raio, tam_meio - raio, tam_meio - raio)],
        [(-tam_meio + raio, -tam_meio + raio, tam_meio - raio), (-tam_meio + raio, tam_meio - raio, tam_meio - raio)],
    ]

    for a in arestas:
        desenharCilindroEntre(a[0], a[1], raio)

    vertices = [
        (tam_meio - raio, tam_meio - raio, tam_meio - raio),
        (tam_meio - raio, tam_meio - raio, -tam_meio + raio),
        (tam_meio - raio, -tam_meio + raio, tam_meio - raio),
        (tam_meio - raio, -tam_meio + raio, -tam_meio + raio),
        (-tam_meio + raio, tam_meio - raio, tam_meio - raio),
        (-tam_meio + raio, tam_meio - raio, -tam_meio + raio),
        (-tam_meio + raio, -tam_meio + raio, tam_meio - raio),
        (-tam_meio + raio, -tam_meio + raio, -tam_meio + raio)
    ]

    for v in vertices:
        desenharEsfera(v, raio)

def setupLighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    if luz_ambiente_ativa:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
    else:
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

    light0_pos = [1.0, 1.0, 1.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light0_pos)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    if luz_ambiente_ativa:
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    else:
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.95, 0.8, 1.0])
    if luz_ambiente_ativa:
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.2, 0.18, 0.15, 1.0])
    else:
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

def desenharLampada(pos=(0,3,0), raio=0.25):
    glPushMatrix()
    glTranslatef(*pos)

    emissao = [1.0, 0.95, 0.6, 1.0]
    zero = [0.0, 0.0, 0.0, 1.0]

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emissao)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, emissao)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, zero)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, raio, 32, 16)
    gluDeleteQuadric(quad)

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, zero)
    glPopMatrix()

def key_callback(window, key, scancode, action, mods):
    global pos_cubo, pos_luz, angulo_rotacao, luz_ambiente_ativa

    if action == glfw.PRESS or action == glfw.REPEAT:
        step = 0.1
        step_luz = 0.1
        step_rot = 3.0

        if key == glfw.KEY_L:
            luz_ambiente_ativa = not luz_ambiente_ativa
            if luz_ambiente_ativa:
                glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
                glLightfv(GL_LIGHT0, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
                glLightfv(GL_LIGHT1, GL_AMBIENT, [0.2, 0.18, 0.15, 1.0])
            else:
                glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
                glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
                glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
            return

        if key == glfw.KEY_W:
            pos_cubo[1] += step
        elif key == glfw.KEY_S:
            pos_cubo[1] -= step
        elif key == glfw.KEY_A:
            pos_cubo[0] -= step
        elif key == glfw.KEY_D:
            pos_cubo[0] += step
        elif key == glfw.KEY_Q:
            angulo_rotacao += step_rot
            if angulo_rotacao >= 360:
                angulo_rotacao -= 360
        elif key == glfw.KEY_E:
            angulo_rotacao -= step_rot
            if angulo_rotacao < 0:
                angulo_rotacao += 360
        elif key == glfw.KEY_UP:
            pos_luz[1] += step_luz
        elif key == glfw.KEY_DOWN:
            pos_luz[1] -= step_luz
        elif key == glfw.KEY_LEFT:
            pos_luz[0] -= step_luz
        elif key == glfw.KEY_RIGHT:
            pos_luz[0] += step_luz

def mouse_button_callback(window, button, action, mods):
    global mouse_ativo, ultimo_x, ultimo_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouse_ativo = True
            ultimo_x, ultimo_y = glfw.get_cursor_pos(window)
        elif action == glfw.RELEASE:
            mouse_ativo = False

def cursor_pos_callback(window, xpos, ypos):
    global mouse_ativo, ultimo_x, ultimo_y, pos_cubo

    if mouse_ativo:
        dx = xpos - ultimo_x
        dy = ypos - ultimo_y

        pos_cubo[0] += dx * 0.01
        pos_cubo[1] -= dy * 0.01

        ultimo_x, ultimo_y = xpos, ypos

def main():
    global pos_cubo, pos_luz, angulo_rotacao, luz_ambiente_ativa

    if not glfw.init():
        print("Erro ao iniciar GLFW")
        return
    window = glfw.create_window(width, height, "Cubo Arredondado com Luz e Controle", None, None)
    if not window:
        glfw.terminate()
        print("Erro ao criar janela GLFW")
        return
    glfw.make_context_current(window)

    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_pos_callback)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / float(height or 1), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)

    setupLighting()

    while not glfw.window_should_close(window):
        glfw.poll_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()
        gluLookAt(5, 3, 2, 0, 0, 0, 0, 1, 0)

        pos_luz_4 = [pos_luz[0], pos_luz[1], pos_luz[2], 1.0]
        glLightfv(GL_LIGHT1, GL_POSITION, pos_luz_4)

        desenharLampada(pos=pos_luz, raio=0.25)

        glPushMatrix()
        glTranslatef(*pos_cubo)
        glRotatef(angulo_rotacao, 0, 1, 0)
        desenharCuboArredondado()
        glPopMatrix()

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
