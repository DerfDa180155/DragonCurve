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

        self.screen = pygame.display.set_mode((1000, 1000), pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)
        pygame.display.set_caption("Dragon Curve by Derflinger David")

        self.clock = pygame.time.Clock()

        self.ctx = moderngl.create_context()

        vertex_shader = '''
        #version 330 core
        
        in vec2 in_Position;
        //in vec3 in_Color;
        in float in_vNumber;
        
        uniform float scaler;
        uniform vec2 middle;
        
        //out vec3 v_Color;
        out float v_Number;
        
        void main() {
            gl_Position = vec4((in_Position-middle)*scaler, 0.0, 1.0);
            //v_Color = in_Color;
            v_Number = in_vNumber;
        }
        '''

        fragment_shader = '''
        #version 330 core
        
        in vec3 v_Color;
        in float v_Number;
        
        uniform vec3 startColor;
        uniform vec3 endColor;
        uniform int amount;
        
        out vec4 f_Color;
        
        vec3 tempColor;
        vec3 tempColor2;
        vec3 finalColor;
        
        void main() {
            //f_Color = vec4(v_Color*v_Number/255, 1.0);
            tempColor = (endColor-startColor)/amount;
            tempColor2 = tempColor*v_Number;
            finalColor = startColor + tempColor2;
            f_Color = vec4(finalColor/255, 1.0);
        }
        '''

        self.prog = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        self.dragonCurve = DragonCurve.DragonCurve()
        self.pointsArray = self.dragonCurve.generateStartArray()

        self.running = True

    def run(self):
        scaler = 1.5
        vertices = self.dragonCurve.generateVerticesArray(self.pointsArray)
        middle = [0, 0.5]

        while self.running:
            generateNext = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
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

            if generateNext:
                scaler, self.pointsArray, vertices, middle = self.dragonCurve.generateNext(self.pointsArray)
                print("Generate")

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

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == '__main__':
    main = main()
    main.run()