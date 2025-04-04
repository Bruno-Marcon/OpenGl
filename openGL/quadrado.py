from OpenGL.GL import *
from OpenGL.GLUT import *

def inicio():
    #define a cor de fundo da tela
    glClearColor(0, 1, 0)

def desenha():
    # limpa a tela e mantem a cor definida no inicio
    glClear(GL_COLOR_BUFFER_BIT)
    glFlush()


def main():
    try:
        # inicialização do glut; tbm inicializa a maquina de estados do OpenGL
        glutInit() 
        # define modo de exibição
        glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB) 
        # posicao da janela 
        glutInitWindowPosition(100, 100)
        # tamanho da janela
        glutInitWindowSize(600, 600)
        glutCreateWindow(b"Ola mundo grafico!")
    except Exception as e:
        printf("Erro ao criar contexto OpenGL: {e}")

    inicio()
    glutDisplayFunc(desenha)
    glutMainLoop()

if __name__ == '__main__':
    main()

