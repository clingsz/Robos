from config import *
from gui import *

class Map:
    def __init__(self, player):
        self.items = []
        self.player = player
        self.animations = []
        self.stat = 0
        self.gui = None
        self.end_progress = 0

    def add_item(self, item):
        self.items.append(item)

    def add_animation(self, animation):
        self.animations.append(animation)

    def update(self):
        if self.stat > 10:
            self.end_progress += 1
            if self.stat == 11 and self.end_progress > progress_split[4]:
                if random.randint(0, 4) == 1:
                    self.add_animation(Meteorite(self.player))
            if self.stat == 12 and self.end_progress > progress_split[4]:
                if random.randint(0, 4) == 1:
                    self.add_animation(Bolt(self.player))
            if self.stat == 13 and self.end_progress > progress_split[4]:
                if random.randint(0, 60) == 1:
                    if len(self.items) != 1:
                        for i in range(len(self.items)-1, -1, -1):
                            if not isinstance(self.items[i], Chatter):
                                self.items[i].dead = True
                                self.add_animation(Disappear(self.player,
                                                             [self.items[i].pos[0]-75, self.items[i].pos[1]-75]))
                                break

            if self.end_progress == progress_split[0]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("The password attracted unwanted attention", 80))
                if self.stat == 12:
                    text_scroll.add_to_queue(UniTextFormat("It added ions to a water source", 80))
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("It reversed the flow of a fluid supply", 80))
            if self.end_progress == progress_split[1]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("The staring intensifies...", 80))
                if self.stat == 12:
                    text_scroll.add_to_queue(UniTextFormat("An alien civilization is using this water source", 80))
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("The fluid is used by a time machine", 80))
            elif self.end_progress == progress_split[2]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("The doom gets closer", 80))
                if self.stat == 12:
                    text_scroll.add_to_queue(UniTextFormat("Half of its population died", 80))
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("It caused machine disfunction", 80))
            elif self.end_progress == progress_split[3]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("Hell is arriving", 80))
                if self.stat == 12:
                    text_scroll.add_to_queue(UniTextFormat("They found out that this is caused by human beings", 80))
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("The machine is starting to affect the world", 80))
            elif self.end_progress == progress_split[4]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("Hell fires are falling from the sky", 80))
                if self.stat == 12:
                    text_scroll.add_to_queue(UniTextFormat("Earth was attacked, leaving the planet half wrecked", 80))
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("disappearing are items The", 80))
            elif self.end_progress == progress_split[5]:
                if self.stat == 11:
                    text_scroll.add_to_queue(UniTextFormat("The end has come", 80))
                if self.stat == 12:
                    self.gui = End2Gui()
                if self.stat == 13:
                    text_scroll.add_to_queue(UniTextFormat("?up ending this is Where", 80))
            elif self.end_progress == progress_split[6]:
                if self.stat == 11:
                    self.gui = End1Gui()
                if self.stat == 13:
                    self.gui = End3Gui()

        for item in self.items:
            item.update()
            self.set_inspection(item)

    def draw_stat_effect(self):
        if self.stat == 11:
            if self.end_progress > progress_split[3]:
                screen.blit(end_overlays[0][3], (0, 0))
            elif self.end_progress > progress_split[2]:
                screen.blit(end_overlays[0][2], (0, 0))
            elif self.end_progress > progress_split[1]:
                screen.blit(end_overlays[0][1], (0, 0))
            elif self.end_progress > progress_split[0]:
                screen.blit(end_overlays[0][0], (0, 0))
        if self.stat == 12:
            if self.end_progress > progress_split[3]:
                screen.blit(end_overlays[1][3], (0, 0))
            elif self.end_progress > progress_split[2]:
                screen.blit(end_overlays[1][2], (0, 0))
            elif self.end_progress > progress_split[1]:
                screen.blit(end_overlays[1][1], (0, 0))
            elif self.end_progress > progress_split[0]:
                screen.blit(end_overlays[1][0], (0, 0))
        if self.stat == 13:
            if self.end_progress > progress_split[3]:
                screen.blit(end_overlays[2][3], (0, 0))
            elif self.end_progress > progress_split[2]:
                screen.blit(end_overlays[2][2], (0, 0))
            elif self.end_progress > progress_split[1]:
                screen.blit(end_overlays[2][1], (0, 0))
            elif self.end_progress > progress_split[0]:
                screen.blit(end_overlays[2][0], (0, 0))

    def draw_gui(self):
        self.gui.draw()

    def update_gui(self):
        self.gui.update()
        if self.gui.dead:
            self.gui = None

    def handle_gui(self, event):
        self.gui.handle_event(event)

    def draw_back(self):
        if self.stat == 11 and self.end_progress > progress_split[5]:
            screen.blit(texture_lib["wall_top_h"], self.get_offset_pos((-ground_size / 2, -ground_size / 2 - 100)))
        else:
            screen.blit(texture_lib["wall_top"], self.get_offset_pos((-ground_size / 2, -ground_size / 2 - 100)))
        pygame.draw.rect(screen, (100, 100, 100),
                         pygame.Rect(self.get_offset_pos((-ground_size / 2, -ground_size / 2 - 80)),
                                     (20, ground_size + 100)))
        pygame.draw.rect(screen, (100, 100, 100),
                         pygame.Rect(self.get_offset_pos((ground_size/2 - 20, -ground_size / 2 - 80)),
                                     (20, ground_size + 100)))

        for i in range(len(self.animations)-1, -1, -1):
            if self.animations[i].pos[1] + self.animations[i].size< self.player.pos[1] + player_size:
                self.animations[i].draw()
                if self.animations[i].dead:
                    del self.animations[i]
        for i in range(len(self.items)-1, -1, -1):
            if self.items[i].on_ground or \
                    self.items[i].pos[1] + self.items[i].size < self.player.pos[1] + player_size:
                self.items[i].draw()
                if self.items[i].dead:
                    del self.items[i]

    def draw_front(self):
        for i in range(len(self.animations)-1, -1, -1):
            if self.animations[i].pos[1] + self.animations[i].size >= self.player.pos[1] + player_size:
                self.animations[i].draw()
                if self.animations[i].dead:
                    del self.animations[i]
        for i in range(len(self.items)-1, -1, -1):
            if not self.items[i].on_ground and \
                    self.items[i].pos[1] + self.items[i].size >= self.player.pos[1] + player_size:
                self.items[i].draw()
                if self.items[i].dead:
                    del self.items[i]
        if self.stat == 11 and self.end_progress > progress_split[5]:
            screen.blit(texture_lib["wall_bottom_h"], self.get_offset_pos((-ground_size / 2, ground_size / 2 - 100)))
        else:
            screen.blit(texture_lib["wall_bottom"], self.get_offset_pos((-ground_size / 2, ground_size / 2 - 100)))
        self.draw_stat_effect()

    def draw_shadow(self):
        for item in self.items:
            item.draw_shadow()

    def draw_ground(self):
        if self.stat == 11 and self.end_progress > progress_split[5]:
            screen.blit(texture_lib["ground_h"], self.get_offset_pos((-ground_size / 2, -ground_size / 2)))
        else:
            screen.blit(texture_lib["ground"], self.get_offset_pos((-ground_size/2, -ground_size/2)))

    def get_offset_pos(self, pos):
        return overlay(pos,
                       (-(self.player.pos[0]-self.player.draw_pos[0]) + player_size/2,
                         -(self.player.pos[1]-self.player.draw_pos[1]) + player_size/2))

    def set_inspection(self, item):
        pos1 = (item.pos[0] + item.size/2, item.pos[1]+item.size/2)
        pos2 = (self.player.pos[0]+player_size/2, self.player.pos[1]+player_size)
        if abs(pos1[0] - pos2[0]) < ins_radius \
                and abs(pos1[1] - pos2[1]) < ins_radius:
            item.close = True

        else:
            item.close = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_k:
                for item in self.items:
                    if item.close:
                        if not item.activated:
                            inspect_audio.playOnce()
                            item.activate()

