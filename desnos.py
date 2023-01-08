import math
import pygame
import random
import StringSolver as ss
import text_input_test as tf

class funcPanel:
    def __init__(self, x, y, width, height, g_scale, g_mode, func):
        self.rect = pygame.Rect(x,y,width,height)
        self.func = func
        self.mode = g_mode
        if self.mode == "random":
            self.color_a = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.color_b = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        elif self.mode == "light":
            self.color_a = (255,255,255)
            self.color_b = (30, 30, 30)
        else:
            self.color_a = (30, 30, 30)
            self.color_b = (255,255,255)
        self.card_width = width
        self.card_height = 150
        self.func_cards = []
        self.scale = g_scale
        self.addfunc_card = {"rect": pygame.Rect(x, self.rect.y+len(self.func_cards)*self.card_height, width, 100)}
        self.addfunc_card["button"] = tf.button((self.addfunc_card["rect"].x+75,self.rect.y+len(self.func_cards)*self.card_height+25,50,50),"clear",self.addCard,None,"icons8-plus.png")
        self.back_button = tf.button([10,758,32,32], "clear", self.func,None,"back.png")

    def addCard(self):
        self.func_cards.append(funcCard(self.rect.x,self.rect.y+len(self.func_cards)*self.card_height,self.card_width,
                                        self.card_height,"red", self.scale, self.mode))
        self.addfunc_card["rect"].y += self.card_height
        self.addfunc_card["button"].rect.y += self.card_height
        self.rect.h = max(800, len(self.func_cards)*self.card_height+self.addfunc_card["rect"].h)

    def drawCards(self, scr):
        for card in self.func_cards:
            card.draw(scr)
        if self.mode == "rainbow":
            pygame.draw.rect(scr, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), self.addfunc_card["rect"])
            pygame.draw.rect(scr, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), self.addfunc_card["rect"], 4)
        else:
            pygame.draw.rect(scr, self.color_a, self.addfunc_card["rect"])
            pygame.draw.rect(scr, self.color_b, self.addfunc_card["rect"], 4)
        self.addfunc_card["button"].draw(scr)
        self.back_button.draw(scr)

    def getInfo(self,event):
        if event.type == pygame.MOUSEWHEEL:
            self.rect.y += event.y * 30

        if self.rect.y >= 0:
            self.rect.y = 0
        elif self.rect.y+self.rect.h <= 800:
            self.rect.y = 800 - self.rect.h
        self.resetTXpos()

        for card in self.func_cards:
            card.getFunc(event)
        self.addfunc_card["button"].click(event)
        self.deleteCard(event)
        self.back_button.click(event)

    def resetTXpos(self):
        for i in range(len(self.func_cards)):
            self.func_cards[i].rect.y = self.rect.y+i*self.card_height
            self.func_cards[i].resetPos()
        self.addfunc_card["rect"].y = self.rect.y+len(self.func_cards)*self.card_height
        self.addfunc_card["button"].rect.y = self.addfunc_card["rect"].y + 25

    def deleteCard(self,event):
        for c in range(len(self.func_cards)):
            try:
                if self.func_cards[c].delete(event):
                    del self.func_cards[c]
                    for i in range(c,len(self.func_cards)):
                        self.func_cards[i].rect.y -= self.card_height
                        self.func_cards[i].resetPos()
                    self.addfunc_card["rect"].y -= self.card_height
                    self.addfunc_card["button"].rect.y -= self.card_height
                self.rect.h = max(800, len(self.func_cards) * self.card_height + self.addfunc_card["rect"].h)
            except Exception:
                break

