import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class RotatingLampScene:
    def __init__(self, width=800, height=600, use_ambient_light=True):
        self.width = width
        self.height = height
        self.use_ambient_light = use_ambient_light
        self.angle = 0.0

        if not glfw.init():
            raise RuntimeError("Failed to initialize GLFW")

        self.window = glfw.create_window(self.width, self.height, "Lâmpada Giratória", None, None)
        if not self.window:
            glfw.terminate()
            raise RuntimeError("Failed to create GLFW window")

        glfw.make_context_current(self.window)

        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, self.width / float(self.height or 1), 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glEnable(GL_DEPTH_TEST)

        self.setup_lighting()

    def setup_lighting(self):
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT1)

        if self.use_ambient_light:
            glEnable(GL_LIGHT0)
            # Luz ambiente global fraca
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.02, 0.02, 0.02, 1.0])
            # Luz fixa
            light0_pos = [1.0, 1.0, 1.0, 1.0]
            glLightfv(GL_LIGHT0, GL_POSITION, light0_pos)
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
            glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])
        else:
            glDisable(GL_LIGHT0)
            # Luz ambiente global zero
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def update_moving_light(self):
        radius = 3.0
        height = 2.5
        x = radius * math.cos(math.radians(self.angle))
        z = radius * math.sin(math.radians(self.angle))
        pos = [x, height, z, 1.0]

        glLightfv(GL_LIGHT1, GL_POSITION, pos)
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.95, 0.8, 1.0])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 0.95, 0.8, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        return pos

    def draw_lamp(self, position, radius=0.25):
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

    def run(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glLoadIdentity()
            # Câmera fixa olhando para origem
            gluLookAt(0, 2, 6, 0, 0, 0, 0, 1, 0)

            lamp_pos = self.update_moving_light()
            self.draw_lamp(lamp_pos[:3])

            glfw.swap_buffers(self.window)

            self.angle += 0.2
            if self.angle >= 360:
                self.angle -= 360

        glfw.terminate()


if __name__ == "__main__":
    # Escolha True para ter luz ambiente e luz fixa + lâmpada móvel
    # Escolha False para ter só a lâmpada móvel iluminando no escuro
    scene = RotatingLampScene(use_ambient_light=False)
    scene.run()