class Item:
    def __init__(self, player):
        self.size = 0
        self.player = player
        self.pos = [0, 0]
        self.dead = False
        self.close = False
        self.inspect_cycle = ReCycle(5, 2)
        self.on_ground = False
        self.activated = False

    def activate(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def draw_shadow(self):
        pass

    def draw_close(self):
        if self.close:
            screen.blit(texture_lib["inspection"],
                        self.get_offset_pos((self.pos[0] + self.size/2 - 72,
                                             self.pos[1] - 20 + self.inspect_cycle.get())))

    def get_offset_pos(self, pos):
        return overlay(pos,
                       (-(self.player.pos[0]-self.player.draw_pos[0]),
                         -(self.player.pos[1]-self.player.draw_pos[1])))

class Animation:
    def __init__(self, player):
        self.pos = [0, 0]
        self.dead = False
        self.player = player
        self.size = 0

    def draw(self):
        pass

    def get_offset_pos(self, pos):
        return overlay(pos,
                       (-(self.player.pos[0]-self.player.draw_pos[0]) + player_size/2,
                         -(self.player.pos[1]-self.player.draw_pos[1]) + player_size/2))

class WalkDust(Animation):
    def __init__(self, player, left):
        Animation.__init__(self, player)
        self.size = 50
        self.cycle = Cycle(7, 1)
        if left:
            self.texture = texture_lib["walk_dust_left"]
            self.pos = (player.pos[0] - 40, player.pos[1] + 15)
        else:
            self.texture = texture_lib["walk_dust"]
            self.pos = (player.pos[0], player.pos[1] + 15)

    def draw(self):
        screen.blit(self.texture, self.get_offset_pos(self.pos),
                    (0, self.cycle.get() * self.size, self.size, self.size))
        self.dead = self.cycle.one

class Bolt(Animation):
    def __init__(self, player):
        Animation.__init__(self, player)
        self.size = 50
        self.cycle = Cycle(4, 3)
        self.texture = texture_lib["bolt"]
        self.pos = (random.randint(-275, 225), random.randint(-275, 225))
        self.draw_pos = (self.pos[0], self.pos[1] - 200)

    def draw(self):
        screen.blit(self.texture, self.get_offset_pos(self.pos),
                    (0, self.cycle.get() * 200, 100, 200))
        self.dead = self.cycle.one

class Disappear(Animation):
    def __init__(self, player, pos):
        Animation.__init__(self, player)
        self.size = 100
        self.cycle = Cycle(4, 3)
        self.texture = texture_lib["pop"]
        self.pos = pos

    def draw(self):
        screen.blit(self.texture, self.get_offset_pos(self.pos),
                    (0, self.cycle.get() * 100, 100, 100))
        self.dead = self.cycle.one


class Meteorite(Animation):
    def __init__(self, player):
        Animation.__init__(self, player)
        self.size = 100
        self.cycle = Cycle(4, 2)
        self.dying = Cycle(3, 3)
        self.speed = [-2, 8]
        self.life = 50
        self.tick = 0
        self.texture1 = texture_lib["meteorite"]
        self.texture2 = texture_lib["meteorite_dying"]
        self.draw_pos = [random.randint(-275, 225) - self.life * self.speed[0],
                    random.randint(-275, 225) - self.life * self.speed[1]]
        self.pos = [random.randint(-275, 225), random.randint(-275, 225)]

    def draw(self):
        if self.tick < self.life:
            self.tick += 1
            self.draw_pos[0] += self.speed[0]
            self.draw_pos[1] += self.speed[1]
            screen.blit(self.texture1, self.get_offset_pos(self.draw_pos),
                        (0, self.cycle.get() * self.size, self.size, self.size))
        elif not self.dying.one:
            screen.blit(self.texture2, self.get_offset_pos(self.draw_pos),
                        (0, self.dying.get() * self.size, self.size, self.size))
        else:
            self.dead = True


class SoundAni(Animation):
    width = 100
    def __init__(self, player, pos):
        Animation.__init__(self, player)
        self.pos = [pos[0] - 50, pos[1] - 40]
        self.size = 50
        self.cycle = Cycle(3, 2)
        self.texture = texture_lib["voice"]

    def draw(self):
        screen.blit(self.texture, self.get_offset_pos(self.pos),
                    (0, self.cycle.get() * self.size, self.width, self.size))
        self.dead = self.cycle.one


class Chatter(Item):
    def __init__(self, player, pos, map):
        Item.__init__(self, player)
        self.map = map
        self.size = 100
        self.pos = pos
        self.speak_cycle = Cycle(5, 3)
        self.sound_gen_cycle = Cycle(2, 8)
        self.text_x = 0
        self.current_text = None
        self.countdown = 0
        self.next_countdown = between_line
        self.current_chats = [0 for _ in range(20)]

    def activate(self):
        if not self.current_text:
            self.next_line(chats[self.map.stat][self.current_chats[self.map.stat]])
            self.current_chats[self.map.stat] += 1
            chatbox_audio.playNonStop()
            if self.current_chats[self.map.stat] >= len(chats[self.map.stat]):
                if self.map.stat == 0:
                    self.map.stat = 1
                    self.map.add_item(Button(self.player, (-125, 195), 1, self.map))
                if self.map.stat == 10:
                    self.map.gui = End0Gui()
                self.current_chats[self.map.stat] = 0


    def next_line(self, textformat):
        self.text_x = self.pos[0] - (font1.size(textformat.text)[0] - 100)/2
        self.current_text = font1.render(textformat.text, False, (0, 0, 0))
        self.countdown = textformat.time
        self.next_countdown = between_line

    def draw(self):
        if self.next_countdown:
            self.next_countdown -= 1
            screen.blit(texture_lib["chatter"], self.get_offset_pos(self.pos),
                        (0, 0, self.size, self.size))
        elif self.current_text:
            screen.blit(texture_lib["chatter"], self.get_offset_pos(self.pos),
                        (0, self.speak_cycle.get() * self.size, self.size, self.size))
            tw, th = self.current_text.get_size()
            pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(self.get_offset_pos((self.text_x - 7, self.pos[1] - 7)), (tw + 14, th + 14)))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(self.get_offset_pos((self.text_x - 5, self.pos[1] - 5)), (tw + 10, th + 10)))
            screen.blit(self.current_text, self.get_offset_pos((self.text_x, self.pos[1])))
            if self.sound_gen_cycle.get() == 1:
                self.player.map.add_animation(SoundAni(self.player, self.pos))
            self.countdown -= 1
            if self.countdown == 0:
                self.current_text = None
                chatbox_audio.stop()
        else:
            screen.blit(texture_lib["chatter"], self.get_offset_pos(self.pos),
                        (0, 0, self.size, self.size))
        if not self.current_text:
            Item.draw_close(self)

    def draw_shadow(self):
        pygame.draw.ellipse(screen, (187, 187, 187),
                            pygame.Rect(overlay(self.get_offset_pos(self.pos), (15, 85)), (70, 20)))

