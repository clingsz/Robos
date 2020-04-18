import pygame, sys, os
from jeffsMath import *

pygame.init()

screen_width, screen_height = 600, 400
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

ins_radius = 50
ground_size = 600
vision_size = (100, 200)
player_size = 100
between_line = 5
default_center = overlay((screen_width/2, screen_height/2), (-player_size/2, -player_size/2))
mouse_pos = [0, 0]

font1 = pygame.font.Font(os.path.join("fonts", "AmaticSC-Regular.ttf"), 25)
font2 = pygame.font.Font(os.path.join("fonts", "Aller_Rg.ttf"), 25)
font3 = pygame.font.Font(os.path.join("fonts", "Aller_Rg.ttf"), 50)

pygame.display.set_caption("Be careful with your steps!")


progress_split = [400, 700, 1000, 1300, 1600, 1900, 2400]

def load(n):
    return pygame.image.load(os.path.join("texture",  n + ".png")).convert_alpha()

texture_names = ["player_walk", "player_stand", "wall_bottom", "wall_top", "ground", "walk_dust", "blink",
                 "player_sit", "voice", "chatter", "inspection", "text_scroll", "button1", "button2",
                 "button3", "appear", "password", "password_gui", "hovered", "hint", "hint_gui", "pipe",
                 "pipe_gui", "pipe1", "pipe2", "pipe3", "select", "title_0", "title_1", "title_2", "title_3",
                 "title_bg", "quote_0", "quote_1", "quote_2", "quote_3", "ground_h", "wall_top_h", "icon",
                 "wall_bottom_h", "meteorite", "meteorite_dying", "bolt", "pop", "title_screen", "restart"]

texture_lib = {}
for name in texture_names:
    texture_lib[name] = load(name)
pygame.display.set_icon(texture_lib["icon"])
def add_left(names):
    for name in names:
        texture_lib[name+"_left"] = pygame.transform.flip(texture_lib[name], True, False)

add_left(["player_walk", "player_stand", "walk_dust"])
texture_lib["pipe1_0"] = texture_lib["pipe1"]
texture_lib["pipe1_1"] = texture_lib["pipe3"]
texture_lib["pipe1_2"] = texture_lib["pipe1"]
texture_lib["pipe1_3"] = texture_lib["pipe3"]
texture_lib["pipe2_0"] = texture_lib["pipe2"]
texture_lib["pipe2_1"] = pygame.transform.flip(texture_lib["pipe2"], False, True)
texture_lib["pipe2_2"] = pygame.transform.flip(texture_lib["pipe2"], True, True)
texture_lib["pipe2_3"] = pygame.transform.flip(texture_lib["pipe2"], True, False)

class Cycle:
    def __init__(self, num, speed):
        self.tick = 0
        self.current = 0
        self.speed = speed
        self.num = num
        self.one = False
        self.prev = self.current

    def get(self):
        self.tick += 1
        self.prev = self.current
        if self.tick > self.speed:
            self.tick = 0
            self.current += 1
            if self.current >= self.num:
                self.current = 0
        if self.tick+1 > self.speed and self.current+1 >= self.num:
            self.one = True
        return  self.current

    def reset(self):
        self.tick = 0
        self.current = 0

class ReCycle:
    def __init__(self, num, speed, start=0):
        self.tick = 0
        self.current = start
        self.speed = speed
        self.num = num
        self.one = False
        self.v = 1
        self.prev = self.current

    def get(self):
        self.tick += 1
        if self.tick > self.speed:
            self.tick = 0
            self.prev = self.current
            self.current += self.v
            if self.current >= self.num:
                self.current = self.num - 1
                self.v = -1
                self.one = True
            elif self.current < 0:
                self.current = 0
                self.v = 1
        return  self.current

    def reset(self):
        self.tick = 0
        self.current = 0

class UniTextFormat():
    def __init__(self, text, time):
        self.text = text
        self.time = time

