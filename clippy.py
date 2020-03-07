from PIL import Image
from random import randint
from time import sleep
from telnetlib import Telnet


def colors_to_rgb(color):
    def aux(c):
        return hex(c)[2:].zfill(2)
    return ''.join(aux(c) for c in color)


def draw_img(img, w, h, tn):
    size = randint(35, 520)
    if size > 250: size = randint(35, 1020)
    im = img.rotate(randint(0, 360))
    im.thumbnail((size, size))

    clippy = []
    for x in range(im.width):
        for y in range(im.height):
            r, g, b, _ = im.getpixel((x,y))
            color = colors_to_rgb([r, g, b])
            if color != '000000':
                clippy.append((x, y, color))

    clippy_height = max([y for (x,y,c) in clippy])
    clippy_width = max([x for (x,y,c) in clippy])
    offset = (randint(0, w - clippy_height), randint(0, h - clippy_width))

    for (x, y, color) in clippy:
        tn.write(f'PX {x+offset[0]} {y+offset[1]} {color}\n'.encode())

with Telnet('192.168.0.109', 1337) as tn:
    tn.write(b"SIZE\n")
    size = tn.read_until(b'\n').decode()[:-1].split(' ')
    w, h = int(size[1]), int(size[2])

    img = Image.open('./clippy.png')
    while True:
        draw_img(img, w, h, tn)
        sleep(4)