class Button(Item):
    def __init__(self, player, pos, num, map):
        Item.__init__(self, player)
        self.map = map
        self.num = num
        self.size = 50
        self.pos = pos
        self.activated = False
        self.active_cycle = Cycle(4, 8)
        self.on_ground = True
        self.spawned = False
        if self.num == 1:
            text_scroll.add_to_queue(UniTextFormat("Something in the room has changed", 100))
            self.map.stat = 1

    def activate(self):
        if not self.activated:
            pad_audio.playOnce()
            self.activated = True
            if self.num == 1:
                self.map.add_item(Button(self.player, (175, -105), 2, self.map))
            elif self.num == 2:
                self.map.add_item(Button(self.player, (175, 195), 3, self.map))

    def draw(self):
        if not self.active_cycle.one:
            if self.activated:
                screen.blit(texture_lib["button" + str(self.num)], self.get_offset_pos(self.pos),
                            (0, self.active_cycle.get()*self.size, self.size, self.size))
        else:
            screen.blit(texture_lib["button" + str(self.num)], self.get_offset_pos(self.pos),
                        (0, 3 * self.size, self.size, self.size))
        if not self.activated:
            Item.draw_close(self)

    def update(self):
        if not self.spawned and self.num == 3 and self.active_cycle.one:
            self.spawned = True
            self.map.add_item(PasswordEnter(self.player, [170, 0], self.map))
            self.map.add_item(Hint(self.player, [-170, 0], self.map))
            self.map.stat = 2
            text_scroll.add_to_queue(UniTextFormat("A little puzzle appears", 70))

