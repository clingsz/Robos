from config import *

class Gui():
    def __init__(self, name):
        self.name = name
        self.dead = False
        self.return_info = []

    def update(self):
        pass

    def draw(self):
        pass

    def handle_event(self, event):
        pass

class PasswordGui(Gui):
    def __init__(self):
        Gui.__init__(self, "password")
        self.areas = [pygame.Rect(270, 280, 60, 25),
                      pygame.Rect(200, 160, 60, 25), pygame.Rect(270, 160, 60, 25), pygame.Rect(350, 160, 60, 25),
                      pygame.Rect(200, 200, 60, 25), pygame.Rect(270, 200, 60, 25), pygame.Rect(350, 200, 60, 25),
                      pygame.Rect(200, 240, 60, 25), pygame.Rect(270, 240, 60, 25), pygame.Rect(350, 240, 60, 25)]
        self.hovered = [False for _ in range(10)]
        self.rendered_num = [font3.render(str(i), False, (40, 40, 40)) for i in range(10)]

    def draw(self):
        screen.blit(texture_lib["password_gui"], (0, 0))
        for i in range(10):
            if self.hovered[i]:
                screen.blit(texture_lib["hovered"], self.areas[i].topleft)
        for i in range(len(self.return_info)):
            screen.blit(self.rendered_num[self.return_info[i]], (215+i*70, 80))

    def update(self):
        for i in range(10):
            if self.areas[i].collidepoint(mouse_pos[0], mouse_pos[1]):
                self.hovered[i] = True
            else:
                self.hovered[i] = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            temp = -1
            for i in range(10):
                if self.hovered[i]:
                    temp = i
            if temp != -1:
                self.return_info.append(temp)
                password_audio.playOnce()
                if len(self.return_info) == 3:
                    self.dead = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

class HintGui(Gui):
    def __init__(self):
        Gui.__init__(self, "hint")

    def draw(self):
        screen.blit(texture_lib["hint_gui"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dead = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

class PipeGui(Gui):
    def __init__(self):
        Gui.__init__(self, "pipe")
        self.directions = [[0, 2, 1],
                           [1, 1, 0],
                           [0, 0, 3]]
        self.result1 = [[3, 0, 0,],
                       [0, 0, 0,],
                       [0, 2, 1,]]
        self.result2 = [[3, 0, -1, ],
                        [0, 0, -1, ],
                        [0, 2, 0, ]]
        self.pipes = [[2, 2, 1],
                      [1, 1, 1],
                      [1, 2, 2]]
        self.hovered = [[False for _ in range(3)] for _ in range(3)]
        self.areas = [[], [], []]
        for i in range(3):
            for ii in range(3):
                self.areas[i].append(pygame.Rect(210 + ii * 70, 80 + i * 70, 70, 70))

    def check(self):
        flag1 = True
        flag2 = True
        for i in range(3):
            for ii in range(3):
                if self.pipes[i][ii] == 1:
                    if self.result1[i][ii] != self.directions[i][ii] and \
                            self.result1[i][ii] + 2 != self.directions[i][ii]:
                        flag1 = False
                    if self.result2[i][ii] != -1:
                        if self.result2[i][ii] != self.directions[i][ii] and \
                                self.result2[i][ii] + 2 != self.directions[i][ii]:
                            flag2 = False
                else:
                    if self.result1[i][ii] != self.directions[i][ii]:
                        flag1 = False
                    if self.result2[i][ii] != -1:
                        if self.result2[i][ii] != self.directions[i][ii]:
                            flag2 = False
        if flag1:
            return 1
        elif flag2:
            return 2
        return 0


    def draw(self):
        screen.blit(texture_lib["pipe_gui"], (0, 0))
        for i in range(3):
            for ii in range(3):
                screen.blit(texture_lib["pipe"+str(self.pipes[i][ii])+"_"+str(self.directions[i][ii])],
                            (210 + ii * 70, 80 + i * 70))
                if self.hovered[i][ii]:
                    screen.blit(texture_lib["select"], (210 + ii * 70, 80 + i * 70))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(3):
                for ii in range(3):
                    if self.hovered[i][ii]:
                        self.directions[i][ii] += 1
                        if self.directions[i][ii] > 3:
                            self.directions[i][ii] = 0
                        temp = self.check()
                        if temp:
                            self.return_info.append(temp)
                            self.dead = True
                        return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

    def update(self):
        for i in range(3):
            for ii in range(3):
                if self.areas[i][ii].collidepoint(mouse_pos[0], mouse_pos[1]):
                    self.hovered[i][ii] = True
                else:
                    self.hovered[i][ii] = False

class End0Gui(Gui):
    def __init__(self):
        Gui.__init__(self, "end0")

    def draw(self):
        screen.blit(texture_lib["title_bg"], (0, 0))
        screen.blit(texture_lib["title_0"], (190, 150))
        screen.blit(texture_lib["quote_0"], (190, 150))
        screen.blit(texture_lib["restart"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

class End1Gui(Gui):
    def __init__(self):
        Gui.__init__(self, "end1")
        self.title_cycle = Cycle(3, 4)

    def draw(self):
        screen.blit(texture_lib["title_bg"], (0, 0))
        screen.blit(texture_lib["title_1"], (190, 150), pygame.Rect(0, self.title_cycle.get()*50, 250, 50))
        screen.blit(texture_lib["quote_1"], (190, 150))
        screen.blit(texture_lib["restart"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

class End2Gui(Gui):
    def __init__(self):
        Gui.__init__(self, "end2")
        self.title_cycle = Cycle(3, 4)

    def draw(self):
        screen.blit(texture_lib["title_bg"], (0, 0))
        screen.blit(texture_lib["title_2"], (190, 150), pygame.Rect(0, self.title_cycle.get() * 50, 250, 50))
        screen.blit(texture_lib["quote_2"], (190, 150))
        screen.blit(texture_lib["restart"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True

class End3Gui(Gui):
    def __init__(self):
        Gui.__init__(self, "end3")
        self.title_cycle = Cycle(3, 4)

    def draw(self):
        screen.blit(texture_lib["title_bg"], (0, 0))
        screen.blit(texture_lib["title_3"], (190, 150), pygame.Rect(0, self.title_cycle.get() * 50, 250, 50))
        screen.blit(texture_lib["quote_3"], (190, 150))
        screen.blit(texture_lib["restart"], (0, 0))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                self.dead = True
