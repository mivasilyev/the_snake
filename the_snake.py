"""Игра Змейка.

На игровом поле появляется статичный квадрат красного цвета (яблоко)
и движущийся квадрат зеленого цвета (змейка). Игрок управляет направлением
движения змейки с помощью клавиш вверх, вниз, вправо, влево. При столкновении
с яблоком змейка увеличивается на один квадрат. При этом возникает новое
яблоко в случайном месте игрового поля. При столкновении змейки со своим телом
игра начинается с начала с рандомным направлением движения змейки.

Скорость игры регулируется переменной SPEED.

Классы:
    GameObject (родительский),
    Apple (дочерний от GameObject),
    Snake (дочерний от GameObject).

Функции:
    __init__ (для каждого класса, переопределяется),
    draw (для каждого класса, переопределяется),
    randomize_position (для класса Apple),
    move (для класса Snake),
    get_head_position (для класса Snake),
    update_direction (для класса Snake),
    reset (для класса Snake).
"""

from random import randint, choice
import pygame as pg


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


class GameObject:
    """Описание родительского класса игры."""

    def __init__(self) -> None:
        """Инициализирует объект класса.

        Устанавливает исходную позицию по центру поля.
        Используется дочерними классами.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None
        self.positions = [self.position]

    def draw(self):
        """Отрисовка объекта родительского класса.

        Переопределяется в дочерних классах.
        """
        raise NotImplementedError('Метод draw родительского класса не '
                                  'определен.')


class Apple(GameObject):
    """Описание дочернего класса Apple(Яблоко)."""

    def __init__(self, forbidden=[(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)],
                 color=APPLE_COLOR):
        """Метод задействует инициализатор родительского класса.

        Затем переопределяет цвет и позицию объекта исключая местоположение
        тела змейки.
        """
        super().__init__()
        self.body_color = color
        self.randomize_position(forbidden)

    def randomize_position(self, forbidden):
        """Рандомное размещение яблока на поле."""
        while True:
            position = (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                        randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)
            if position not in forbidden:
                self.position = position
                break

    def draw(self):
        """Отрисовка яблока на поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание дочернего класса Snake(Змейка)."""

    def __init__(self, color=SNAKE_COLOR):
        """Метод задействует reset и переопределяет направление движения."""
        self.reset(color=color)
        self.direction = RIGHT

    def move(self):
        """Метод движения змейки."""
        # Добавляем голову по ходу движения
        head_x, head_y = self.get_head_position()
        head_x_inc, head_y_inc = self.direction
        head_x = (head_x + head_x_inc * GRID_SIZE) % SCREEN_WIDTH
        head_y = (head_y + head_y_inc * GRID_SIZE) % SCREEN_HEIGHT
        new_head_position = (head_x, head_y)
        self.positions.insert(0, new_head_position)
        # При превышении длины отрезаем хвост
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод отрисовки змейки."""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения позиции головы змейки."""
        return self.positions[0]

    def update_direction(self, next_direction):
        """Метод обновления направления после нажатия игроком на клавишу."""
        if next_direction:
            self.direction = next_direction

    def reset(self, color=SNAKE_COLOR):
        """Метод инициализации змейки при создании или после столкновения."""
        super().__init__()
        self.body_color = color
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.length = 1


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit('Пользователь закрыл окно.')
        if event.type == pg.KEYDOWN:
            # Словарь обработки нажатий для управления змейкой:
            snake_dir = {(pg.K_UP, LEFT): UP, (pg.K_UP, RIGHT): UP,
                         (pg.K_DOWN, LEFT): DOWN, (pg.K_DOWN, RIGHT): DOWN,
                         (pg.K_LEFT, UP): LEFT, (pg.K_LEFT, DOWN): LEFT,
                         (pg.K_RIGHT, UP): RIGHT, (pg.K_RIGHT, DOWN): RIGHT}

            snake_dir_key = (event.key, game_object.direction)
            game_object.next_direction = snake_dir.get(snake_dir_key)


def main():
    """Тело игры."""
    # Инициализация PyGame:
    pg.init()
    # Создаем объекты классов.
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        """Основной цикл игры."""
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction(snake.next_direction)
        snake.move()

        # Если голова змейки совпала с положением яблока, то
        snake_head = snake.get_head_position()
        if snake_head == apple.position:
            snake.length += 1  # увеличиваем змейку,
            apple.randomize_position(snake.positions)

        # Если змейка столкнулась со своим телом, то
        if snake_head in snake.positions[1:]:
            screen.fill(color=BOARD_BACKGROUND_COLOR)  # всё поле в цвет фона
            snake.reset()  # сбрасываем змейку до исходного состояния
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
