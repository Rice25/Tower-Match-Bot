from PIL import ImageGrab
from PIL import ImageOps
from numpy import *
import os
import time
import win32api, win32con
import win32ui

# Globals for entire game screen
# ---------------

x1_pad = 235
y1_pad = 138
x2_pad = 709
y2_pad = 976

# Pixel y positions
layer1 = 564
layer2 = 477
layer3 = 384
layerDefault = 368

# Pixel x positions
leftPos = 108
rightPos = 367

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
     
def get_coords():
    x,y = win32api.GetCursorPos()
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
    box = (x1_pad, y1_pad, x2_pad, y2_pad)
    name = "Facebook - Google Chrome"
    w = win32ui.FindWindow( None, name )
    count = 0
    dc = w.GetWindowDC()
    i = dc.GetPixel (60,20)
    dc.DeleteDC()
    print(r)
    
if __name__ == '__main__':
    main()