class GlobalTextScroll():
    def __init__(self):
        self.queue = []
        self.appear = 0
        self.countdown = 0
        self.disappear = 0
        self.text = None
        self.text_x = 0

    def add_to_queue(self, text):
        self.queue.append(text)

    def next_line(self):
        temp = self.queue.pop(0)
        self.appear = 5
        self.countdown = temp.time
        self.disappear = 5
        self.text_x = screen_width/2 - font2.size(temp.text)[0]/2
        self.text = font2.render(temp.text, False, (0, 0, 0))

    def end_line(self):
        self.text= None

    def draw(self):
        if self.text:
            if self.appear:
                self.appear -= 1
                screen.blit(texture_lib["text_scroll"], (0, screen_height - (5 - self.appear) * 10))
                screen.blit(self.text, (self.text_x, 5 + screen_height - (5 - self.appear) * 10))
            elif self.countdown:
                self.countdown -= 1
                screen.blit(texture_lib["text_scroll"], (0, screen_height - 50))
                screen.blit(self.text, (self.text_x, 5 + screen_height - 50))
            elif self.disappear:
                self.disappear -= 1
                screen.blit(texture_lib["text_scroll"], (0, screen_height - self.disappear * 10))
                screen.blit(self.text, (self.text_x, 5 + screen_height - self.disappear * 10))
            else:
                self.end_line()
        elif self.queue:
            self.next_line()

text_scroll = GlobalTextScroll()

chats = [[] for _ in range(20)]

chat_text0 = [UniTextFormat("Hello!", 40),
               UniTextFormat("Welcome to the empty room!", 80),
               UniTextFormat("There's nothing!", 60),
               UniTextFormat("Nothing to do here", 70),
               UniTextFormat("...", 30),
               UniTextFormat("Do you want something?", 60),
               UniTextFormat("You sure?", 40),
               UniTextFormat("Alright", 30),
               UniTextFormat("I just added something!", 80)]

chat_text1 = [UniTextFormat("Have you find it yet?", 70),
              UniTextFormat("It's in the room!", 60),
              UniTextFormat("Friendly reminder: there's more than one", 100),
              UniTextFormat("Something well hidden...", 60),
              UniTextFormat("Something on the ground", 60),
              UniTextFormat("Something that points to another", 80),
              UniTextFormat("Something in the corners", 60)]

chat_text2 = [UniTextFormat("Hint: the password consists of numbers!", 120),
              UniTextFormat("More hints: three numbers!", 70),
              UniTextFormat("Did you see what's on the left?", 80),
              UniTextFormat("The locations are key!", 60),
              UniTextFormat("You can do this!", 50),
              UniTextFormat("A link to the past", 60),
              UniTextFormat("Remember how you find the pads?", 80),
              UniTextFormat("Re-walk the path!", 60),
              UniTextFormat("NEVER ENTER 666", 90)]

chat_text3 = [UniTextFormat("Make haste!", 50),
              UniTextFormat("Did you see that? There are two paths!", 120),
              UniTextFormat("Make your choice!", 60),
              UniTextFormat("You can only choose one", 80),
              UniTextFormat("You can never see the other one!", 90),
              UniTextFormat("...unless you restart the game", 80),
              UniTextFormat("But why would you come to such a boring room again?", 160)]

chat_text10 = [UniTextFormat("Wow you did nothing!", 70),
              UniTextFormat("Amazing!", 40),
              UniTextFormat("I wish there are more players like you!", 120),
              UniTextFormat("But, what could you do anyways?", 90),
              UniTextFormat("Maybe destroy the universe?", 80),
              UniTextFormat("Maybe turn this world into hell?", 90),
              UniTextFormat("Maybe time travel to the past?", 90),
              UniTextFormat("Just kidding!", 90),
              UniTextFormat("Congratulations on finishing the game!", 90),
               UniTextFormat(" ", 1)]
