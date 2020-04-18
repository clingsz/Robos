from map import *

class Player:
    def __init__(self):
        self.map = None
        self.pos = [0, 0]
        self.draw_pos = default_center
        self.speed = 7
        self.speed_di = self.speed * 0.7
        self.dir = [0, 0]
        self.texture = [texture_lib["player_stand"], texture_lib["player_stand_left"],
                        texture_lib["player_walk"], texture_lib["player_walk_left"]]
        self.status = 0

        self.walk_cycle = Cycle(8, 3)
        self.stand_cycle = Cycle(2, 15)

    def change_map(self, map):
        self.map = map

    def change_speed(self, new_speed):
        self.speed = new_speed
        self.speed_di = self.speed * 0.7

    def update(self):
        if self.map.stat == 13 and self.map.end_progress > progress_split[4]:
            self.texture[0], self.texture[1] = texture_lib["player_stand_left"], texture_lib["player_stand"]
            self.texture[2], self.texture[3] = texture_lib["player_walk_left"], texture_lib["player_walk"]
        self.update_dateinfo()
        self.update_renderinfo()

    def update_dateinfo(self):
        k = pygame.key.get_pressed()
        if not (k[pygame.K_w] or k[pygame.K_a] or k[pygame.K_s] or k[pygame.K_d]):
            self.dir[0] = 0
            self.dir[1] = 0
        if self.dir[0] != 0 or self.dir[1] != 0:
            if self.dir[0] == 0 or self.dir[1] == 0:
                self.pos[0] += self.dir[0] * self.speed
                self.pos[1] += self.dir[1] * self.speed
            else:
                self.pos[0] += self.dir[0] * self.speed_di
                self.pos[1] += self.dir[1] * self.speed_di
        if self.pos[0] > (ground_size - player_size) / 2:
            self.pos[0] = (ground_size - player_size)/2
        elif self.pos[0] < -(ground_size - player_size) / 2:
            self.pos[0] = -(ground_size - player_size)/2
        if self.pos[1] > (ground_size - player_size) / 2:
            self.pos[1] = (ground_size - player_size)/2
        elif self.pos[1] < -(ground_size - player_size/4) / 2:
            self.pos[1] = -(ground_size - player_size/4)/2

    def update_renderinfo(self):
        if self.dir[0] == -1:
            self.status = 3
        elif self.dir[0] == 1:
            self.status = 2
        elif self.dir[1] == 0:
            if self.status == 2:
                self.status = 0
            elif self.status == 3:
                self.status = 1
        elif self.dir[1] != 0:
            if self.status == 0:
                self.status = 2
            elif self.status == 1:
                self.status = 3

        self.draw_pos = default_center
        if self.pos[0] > vision_size[0]:
            self.draw_pos = overlay(self.draw_pos, (self.pos[0]-vision_size[0], 0))
        elif self.pos[0] < -vision_size[0]:
            self.draw_pos = overlay(self.draw_pos, (self.pos[0] + vision_size[0], 0))
        if self.pos[1] > vision_size[1]:
            self.draw_pos = overlay(self.draw_pos, (0, self.pos[1] - vision_size[1]))
        elif self.pos[1] < -vision_size[1]:
            self.draw_pos = overlay(self.draw_pos, (0, self.pos[1] + vision_size[1]))

    def draw(self):
        if self.status == 2 or self.status == 3:
            temp = self.walk_cycle.get()
            prev_temp = self.walk_cycle.prev
            screen.blit(self.texture[self.status], self.draw_pos,
                        pygame.Rect(0, temp * player_size, player_size, player_size))
            if temp != prev_temp and (temp == 3 or temp == 7):
                self.map.add_animation(WalkDust(self, self.status==2))
            if temp != prev_temp and (temp == 1 or temp == 5):
                step_audio.playOnce()
        elif self.status == 0 or self.status == 1:
            screen.blit(self.texture[self.status], self.draw_pos,
                        pygame.Rect(0, self.stand_cycle.get() * player_size, player_size, player_size))

    def draw_shadow(self):
        pygame.draw.ellipse(screen, (187, 187, 187), pygame.Rect(overlay(self.draw_pos, (25, 95)), (50, 20)))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.dir[1] -= 1
            elif event.key == pygame.K_s:
                self.dir[1] += 1
            elif event.key == pygame.K_a:
                self.dir[0] -= 1
            elif event.key == pygame.K_d:
                self.dir[0] += 1

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                self.dir[1] += 1
            elif event.key == pygame.K_s:
                self.dir[1] -= 1
            elif event.key == pygame.K_a:
                self.dir[0] += 1
            elif event.key == pygame.K_d:
                self.dir[0] -= 1

class Game:
    def __init__(self):
        self.player = Player()
        map1 = Map(self.player)
        self.chatter = Chatter(self.player, (0, -120), map1)
        self.time = 0

        #creating map1
        self.sit_cycle = Cycle(7, 7)
        self.blink = BlinkOverlay()
        map1.add_item(self.chatter)
        self.maps = (map1, )

        self.player.change_map(map1)

    def update(self):
        if self.maps[0].stat == 0:
            self.time += 1
            if self.time > 4000:
                self.maps[0].stat = 10
                text_scroll.add_to_queue(UniTextFormat("The game is bored of you doing nothing", 90))
                text_scroll.add_to_queue(UniTextFormat("Go talk to the chatbox to end your run", 70))
        if self.maps[0].gui:
            self.maps[0].update_gui()
        else:
            self.maps[0].update()
            if self.blink.dead:
                self.player.update()

    def draw(self):
        self.maps[0].draw_ground()
        self.maps[0].draw_shadow()
        self.player.draw_shadow()
        self.maps[0].draw_back()

        if self.blink.dead:
            self.player.draw()
        else:
            if self.blink.stat == 0:
                screen.blit(texture_lib["player_sit"], default_center,
                    pygame.Rect(0, 0,
                                player_size, player_size))
            elif self.blink.stat == 1:
                screen.blit(texture_lib["player_sit"], default_center,
                    pygame.Rect(0, self.sit_cycle.get() * player_size,
                                player_size, player_size))

        self.maps[0].draw_front()
        if self.maps[0].gui:
            self.maps[0].draw_gui()
        if not self.blink.dead:
            self.blink.draw()

        if self.maps[0].end_progress > progress_split[-1]:
            screen.blit(texture_lib["restart"], (0, 0))

    def handle_event(self, event):
        if self.maps[0].gui:
            self.maps[0].handle_gui(event)
        else:
            self.player.handle_event(event)
            self.maps[0].handle_event(event)


class BlinkOverlay:
    open_sequence = (0, 0, 1, 0, 0, 0, 1, 2, 1, 0, 0, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 5)
    def __init__(self):
        self.tick = 0
        self.cycle = Cycle(22, 4)
        self.dead = False
        self.stat = 0

    def draw(self):
        if self.tick > 331:
            self.dead = True
            return
        elif self.tick > 282:
            self.stat = 1
            if self.tick == 290:
                text_scroll.add_to_queue(UniTextFormat("You are awake", 70))
        elif self.tick > 90:
            s = pygame.Surface((600, 400))
            s.fill((255, 255, 255))
            s.set_alpha(255 - self.tick*1.5 + 135)
            screen.blit(s, (0, 0))
        elif self.tick == 90:
            bgs[1].playNonStop()
            screen.fill(-1)
        else:
            screen.fill(-1)

        if not self.cycle.one:
            screen.blit(texture_lib["blink"], (0, 0),
                    pygame.Rect(0, self.open_sequence[self.cycle.get()] * screen_height,
                                screen_width, screen_height))
        self.tick += 1
