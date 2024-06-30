import pygame, sys, random
from pygame.math import Vector2


class SNAKE:
    """
    Create snake
    """

    def __init__(self):
        self.screen = MAIN.screen
        # create blocks that constitute a snake
        self.body = [
            Vector2(5, 10),
            Vector2(4, 10),
            Vector2(3, 10),
        ]  # starting position, 3 blocks that are next to each other
        self.direction = Vector2(1, 0)  # automatic move to the right
        self.new_block = False

        # load images for snake
        self.head_up = pygame.image.load("Graphics/head_up.png").convert_alpha()
        self.head_down = pygame.image.load("Graphics/head_down.png").convert_alpha()
        self.head_right = pygame.image.load("Graphics/head_right.png").convert_alpha()
        self.head_left = pygame.image.load("Graphics/head_left.png").convert_alpha()

        self.tail_up = pygame.image.load("Graphics/tail_up.png").convert_alpha()
        self.tail_down = pygame.image.load("Graphics/tail_down.png").convert_alpha()
        self.tail_right = pygame.image.load("Graphics/tail_right.png").convert_alpha()
        self.tail_left = pygame.image.load("Graphics/tail_left.png").convert_alpha()

        self.body_vertical = pygame.image.load(
            "Graphics/body_vertical.png"
        ).convert_alpha()
        self.body_horizontal = pygame.image.load(
            "Graphics/body_horizontal.png"
        ).convert_alpha()

        self.body_tr = pygame.image.load("Graphics/body_tr.png").convert_alpha()
        self.body_tl = pygame.image.load("Graphics/body_tl.png").convert_alpha()
        self.body_br = pygame.image.load("Graphics/body_br.png").convert_alpha()
        self.body_bl = pygame.image.load("Graphics/body_bl.png").convert_alpha()

        self.crunch_sound = pygame.mixer.Sound("Sound/crunch.wav")  # add sound

    def draw_snake(self):
        """
        Draw the first snake on the main screen
        """
        # for block in self.body:
        #     # create a rect
        #     this_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
        #     # draw the rect
        #     pygame.draw.rect(surface=screen, color=(183, 111, 112), rect=this_rect)

        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # 1. we still need a rect for the positioning:
            this_rect = pygame.Rect(
                block.x * cell_size, block.y * cell_size, cell_size, cell_size
            )

            # 2. what direction is heading
            if index == 0:  # for head
                self.screen.blit(self.head, this_rect)

            elif index == len(self.body) - 1:  # for tail
                self.screen.blit(self.tail, this_rect)

            else:  # for body
                # get relation between this block and prev/next block
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, this_rect)

                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, this_rect)

                else:  # at the turning body part
                    if (
                        previous_block.x == -1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == -1
                    ):
                        self.screen.blit(self.body_tl, this_rect)
                    if (
                        previous_block.x == -1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == -1
                    ):
                        self.screen.blit(self.body_bl, this_rect)
                    if (
                        previous_block.x == 1
                        and next_block.y == -1
                        or previous_block.y == -1
                        and next_block.x == 1
                    ):
                        self.screen.blit(self.body_tr, this_rect)
                    if (
                        previous_block.x == 1
                        and next_block.y == 1
                        or previous_block.y == 1
                        and next_block.x == 1
                    ):
                        self.screen.blit(self.body_br, this_rect)

            # else: # for body
            #     pygame.draw.rect(screen, (183, 111, 112), this_rect)

    def update_head_graphics(self):
        """
        Check head direction and update graphics
        """
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left  # body is on the right of head -> head left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        """
        Check tail direction and update graphics
        """
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left  # body is on the right of head -> head left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        """
        Move snake
        """
        if self.new_block == True:  # if want new block is added
            body_copy = self.body[:]  # copy whole body
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]  # copy whole body except the last part
            body_copy.insert(
                0, body_copy[0] + self.direction
            )  # insert new head at the beginning of body
            self.body = body_copy[:]  # update new body

    def add_block(self):
        """
        When snake eats fruit, add another block to it
        """
        self.new_block = True

    def play_crunch_sound(self):
        """
        Play crunch sound
        """
        self.crunch_sound.play()


class FRUIT:
    """
    Create random fruits onto main screen
    """

    def __init__(self):
        self.screen = MAIN.screen
        self.randomize()
        # load apple drawing
        self.apple = pygame.image.load("Graphics/apple.png").convert_alpha()

    def draw_fruit(self):
        """
        Draw a square as fruit
        """
        # create a rectangle
        fruit_rect = pygame.Rect(
            self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size
        )

        # draw a rectangle onto main screen
        # pygame.draw.rect(surface=screen, color=(126, 166, 114), rect=fruit_rect)
        self.screen.blit(self.apple, fruit_rect)  # add photo into the rectangle

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    """
    Contain the logic of the whole game, easier to maintain
    """

    screen = None

    def __init__(self):
        self.snake = SNAKE()  # initiate object snake
        self.fruit = FRUIT()  # initiate object fruit

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        """
        Draw all elements here
        """
        self.draw_grass()
        self.fruit.draw_fruit()  # draw fruit into main screen
        self.snake.draw_snake()  # draw snake into main screen
        self.draw_score()

    def check_collision(self):
        """
        Check if snake's head and fruit at the same spot:
        - reposition the fruit
        - add another block to the snake
        - in case new fruit is at the body of snake -> generate again
        """
        if self.fruit.pos == self.snake.body[0]:
            # reposition the fruit
            self.fruit.randomize()
            # add another block to the snake
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        """
        Check if game over: snake is outside of the screen/snake hits itself
        """
        # hit the wall
        if (
            not 0 <= self.snake.body[0].x < cell_number
            or not 0 <= self.snake.body[0].y < cell_number
        ):
            self.game_over()
        # hit itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        """
        When game over, display Game Over text with name and scores.
        """
        # Display "Game Over" text
        font = pygame.font.Font(None, 50)  # You can choose your desired font and size
        game_over_text = font.render(
            "Game Over", True, (255, 0, 0)
        )  # Red color example
        game_over_rect = game_over_text.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2)
        )  # Center the text

        # Display name and score:
        score_font = pygame.font.Font(None, 30)
        score_text = score_font.render(
            f"Your score: {str(len(self.snake.body) - 3)}", True, (255, 0, 0)
        )
        score_text_rect = score_text.get_rect(
            centerx=game_over_rect.centerx, top=game_over_rect.bottom
        )
        # goodbye_text = font.render(f"Goodbye, {name}!", True, (255, 0, 0))

        # Blit the text onto the screen
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_text_rect)

        # Update the display
        pygame.display.flip()

        # Wait for a short time before quitting (optional)
        pygame.time.delay(3000)  # Delay in milliseconds (2 seconds in this example)

        # Quit Pygame and exit the program
        pygame.quit()
        sys.exit()

    def draw_grass(self):
        """
        Draw grass as in chess board
        """
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(self.screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(
                            col * cell_size, row * cell_size, cell_size, cell_size
                        )
                        pygame.draw.rect(self.screen, grass_color, grass_rect)

    def draw_score(self):
        """
        Count score and display
        """
        score_text = str(len(self.snake.body) - 3)  # count score
        # Display score:
        game_font = pygame.font.Font(None, 25)
        score_surface = game_font.render(
            score_text, True, (56, 74, 12)
        )  # create surface to display text score
        score_x = cell_size * cell_number - 60  # identify cordinates
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(
            center=(score_x, score_y)
        )  # create a rect around score_surface

        # Display an apple to the right of score:
        apple_rect = self.fruit.apple.get_rect(
            midright=(score_rect.left, score_rect.centery)
        )  # create apple rect on the left of score

        # Create background for score:
        bg_rect = pygame.Rect(
            apple_rect.left,
            apple_rect.top,
            apple_rect.width + score_rect.width + 6,
            apple_rect.height,
        )  # create a background for score

        # Add into main screen
        pygame.draw.rect(self.screen, (56, 74, 12), bg_rect, 2)
        self.screen.blit(score_surface, score_rect)  # add score into main screen
        self.screen.blit(
            self.fruit.apple, apple_rect
        )  # add apple next to score - pretty


def get_level():
    while True:
        level = input("Please choose level: easy, medium, hard: ").strip().lower()
        loop = set_level(level)
        if loop > 0:
            return loop


def set_level(level):
    """
    Get level
    """
    if level in ["easy", "e"]:
        loop = 200
    elif level in ["medium", "m", "med"]:
        loop = 160
    elif level in ["hard", "h"]:
        loop = 120
    else:
        loop = 0
    return loop


def hello(to="user"):
    return f"Hello, {to}!"


def get_answer_ready():
    while True:
        answer = input("ARE YOU READYYYY? ").strip().lower()

        if answer.startswith("yes") or answer == "y":
            print("Let's go!!!!")
            break
        elif answer.startswith("no") or answer == "n":
            print("Take a deep breath and try again later :)")
            sys.exit()
        else:
            print("What are you saying?")


cell_size = 40
cell_number = 20


def main():

    name = input("What's your name?: ").strip().capitalize()
    print(hello(name))

    loop = get_level()
    get_answer_ready()

    pygame.mixer.pre_init(
        44100, -16, 2, 512
    )  # good sound + play immediately when triggered
    pygame.init()
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    pygame.display.set_caption(f"{name}'s Snake")

    # create speed for game:
    clock = pygame.time.Clock()  # influence number of loops/s
    SCREEN_UPDATE = (
        pygame.USEREVENT
    )  # create custom event that was triggered every loop ms.
    pygame.time.set_timer(SCREEN_UPDATE, loop)

    MAIN.screen = screen

    main_game = MAIN()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # add the event to move snake
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:  # any button on keyboard

                if event.key == pygame.K_UP:  # move direction to be up
                    if (
                        main_game.snake.direction.y != 1
                    ):  # prevent it to move to opposite direction to itself
                        main_game.snake.direction = Vector2(0, -1)

                if event.key == pygame.K_DOWN:  # move direction to be down
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)

                if event.key == pygame.K_RIGHT:  # move direction to be right
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

                if event.key == pygame.K_LEFT:  # move direction to be left
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)

        screen.fill((175, 215, 70))  # add color to main screen
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
