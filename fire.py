from random import randint, random
from time import sleep
from telnetlib import Telnet



def random_shift(x, p):
    """Change x by up to p percent (where 0 <= p < 1)"""
    d = x * p
    return x + (random() * 2 * d - d)

def randcolor(a, b, chance_of_low=0):
    return hex(randint(a, b))[2:].zfill(2)

with Telnet('192.168.0.109', 1337) as tn:
    tn.write(b"SIZE\n")
    size = tn.read_until(b'\n').decode()[:-1].split(' ')
    w, h = int(size[1]), int(size[2])

    def rand_point():
        x, y = randint(0, w), randint(round(h - (random()*300)), h)
        r = randcolor(0x4F, 0xFF)  # y lower => better chance of 0x7F
        g = randcolor(0X00, 0xAA)  # y lower => better chance of 0x00
        return x, y, f"{r}{g}00"

    # Clean bottom:
    for x in range(w):
        for y in range(h-100, h):
            tn.write(f'PX {x} {y} 000000\n'.encode())

    while True:
        x, y, color = rand_point()
        tn.write(f'PX {x} {y} {color}\n'.encode())
        sleep(0.0003)
