import pygame

pygame.init()
# характеристики окна
win = pygame.display.set_mode((500, 500))
# название окна
pygame.display.set_caption("Cubes_Game")

#Загрузка графики в игру
walkRight = [pygame.image.load('right_1.png'),
pygame.image.load('right_2.png'), pygame.image.load('right_3.png'),
pygame.image.load('right_4.png'), pygame.image.load('right_5.png'),
pygame.image.load('right_6.png')]

walkLeft = [pygame.image.load('left_1.png'),
pygame.image.load('left_2.png'), pygame.image.load('left_3.png'),
pygame.image.load('left_4.png'), pygame.image.load('left_5.png'),
pygame.image.load('left_6.png')]

bg = pygame.image.load('bg.jpg')
playerStand = pygame.image.load('idle.png')

#переменная для указания кадров в секунду
clock = pygame.time.Clock()

# характеристики героя
x = 50
y = 425
width = 60
height = 71
speed = 5

isJump = False
jumpCount = 10

#анимация героя (спрайты)
left = False
right = False
animCount = 0
lastMove = "right"

class Snaryad():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        # скорость снаряда. facing для отправки снаряда в нужную сторону
        self.vel = 8 * facing #

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


def drawWindow():
    global animCount
    win.blit(bg, (0, 0))
    #Проверка. для отрисовки анимации в 30 кадров в секунду
    if animCount + 1 >= 30:
        animCount = 0
    # отрисовка анимации
    if left:
        win.blit(walkLeft[animCount // 5], (x, y))
        animCount += 1
    elif right:
        win.blit(walkRight[animCount // 5], (x, y))
        animCount += 1
    else:
        win.blit(playerStand, (x, y))

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()

run = True
#список для снарядов
bullets = []
# проверка в цикле нажатия на клавиатут в мксек.
while run:
    clock.tick(30)
    # скорость героя
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #поведение снаряда, если выходит за пределы окна, удаляется из списка
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    # управление с клавиатуры и проверка наличия героя в видимом окне
    keys = pygame.key.get_pressed()

    # стрельба. направление полета пули
    if keys[pygame.K_f]:
        if lastMove == "right":
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(Snaryad(round(x + width // 2),
            round(y + height // 2), 5, (255,0,0), facing))

    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        lastMove = "left"
    elif keys[pygame.K_RIGHT] and x < 500 - width - 5:
        x += speed
        left = False
        right = True
        lastMove = "right"
    else:
        left = False
        right = False
        animCount = 0
    # если не прыжок, то двигаться
    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    # обработка механики прыжка
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount**2) / 2
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    drawWindow()

pygame.quit()
