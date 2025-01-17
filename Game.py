import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("Sacrifices must be made")

colours = ['crimson', 'coral', 'cyan', 'brown', 'yellow', 'blue', 'magenta', 'teal', 'red', 'orange', 'violet']
BG = pygame.image.load('C://Users//Lenovo//Desktop//Background.png')
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
brightness = 1.0
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos, self.y_pos = pos
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


def get_font(size):
    return pygame.font.Font('C://Users//Lenovo//Desktop//font.ttf', size)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Green color for the player
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, pos):
        self.rect.center = pos


class Square(pygame.sprite.Sprite):
    def __init__(self, color, x, y, velocity):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.color = color
        self.velocity = velocity

    def update(self):
        self.rect.move_ip(self.velocity)
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.velocity = (self.velocity[0], -self.velocity[1])
        if self.color == "cyan":
            self.rect.move_ip(-1, 5)
        elif self.color == "crimson":
            self.rect.move_ip(-2, 6)
        elif self.color == "yellow":
            self.rect.move_ip(2, 5)
        elif self.color == "brown":
            self.rect.move_ip(-3, 7)
        elif self.color == "coral":
            self.rect.move_ip(0, 8)
        elif self.color == "blue":
            self.rect.move_ip(0, 9)
        elif self.color == "magenta":
            self.rect.move_ip(0, 10)
        elif self.color == "teal":
            self.rect.move_ip(-3, 10)
        elif self.color == "red":
            self.rect.move_ip(-2, 8)
        elif self.color == "orange":
            self.rect.move_ip(-2, 7)
        elif self.color == "violet":
            self.rect.move_ip(2, 10)
        if self.rect.top > SCREEN_HEIGHT or self.rect.left > SCREEN_WIDTH or self.rect.right > SCREEN_WIDTH:
            self.kill()