chat_text11 = [UniTextFormat("Did you do it?", 70),
              UniTextFormat("Do you regret it?", 80),
              UniTextFormat("There's no stopping!", 80),
              UniTextFormat("No action was the correct option all along", 130),
              UniTextFormat("It never ends better than doing nothing!", 120),
              UniTextFormat("..Just wait for the ending", 90),
              UniTextFormat("And restart the game, maybe?", 90)]
chat_text12 = [UniTextFormat("You never know", 70),
              UniTextFormat("Such a small action can cause this?", 80),
              UniTextFormat("I mean, you know nothing about the pipes", 130),
              UniTextFormat("But imagine how wild the butterfly effect can go!", 130),
              UniTextFormat("It never ends better than doing nothing!", 120),
              UniTextFormat("..Just wait for the ending", 90),
              UniTextFormat("And restart the game, maybe?", 90)]
chat_text13 = [UniTextFormat("You never know", 70),
              UniTextFormat("Such a small action can cause this?", 80),
              UniTextFormat("I mean, you know nothing about the pipes", 130),
            UniTextFormat("But imagine how wild the butterfly effect can go!", 130),
               UniTextFormat("I feel.. strange", 70),
              UniTextFormat("Just kidding!", 40),
              UniTextFormat("I'm not affected by the rewind, at all!", 120),
              UniTextFormat("Why, you ask?", 50),
              UniTextFormat("Well, you see, I'm above the game!", 80),
              UniTextFormat("How to beat me, you ask?", 50),
              UniTextFormat("Maybe try dividing by 0, next time", 90),
              UniTextFormat("I believe that will free me!", 80),
              UniTextFormat("..Just wait for the ending", 90),
              UniTextFormat("And restart the game, maybe?", 90)]

chats[0] = chat_text0
chats[1] = chat_text1
chats[2] = chat_text2
chats[3] = chat_text3
chats[10] = chat_text10
chats[11] = chat_text11
chats[12] = chat_text12
chats[13] = chat_text13

end_overlays = [[pygame.Surface((screen_width, screen_height)) for _ in range(4)] for _ in range(3)]
for i in range(4):
    end_overlays[0][i].set_alpha(20*(i+1))
    end_overlays[1][i].set_alpha(20*(i+1))
    end_overlays[2][i].set_alpha(20*(i+1))
    end_overlays[0][i].fill((255, 27, 15))
    end_overlays[1][i].fill((216, 0, 216))
    end_overlays[2][i].fill((56, 211, 216))

class AudioPlayer():
    def __init__(self,id,type,volume=0.2):
        self.id = id
        self.music = pygame.mixer.Sound(os.path.join('audio', id+'.ogg'))
        self.music.set_volume(volume)
        if type == "bg":
            self.channel = pygame.mixer.Channel(1)
        if type == "se":
            self.channel = pygame.mixer.Channel(2)
        if type == "cb":
            self.channel = pygame.mixer.Channel(3)
        if type == "ft":
            self.channel = pygame.mixer.Channel(4)

    def playNonStop(self):
        self.channel.play(self.music,-1)
        if self.id.startswith("ending"):
            text_scroll.add_to_queue(UniTextFormat("The butterfly effect begins", 70))

    def playOnce(self):
        self.channel.play(self.music, 0)

    def stop(self):
        self.channel.stop()

bgs = (AudioPlayer("mainmenubg", "bg"), AudioPlayer("defaultroom", "bg"),
       AudioPlayer("ending1", "bg", volume=0.1),
       AudioPlayer("ending2", "bg", volume=0.1),
       AudioPlayer("ending3", "bg", volume=0.1),)
chatbox_audio = AudioPlayer("chatbox", "cb", volume=0.15)
door_audio = AudioPlayer("dooropen", "se")
inspect_audio = AudioPlayer("inspect", "se")
step_audio = AudioPlayer("step", "ft")
pad_audio = AudioPlayer("pad", "se")
password_audio = AudioPlayer("password", "se", volume=0.2)