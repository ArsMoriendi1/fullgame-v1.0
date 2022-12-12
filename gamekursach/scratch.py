import time
import pygame
import sys
from random import randint
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(('localhost', 10000))
my_colour = sock.recv(16).decode()
run = True

pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 100
TILE = 32
x,y =WIDTH//2, HEIGHT//2
colours = {'0': (255, 0, 0), '1': (255, 20, 147), '2': (255, 69, 0), '3': (255, 255, 0), '4': (255, 0, 125), '5': (218, 112, 214), '6': (128, 0, 128), '7': (128, 0, 0), '8': (0, 255, 0), '9': (0, 0, 139), '10': (123, 104, 238)}
pygame.display.set_caption('ТАHЧИКИ 1944')
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
DIR = 0
bullets = []
def dirrects(i):
    if i == 0 or i == 1:
        dx = 0
    elif i == 4:
        dx = -16
    elif i ==3:
        dx = 16
    elif i ==2:
        dx = 0
    return dx
def directs(i):
    if i == 0 or i == 1:
        dy = -16
    elif i ==4:
        dy = 0
    elif i ==3:
        dy = 0
    elif i ==2:
        dy = 16
    return dy
def draw_opponents(data):
    for i in range(len(data)):
        j = data[i].split(' ')
        x = WIDTH//2 + int(j[0])
        y = HEIGHT//2 + int(j[1])
        a = int(j[2])
        c = colours[j[3]]
        d = int(j[4])
        pygame.draw.rect(screen, c, (x, y, a, a))
        if d == 0:
            pygame.draw.line(screen, 'white', (x + 16, y - 10), (x + 16, y + 20), 4)
        if d == 1:
            pygame.draw.line(screen, 'white', (x + 16, y - 10), (x + 16, y + 20), 4)
        elif d == 2:
            pygame.draw.line(screen, 'white', (x + 16, y + 50), (x + 16, y + 20), 4)
        elif d == 3:
            pygame.draw.line(screen, 'white', (x + 48, y + 16), (x + 16, y + 16), 4)
        elif d == 4:
            pygame.draw.line(screen, 'white', (x - 16, y + 16), (x + 16, y + 16), 4)

def find(s):
    otkr = None
    for i in range(len(s)):
        if s[i] == '[':
            otkr = i
        if s[i] == ']':
            zakr = i
            res = s[otkr + 1:zakr]
            return res
    return ''

class Bullet():
    def __init__(self, x, y, dx, dy):
        bullets.append(self)
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    def update(self):
        self.x +=self.dx
        self.y +=self.dy
        if self.x <0 or self.x > WIDTH or self.y > HEIGHT:
            bullets.remove(self)
    def draw(self):
        pygame.draw.circle(screen, 'red', (self.x, self.y), 3)
while run:
    clock.tick(FPS)
    for bullet in bullets: bullet.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_a]:
                sock.send('[0, -1]'.encode())
                DIR = 4
            elif pygame.key.get_pressed()[pygame.K_d]:
                sock.send('[1, 0]'.encode())
                DIR = 3
                time.sleep(0.02)
            elif pygame.key.get_pressed()[pygame.K_w]:
                sock.send('[0, 1]'.encode())
                DIR = 1
                time.sleep(0.02)
            elif pygame.key.get_pressed()[pygame.K_s]:
                sock.send('[-1, 0]'.encode())
                DIR = 2
                time.sleep(0.02)
            elif pygame.key.get_pressed()[pygame.K_SPACE]:
                sock.send('[1, 1]'.encode())
                dx = dirrects(DIR) * 2
                dy = directs(DIR) * 2
                Bullet(WIDTH//2 + 16, HEIGHT//2 + 16, dx, dy)
        if event.type == pygame.KEYUP:
            if not pygame.key.get_pressed()[pygame.K_a]:
                sock.send('[0, 0]'.encode())

            elif not pygame.key.get_pressed()[pygame.K_d]:
                    sock.send('[0, 0]'.encode())

            elif not pygame.key.get_pressed()[pygame.K_w]:
                    sock.send('[0, 0]'.encode())

            elif not pygame.key.get_pressed()[pygame.K_s]:
                    sock.send('[0, 0]'.encode())




    data = sock.recv(2**20)
    data = data.decode()
    data = find(data)
    data = data.split(',')
    print(data)

    screen.fill('silver')
    pygame.draw.rect(screen, colours[my_colour], (x,y,TILE,TILE))
    if DIR == 0:
        pygame.draw.line(screen, 'white', (WIDTH//2+16, HEIGHT//2-10), (WIDTH//2+16, HEIGHT//2+20), 4)
    if DIR == 1:
        pygame.draw.line(screen, 'white', (WIDTH//2+16, HEIGHT//2-10), (WIDTH//2+16, HEIGHT//2+20), 4)
    if DIR == 2:
        pygame.draw.line(screen, 'white', (WIDTH//2+16, HEIGHT//2+50), (WIDTH//2+16, HEIGHT//2+20), 4)
    if DIR == 3:
        pygame.draw.line(screen, 'white', (WIDTH//2+48, HEIGHT//2+16), (WIDTH//2+16, HEIGHT//2+16), 4)
    if DIR == 4:
        pygame.draw.line(screen, 'white', (WIDTH//2-16, HEIGHT//2+16), (WIDTH//2+16, HEIGHT//2+16), 4)

    if data !=['']:
        draw_opponents(data)
    for bullet in bullets: bullet.draw()
    pygame.display.update()
pygame.quit()
sys.exit()

