import pygame as pg
import random
import StringSolver as ss

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz=_)(*&^%$#@!~`<>?/:;'\""
class button:
    def __init__(self, rect, color, func = None, args = None, img = None, font=None):
        self.rect = pg.Rect(rect)
        self.color = color
        self.func = func
        self.args = args
        self.img = img
        self.font_d = font
        self.tx = None
        if img is not None:
            self.img = pg.transform.scale(pg.image.load(img), (self.rect.width,self.rect.height))
        if self.font_d is None:
            self.font = None
        else:
            self.tx = self.font_d[0]
            self.font = pg.font.SysFont("ariel",self.font_d[2]).render(self.font_d[0],True,self.font_d[1])

    def draw(self, scr):
        if self.color != "clear":
            pg.draw.rect(scr, self.color, self.rect)
        if self.img is not None:
            scr.blit(self.img, (self.rect.x,self.rect.y))
        if self.font is not None:
            scr.blit(self.font,(self.rect.x+(self.rect.w-self.font.get_width())/2,self.rect.y+(self.rect.h-self.font.get_height())/2))

    def click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.rect.collidepoint(event.pos):
                    if self.func is None:
                        return True
                    else:
                        if self.args is not None:
                            self.func(self.args)
                            return True
                        elif callable(self.func):
                            #elif type(self.func) == type(self.draw) or type(self.func) == type(lettersCheck):
                            self.func()
                            return True
        if self.func is None:
            return False

class textField:
    def __init__(self, x, y, width, height, l_max = 15, font = "ariel",start = "", end = "", size = 15, bold = False, ran = False):
        self.wd = width
        self.input_box = pg.Rect(x, y, width, height)
        if ran:
            self.color_inactive = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            self.color_active = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            self.color_inactive = pg.Color('lightskyblue3')
            self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.font = pg.font.SysFont(font, height-2, bold) #pg.font.Font(None, height - 2)
        self.dfont = pg.font.SysFont(font, size, bold)
        self.start_text = start
        self.end_text = end
        self.start = self.dfont.render(self.start_text, True, self.color)
        self.end = self.dfont.render(self.end_text, True, self.color)
        self.active = False
        self.text = ""
        self.l_max = l_max
    def getText(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.input_box.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if len(self.text)>0:
                        return self.text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif len(self.text) < self.l_max:
                    if event.key != pg.K_SPACE:
                        self.text += event.unicode
        if len(self.text)>self.l_max:
            self.text = self.text[:self.l_max]
        return None
    def draw(self, scr):
        txt_surface = self.font.render(self.text, True, self.color)
        width = max(self.wd, txt_surface.get_width() + 10)
        self.input_box.w = width
        scr.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pg.draw.rect(scr, self.color, self.input_box, 2)
        self.start = self.dfont.render(self.start_text, True, self.color)
        self.end = self.dfont.render(self.end_text, True, self.color)
        scr.blit(self.start, (self.input_box.x - self.start.get_width(), self.input_box.y))
        scr.blit(self.end, (self.input_box.w + self.input_box.x, self.input_box.y))

    def setText(self, text : str):
        self.text = text

    def Error(self):
        self.color = (255,0,0)
        self.text = ""
        self.active = False

def lettersCheck(s):
    for l in letters:
        if l in s:
            return True
    return False

def forbbidenCheck(s,isx : bool = False):
    char = ss.forbidden_chars.replace("pi","").replace("e","")
    if isx:
        char = char.replace("X", "").replace("x","")
    for l in char:
        if l in s:
            return True
    return False