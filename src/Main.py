import pygame
import moderngl
import numpy as np
import DragonCurve
from PIL import Image

class main:
    def __init__(self):
        # pygame init
        pygame.init()
        pygame.display.init()

        size = (1000, 1000)

        # crate screen
        self.screen = pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
        pygame.display.set_caption("Dragon Curve by Derflinger David")

        # clock
        self.clock = pygame.time.Clock()

        # read vertex shader
        with open('shaders/VertexShader.glsl', 'r') as file:
            vertex_shader = file.read()

        # read fragment shader
        with open('shaders/FragmentShader.glsl', 'r') as file:
            fragment_shader = file.read()

        # create moderngl context and program
        self.ctx = moderngl.create_context()
        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.dragonCurve = DragonCurve.DragonCurve()
        self.pointsArray = self.dragonCurve.generateStartArray()

        self.running = True

    def run(self):
        # generate dragon curve first generation
        scaler = 1.5
        vertices = self.dragonCurve.generateVerticesArray(self.pointsArray)
        middle = [0, 0.5]

        while self.running:
            generateNext = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # quit
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE: # quit
                        self.running = False
                    elif event.key == pygame.K_SPACE: # generate next dragon curve generation
                        generateNext = True
                    elif event.key == pygame.K_s: # save rendert image
                        print("Save")
                        Image.frombytes('RGB', self.screen.get_size(), self.ctx.screen.read(), 'raw', 'RGB', 0, -1).save("DragonCurve.png")

            # hotkeys for zooming in and out
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                scaler += 0.005 * scaler
            elif keys[pygame.K_DOWN]:
                scaler -= 0.005 * scaler

            # clear Screen
            bgColor = (0.1, 0.1, 0.1)
            self.ctx.clear(bgColor[0], bgColor[1], bgColor[2])

            # generate next dragon curve generation
            if generateNext:
                scaler, self.pointsArray, vertices, middle = self.dragonCurve.generateNext(self.pointsArray)
                print("Generate")

            # create buffer object and vertex array object
            vbo = self.ctx.buffer(vertices)
            vao = self.ctx.vertex_array(self.prog, vbo, 'in_Position', 'in_vNumber')

            # vertex shader variables
            self.prog['scaler'] = scaler
            self.prog['middle'] = middle

            # fragment shader variables
            self.prog['startColor'] = [255,0,0]
            self.prog['endColor'] = [0,255,0]
            self.prog['amount'] = len(self.pointsArray)-1

            # render the image
            vao.render(moderngl.LINE_STRIP)

            # releasing
            vbo.release()
            vao.release()

            # display the rendered image
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    main = main()
    main.run()