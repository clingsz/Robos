import random
import pygame

class NoiseArea:
    def __init__(self, pos, deme, screen, level = 5):
        self.pos = pos
        self.deme = deme
        self.lines = [random.randint(self.pos[0], self.pos[0] + self.deme[0]) for i in range(level*5)]
        self.speed = 1
        self.chance = 8
        self.tick = 2
        self.screen = screen

    def draw(self):
        if random.randint(0, self.chance) == 0:
            for i in self.lines:
                temp = random.randint(220, 250)
                pygame.draw.line(self.screen, (temp, temp, temp), (i, self.pos[1]), (i, self.pos[1]+self.deme[1]))

    def update(self):
        if random.randint(0, self.chance) == 0:
            self.tick += 1
            if self.tick > self.speed:
                self.tick = 0
                for i in range(len(self.lines)):
                    self.lines[i] = random.randint(self.pos[0], self.pos[0] + self.deme[0])

if __name__ == "__main__":
    screen = pygame.display.set_mode((400, 400))
    line = NoiseArea((0, 0), (400, 400), screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        line.update()
        screen.fill(0)
        line.draw()
        pygame.display.flip()
        clock.tick(30)