class funcCard:
    def __init__(self, x, y, width, height, color, d_scale, g_mode):
        self.colors = {"black":(0,0,0),"white":(255,255,255),"gray":(128,128,128),"red":(255,0,0),"blue":(0,0,255),"green":(0,255,0),"yellow":(255,255,0),
          "orange":(255,165,0),"purple":(255,0,255),"cyan":(0,255,255),"turquoise":(64,224,208),"phantom_red":(255,100,100),
          "phantom_blue":(100,100,255),"phantom_green":(100,255,100),"phantom_yellow":(255,255,100),
          "maroon":(128,0,0),"crimson":(220,20,60),"violet":(238,130,238),"sky":(0,191,255),"sea_green":(60,179,113),
          "gold":(255,215,0),"coral":(240,128,128),"khaki":(240,230,140),"teal":(0,128,128),"steal_blue":(70,130,180),
          "spring_green":(0,255,127),"yellow_green":(154,205,50),"salmon":(250,128,114),"aqua_marine":(127,255,212),
          "royal_blue":(65,105,225)}
        self.rect = pygame.Rect(x, y, width, height)
        self.g_mode =g_mode
        self.color_a = None
        self.color_b = None
        self.setColor()
        self.rainbow = False
        self.color = self.colors[color]
        self.func = ""
        self.place = "0"
        self.func_pts = []
        self.func_size = 5
        self.func_clr = self.colors["red"]
        self.scale = d_scale
        self.func_tx = tf.textField(self.rect.x+28,self.rect.y+10,90,25,25,"ariel","y=","",30,False,g_mode == "random")
        self.place_tx = tf.textField(self.rect.x+20,self.func_tx.input_box.y+self.func_tx.input_box.h+10,20,20,5,"ariel","f(",")=",30,False,g_mode == "random")
        self.color_tx = tf.textField(self.rect.x+56,self.place_tx.input_box.y+self.place_tx.input_box.h+10,50,20,14,"ariel","color=","",25,False,g_mode == "random")
        self.color_tx.setText("red")
        self.size_tx = tf.textField(self.rect.x+50,self.color_tx.input_box.y+self.color_tx.input_box.h+10,30,20,2,"ariel","size=","",25,False,g_mode == "random")
        self.size_tx.setText(str(self.func_size))
        self.delete_button = tf.button((self.rect.x+165,self.rect.y+10,25,25),"clear",None,None,"x-button.png")
        self.m = 3

    def setColor(self):
        if self.g_mode == "light":
            self.color_a = self.colors["white"]
            self.color_b = (30,30,30)
        elif self.g_mode == "dark":
            self.color_a = (30, 30, 30)
            self.color_b = self.colors["white"]
        elif self.g_mode == "random":
            self.color_a = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.color_b = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def draw(self, scr):
        if self.rainbow:
            self.func_clr = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for k in range(len(self.func_pts)):
            try:
                if len(self.func_pts[k]) < 1:
                    continue
                pygame.draw.lines(scr, self.func_clr, False, self.func_pts[k], self.func_size)
            except Exception:
                pass
        if self.g_mode == "rainbow":
            pygame.draw.rect(scr, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), self.rect)
            pygame.draw.rect(scr, (random.randint(0,255),random.randint(0,255),random.randint(0,255)), self.rect, 2)
            self.func_tx.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.place_tx.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.color_tx.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.size_tx.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            pygame.draw.rect(scr,self.color_a,self.rect)
            pygame.draw.rect(scr, self.color_b, self.rect, 2)
        self.func_tx.draw(scr)
        self.place_tx.draw(scr)
        self.color_tx.draw(scr)
        self.size_tx.draw(scr)
        self.delete_button.draw(scr)

    def resetPos(self):
        self.func_tx.input_box.y = self.rect.y+10
        self.place_tx.input_box.y = self.func_tx.input_box.y+self.func_tx.input_box.h+10
        self.color_tx.input_box.y = self.place_tx.input_box.y+self.place_tx.input_box.h+10
        self.size_tx.input_box.y = self.color_tx.input_box.y+self.color_tx.input_box.h+10
        self.delete_button.rect.y = self.rect.y+10

    def getFunc(self, event):
        if self.size_tx.getText(event) is not None:
            try:
                self.func_size = int(self.size_tx.getText(event))
                self.size_tx.color = (0,220,0)
            except Exception:
                self.size_tx.Error()

        if self.color_tx.getText(event) is not None:
            if self.color_tx.getText(event) in self.colors:
                self.func_clr = self.colors[self.color_tx.getText(event)]
                self.color_tx.color = (0,220,0)
                self.rainbow = False
            elif self.color_tx.getText(event) == "random":
                self.func_clr = self.colors[random.choice(list(self.colors.keys()))]
                self.rainbow = False
            elif self.color_tx.getText(event) == "rainbow":
                self.rainbow = True
            else:
                self.color_tx.Error()

        if self.func_tx.getText(event) is not None:
            if ss.unKnowFunc(self.func_tx.getText(event), True):
                self.func_tx.Error()
                self.func = ""
            else:
                try:
                    if tf.forbbidenCheck(self.func_tx.getText(event),True):
                        self.func_tx.Error()
                        self.func = ""
                    elif not ss.check_chars(self.func_tx.getText(event)):
                        self.func_tx.Error()
                        self.func = ""
                    else:
                        self.func = self.func_tx.getText(event)
                        self.addFunc()
                        self.func_tx.color = (0,220,0)
                        self.place_tx.end_text = ")="
                        self.place_tx.setText("")
                except Exception:
                    self.func_tx.Error()
                    self.func = ""

        if self.place_tx.getText(event) is not None:
            if tf.lettersCheck(self.place_tx.getText(event).replace("pi",str(math.pi)).replace("e",str(math.e))):
                self.place_tx.end_text = ")="
                self.place_tx.Error()
                self.place = "0"
            elif self.func != "":
                try:
                    self.place = self.place_tx.getText(event).replace("pi",str(math.pi)).replace("e",str(math.e))
                    y_in_func = self.point_y(self.func,float(self.place))
                    if y_in_func is None:
                        self.place_tx.end_text = ")=undefined"
                    elif y_in_func%1==0:
                        self.place_tx.end_text = f")={y_in_func}"
                    else:
                        self.place_tx.end_text = f")={self.b_dot(y_in_func,4)}"
                    self.place_tx.color = (0,220,0)
                except Exception:
                    self.place_tx.Error()
                    self.place = "0"
            else:
                self.place_tx.Error()
                self.place = "0"

    @staticmethod
    def b_dot(f, dot):
        f = int(f * 10 ** dot)
        return f / 10 ** dot

    @staticmethod
    def distance(pointA, pointB):
        c = math.sqrt(math.pow(pointA[0] - pointB[0], 2) + math.pow(pointA[1] - pointB[1], 2))
        return c

    @staticmethod
    def point_y(func: str, x):
        func = func.replace("x", "(" + str(x) + ")")
        func = func.replace("X", "(" + str(x) + ")")
        return ss.StringCalculator(func)

    def addFunc(self):
        try:
            self.func_pts = []
            self.func_pts.append([])
            for x in range(-int(800 / 2) + 1, int(800 / 2) + 1):
                if self.point_y(self.func, x / self.scale) is None:
                    self.func_pts.append([])
                    continue
                try:
                    if x > -int(800 / 2) + 1 and self.distance(self.func_pts[-1][-1], [x + 800 / 2, 800 / 2 + (
                            -self.point_y(self.func, x / self.scale) * self.scale)]) > 800:
                        self.func_pts.append([])
                except Exception:
                    pass

                self.func_pts[-1].append([x + 800 / 2, HEIGHT / 2 + (-self.point_y(self.func, x / self.scale) * self.scale)])
        except Exception as e:
            print(e)

    def delete(self,event):
        if self.delete_button.click(event):
            return True
        return False

