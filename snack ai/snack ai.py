import pygame
import random
from collections import deque

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Set the dimensions of the grid
GRID_SIZE = (20, 20)
GRID_CELL_SIZE = 20

# Define directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Snake class
class Snake:
    def _init_(self):
        self.body = deque([(5, 5), (4, 5), (3, 5)])
        self.direction = RIGHT

    def move(self, direction):
        new_head = (self.body[0][0] + direction[0], self.body[0][1] + direction[1])
        self.body.appendleft(new_head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0]*GRID_CELL_SIZE, segment[1]*GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

# Food class
class Food:
    def _init_(self):
        self.position = self.generate_position()

    def generate_position(self):
        return (random.randint(0, GRID_SIZE[0]-1), random.randint(0, GRID_SIZE[1]-1))

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.position[0]*GRID_CELL_SIZE, self.position[1]*GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

# Snake AI class
class SnakeAI:
    def _init_(self, grid_size, snake, foods):
        self.grid_size = grid_size
        self.snake = snake
        self.foods = foods
        self.visited = set()
        self.parent = {}
        self.directions = [RIGHT, LEFT, DOWN, UP]

    def is_valid(self, x, y):
        return 0 <= x < self.grid_size[0] and 0 <= y < self.grid_size[1]

    def bfs(self, start_pos, target_positions):
        queue = deque([(start_pos, [])])
        self.visited.add(start_pos)

        while queue:
            current_pos, path = queue.popleft()
            x, y = current_pos

            if current_pos in target_positions:
                return path

            for direction in self.directions:
                new_x, new_y = x + direction[0], y + direction[1]
                new_pos = (new_x, new_y)

                if self.is_valid(new_x, new_y) and new_pos not in self.visited and new_pos not in self.snake.body:
                    queue.append((new_pos, path + [direction]))
                    self.visited.add(new_pos)
                    self.parent[new_pos] = current_pos

        return None  # If no path is found

    def next_move(self):
        all_foods = [food.position for food in self.foods]
        best_path = None
        for food_pos in all_foods:
            self.visited.clear()
            path = self.bfs(self.snake.body[0], [food_pos])
            if path and (best_path is None or len(path) < len(best_path)):
                best_path = path

        if best_path:
            return best_path[0]
        else:
            return None

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = GRID_SIZE[0] * GRID_CELL_SIZE
screen_height = GRID_SIZE[1] * GRID_CELL_SIZE
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake AI")

# Initialize the snake and food
snake = Snake()
foods = [Food() for _ in range(3)]
ai = SnakeAI(GRID_SIZE, snake, foods)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the snake
    next_move = ai.next_move()
    if next_move:
        snake.move(next_move)
    else:
        # If no valid move, just move randomly (can be improved)
        snake.move(random.choice([UP, DOWN, LEFT, RIGHT]))

    # Check for collision with food
    for food in foods:
        if snake.body[0] == food.position:
            snake.grow()
            food.position = food.generate_position()

    # Check for collision with itself
    if snake.body[0] in list(snake.body)[1:]:
        running = False  # Game over

    # Clear the screen
    screen.fill(BLACK)

    # Draw snake and food
    snake.draw(screen)
    for food in foods:
        food.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)

pygame.quit()