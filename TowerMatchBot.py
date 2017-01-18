from PIL import ImageGrab
from PIL import ImageOps
from numpy import *
import os
import time
import win32api, win32con

"""

All coordinates assume a screen resolution of 2048x1152, and Chrome dragged
to the left side of the screen with the Bookmarks Toolbar enabled.
x_pad = 327
y_pad = 206
Play area = x_pad+1, y_pad+1, 953, 1319
"""


# Globals
# ---------------

x_pad = 327
y_pad = 206

# Pixel y positions
layer1 = 832
layer2 = 702
layer3 = 571
layerDefault = 536

# Pixel x positions
leftPos = 149   # min is 145
rightPos = 478  # max is 482

def screenGrab():
    box = (x_pad+1, y_pad+1, x_pad+626, y_pad+1113)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    print('Click.')

def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('left Down')

def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('left release')

def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
     
def get_cords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

# Use this for RGB value reference
class Cord:
    # pixel locations of where to look for color change
    layer1left = (145,832)  # RGB: 179 60 57
    layer1right = (482,832)  # RGB: 162 38 39 (red) - sum is 239
    layer2left = (145,702) # RGB: 180 46 43
    layer2right = (482,702)  # RGB: 162 34 34 (red) - sum is 230
    layer3left = (145,571)  # RGB: 219 178 148
    layer3right = (482,571)  # RGB: 206 173 130 (white) - sum is 509 (514)
    default = (482,536) # 4 and beyond

"""
RGB Sum Database:
Red left: 296, 269
Red right: 239, 230
White left: 545, 544
White right: 509, 514
"""

def resetGame():
    # location of "Play" and "Play Again"
    mousePos((312, 1053))
    leftClick()
    time.sleep(.1)

def getRGBSum(side,layer,im):
    if side == 'left':
        a = array(im.getpixel((leftPos,layer)))
        a = a.sum()
        return a
    elif side == 'right':
        b = array(im.getpixel((rightPos,layer)))
        b = b.sum()
        return b
    else:
        print("Invalid side")
        
def isRed(a,b):
    if ( a >= 260 and a <= 310 ) and ( b >= 220 and b <= 240 ):
        return True
    else:
        return False

def isWhite(a,b):
    if (a >= 540 and a <= 555 ) and ( b >= 500 and b <= 520 ):
        return True
    else:
        return False

def checkLayer(layer, im):
    if layer == 'defaultRed':
        a = getRGBSum('left',layerDefault,im)
        b = getRGBSum('right',layerDefault,im)
        if isRed(a,b):
            leftClick()
            return 'red'
            
    if layer == 'defaultWhite':
        a = getRGBSum('left',layerDefault,im)
        b = getRGBSum('right',layerDefault,im)
        if isWhite(a,b):
            leftClick()
            return 'white'
    
    if layer == 1:
        a = getRGBSum('left',layer1,im)
        b = getRGBSum('right',layer1,im)
        if isRed(a,b):
            leftClick()
            return 1

    if layer == 2:
        a = getRGBSum('left',layer2,im)
        b = getRGBSum('right',layer2,im)
        if isRed(a,b):
            leftClick()
            return 2

    if layer == 3:
        a = getRGBSum('left',layer3,im)
        b = getRGBSum('right',layer3,im)
        if isWhite(a,b):
            leftClick()
            return 3

def startGame():
    layer = 1
    while True:
        print ("Running")
        im = screenGrab()
        if layer == 'defaultRed':
            if checkLayer(layer,im) == 'red':
                layer = 'defaultWhite'
                
        if layer == 'defaultWhite':
            if checkLayer(layer,im) == 'white':
                layer = 'defaultRed'
                
        if layer == 1:
            if checkLayer(layer,im) == 1:
                layer = 2
                
        if layer == 2:
            if checkLayer(layer,im) == 2:
                layer = 3
                
        if layer == 3:
            if checkLayer(layer,im) == 3:
                layer == 'defaultRed'

def main():
    startGame()

if __name__ == '__main__':
    main()