class homeScreen:
    def __init__(self, s_mode, func1,func2):
        self.mode = s_mode
        self.func = func1
        self.func2 = func2
        self.img = pygame.image.load("desnos-logo-1.png")
        self.g_b_color = (255, 0, 0)
        self.g_f_color = (0, 0, 0)
        self.s_b_color = (255, 0, 0)
        self.s_f_color = (0, 0, 0)
        if self.mode == "light":
            self.img = pygame.image.load("desnos-logo-2.png")
            self.g_b_color = (0, 0, 255)
            self.g_f_color = (255, 255, 255)
            self.s_b_color = (0, 0, 255)
            self.s_f_color = (255, 255, 255)
        elif self.mode == "random":
            self.img = random.choice([pygame.image.load("desnos-logo-1.png"),pygame.image.load("desnos-logo-2.png")])
            self.g_b_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.g_f_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.s_b_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.s_f_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        self.img = pygame.transform.scale(self.img,(800,800))
        self.graph_button = tf.button([350,375,100,50], self.g_b_color, self.func, None, None, ["graph", self.g_f_color, 30])
        self.setting_button = tf.button([350,450,100,50], self.s_b_color, self.func2, None, None, ["setting", self.s_f_color, 30])
        self.switch = False
        self.switch2 = False

    def draw(self, scr):
        if self.mode == "rainbow":
            self.img = pygame.transform.scale(random.choice((pygame.image.load("desnos-logo-1.png"),pygame.image.load("desnos-logo-2.png"))),(800,800))
            self.g_b_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.g_f_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.graph_button = tf.button([350,375,100,50], self.g_b_color, self.func, None, None, ["graph", self.g_f_color, 30])
            self.s_b_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.s_f_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.setting_button = tf.button([350, 450, 100, 50], self.s_b_color, self.func2, None, None,["setting", self.s_f_color, 30])
        scr.blit(self.img, (0,0))
        self.graph_button.draw(scr)
        self.setting_button.draw(scr)
        pygame.draw.rect(scr, self.g_f_color, self.graph_button.rect, 5)
        pygame.draw.rect(scr, self.s_f_color, self.setting_button.rect, 5)

    def getEvent(self,event):
        if self.graph_button.rect.collidepoint(pygame.mouse.get_pos()) and not self.switch:
            self.switch = True
            c = self.g_b_color
            self.g_b_color = self.g_f_color
            self.g_f_color = c
            self.graph_button = tf.button([350,375,100,50], self.g_b_color, self.func, None, None, ["graph", self.g_f_color, 30])
        elif self.switch and not self.graph_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.switch = False
            c = self.g_b_color
            self.g_b_color = self.g_f_color
            self.g_f_color = c
            self.graph_button = tf.button([350,375,100,50], self.g_b_color, self.func, None, None, ["graph", self.g_f_color, 30])

        if self.setting_button.rect.collidepoint(pygame.mouse.get_pos()) and not self.switch2:
            self.switch2 = True
            c2 = self.s_b_color
            self.s_b_color = self.s_f_color
            self.s_f_color = c2
            self.setting_button = tf.button([350,450,100,50],self.s_b_color,self.func2,None,None,["setting", self.s_f_color, 30])
        elif self.switch2 and not self.setting_button.rect.collidepoint(pygame.mouse.get_pos()):
            self.switch2 = False
            c2 = self.s_b_color
            self.s_b_color = self.s_f_color
            self.s_f_color = c2
            self.setting_button = tf.button([350, 450, 100, 50],self.s_b_color, self.func2, None, None,["setting", self.s_f_color, 30])

        self.graph_button.click(event)
        self.setting_button.click(event)

