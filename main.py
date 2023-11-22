import pygame

pygame.init()# команда необхідна для використання обьектів бібліотеки

back = (200, 255, 255)# створюємо зміну з кольором для фону
mw = pygame.display.set_mode((500, 500))# створюємо вікно
clock = pygame.time.Clock()
mw.fill(back)
# початкові скорості
dx = 3
dy = 3
# розмір платформи
platform_x = 200
platform_y = 330
# виключення прапорців
move_right = False
move_left = False
game_over = False

# клас прямокутника
class Area():
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def color(self, new_color):# змінює колір
        self.fill_color = new_color

    def fill(self):# створює прямокутник
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):# створює обводку
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):# перевіряє стикання
        return self.rect.colliderect(rect)

# клас напису
class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):# створює напис
        self.image = pygame.font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):# відображає напис на прямокутнику
        self.fill()
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))

# клас зображення
class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height, color=None)
        self.image = pygame.image.load(filename)# створення зображення

    def draw(self):# відображає зображення в прямокутнику
        mw.blit(self.image, (self.rect.x, self.rect.y))

# створення обєктів гри
ball = Picture('ll.png', 160, 200, 50, 50)
platform = Picture('platform.png', platform_x, platform_y, 100, 30)
# початкові координати спавна монстрів
start_x = 5
start_y = 5
# кількість монстрів в рядку
count = 9
# список для зберігання монстрів
monsters = []
# цикл для створення монстрів
for j in range(3):
    y = start_y + (55 * j)
    x = start_x + (27.5 * j)
    for i in range(count):
        d = Picture('enemy.png', x, y, 50, 50)
        monsters.append(d)
        x = x + 55
    count = count - 1
# ігровий цикл
while not game_over:
    ball.fill()
    platform.fill()
    # команди які зчитують натискання на клавіші
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_LEFT:
                move_left = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                move_right = False
            if event.key == pygame.K_LEFT:
                move_left = False
    # переміщення платформи в право
    if move_right:
        platform.rect.x += 3
    # переміщення платформи в ліво
    if move_left:
        platform.rect.x -= 3
    ball.rect.x += dx
    ball.rect.y += dy
    # відбиття мяча віж верхньої межі
    if ball.rect.y < 0:
        dy *= -1
    # відбиття мяча віж лівої та правої межі
    if ball.rect.x > 450 or ball.rect.x < 0:
        dx *= -1
    # перевірка на програш
    if ball.rect.y > 350:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU LOSE', 60, (255, 0, 0))
        time_text.draw(10, 10)
        game_over = True
    # перевірка на перемогу
    if len(monsters) == 0:
        time_text = Label(150, 150, 50, 50, back)
        time_text.set_text('YOU WIN', 60, (0, 200, 0))
        time_text.draw(10, 10)
        game_over = True
    # відбиття мяча віж платформи
    if ball.rect.colliderect(platform.rect):
        dy *= -1
    for m in monsters:
        m.draw()
        # якщо монстра торкнувся м'яч, видаляємо монстра зі списку та міняємо напрямки руху м'яча
        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            dy *= -1
    # відмальовка обєктів
    platform.draw()
    ball.draw()
    # оновлення екрану
    pygame.display.update()
    # частота оновлення
    clock.tick(40)
