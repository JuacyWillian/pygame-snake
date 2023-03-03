from enum import Enum
import sys
from random import randint

import pygame
from pygame.math import Vector2

pygame.init()
pygame.font.init()
pygame.font.get_init()


CELL_SIZE = 20
COLLS = 40
ROWS = 25
SCREEN = pygame.display.set_mode((CELL_SIZE*COLLS, CELL_SIZE*ROWS))


class UserInterface():
    def __init__(self) -> None:
        self.font1 = pygame.font.SysFont('Ubuntu', 72)
        self.font2 = pygame.font.SysFont('Ubuntu Regular', 32)
        self.font3 = pygame.font.SysFont('Ubuntu Mono', 16)

        self.score = 0

    def draw(self, ):
        # pygame.draw.rect(
        #     SCREEN, (0, 0, 0, 50),
        #     pygame.Rect(0, 0, SCREEN.get_width(), SCREEN.get_height()))
        SCREEN.fill((0, 0, 0, 128))

        game_over = self.font1.render(f"Game Over", True, "#FFFFFF")
        gameover_rect = game_over.get_rect(
            center=(int(SCREEN.get_width()/2), int(SCREEN.get_height()/2 - 60)))
        SCREEN.blit(game_over, gameover_rect)

        highscore = self.font2.render(
            f"Highscore: {self.score}", True, "#FFFFFF")
        SCREEN.blit(highscore, highscore.get_rect(
            center=SCREEN.get_rect().center))

        gameTips = self.font3.render(
            f"""[Press 'ENTER' to restart]{45*' '}[Press 'Q' to exit]""", True, "#ffffff")
        SCREEN.blit(gameTips, gameTips.get_rect(
            center=(int(SCREEN.get_width()/2), int(SCREEN.get_height()-50))
        ).bottomleft)


class Game():
    MAX_GAME_SPEED = 120
    GAME_SPEED = 200

    def __init__(self) -> None:
        self.CLOCK = pygame.time.Clock()
        self.SCREEN_UPDATE = pygame.USEREVENT
        pygame.display.set_caption('Snake Game :: Juacy Willian')
        pygame.time.set_timer(self.SCREEN_UPDATE, self.GAME_SPEED)

        self.fruit = Fruit()
        self.snake = Snake()
        self.gui = UserInterface()

        self.score = 0
        self.isGameOver = False

    def run(self, ):
        while True:
            self.handle_event()

            self.check_colision()
            self.draw()
            dt = self.CLOCK.tick(30)

    def update(self, ):
        if not self.isGameOver:
            self.snake.move()
            self.gui.score = self.score

    def draw(self, ):
        SCREEN.fill('#4d79ff')

        self.fruit.draw()
        self.snake.draw()

        if self.isGameOver:
            self.gui.draw()

        pygame.display.update()

    def handle_event(self, ):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                self.game_over()

            if e.type == pygame.KEYDOWN:
                if e.key in (pygame.K_UP, pygame.K_w) \
                        and self.snake.direction is not Directions.down:
                    self.snake.next_direction = Directions.up

                elif e.key in (pygame.K_DOWN, pygame.K_s) \
                        and self.snake.direction is not Directions.up:
                    self.snake.next_direction = Directions.down

                elif e.key in (pygame.K_LEFT, pygame.K_a) \
                        and self.snake.direction is not Directions.right:
                    self.snake.next_direction = Directions.left

                elif e.key in (pygame.K_RIGHT, pygame.K_d) \
                        and self.snake.direction is not Directions.left:
                    self.snake.next_direction = Directions.right

                elif e.key == pygame.K_q and self.isGameOver:
                    self.game_over()

                elif e.key == pygame.K_RETURN and self.isGameOver:
                    self.restart_game()

            if e.type == self.SCREEN_UPDATE:
                self.update()

    def check_colision(self, ):
        if self.fruit.pos == self.snake.body[0]:
            self.snake.add_block()
            self.score += 1

            while True:
                self.fruit.randomize()
                if self.fruit.pos in self.snake.body:
                    continue
                break

            self.update_game_speed()

        if self.snake.isOutBorder or self.snake.collideHerself:
            self.isGameOver = True

    def update_game_speed(self, ):
        if self.GAME_SPEED >= self.MAX_GAME_SPEED:
            self.GAME_SPEED -= 5
            pygame.time.set_timer(self.SCREEN_UPDATE, self.GAME_SPEED)

    def restart_game(self, ):
        self.snake.start()
        self.fruit.randomize()

        self.score = 0
        self.isGameOver = False

    def game_over(self, ):
        pygame.quit()
        sys.exit()


class Directions(Enum):
    down = Vector2(0, 1)
    left = Vector2(-1, 0)
    right = Vector2(1, 0)
    up = Vector2(0, -1)


class Snake:
    def __init__(self) -> None:
        self.start()

    def start(self, ):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10),]
        self.direction = Directions.right
        self.next_direction = Directions.right
        self.new_block = False

    @property
    def isOutBorder(self, ):
        return not (0 <= self.body[0].x <= COLLS and 0 <= self.body[0].y <= ROWS)

    @property
    def collideHerself(self, ):
        return self.body[0] in self.body[1:]

    def draw(self, ):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x*CELL_SIZE), int(block.y*CELL_SIZE),
                                     CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(SCREEN, '#33ffcc', block_rect)

    def move(self, ):
        self.direction = self.next_direction
        body_copy = self.body[:-1]
        if self.new_block == True:
            body_copy = self.body[:]
            self.new_block = False

        body_copy.insert(0, body_copy[0]+self.direction.value)
        self.body = body_copy[:]

    def add_block(self, ):
        self.new_block = True


class Fruit:
    def __init__(self) -> None:
        self.randomize()

    def draw(self):
        rect = pygame.Rect(
            int(self.pos.x*CELL_SIZE),
            int(self.pos.y*CELL_SIZE),
            CELL_SIZE,
            CELL_SIZE)

        pygame.draw.rect(SCREEN, '#cc0000', rect)

    def randomize(self, ):
        self.x = randint(0, COLLS-1)
        self.y = randint(0, ROWS-1)
        self.pos = Vector2(self.x, self.y)


game = Game()
game.run()
