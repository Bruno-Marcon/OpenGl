from OpenGL.GL import *
from shapes import draw_cube_face, draw_cylinder_between_points, draw_sphere

def draw_rounded_cube(size=2.0, corner_radius=0.2):
    half_size = size / 2
    face_size = size - 2 * corner_radius

    # Material - inox look
    mat_ambient = [0.3, 0.3, 0.3, 1.0]
    mat_diffuse = [0.8, 0.8, 0.8, 1.0]
    mat_specular = [1.0, 1.0, 1.0, 1.0]
    shininess = [100.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

    # Desenha as faces centrais
    glPushMatrix()
    glTranslatef(0, 0, half_size - corner_radius/2)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, 0, -half_size + corner_radius/2)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(half_size - corner_radius/2, 0, 0)
    glRotatef(90, 0, 1, 0)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-half_size + corner_radius/2, 0, 0)
    glRotatef(90, 0, 1, 0)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, half_size - corner_radius/2, 0)
    glRotatef(90, 1, 0, 0)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0, -half_size + corner_radius/2, 0)
    glRotatef(90, 1, 0, 0)
    draw_cube_face(face_size, corner_radius)
    glPopMatrix()

    # Desenha as arestas (cilindros)
    edges = [
        [(half_size - corner_radius, half_size - corner_radius, -half_size + corner_radius),
         (half_size - corner_radius, half_size - corner_radius, half_size - corner_radius)],
        [(-half_size + corner_radius, half_size - corner_radius, -half_size + corner_radius),
         (-half_size + corner_radius, half_size - corner_radius, half_size - corner_radius)],
        [(half_size - corner_radius, -half_size + corner_radius, -half_size + corner_radius),
         (half_size - corner_radius, -half_size + corner_radius, half_size - corner_radius)],
        [(-half_size + corner_radius, -half_size + corner_radius, -half_size + corner_radius),
         (-half_size + corner_radius, -half_size + corner_radius, half_size - corner_radius)],

        [(-half_size + corner_radius, half_size - corner_radius, half_size - corner_radius),
         (half_size - corner_radius, half_size - corner_radius, half_size - corner_radius)],
        [(-half_size + corner_radius, -half_size + corner_radius, half_size - corner_radius),
         (half_size - corner_radius, -half_size + corner_radius, half_size - corner_radius)],
        [(-half_size + corner_radius, half_size - corner_radius, -half_size + corner_radius),
         (half_size - corner_radius, half_size - corner_radius, -half_size + corner_radius)],
        [(-half_size + corner_radius, -half_size + corner_radius, -half_size + corner_radius),
         (half_size - corner_radius, -half_size + corner_radius, -half_size + corner_radius)],

        [(half_size - corner_radius, -half_size + corner_radius, -half_size + corner_radius),
         (half_size - corner_radius, half_size - corner_radius, -half_size + corner_radius)],
        [(-half_size + corner_radius, -half_size + corner_radius, -half_size + corner_radius),
         (-half_size + corner_radius, half_size - corner_radius, -half_size + corner_radius)],
        [(half_size - corner_radius, -half_size + corner_radius, half_size - corner_radius),
         (half_size - corner_radius, half_size - corner_radius, half_size - corner_radius)],
        [(-half_size + corner_radius, -half_size + corner_radius, half_size - corner_radius),
         (-half_size + corner_radius, half_size - corner_radius, half_size - corner_radius)],
    ]

    for edge in edges:
        draw_cylinder_between_points(edge[0], edge[1], corner_radius)

    # Desenha os vértices (esferas)
    vertices = [
        (half_size - corner_radius, half_size - corner_radius, half_size - corner_radius),
        (half_size - corner_radius, half_size - corner_radius, -half_size + corner_radius),
        (half_size - corner_radius, -half_size + corner_radius, half_size - corner_radius),
        (half_size - corner_radius, -half_size + corner_radius, -half_size + corner_radius),
        (-half_size + corner_radius, half_size - corner_radius, half_size - corner_radius),
        (-half_size + corner_radius, half_size - corner_radius, -half_size + corner_radius),
        (-half_size + corner_radius, -half_size + corner_radius, half_size - corner_radius),
        (-half_size + corner_radius, -half_size + corner_radius, -half_size + corner_radius)
    ]

    for vertex in vertices:
        draw_sphere(vertex, corner_radius)