class settingScreen:
    def __init__(self,g_mode, font, func,title,back):
        self.mode = g_mode
        self.font = font
        self.func = func
        self.title_color = (255,0,0)
        self.color = (30,30,30)
        if self.mode == "light":
            self.color = (255,255,255)
            self.title_color = (0, 0, 255)
        elif self.mode == "random":
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.title_color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        if title is not None:
            self.title_size = title[1]
            self.title_tx = title[0]
            self.title = pygame.font.SysFont("ariel",self.title_size)
            self.title = self.title.render(self.title_tx,True,self.title_color)
        if func is not None:
            self.mode_card = settingCard(500,120,["select mode:",40],self.func[0],["light","dark","random","rainbow"],["Light","Dark","Random","Rainbow"],self.mode)
            self.scale_card = settingCard(50,370,["select graph scale:",40],self.func[1],[0,1,2,3,4,5,6],["2","5","10","20","25","50","100"],self.mode)
            self.graph_card = settingCard(50,120,["select graph type:",40],self.func[2],[0,1,2],["4x4","10x10","20x20"],self.mode)
            self.fill_card = settingCard(500,370,["auto fill?:",40],self.func[3],[True,False],["Yes","No"],self.mode)
        self.back_button = tf.button([10,758,32,32],"clear",back,None,"back.png")

    def draw(self,scr):
        if self.mode == "rainbow":
            self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.title_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.title = pygame.font.SysFont("ariel", self.title_size)
            self.title = self.title.render(self.title_tx, True, self.title_color)
        scr.fill(self.color)
        self.mode_card.draw(scr)
        self.scale_card.draw(scr)
        self.graph_card.draw(scr)
        self.fill_card.draw(scr)
        scr.blit(self.title,((800-self.title.get_width())/2,10))
        self.back_button.draw(scr)

    def getEvent(self,event):
        self.mode_card.getEvent(event)
        self.scale_card.getEvent(event)
        self.graph_card.getEvent(event)
        self.fill_card.getEvent(event)
        self.back_button.click(event)

    def setMode(self,s_mode):
        self.mode = s_mode
        self.title_color = (255, 0, 0)
        self.color = (30, 30, 30)
        if self.mode == "light":
            self.color = (255, 255, 255)
            self.title_color = (0, 0, 255)
        elif self.mode == "random":
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.title_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.title = pygame.font.SysFont("ariel", self.title_size)
        self.title = self.title.render(self.title_tx, True, self.title_color)
        self.mode_card.setMode(s_mode)
        self.scale_card.setMode(s_mode)
        self.graph_card.setMode(s_mode)
        self.fill_card.setMode(s_mode)

