import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math

# Variáveis globais
rotacao_x = 0.0
rotacao_y = 0.0
dist_zoom = 8.0  # Distância da câmera
mouse_clicado = False
mouse_pos = (0, 0)

def carregar_textura(caminho):
    img = Image.open(caminho).transpose(Image.FLIP_TOP_BOTTOM)
    img_data = img.convert("RGB").tobytes()
    largura, altura = img.size

    textura_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textura_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largura, altura, 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return textura_id

def init_window():
    width, height = 800, 600
    glfw.init()        
    window = glfw.create_window(width, height, "Cubo com Zoom", None, None)
    glfw.make_context_current(window)
    
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Callbacks de entrada
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    return window

# Callback de teclado
def key_callback(window, key, scancode, action, mods):
    global rotacao_x, rotacao_y
    if action in [glfw.PRESS, glfw.REPEAT]:
        if key == glfw.KEY_UP:
            rotacao_x -= 5
        elif key == glfw.KEY_DOWN:
            rotacao_x += 5
        elif key == glfw.KEY_LEFT:
            rotacao_y -= 5
        elif key == glfw.KEY_RIGHT:
            rotacao_y += 5

# Callback de rolagem do mouse (zoom)
def scroll_callback(window, xoffset, yoffset):
    global dist_zoom
    dist_zoom -= yoffset  # Aproxima ou afasta
    dist_zoom = max(2.0, min(dist_zoom, 50.0))  # Limites de zoom

# Callback de clique do mouse
def mouse_button_callback(window, button, action, mods):
    global mouse_clicado
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_clicado = (action == glfw.PRESS)

# Callback de movimento do mouse
def cursor_position_callback(window, xpos, ypos):
    global mouse_pos, rotacao_x, rotacao_y
    if mouse_clicado:
        dx = xpos - mouse_pos[0]
        dy = ypos - mouse_pos[1]
        rotacao_y += dx * 0.5
        rotacao_x += dy * 0.5
    mouse_pos = (xpos, ypos)

# Desenha o cilindro com textura
def draw_cylinder(radius=2.0, height=4.0, num_segments=40, textura_id=None):
    # Base inferior
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, 0.0)  # centro
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, 0.0)
    glEnd()

    # Base superior
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, height)  # centro
    for i in range(num_segments + 1):
        angle = 2 * math.pi * i / num_segments
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        glVertex3f(x, y, height)
    glEnd()

    # Lateral do cilindro com textura
    if textura_id:
        glBindTexture(GL_TEXTURE_2D, textura_id)
        glBegin(GL_QUAD_STRIP)
        for i in range(num_segments + 1):
            angle = 2 * math.pi * i / num_segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            u = i / num_segments  # Coordenada horizontal
            glTexCoord2f(u, 0.0)
            glVertex3f(x, y, 0.0)
            glTexCoord2f(u, 1.0)
            glVertex3f(x, y, height)
        glEnd()

# Loop principal
def main():
    global rotacao_x, rotacao_y, dist_zoom
    window = init_window()
    textura_id = carregar_textura("nescau.png")
    glEnable(GL_TEXTURE_2D)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Define a posição da câmera com base na distância (zoom)
        gluLookAt(
            dist_zoom * 0.5, dist_zoom * 0.4, dist_zoom,
            0, 0, 0,
            0, 1, 0
        )

        # Aplica rotação
        glRotatef(rotacao_x, 1, 0, 0)
        glRotatef(rotacao_y, 0, 1, 0)

        draw_cylinder(textura_id=textura_id)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