def restart_or_main():
    global brightness
    while True:
        pygame.mouse.set_visible(True)
        SCREEN.blit(BG, (0, 0))
        restart_or_main_mouse_pos = pygame.mouse.get_pos()
        restart_or_main_text = get_font(100).render("YOU LOST", True, "#b68f40")
        restart_or_main_rect = restart_or_main_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        SCREEN.blit(restart_or_main_text, restart_or_main_rect)
        restart_button = Button(
            image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50),
            text_input="RESTART GAME", font=get_font(75),
            base_color="Black", hovering_color="#b68f40"
        )
        main_button = Button(
            image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50),
            text_input="BACK TO MAIN MENU", font=get_font(75),
            base_color="Black", hovering_color="#b68f40"
        )

        for button in [restart_button, main_button]:
            button.change_color(restart_or_main_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.check_for_input(restart_or_main_mouse_pos):
                    restart_game()
                    return
                elif main_button.check_for_input(restart_or_main_mouse_pos):
                    main_menu()
                    return

        adjust_brightness(SCREEN, brightness)

        pygame.display.update()


def restart_game():
    global squares, wave, player
    squares.empty()
    wave = 0
    player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


def play():
    global wave, score, current_level, player, squares, lvl_text, brightness

    squares = pygame.sprite.Group()
    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    wave = 0
    score = 0
    current_level = 1
    run = True

    # Main game loop
    while run:
        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        player.update(pos)
        clock.tick(FPS)
        SCREEN.fill((0, 0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mouse.set_visible(True)

        if current_level == 1:
            level_one()
        elif current_level == 2:
            level_two()

        squares.update()
        squares.draw(SCREEN)
        player_group.draw(SCREEN)

        adjust_brightness(SCREEN, brightness)

        pygame.display.update()


def tutorial():
    global brightness
    global wave, score, current_level, player, squares, lvl_text

    squares = pygame.sprite.Group()
    player = Player()
    player_group = pygame.sprite.GroupSingle(player)
    wave = 0
    score = 0
    run = True
    time_frozen = True

    while run:

        pygame.mouse.set_visible(False)
        pos = pygame.mouse.get_pos()
        player.update(pos)
        clock.tick(FPS)
        SCREEN.fill((0, 0, 0))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mouse.set_visible(True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                time_frozen = False

        if time_frozen:
            tutorial_text = get_font(40).render(f"You are the green square", True, (255, 255, 255))
            SCREEN.blit(tutorial_text, (SCREEN_WIDTH // 2 - tutorial_text.get_width() // 2,
                                        SCREEN_HEIGHT // 2 - tutorial_text.get_height() // 2))
            tutorial_text2 = get_font(40).render(f"Your job is to avoid the enemies", True, (255, 255, 255))
            SCREEN.blit(tutorial_text2, (SCREEN_WIDTH // 2 - tutorial_text2.get_width() // 2,
                                         SCREEN_HEIGHT // 1.75 - tutorial_text2.get_height() // 1.75))
            tutorial_text3 = get_font(40).render(f"Click to begin!", True, (255, 255, 255))
            SCREEN.blit(tutorial_text3, (SCREEN_WIDTH // 2 - tutorial_text3.get_width() // 2,
                                         SCREEN_HEIGHT // 1.55 - tutorial_text3.get_height() // 1.55))
            tt_text = get_font(55).render(f'This is the tutorial', True, (255, 255, 255))
            SCREEN.blit(tt_text, (SCREEN_WIDTH // 2 - tt_text.get_width() // 2,
                                  SCREEN_HEIGHT // 100 - tt_text.get_height() // 100))
        else:
            if pygame.sprite.spritecollideany(player, squares):
                restart_or_main()

            for square in squares:
                collided_square = pygame.sprite.spritecollideany(square, squares)
                if collided_square and collided_square != square:
                    square.velocity = (-square.velocity[0], -square.velocity[1])
                    collided_square.velocity = (-collided_square.velocity[0], -collided_square.velocity[1])

            if len(squares) == 0 and wave < 10:
                wave += 1
                if wave == 1:
                    score = 0
                else:
                    score += wave

                for _ in range(wave):
                    pos_x = random.randint(50, SCREEN_WIDTH - 50)
                    pos_y = random.randint(-150, -50)
                    velocity = (random.choice([-3, 3]), random.choice([2, 3]))
                    square = Square(random.choice(colours), pos_x, pos_y, velocity)

                    while pygame.sprite.spritecollideany(square, squares):
                        pos_x = random.randint(50, SCREEN_WIDTH - 50)
                        pos_y = random.randint(-150, -50)
                        square = Square(random.choice(colours), pos_x, pos_y, velocity)

                    squares.add(square)

            elif len(squares) == 0 and wave == 10:
                pygame.mouse.set_visible(True)
                SCREEN.blit(BG, (0, 0))
                restart_or_main_mouse_pos = pygame.mouse.get_pos()
                congrats_text = get_font(100).render("Congratulations! The tutorial has ended!", True, "#b68f40")
                congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
                SCREEN.blit(congrats_text, congrats_rect)
                main_button = Button(
                    image=None, pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50),
                    text_input="BACK TO MAIN MENU", font=get_font(75),
                    base_color="Black", hovering_color="#b68f40"
                )

                for button in [main_button]:
                    button.change_color(restart_or_main_mouse_pos)
                    button.update(SCREEN)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if main_button.check_for_input(restart_or_main_mouse_pos):
                            main_menu()
                            return

            squares.update()
            squares.draw(SCREEN)
            player_group.draw(SCREEN)

        adjust_brightness(SCREEN, brightness)

        pygame.display.update()


def level_one():
    global wave, score, current_level, player, squares, lvl_text

    lvl_text = get_font(55).render(f'Level: {current_level}', True, (255, 255, 255))
    SCREEN.blit(lvl_text, (SCREEN_WIDTH // 2 - lvl_text.get_width() // 2, SCREEN_HEIGHT - lvl_text.get_height()))
    text = get_font(40).render(f'Wave: {wave}', True, (255, 255, 255))
    score_text = get_font(30).render(f'Score: {score}', True, (255, 255, 255))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    SCREEN.blit(score_text, [SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                             SCREEN_HEIGHT // 1.75 - score_text.get_height() // 1.75])
    if pygame.sprite.spritecollideany(player, squares):
        restart_or_main()

    for square in squares:
        collided_square = pygame.sprite.spritecollideany(square, squares)
        if collided_square and collided_square != square:
            square.velocity = (-square.velocity[0], -square.velocity[1])
            collided_square.velocity = (-collided_square.velocity[0], -collided_square.velocity[1])

    if len(squares) == 0 and wave < 20:
        wave += 1
        if wave == 1:
            score = 0
        else:
            score += wave

        for _ in range(wave):
            pos_x = random.randint(50, SCREEN_WIDTH - 50)
            pos_y = random.randint(-150, -50)
            velocity = (random.choice([-3, 3]), random.choice([2, 3]))
            square = Square(random.choice(colours), pos_x, pos_y, velocity)

            while pygame.sprite.spritecollideany(square, squares):
                pos_x = random.randint(50, SCREEN_WIDTH - 50)
                pos_y = random.randint(-150, -50)
                square = Square(random.choice(colours), pos_x, pos_y, velocity)

            squares.add(square)

    elif len(squares) == 0 and wave == 20:
        current_level += 1
        wave = 0
        squares.empty()


def level_two():
    global wave, score, current_level, player, squares, lvl_text

    lvl_text = get_font(55).render(f'Level: {current_level}', True, (255, 255, 255))
    SCREEN.blit(lvl_text, (SCREEN_WIDTH // 2 - lvl_text.get_width() // 2, SCREEN_HEIGHT - lvl_text.get_height()))
    text = get_font(40).render(f'Wave: {wave}', True, (255, 255, 255))
    score_text = get_font(30).render(f'Score: {score}', True, (255, 255, 255))
    SCREEN.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    SCREEN.blit(score_text, [SCREEN_WIDTH // 2 - score_text.get_width() // 2,
                             SCREEN_HEIGHT // 1.75 - score_text.get_height() // 1.75])
    if pygame.sprite.spritecollideany(player, squares):
        restart_or_main()

    for square in squares:
        collided_square = pygame.sprite.spritecollideany(square, squares)
        if collided_square and collided_square != square:
            square.velocity = (-square.velocity[0], -square.velocity[1])
            collided_square.velocity = (-collided_square.velocity[0], -collided_square.velocity[1])

    if len(squares) == 0 and wave < 35:
        wave += 1
        if wave == 1:
            score = 0
        else:
            score += wave

        for _ in range(wave):
            pos_x = random.randint(50, SCREEN_WIDTH - 50)
            pos_y = random.randint(-150, -50)
            velocity = (random.choice([-3, 3]), random.choice([2, 3]))
            square = Square(random.choice(colours), pos_x, pos_y, velocity)

            while pygame.sprite.spritecollideany(square, squares):
                pos_x = random.randint(50, SCREEN_WIDTH - 50)
                pos_y = random.randint(-150, -50)
                square = Square(random.choice(colours), pos_x, pos_y, velocity)

            squares.add(square)

    elif len(squares) == 0 and wave == 35:
        main_menu()


def adjust_brightness(surface, brightness):
    brightness_surface = pygame.Surface(surface.get_size(), flags=pygame.SRCALPHA)

    # Ca sa ramana luminozitatea intre 0-255 (invalid color argument altfel)
    brightness_value = max(0, min(255, int(brightness * 255)))

    brightness_surface.fill((brightness_value, brightness_value, brightness_value, 255))
    surface.blit(brightness_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


def options():
    global brightness
    while True:
        options_mouse_pos = pygame.mouse.get_pos()
        SCREEN.fill("white")
        value_text = get_font(40).render(f'Brightness: {brightness}', True, "Black")
        value_rect = value_text.get_rect(center=(640, 400))
        opt_text = get_font(100).render("OPTIONS MENU", True, "#b68f40")
        opt_rect = opt_text.get_rect(center=(640, 100))
        up_text = get_font(35).render("Press 'UP' to increase brightness", True, "Black")
        up_rect = up_text.get_rect(center=(640, 300))
        down_text = get_font(35).render("Press 'DOWN' to decrease brightness", True, "Black")
        down_rect = down_text.get_rect(center=(640, 340))
        options_back = Button(image=None, pos=(640, 650),
                              text_input="BACK", font=get_font(75), base_color="Black", hovering_color="#b68f40")

        options_back.change_color(options_mouse_pos)
        options_back.update(SCREEN)
        SCREEN.blit(opt_text, opt_rect)
        SCREEN.blit(up_text, up_rect)
        SCREEN.blit(down_text, down_rect)
        SCREEN.blit(value_text, value_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if options_back.check_for_input(options_mouse_pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    brightness = min(2.0, brightness + 0.1)
                elif event.key == pygame.K_DOWN:
                    brightness = max(0.0, brightness - 0.1)

        adjust_brightness(SCREEN, brightness)

        pygame.display.update()


def main_menu():
    global brightness
    while True:
        pygame.mouse.set_visible(True)
        SCREEN.blit(BG, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(640, 100))

        play_button = Button(image=pygame.image.load('C://Users//Lenovo//Desktop//Play Rect.png'), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="#b68f40")
        tut_button = Button(image=None, pos=(1000, 250),
                            text_input="TUTORIAL", font=get_font(40), base_color="White", hovering_color="#b68f40")
        options_button = Button(image=pygame.image.load('C://Users//Lenovo//Desktop//Options Rect.png'), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="#b68f40")
        quit_button = Button(image=pygame.image.load('C://Users//Lenovo//Desktop//Quit Rect.png'), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="#b68f40")
        SCREEN.blit(menu_text, menu_rect)

        for button in [play_button, options_button, quit_button, tut_button]:
            button.change_color(menu_mouse_pos)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                elif tut_button.check_for_input(menu_mouse_pos):
                    tutorial()
                elif options_button.check_for_input(menu_mouse_pos):
                    options()
                elif quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        adjust_brightness(SCREEN, brightness)

        pygame.display.update()


try:
    main_menu()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pygame.quit()
    sys.exit()