class settingCard:
    def __init__(self,x,y, title, func, args : list, buttons_tx, s_mode, space = 10):
        self.buttons = []
        self.x = x
        self.y = y
        self.space = space
        self.title_tx = title[0]
        self.title_size = title[1]
        self.func = func
        self.args = args
        self.button_h = 35
        self.b_tx = buttons_tx
        self.mode = s_mode
        self.color = [(0,0,0)]*(len(self.args)+1)
        self.f_color = [(0,0,0)]*len(self.args)
        self.setMode(self.mode)
        self.title = pygame.font.SysFont("ariel",self.title_size)
        self.title = self.title.render(self.title_tx,True,self.color[0])
        for b in range(len(self.args)):
            self.buttons.append(tf.button([self.x+10,self.y+(self.space + self.button_h)*b+self.title.get_height()+10,70,self.button_h],self.color[b-1],self.func,self.args[b],None,[self.b_tx[b],self.f_color[b],25]))

    def draw(self,scr):
        if self.mode == "rainbow":
            self.color[0] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for c in range(len(self.color) - 1):
                self.color[c + 1] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.f_color[c] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            self.title = pygame.font.SysFont("ariel", self.title_size)
            self.title = self.title.render(self.title_tx, True, self.color[0])
            for b in range(len(self.buttons)):
                self.buttons[b] = tf.button([self.x+10,self.y+(self.space+self.button_h)*b+self.title.get_height()+10,70,self.button_h],self.color[b],self.func,self.args[b],None,[self.b_tx[b],self.f_color[b],25])
        scr.blit(self.title,(self.x,self.y))
        for b in range(len(self.buttons)):
            self.buttons[b].draw(scr)

    def getEvent(self,event):
        for b in range(len(self.buttons)):
            if self.buttons[b].click(event):
                dot = self.title_tx.find(":")
                self.title_tx = self.title_tx[:dot+1] + " " + self.buttons[b].tx
                self.title = pygame.font.SysFont("ariel", self.title_size)
                self.title = self.title.render(self.title_tx, True, self.color[0])

    def setMode(self, s_mode):
        self.mode = s_mode
        self.color = [(255, 0, 0)] * (len(self.args)+1)
        self.f_color = [(30, 30, 30)] * len(self.args)
        if self.mode == "light":
            self.color = [(0, 0, 255)] * (len(self.args)+1)
            self.f_color = [(255, 255, 255)] * len(self.args)
        elif self.mode == "random":
            self.color[0] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            for c in range(len(self.color)-1):
                self.color[c+1] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                self.f_color[c] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.title = pygame.font.SysFont("ariel", self.title_size)
        self.title = self.title.render(self.title_tx, True, self.color[0])
        for b in range(len(self.buttons)):
            self.buttons[b] = tf.button([self.x+10,self.y+(self.space+self.button_h)*b+self.title.get_height()+10,70,self.button_h],self.color[b],self.func,self.args[b],None,[self.b_tx[b],self.f_color[b],25])

