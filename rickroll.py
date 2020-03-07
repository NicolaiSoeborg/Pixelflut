import os
from PIL import Image
from random import randint, shuffle
from time import sleep
from telnetlib import Telnet


def colors_to_rgb(color):
    def aux(c):
        return hex(c)[2:].zfill(2)
    return ''.join(aux(c) for c in color)


with Telnet('192.168.0.109', 1337) as tn:
    tn.write(b"SIZE\n")
    size = tn.read_until(b'\n').decode()[:-1].split(' ')
    w, h = int(size[1]), int(size[2])

    imgs = sorted(os.listdir('/tmp/rickroll/'), key=lambda f: int(f[3:-4]))
    imgs = [Image.open(f'/tmp/rickroll/{img}') for img in imgs]

    coordinates = []
    for x in range(imgs[0].width):
        for y in range(imgs[0].height):
            coordinates.append((x, y))
    shuffle(coordinates)

    data = []
    for img in imgs:
        print(img)
        data.append([])
        for (x, y) in coordinates:
            r, g, b = img.getpixel((x,y))
            color = colors_to_rgb([r, g, b])
            if color != '000000':
                data[-1].append(f'PX {680+x} {y} {color}\n'.encode())

    while True:
        for img in data:
            sleep(0.3)
            for pixel in img:
                tn.write(pixel)

