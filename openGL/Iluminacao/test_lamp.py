from lamp_component import RotatingLampScene
from OpenGL.GL import *
from OpenGL.GLU import gluLookAt
import glfw

def draw_simple_cube(size=1.5):
    half = size / 2
    glBegin(GL_QUADS)

    # Frente (normal para frente)
    glNormal3f(0, 0, 1)
    glVertex3f(-half, -half, half)
    glVertex3f(half, -half, half)
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)

    # Atrás
    glNormal3f(0, 0, -1)
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(-half, half, -half)

    # Direita
    glNormal3f(1, 0, 0)
    glVertex3f(half, -half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(half, half, half)
    glVertex3f(half, -half, half)

    # Esquerda
    glNormal3f(-1, 0, 0)
    glVertex3f(-half, -half, -half)
    glVertex3f(-half, half, -half)
    glVertex3f(-half, half, half)
    glVertex3f(-half, -half, half)

    # Cima
    glNormal3f(0, 1, 0)
    glVertex3f(-half, half, -half)
    glVertex3f(half, half, -half)
    glVertex3f(half, half, half)
    glVertex3f(-half, half, half)

    # Baixo
    glNormal3f(0, -1, 0)
    glVertex3f(-half, -half, -half)
    glVertex3f(half, -half, -half)
    glVertex3f(half, -half, half)
    glVertex3f(-half, -half, half)

    glEnd()

class TestLampWithCube(RotatingLampScene):
    def run(self):
        while not self.window_should_close():
            self.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glLoadIdentity()
            # câmera um pouco mais afastada para ver o cubo e a lâmpada
            gluLookAt(0, 2, 6, 0, 0, 0, 0, 1, 0)

            lamp_pos = self.update_moving_light()
            self.draw_lamp(lamp_pos[:3])

            draw_simple_cube()

            self.swap_buffers()

            self.angle += 0.1
            if self.angle >= 360:
                self.angle -= 360

    def window_should_close(self):
        return glfw.window_should_close(self.window)

    def poll_events(self):
        glfw.poll_events()

    def swap_buffers(self):
        glfw.swap_buffers(self.window)

def test_lamp_with_cube_and_ambient():
    scene = TestLampWithCube(use_ambient_light=True)
    scene.run()

def test_lamp_with_cube_no_ambient():
    scene = TestLampWithCube(use_ambient_light=False)
    scene.run()

if __name__ == "__main__":
    #test_lamp_with_cube_and_ambient()
    test_lamp_with_cube_no_ambient()
