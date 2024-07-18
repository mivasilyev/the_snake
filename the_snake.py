"""Игра Змейка. На игровом поле появляется статичный квадрат красного цвета
(яблоко) и движущийся квадрат зеленого цвета (змейка). Игрок управляет
направлением движения змейки с помощью клавиш вверх, вниз, вправо, влево. При
столкновении с яблоком змейка увеличивается на один квадрат. При этом
возникает новое яблоко в случайном месте игрового поля. При столкновении
змейки со своим телом игра начинается с начала с рандомным направлением
движения змейки.

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
        """Инициализирует объект класса, устанавливает исходную позицию по
        центру поля. Используется дочерними классами.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None
        self.positions = (self.position,)

    def draw(self):
        """Отрисовка объекта родительского класса. Переопределяется в
        дочерних классах.
        """
        raise NotImplementedError


class Apple(GameObject):
    """Описание дочернего класса Apple(Яблоко)."""

    def __init__(self):
        """Метод задействует инициализатор родительского класса и
        затем переопределяет цвет и позицию объекта исключая местоположение
        тела змейки.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.forbidden = self.positions
        self.randomize_position()

    def randomize_position(self):
        """Рандомное размещение яблока на поле."""
        # Рандомно размещаем яблоко. Если попало на змейку, то повторяем.
        while True:
            _ = (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                 randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)
            if _ not in self.forbidden:
                self.position = _
                break

    def draw(self):
        """Отрисовка яблока на поле."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание дочернего класса Snake(Змейка)."""

    def __init__(self):
        """Метод задействует reset и переопределяет направление движения."""
        self.reset()
        self.direction = RIGHT

    def move(self):
        """Метод движения змейки."""
        # Добавляем голову по ходу движения
        head_x, head_y = self.get_head_position()
        head_x += self.direction[0] * GRID_SIZE
        head_x = head_x % SCREEN_WIDTH
        head_y += self.direction[1] * GRID_SIZE
        head_y = head_y % SCREEN_HEIGHT
        new_head_position = (head_x, head_y)
        self.positions = (new_head_position,) + self.positions
        # При превышении длины отрезаем хвост
        if len(self.positions) > self.length:
            positions_list = list(self.positions)
            self.last = positions_list.pop(-1)
            self.positions = tuple(positions_list)
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

    def update_direction(self):
        """Метод обновления направления после нажатия игроком на клавишу."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод инициализации змейки при создании или после столкновения со
        своим телом.
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.last = None
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.length = 1


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Тело игры."""
    # Инициализация PyGame:
    pg.init()
    # Создаем объекты классов.
    snake = Snake()
    apple = Apple()

    while True:
        """Основной цикл игры."""
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Если голова змейки совпала с положением яблока, то
        snake_head = snake.get_head_position()
        if snake_head == apple.position:
            snake.length += 1  # увеличиваем змейку,
            apple.forbidden = snake.positions  # передаем полож-е змейки.
            apple.randomize_position()

        # Если змейка столкнулась со своим телом, то
        if snake_head in snake.positions[1:]:
            screen.fill(color=BOARD_BACKGROUND_COLOR)  # всё поле в цвет фона
            snake.reset()  # сбрасываем змейку до исходного состояния
            apple.forbidden = snake.positions  # передаем тело змейки
            apple.randomize_position()

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
