import pygame
import random

# These are the color representation of each block based on the HTML color picker (rgb)
colors = [(255, 0, 102), (51, 204, 51), (51, 153, 255), (153, 102, 255), (255, 51, 0), (255, 204, 0), (255, 102, 0)]

# The color settings of the game program
PINK, DARKBLUE, LIGHTGRAY = (255, 51, 119), (179, 204, 204), (115, 115, 115)

# This the screen settings of the overall screen size of the program
class Screen:
    def __init__(self):
        self.screen_width, self.screen_height, self.grid_size = 300, 600, 30
        self.grid_width, self.grid_height = self.screen_width // self.grid_size, self.screen_height // self.grid_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("M&M: PyXeltris")

#  Prompts the potential figures of each block that will be coming off while you run the program
class Figure:
    def __init__(self, x, y):  # Assign the random pick of color and figure of each block in the program
        self.x, self.y = x, y
        # Define different figure shapes
        self.figures = [
            [[1, 5, 9, 13], [4, 5, 6, 7]],
            [[4, 5, 9, 10], [2, 6, 5, 9]],
            [[6, 7, 9, 10], [1, 5, 6, 10]],
            [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
            [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
            [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
            [[1, 2, 5, 6]]
        ]
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

# The game settings of the program that are assigned to the random figures of each block and monitors its motion
class Tetris:
    def __init__(self, height, width):
        self.height, self.width = height, width
        self.field, self.score, self.state, self.figure, self.level = [[0] * width for _ in range(height)], 0, "start", None, 2

    def new_figure(self):
        self.figure = Figure(3, 0)

# Check each block if it is in the right grid and avoid to overlap with other block
    def intersects(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if (i + self.figure.y > self.height - 1 or j + self.figure.x > self.width - 1 or j + self.figure.x < 0 or self.field[i + self.figure.y][j + self.figure.x] > 0):
                        return True
        return False

# This defines the allowable motions in keyboard that can be use in the game
    def break_lines(self):
        lines = sum(all(self.field[i]) for i in range(1, self.height))
        self.field = [[0] * self.width] * lines + [row for row in self.field if not all(row)]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation


pygame.init()

# This will load the background image of the game
background_image = pygame.image.load("M&M PyXeltris background.jpg")

# PyXeltris class to manage game execution
class PyXeltris:
    def __init__(self):
        self.screen = Screen().screen
        self.game = Tetris(20, 10)

    def run(self):
        done, clock, fps, pressing_down = False, pygame.time.Clock(), 25, False
# This prompts the different keyboard keys that can be use to maneuver the different motions of each block in the program
        while not done:
            if self.game.figure is None:
                self.game.new_figure()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.game.rotate()
                    elif event.key == pygame.K_DOWN:
                        pressing_down = True
                    elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        self.game.go_side(-1 if event.key == pygame.K_LEFT else 1)
                    elif event.key == pygame.K_SPACE:
                        self.game.go_space()
                    elif event.key == pygame.K_ESCAPE:
                        self.game = Tetris(20, 10)
                elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                    pressing_down = False

            if pressing_down or pygame.time.get_ticks() % (1000 // self.game.level) == 0:
                if self.game.state == "start":
                    self.game.go_down()
# Blit the background image onto the screen to display the image
            self.screen.blit(background_image, (0, 0))
# This presents the game grid of the program and the motions of each figure of block on the screen
            for i in range(self.game.height):
                for j in range(self.game.width):
                    pygame.draw.rect(self.screen, DARKBLUE, [j * 30, i * 30, 30, 30], 1)
                    if self.game.field[i][j] > 0:
                        pygame.draw.rect(self.screen, colors[self.game.field[i][j]], [j * 30 + 1, i * 30 + 1, 28, 28])

            if self.game.figure is not None:
                for i in range(4):
                    for j in range(4):
                        p = i * 4 + j
                        if p in self.game.figure.image():
                            pygame.draw.rect(self.screen, colors[self.game.figure.color], [(j + self.game.figure.x) * 30 + 1, (i + self.game.figure.y) * 30 + 1, 28, 28])

            # Render the score
            font = pygame.font.SysFont('Calibri', 25, True, False)
            text = font.render("SCORE: " + str(self.game.score), True, PINK)
            self.screen.blit(text, [0, 0])

            # Render game over message and prompt to press Esc to restart
            if self.game.state == "gameover":
                font_game_over = pygame.font.SysFont('Arial', 45, True, False)
                text_game_over = font_game_over.render("GAME OVER", True, (230, 0, 76))
                text_game_over1 = font_game_over.render("PRESS Esc", True, (255, 255, 0))
                self.screen.blit(text_game_over, [20, 200])
                self.screen.blit(text_game_over1, [25, 265])

            pygame.display.flip()
            clock.tick(fps)

        pygame.quit()


if __name__ == "__main__":
    PyXeltris().run()


