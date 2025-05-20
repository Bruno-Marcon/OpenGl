#COM LUZ AMBIENTE

# from OpenGL.GL import *
# from OpenGL.GLU import *
# import math

# def setup_lighting():
#     glEnable(GL_LIGHTING)
#     glEnable(GL_LIGHT0)
#     glEnable(GL_LIGHT1)

#     # Ativa o uso das cores como material para iluminação
#     glEnable(GL_COLOR_MATERIAL)
#     glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

#     # Luz ambiente global bem fraca para não "lavar" o efeito das luzes pontuais
#     glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.02, 0.02, 0.02, 1.0])

#     # Luz fixa (GL_LIGHT0) com luz ambiente baixa, luz difusa e especular alta
#     light0_position = [1.0, 1.0, 1.0, 1.0]
#     glLightfv(GL_LIGHT0, GL_POSITION, light0_position)
#     glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
#     glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
#     glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])

# def update_moving_light(angle_deg, radius=3.0, height=2.5):
#     x = radius * math.cos(math.radians(angle_deg))
#     z = radius * math.sin(math.radians(angle_deg))
#     pos = [x, height, z, 1.0]

#     glLightfv(GL_LIGHT1, GL_POSITION, pos)
#     glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0])
#     glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.95, 0.8, 1.0])
#     glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

#     return pos

# def draw_lamp(position=(0,3,0), radius=0.25):
#     glPushMatrix()
#     glTranslatef(*position)

#     emission_color = [1.0, 0.95, 0.6, 1.0]
#     zero_emission = [0.0, 0.0, 0.0, 1.0]

#     glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emission_color)
#     glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, emission_color)
#     glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, zero_emission)
#     glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)

#     quad = gluNewQuadric()
#     gluQuadricNormals(quad, GLU_SMOOTH)
#     gluSphere(quad, radius, 32, 16)
#     gluDeleteQuadric(quad)

#     glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, zero_emission)
#     glPopMatrix()


# SEM LUZ

from OpenGL.GL import *
from OpenGL.GLU import *
import math

def setup_lighting():
    glEnable(GL_LIGHTING)
    # Desliga a luz fixa para ficar só a móvel
    # glEnable(GL_LIGHT0)  # NÃO habilita a luz fixa
    glEnable(GL_LIGHT1)  # habilita só a luz móvel

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    # Luz ambiente global praticamente zero, para ficar tudo escuro exceto luz móvel
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

    # Não configura GL_LIGHT0 pois está desligada

def update_moving_light(angle_deg, radius=3.0, height=2.5):
    x = radius * math.cos(math.radians(angle_deg))
    z = radius * math.sin(math.radians(angle_deg))
    pos = [x, height, z, 1.0]

    glLightfv(GL_LIGHT1, GL_POSITION, pos)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.95, 0.8, 1.0])
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

    return pos

def draw_lamp(position=(0,3,0), radius=0.25):
    glPushMatrix()
    glTranslatef(*position)

    emission_color = [1.0, 0.95, 0.6, 1.0]
    zero_emission = [0.0, 0.0, 0.0, 1.0]

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, emission_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, emission_color)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, zero_emission)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 0)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, 32, 16)
    gluDeleteQuadric(quad)

    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, zero_emission)
    glPopMatrix()
