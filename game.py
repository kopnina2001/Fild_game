import sys, os, pygame, random
x_start_rab = 50
y_start_rab = 50
x_speed_rab = 0
y_speed_rab = 0
score = 1000
shag = 0
go1 = 0
go2 = 0
go3 = 0

def init_window():
    pygame.init()
    window = pygame.display.set_mode((600, 600))
    pygame.display.set_caption('Полевая битва')


def load_image(name, colorkey=None):
    fullname = os.path.join('pictures', name)
    try:
        image = pygame.image.load(fullname)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey)
        image = image.convert_alpha()
        return image, image.get_rect()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

def draw_background():
    screen = pygame.display.get_surface()
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    back, back_rect = load_image("fild.jpg")
    screen.blit(back, (0, 0))
    pygame.display.flip()
    return back

class Animals(pygame.sprite.Sprite):
    def __init__(self, imoo, group,x, y):
        pygame.sprite.Sprite.__init__(self,group)
        self.image, self.rect = load_image(imoo, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = x
        self.rect.y = y


class Rabbit(Animals):
    def __init__(self, rab_group, x, y):
        Animals.__init__(self, "rabbit_2.png",rab_group, x, y)

class Fox(Animals):
    def __init__(self, fox_group, x, y):
        Animals.__init__(self, "fox_2.png",fox_group, x, y)

class Apple(Animals):
    def __init__(self, fox_group, x, y):
        Animals.__init__(self, "cap.png",fox_group, x, y)



def input(events):
    global x_start_rab, y_start_rab, x_speed_rab, y_speed_rab, life
    # Перехватываем нажатия клавиш на клавиатуре
    for event in events:
        if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and  event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        # Когда нажаты стрелки изменяем скорость кр
        # чтобы он летело
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: x_speed_rab = -1
            if event.key == pygame.K_RIGHT: x_speed_rab = 1
            if event.key == pygame.K_UP: y_speed_rab = -1
            if event.key == pygame.K_DOWN: y_speed_rab = 1
        # Когда стрелки не нажаты скорость ставим в ноль
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed_rab = 0
            if event.key == pygame.K_RIGHT: x_speed_rab = 0
            if event.key == pygame.K_UP: y_speed_rab = 0
            if event.key == pygame.K_DOWN: y_speed_rab = 0
    # Меняем положение кролика не выходя за рамки окна
    x_start_rab = x_start_rab + x_speed_rab
    y_start_rab = y_start_rab + y_speed_rab
    if (x_start_rab < 0):
        x_start_rab = 0
    if (x_start_rab > 505):
        x_start_rab = 505
    if (y_start_rab < 0):
        y_start_rab = 0
    if (y_start_rab > 505):
        y_start_rab = 505


def action(bk):
    global x_start_rab, y_start_rab, score, shag, go1, go2, go3
    screen = pygame.display.get_surface()
    fox_group = pygame.sprite.Group()
    rab_group = pygame.sprite.Group()
    apple_group = pygame.sprite.Group()
    bunny = Rabbit(rab_group, 1, 320)
    f_1 = Fox(fox_group,500, 100)
    f_2 = Fox(fox_group,800, 200)
    f_3 = Fox(fox_group,1200, 350)
    a_1 = Apple(apple_group, 600, 100)
    a_2 = Apple(apple_group, 1200, 100)
    apple = []
    apple.append(a_1)
    apple.append(a_2)
    foxes = []
    foxes.append(f_1)
    foxes.append(f_2)
    foxes.append(f_3)
    air = []
    air.append(bunny)
    foxes_1 = pygame.sprite.RenderPlain(foxes)
    rab = pygame.sprite.RenderPlain(air)
    apple_1 = pygame.sprite.RenderPlain(apple)
    timer = pygame.time.Clock()
    music = pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    while 1:
        timer.tick(700)
        input(pygame.event.get())
        blocks_hit_list = pygame.sprite.spritecollide(bunny, foxes_1, False)
        blocks_hit_list_1 = pygame.sprite.spritecollide(bunny, apple_1, False)
        if len(blocks_hit_list) > 0:
            score -= 2*len(blocks_hit_list)
            foxes_1.draw(screen)
            rab.draw(screen)
            if (score < 1):
                pygame.quit()
                sys.exit(0)
        elif len(blocks_hit_list_1)>0:
            score+=len(blocks_hit_list_1)
            apple_1.draw(screen)
            rab.draw(screen)
            if (score < 1):
                pygame.quit()
                sys.exit(0)
        bunny.rect.x = x_start_rab
        bunny.rect.y = y_start_rab
        f_1.rect.x = f_1.rect.x - 1
        f_2.rect.x = f_2.rect.x - 1
        f_3.rect.x = f_3.rect.x - 1
        a_1.rect.x = a_1.rect.x - 1
        a_2.rect.x = a_2.rect.x - 1
        if (f_1.rect.x < 0):
            f_1.rect.x = 500
            f_1.rect.y = 100
        if (f_2.rect.x < 0):
            f_2.rect.x = 800
            f_2.rect.y = 200
        if (f_3.rect.x < 0):
            f_3.rect.x = 1200
            f_3.rect.y = 350
        if (shag > 300):
            shag = 0
            go1 = random.randint(-1, 1)
            go2 = random.randint(-1, 1)
            go3 = random.randint(-1, 1)
        if (a_1.rect.x < 0):
            a_1.rect.x = 500
            a_1.rect.y = 100
        if (a_2.rect.x < 0):
            a_2.rect.x = 800
            a_2.rect.y = 200
        if (shag > 300):
            shag = 0
            go1 = random.randint(-1, 1)
            go2 = random.randint(-1, 1)
            go3 = random.randint(-1, 1)
        f_1.rect.y += go1
        f_2.rect.y += go2
        f_3.rect.y += go3
        a_1.rect.y += go1+go2
        a_2.rect.y += go3+go1
        shag += 1
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)
        life = int(score / 10)
        text = font.render("Жизнь: " + str(life), True, white)
        screen.blit(text, [10, 10])
        foxes_1.update()
        rab.update()
        apple_1.update()
        foxes_1.draw(screen)
        rab.draw(screen)
        apple_1.draw(screen)
        pygame.display.flip()


def main():
    init_window()
    heh = draw_background()
    action(heh)

main()
