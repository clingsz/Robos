from game import *
from whitenoise import *

line = NoiseArea((0, 0), (screen_width, screen_height), screen)

g = None
rects = []
class RandomRect():
    def __init__(self):
        temp = random.randint(230, 250)
        self.color = (temp, temp, temp)
        self.size = (random.randint(200, 300), random.randint(200, 300))
        self.speed = [random.randint(1, 3), random.randint(1, 3)]
        self.pos = [0, 0]
        if random.randint(0, 1):
            if random.randint(0, 1):
                self.pos[1] = -300
                self.pos[0] = random.randint(0, screen_width - 100)
                self.speed[0] = 0
            else:
                self.pos[1] = screen_height
                self.pos[0] = random.randint(0, screen_width - 100)
                self.speed[0] = 0
                self.speed[1] = -self.speed[1]
        else:
            if random.randint(0, 1):
                self.pos[0] = -300
                self.pos[1] = random.randint(0, screen_height - 100)
                self.speed[1] = 0
            else:
                self.pos[0] = screen_width
                self.pos[1] = random.randint(0, screen_height - 50)
                self.speed[1] = 0
                self.speed[0] = -self.speed[0]

    def draw(self):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if self.pos[0] > screen_width:
            self.pos[0] = - 300
        elif self.pos[0] < -300:
            self.pos[0] = screen_width
        elif self.pos[1] > screen_height:
            self.pos[1] = - 300
        elif self.pos[1] < -300:
            self.pos[1] = screen_height
        pygame.draw.rect(screen, self.color, pygame.Rect(self.pos, self.size))

for _ in range(10):
    rects.append(RandomRect())

bgs[0].playNonStop()
while(True):
    mouse_pos[0] = pygame.mouse.get_pos()[0]
    mouse_pos[1] = pygame.mouse.get_pos()[1]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            if g:
                g.handle_event(event)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_k:
                        g = Game()
                        bgs[0].stop()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                g = Game()
                bgs[0].stop()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    if g:
        g.update()
    else:
        line.update()

    screen.fill(-1)
    for r in rects:
        r.draw()
    if g:
        g.draw()
    else:
        screen.blit(texture_lib["title_screen"], (0, 0))
        line.draw()
    text_scroll.draw()

    pygame.display.flip()
    clock.tick(30)