pygame.init()
WIDTH = 800
HEIGHT = 800
panalwidth = 200
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desnos-Beta")
pygame.display.set_icon(pygame.image.load("desnos-logo-1.png"))
current_screen = "home"
fpanel = funcPanel(0, 0, 0, 0, 0, "dark",None)
hscreen = homeScreen("light", None,None)
s_screen = settingScreen(None,None, None,None,None)
img = pygame.image.load("desnos-logo-1.png")
colors = {"black":(30,30,30),"white":(255,255,255),"gray":(128,128,128),"red":(255,0,0),"blue":(0,0,255),"green":(0,255,0),"yellow":(255,255,0),
          "orange":(255,165,0),"purple":(255,0,255),"cyan":(0,255,255),"turquoise":(64,224,208),"phantom_red":(255,100,100),
          "phantom_blue":(100,100,255),"phantom_green":(100,255,100),"phantom_yellow":(255,255,100),
          "maroon":(128,0,0),"crimson":(220,20,60),"violet":(238,130,238),"sky":(0,191,255),"sea_green":(60,179,113),
          "gold":(255,215,0),"coral":(240,128,128),"khaki":(240,230,140),"teal":(0,128,128),"steal_blue":(70,130,180),
          "spring_green":(0,255,127),"yellow_green":(154,205,50),"salmon":(250,128,114),"aqua_marine":(127,255,212),
          "royal_blue":(65,105,225)}
mode = "light"
lines_c = (colors["black"])
background_c = (colors["black"])
pointFont = pygame.font.SysFont("arial",15, True)
defult_clr = colors["black"]
clrv = (150,150,150)
line_size = 1

fill_scale = 20
fill = False
scale = 40
graphsize = 40


def setScale(cm):
    global scale
    if cm == 0:
        scale = 200
    elif cm == 1:
        scale = 80
    elif cm == 2:
        scale = 40
    elif cm == 3:
        scale = 20
    elif cm == 4:
        scale = 16
    elif cm == 5:
        scale = 8
    elif cm == 6:
        scale = 4

def setGraph(gm):
    global graphsize, fill_scale
    if gm == 0:
        graphsize = 200
        fill_scale = 40
    elif gm == 1:
        graphsize = 80
        fill_scale = 16
    elif gm == 2:
        graphsize = 40
        fill_scale = 8

def setFill(fl):
    global fill, line_size
    if fl:
        fill = True
        line_size = 2
    else:
        fill = False

def LoadScreen():
    global img
    if mode == "light":
        img = pygame.image.load("desnos-logo-2.png")
    elif mode == "random":
        img = random.choice((pygame.image.load("desnos-logo-2.png"),pygame.image.load("desnos-logo-1.png")))
    img = pygame.transform.scale(img, (800, 800))
    screen.blit(img,(0,0))
    pygame.display.update()

def setMode(mm):
    global mode, defult_clr, background_c, lines_c, clrv, s_screen
    mode = mm
    if mode == "light":
        background_c = colors["white"]
        lines_c = (0,0,0)
        defult_clr = (0,0,0)
        clrv = (150,150,150)
    elif mode == "dark":
        background_c = colors["black"]
        defult_clr = colors["white"]
        lines_c = colors["white"]
        clrv = (150,150,150)
    elif mode == "random":
        clrv = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        defult_clr = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        background_c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        lines_c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    if current_screen == "setting":
        s_screen.setMode(mode)

