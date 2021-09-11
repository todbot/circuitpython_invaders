# easing_demo_code.py -- play with easing functions using space invader bitmaps
# 10 Sep 2021 - @todbot
import time
from random import randint
import displayio
from adafruit_macropad import MacroPad
import adafruit_imageload

# return a random (x,y) tuple
def random_xy(min_x, max_x, min_y, max_y):
    return randint(min_x,max_x), randint(min_y,max_y) 

# liner interpolation between 'begin' and 'end'
def lerp(begin, end, t):
    return begin + t*(end-begin)

# cubic inout easing
def ease_inout_cubic(begin, end, t):
    tt = 0
    if t < 0.5:
	tt = 4 * t * t * t
    else:
        f = ((2 * t) - 2)
	tt =  0.5 * f * f * f + 1
    return lerp( begin,end, tt)

# quartic inout easing
def ease_inout_quartic(begin, end, t):
    tt=0
    if t<0.5:
        tt = 8 * t * t * t * t
    else:
	f = (t - 1)
	tt =  -8 * f * f * f * f + 1;
    return lerp( begin,end, tt)

class Invader:
    def __init__(self, x,y, w, h, tilegrid=None):
        self.x, self.y = x, y  # x,y pos
        self.w, self.h = w, h  # w,h size
        self.tg = tilegrid
        self.t = 0
        self.tstep = 0.03  # make this configuraable? 
        self.nx = x
        self.ny = y
    def done_moving(self):
        return self.t >= 1 # finished our move
    def new_pos(self, x,y):
        self.t = 0
        self.nx = x
        self.ny = y
    def update(self):
        if self.done_moving(): return # we've done our move
        last_x, last_y = self.x, self.y
        # self.x = lerp(last_x, self.nx, self.t)  # slide x
        # self.y = lerp(last_y, self.ny, self.t)  # slide y
        # self.x = ease_inout_cubic(last_x, self.nx, self.t)  # slide x
        # self.y = ease_inout_cubic(last_y, self.ny, self.t)  # slide y
        self.x = ease_inout_quartic(last_x, self.nx, self.t)  # slide x
        self.y = ease_inout_quartic(last_y, self.ny, self.t)  # slide y
        self.tg.x = int(self.x)
        self.tg.y = int(self.y)
        self.t += self.tstep

#
# main code
#
macropad = MacroPad()
maingroup = displayio.Group()
macropad.display.show(maingroup)

dw = macropad.display.width
dh = macropad.display.height
img_w = 16  # bitmaps are 16x10
img_h = 10  # bitmaps are 16x10
invader_fnames = [
    '/imgs/invader01_16.bmp',
    '/imgs/invader02_16.bmp',
    '/imgs/invader03_16.bmp',
    '/imgs/invader04_16.bmp',
    '/imgs/invader05_16.bmp',
    '/imgs/invader06_16.bmp',
    '/imgs/invader07_16.bmp',
]
invaders = []
# construct our invaders, each with its own TileGrid holding a bitmap
for i in range(len(invader_fnames)):
    img, pal = adafruit_imageload.load(invader_fnames[i])
    pal.make_transparent(0)
    imgtg = displayio.TileGrid(img, pixel_shader=pal)
    invader = Invader(dw//2,dh//2, img_w,img_h, imgtg) 
    maingroup.append(imgtg)
    invaders.append( invader )

tstep = 0.01  # step size for lerp
while True:

    for i in invaders:
        i.update()
        if i.done_moving(): # get new pos if done with old one
            nx,ny = random_xy(0, dw-i.w, 0, dh-i.w)
            i.new_pos(nx,ny)

    time.sleep(0.015)