class PasswordEnter(Item):
    def __init__(self, player, pos, map):
        Item.__init__(self, player)
        self.map = map
        self.pos = pos
        self.size = 60
        self.on_ground = True
        self.start_cycle = Cycle(4, 8)
        self.rise_cycle = Cycle(10, 4)
        self.activated = False
        self.gui = None
        door_audio.playOnce()

    def activate(self):
        if not self.activated:
            self.gui = PasswordGui()
            self.map.gui = self.gui

    def update(self):
        if self.gui:
            if self.gui.dead and len(self.gui.return_info) == 3:
                if self.gui.return_info[0] == 9 and self.gui.return_info[1] == 7 and self.gui.return_info[2] ==2:
                    self.map.add_item(Pipe(self.player, (20, 100), self.map))
                    self.map.stat = 3
                    text_scroll.add_to_queue(UniTextFormat("Your final choice appears", 70))
                    self.activated = True
                elif self.gui.return_info[0] == 6 and self.gui.return_info[1] == 6 and self.gui.return_info[2] ==6:
                    self.map.stat = 11
                    text_scroll.add_to_queue(UniTextFormat("Something unwanted has awakened", 70))
                    bgs[2].playNonStop()
                    self.activated = True
                self.gui = None

    def draw(self):
        if not self.start_cycle.one:
            pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(self.get_offset_pos(self.pos), (self.size, self.size)))
            pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(self.get_offset_pos(self.pos), (self.size, 10)))
            screen.blit(texture_lib["appear"], self.get_offset_pos(self.pos),
                        (0, self.start_cycle.get() * self.size, self.size, self.size))
        elif not self.rise_cycle.one:
            pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(self.get_offset_pos(self.pos), (self.size, self.size)))
            pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(self.get_offset_pos(self.pos), (self.size, 10)))
            tempoffset = self.rise_cycle.get()
            screen.blit(texture_lib["password"], self.get_offset_pos(self.pos),
                        (0, self.size - tempoffset*6, self.size, tempoffset*6))
        else:
            screen.blit(texture_lib["password"], self.get_offset_pos(self.pos))

        if not self.activated:
            Item.draw_close(self)

