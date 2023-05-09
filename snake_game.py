import pygame
import random

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
CELL_SIZE = 20
CELL_WIDTH = SCREEN_WIDTH // CELL_SIZE
CELL_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

SNAKE_COLOR = (255, 255, 255)
APPLE_COLOR = (255, 0, 0)

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game by rakuzan2weak")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

def draw_block(color, row, col):
    pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_text(text, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def get_random_location():
    row = random.randint(0, CELL_HEIGHT - 1)
    col = random.randint(0, CELL_WIDTH - 1)
    return (row, col)

class Snake:
    def __init__(self):
        self.length = 1
        self.body = [(CELL_HEIGHT // 2, CELL_WIDTH // 2)]
        self.direction = random.choice([UP, RIGHT, DOWN, LEFT])

    def move(self):
        if self.direction == UP:
            head = (self.body[0][0] - 1, self.body[0][1])
        elif self.direction == RIGHT:
            head = (self.body[0][0], self.body[0][1] + 1)
        elif self.direction == DOWN:
            head = (self.body[0][0] + 1, self.body[0][1])
        elif self.direction == LEFT:
            head = (self.body[0][0], self.body[0][1] - 1)

        self.body.insert(0, head)
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for block in self.body:
            draw_block(SNAKE_COLOR, block[0], block[1])

    def turn(self, direction):
        if (direction == UP and self.direction != DOWN) or \
            (direction == DOWN and self.direction != UP) or \
            (direction == LEFT and self.direction != RIGHT) or \
            (direction == RIGHT and self.direction != LEFT):
            self.direction = direction

    def check_collision(self):
        if self.body[0][0] < 0 or self.body[0][0] >= CELL_HEIGHT or \
            self.body[0][1] < 0 or self.body[0][1] >= CELL_WIDTH:
            return True

        for block in self.body[1:]:
            if self.body[0] == block:
                return True

        return False

class Apple:
    def __init__(self):
        self.location = get_random_location()

    def draw(self):
        draw_block(APPLE_COLOR, self.location[0], self.location[1])

def main():
    snake = Snake()
    apple = Apple()
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.turn(UP)
                elif event.key == pygame.K_RIGHT:
                    snake.turn(RIGHT)
                elif event.key == pygame.K_DOWN:
                    snake.turn(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.turn(LEFT)

        screen.fill((0, 0, 0))

        if snake.body[0] == apple.location:
            apple.location = get_random_location()
            snake.length += 1
            score += 10

        snake.move()

        if snake.check_collision():
            draw_text("GAME OVER", (255, 0, 0), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            draw_text("Press any key to continue", (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()
            pygame.time.wait(1000)
            pygame.event.clear()
            while True:
                event = pygame.event.wait()
                if event.type == pygame.KEYDOWN:
                    main()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    return

        apple.draw()
        snake.draw()
        draw_text(f"Score: {score}", (255, 255, 255), 10, 10)

        pygame.display.flip()
        clock.tick(10)

if __name__ == "__main__":
    main()