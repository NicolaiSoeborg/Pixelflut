import colorsys
from random import random
from time import sleep
from telnetlib import Telnet

def colors_to_rgb(color):
    def aux(c):
        return hex(round(c * 255))[2:].zfill(2)
    return ''.join(aux(c) for c in color)

with Telnet('192.168.0.109', 1337) as tn:
    tn.write(b"SIZE\n")
    size = tn.read_until(b'\n').decode()[:-1].split(' ')
    w, h = int(size[1]), int(size[2])

    x, y = 0, 0
    xv, yv = 1, 1
    STEP_SIZE = 1
    LINE_SIZE = 2

    i = 0
    while True:
        i = (i + 1) % 4096
        color = colorsys.hsv_to_rgb(i/4096, 1.0, 1.0)
        color = colors_to_rgb(color)
        
        for j in range(-LINE_SIZE, LINE_SIZE):
            tn.write(f'PX {(x+j)%w} {(y+1)%h} {color}\n'.encode())

        if y <= 0:
            yv = STEP_SIZE
        elif y > h:
            yv = -STEP_SIZE
        y += yv if random() < 0.4 else 0

        if x <= 0:
            xv = STEP_SIZE
        elif x > w:
            xv = -STEP_SIZE
        x += xv if random() < 0.6 else 0
        
        sleep(0.003)