class Hint(Item):
    def __init__(self, player, pos, map):
        Item.__init__(self, player)
        self.map = map
        self.pos = pos
        self.size = 60
        self.on_ground = True
        self.start_cycle = Cycle(4, 8)
        self.rise_cycle = Cycle(10, 4)
        self.activated = False
        door_audio.playOnce()

    def activate(self):
        self.map.gui = HintGui()

    def draw(self):
        if not self.start_cycle.one:
            pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(self.get_offset_pos(self.pos), (self.size, self.size)))
            pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(self.get_offset_pos(self.pos), (self.size, 10)))
            screen.blit(texture_lib["appear"], self.get_offset_pos(self.pos),
                        (0, self.start_cycle.get() * self.size, self.size, self.size))
        elif not self.rise_cycle.one:
            pygame.draw.rect(screen, (90, 90, 90), pygame.Rect(self.get_offset_pos(self.pos), (self.size, self.size)))
            pygame.draw.rect(screen, (130, 130, 130), pygame.Rect(self.get_offset_pos(self.pos), (self.size, 10)))
            tempoffset = self.rise_cycle.get()
            screen.blit(texture_lib["hint"], self.get_offset_pos(self.pos),
                        (0, self.size - tempoffset*6, self.size, tempoffset*6))
        else:
            screen.blit(texture_lib["hint"], self.get_offset_pos(self.pos))

        if not self.activated:
            Item.draw_close(self)

class Pipe(Item):
    def __init__(self, player, pos, map):
        Item.__init__(self, player)
        self.map = map
        self.pos = pos
        self.size = 60
        self.on_ground = True
        self.start_cycle = Cycle(4, 8)
        self.activated = False
        self.gui = None
        door_audio.playOnce()

    def activate(self):
        if not self.activated:
            self.gui = PipeGui()
            self.map.gui = self.gui

    def update(self):
        if self.gui:
            if self.gui.dead and len(self.gui.return_info) == 1:
                if self.gui.return_info[0] == 1:
                    self.map.stat = 12
                    bgs[3].playNonStop()
                    text_scroll.add_to_queue(UniTextFormat("Something is connected!", 70))
                elif self.gui.return_info[0] == 2:
                    self.map.stat = 13
                    bgs[4].playNonStop()
                    text_scroll.add_to_queue(UniTextFormat("Something is connected!", 70))
                self.activated = True
                self.gui = None

    def draw(self):
        if not self.start_cycle.one:
            screen.blit(texture_lib["pipe"], self.get_offset_pos(self.pos))
            screen.blit(texture_lib["appear"], self.get_offset_pos(self.pos),
                        (0, self.start_cycle.get() * self.size, self.size, self.size))
        else:
            screen.blit(texture_lib["pipe"], self.get_offset_pos(self.pos))

        if not self.activated:
            Item.draw_close(self)

