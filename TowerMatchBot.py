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

"""
# Globals for entire game screen
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
"""

# Globals for reduced area capture
# -------------------------------

x_pad = 327+144
y_pad = 206+535

# Pixel y positions
layer1 = 297
layer2 = 167
layer3 = 36
layerDefault = 1

# Pixel x positions
leftPos = 6
rightPos = 331

def screenGrab():
    box = (x_pad+1, y_pad+1, x_pad+339, y_pad+833) # full game screen is x_pad+626, y_pad+1113
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
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
    if side == 1:  # 1 is left
        a = array(im.getpixel((leftPos,layer)))
        a = a.sum()
        return a
    elif side == 2:   # 2 is right
        b = array(im.getpixel((rightPos,layer)))
        b = b.sum()
        return b
    else:
        print("Invalid side")
        
def isRed(a,b):
    if ( a > 250 and a < 320 ) and ( b > 210 and b < 250 ):
        return True
    else:
        return False

def isWhite(a,b):
    if (a > 530 and a < 565 ) and ( b > 490 and b < 530 ):
        return True
    else:
        return False

def checkLayer(layer, im):
    if layer == 4:       # 4 is defaultRed
        a = getRGBSum(1,layerDefault,im)
        b = getRGBSum(2,layerDefault,im)
        if isRed(a,b):
            leftClick()
            return 4
            
    if layer == 5: # 5 is defaultWhite
        a = getRGBSum(1,layerDefault,im)
        b = getRGBSum(2,layerDefault,im)
        if isWhite(a,b):
            leftClick()
            return 5
    
    if layer == 1:
        a = getRGBSum(1,layer1,im)
        b = getRGBSum(2,layer1,im)
        if isRed(a,b):
            leftClick()
            return 1

    if layer == 2:
        a = getRGBSum(1,layer2,im)
        b = getRGBSum(2,layer2,im)
        if isRed(a,b):
            leftClick()
            return 2

    if layer == 3:
        a = getRGBSum(1,layer3,im)
        b = getRGBSum(2,layer3,im)
        if isWhite(a,b):
            leftClick()
            return 3

def startGame():
    layer = 1
    while True:
        #print ("Running")
        im = screenGrab()
        if layer == 4:
            if checkLayer(layer,im) == 4:
                layer = 5
                
        if layer == 5:
            if checkLayer(layer,im) == 5:
                layer = 4
                
        if layer == 1:
            if checkLayer(layer,im) == 1:
                layer = 2
                
        if layer == 2:
            if checkLayer(layer,im) == 2:
                layer = 3
                
        if layer == 3:
            if checkLayer(layer,im) == 3:
                layer == 4

def main():
    pass

if __name__ == '__main__':
    main()