def draw():
    global lines_c, background_c, clrv
    if current_screen == "graph":
        if mode == "rainbow":
            background_c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            lines_c = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            clrv = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        screen.fill(background_c)
        pygame.draw.line(screen, lines_c, (WIDTH/2,0), (WIDTH/2, HEIGHT), 5)
        pygame.draw.line(screen, lines_c, (0,HEIGHT/2), (WIDTH, HEIGHT/2), 5)

        if fill:
            for f in range(0,WIDTH,fill_scale):
                pygame.draw.line(screen, lines_c, (f, 0), (f, HEIGHT), 1)
            for p in range(0, HEIGHT, fill_scale):
                pygame.draw.line(screen, lines_c, (0, p), (WIDTH, p), 1)

        for i in range(0, WIDTH+1, graphsize):
            pygame.draw.line(screen, lines_c, (i,0), (i, HEIGHT), line_size)
        for j in range(0, HEIGHT+1, graphsize):
            pygame.draw.line(screen, lines_c, (0,j), (WIDTH, j), line_size)

        pygame.draw.rect(screen, clrv, (WIDTH, 0, panalwidth, HEIGHT))
    elif current_screen == "home":
        screen.blit(img,(0,0))

def number_graph():
    global defult_clr
    if mode == "rainbow":
        defult_clr = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
    for x in range(int(WIDTH/graphsize)+1):
        xc = (x-WIDTH/graphsize/2)*graphsize/scale
        fp = pointFont.render(str(xc), True, defult_clr)
        if xc%1==0:
            fp = pointFont.render(str(int(xc)), True, defult_clr)
        if x == WIDTH/graphsize:
            screen.blit(fp, (x*WIDTH/(WIDTH/graphsize)-18, 400))
        else:
            screen.blit(fp, (x*WIDTH/(WIDTH/graphsize)+3, 400))

    for y in range(int(HEIGHT/graphsize)+1):
        yc = -(y-HEIGHT/graphsize/2)*graphsize/scale
        fp = pointFont.render(str(yc), True, defult_clr)
        if yc % 1 == 0:
            fp = pointFont.render(str(int(yc)), True, defult_clr)
        if y == HEIGHT/graphsize:
            screen.blit(fp, (WIDTH/2+4, y*HEIGHT/(HEIGHT/graphsize)-18))
        elif int((y-HEIGHT/graphsize/2) * graphsize / scale) == 0:
            continue
        else:
            screen.blit(fp, (WIDTH/2+4, y*HEIGHT/(HEIGHT/graphsize)+3))


def graphScreen():
    global screen, current_screen, fpanel
    screen = pygame.display.set_mode((WIDTH + panalwidth, HEIGHT))
    current_screen = "graph"
    fpanel = funcPanel(WIDTH, 0, panalwidth, HEIGHT, scale, mode, HomeScreen)

def HomeScreen():
    global current_screen, hscreen, screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    current_screen = "home"
    hscreen = homeScreen(mode, graphScreen,SettingScreen)

def SettingScreen():
    global current_screen, s_screen, screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    current_screen = "setting"
    s_screen = settingScreen(mode,pygame.font.SysFont("ariel",30),[setMode,setScale,setGraph,setFill],["setting",60],HomeScreen)

def desloop():
    HomeScreen()
    run = True
    clock = pygame.time.Clock()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if current_screen == "graph":
                fpanel.getInfo(event)
            elif current_screen == "home":
                hscreen.getEvent(event)
            elif current_screen == "setting":
                s_screen.getEvent(event)
        draw()
        if current_screen == "graph":
            fpanel.drawCards(screen)
            number_graph()
        elif current_screen == "home":
            hscreen.draw(screen)
        elif current_screen == "setting":
            s_screen.draw(screen)
        clock.tick(60)
        pygame.display.update()

def main():
    setScale(2)
    setGraph(1)
    setFill(False)
    setMode("light")
    LoadScreen()
    desloop()


if __name__ == "__main__":
    print(pygame.font.get_fonts()[92]) #לתקן את ה font
    main()
