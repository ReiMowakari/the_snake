from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

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
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object):
    """Функция по обработке клавиш пользователя для движения змейки."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            return False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


# Описание классов:
class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    body_color = (255, 255, 255)

    def __init__(self):
        """Инициализация объекта с атрибутами позиции и цвета."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self, x, y, surface):
        """Общий метод отрисовки объектов."""
        rect = pg.Rect((x, y), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Инициализация объекта Яблоко."""

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__()
        self.position = self.randomize_position()
        self.body_color = body_color

    @staticmethod
    def randomize_position():
        """Задаёт и возвращает случайную позицию."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,)

    def draw_Apple(self, surface):
        """метод отрисовки объекта Яблоко."""
        Apple.draw(self, self.position[0], self.position[1], surface)


class Snake(GameObject):
    """Инициализация объекта Змейка."""

    def __init__(self):
        super().__init__()
        self.reset()

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self):
        """обновляет позицию змейки (координаты каждой секции)."""
        current_head_pos = self.get_head_position()
        new_head_pos = ((current_head_pos[0] + self.direction[0] * GRID_SIZE)
                        % SCREEN_WIDTH,
                        (current_head_pos[1] + self.direction[1] * GRID_SIZE)
                        % SCREEN_HEIGHT)

        # Условие для сброса змейки после столкновения с собой
        if new_head_pos in self.positions[2:]:
            self.reset()
        # Условие объявлений новой позиции головы, если не столкнулась:
        else:
            self.positions.insert(0, new_head_pos)

        # Условие проверки длины змейки:
        if len(self.positions) > self.length + 1:
            self.last = self.positions.pop()

    def draw_Snake(self, surface):
        """отрисовка змейки."""
        for position in self.positions[:-1]:
            x, y = position
            Snake.draw(self, x, y, surface)

        # Отрисовка головы змейки
        x, y = self.positions[0]
        Snake.draw(self, x, y, surface)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """метод сброса змейки до начальных позиций."""
        self.length = 1
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None


def main():
    """Создание объектов яблоко и змейка."""
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Проверка на съедение яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw_Apple(screen)
        snake.draw_Snake(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
