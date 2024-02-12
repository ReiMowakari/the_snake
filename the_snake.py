from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Описание классов:
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color):
        """Инициализация объекта с атрибутами позиции и цвета."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """абстрактный метод отрисовки игровых объектов, говорящий о том,
         что каждый дочерний объект обязательно должен иметь метод отрисовки
         и переопределяться дочерним классом.
         """
        pass


class Apple(GameObject):
    """Инициализация объекта Яблоко."""
    def __init__(self, body_color):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Задаёт и возвращает случайную позицию."""
        return (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        """метод отрисовки объекта"""
        rect = pygame.Rect(
           (self.position[0], self.position[1]),
           (GRID_SIZE, GRID_SIZE)
         )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Инициализация объекта Змейка"""
    def __init__(self, body_color):
        super().__init__(body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = pygame.K_RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """обновляет позицию змейки (координаты каждой секции)"""
        self.get_head_position()
        dx, dy = self.positions[0], self.position[-1]

    def draw(self, surface):
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
             (self.last[0], self.last[1]),
             (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        return self.positions[-1]
def main():
    # Создание объектов яблоко и змейка.
    apple = Apple(APPLE_COLOR)
    apple.draw(screen)
    snake = Snake(SNAKE_COLOR)
    snake.draw(screen)
    while True:
        clock.tick(SPEED)
        # Основная логика игры.
        def handle_keys(game_object):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                    raise SystemExit
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game_object.direction != DOWN:
                        game_object.next_direction = UP
                    elif event.key == pygame.K_DOWN and game_object.direction != UP:
                        game_object.next_direction = DOWN
                    elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                        game_object.next_direction = LEFT
                    elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                        game_object.next_direction = RIGHT
        pygame.display.update()


if __name__ == '__main__':
    main()


# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
