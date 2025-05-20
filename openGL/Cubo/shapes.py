from OpenGL.GL import *
from OpenGL.GLU import *
import math

def draw_cube_face(size, thickness):
    half = size / 2
    half_thick = thickness / 2
    glBegin(GL_QUADS)
    # Front face
    glNormal3f(0, 0, 1)
    glVertex3f(-half, -half, half_thick)
    glVertex3f(half, -half, half_thick)
    glVertex3f(half, half, half_thick)
    glVertex3f(-half, half, half_thick)
    # Back face
    glNormal3f(0, 0, -1)
    glVertex3f(-half, -half, -half_thick)
    glVertex3f(half, -half, -half_thick)
    glVertex3f(half, half, -half_thick)
    glVertex3f(-half, half, -half_thick)
    # Right face
    glNormal3f(1, 0, 0)
    glVertex3f(half, -half, -half_thick)
    glVertex3f(half, half, -half_thick)
    glVertex3f(half, half, half_thick)
    glVertex3f(half, -half, half_thick)
    # Left face
    glNormal3f(-1, 0, 0)
    glVertex3f(-half, -half, -half_thick)
    glVertex3f(-half, half, -half_thick)
    glVertex3f(-half, half, half_thick)
    glVertex3f(-half, -half, half_thick)
    # Top face
    glNormal3f(0, 1, 0)
    glVertex3f(-half, half, -half_thick)
    glVertex3f(half, half, -half_thick)
    glVertex3f(half, half, half_thick)
    glVertex3f(-half, half, half_thick)
    # Bottom face
    glNormal3f(0, -1, 0)
    glVertex3f(-half, -half, -half_thick)
    glVertex3f(half, -half, -half_thick)
    glVertex3f(half, -half, half_thick)
    glVertex3f(-half, -half, half_thick)
    glEnd()

def draw_cylinder_between_points(p1, p2, radius, segments=16):
    direction = [p2[i] - p1[i] for i in range(3)]
    height = math.sqrt(sum([c**2 for c in direction]))
    if height == 0:
        return
    dir_norm = [c / height for c in direction]

    glPushMatrix()
    glTranslatef(*p1)

    up = [0, 0, 1]
    axis = (
        up[1]*dir_norm[2] - up[2]*dir_norm[1],
        up[2]*dir_norm[0] - up[0]*dir_norm[2],
        up[0]*dir_norm[1] - up[1]*dir_norm[0]
    )
    angle = math.acos(max(min(sum([up[i]*dir_norm[i] for i in range(3)]), 1), -1)) * (180.0 / math.pi)

    if abs(angle) > 0.0001 and any(axis):
        glRotatef(angle, *axis)

    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluCylinder(quad, radius, radius, height, segments, 1)
    gluDeleteQuadric(quad)
    glPopMatrix()

def draw_sphere(position, radius, segments=16):
    glPushMatrix()
    glTranslatef(*position)
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, segments, segments)
    gluDeleteQuadric(quad)
    glPopMatrix()
