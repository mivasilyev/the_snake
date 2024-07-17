from random import randint, choice
import pygame


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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Описание базового класса игры"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Отрисовка объекта базового класса"""
        pass


class Apple(GameObject):
    """Описание класса Apple(Яблоко)"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Рандомное размещение яблока на поле"""
        return (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)

    def draw(self):
        """Отрисовка яблока на поле"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описание класса Snake(Змейка)"""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = (self.position,)
        self.last = None
        self.direction = DOWN
        self.next_direction = None
        self.length = 1

    def move(self):
        """Метод движения змейки"""
        # Добавляем голову по ходу движения
        head_x, head_y = self.get_head_position()
        head_x += self.direction[0] * GRID_SIZE
        if head_x >= SCREEN_WIDTH:
            head_x = head_x - SCREEN_WIDTH
        elif head_x < 0:
            head_x = head_x + SCREEN_WIDTH
        head_y += self.direction[1] * GRID_SIZE
        if head_y >= SCREEN_HEIGHT:
            head_y = head_y - SCREEN_HEIGHT
        elif head_y < 0:
            head_y = head_y + SCREEN_HEIGHT
        new_head_position = (head_x, head_y)
        self.positions = (new_head_position,) + self.positions
        # при превышении длины отрезаем хвост
        if len(self.positions) > self.length:
            positions_list = list(self.positions)
            self.last = positions_list.pop(-1)
            self.positions = tuple(positions_list)

    def draw(self):
        """Метод отрисовки змейки"""
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Отрисовка тела змейки
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения позиции головы змейки"""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def reset(self):
        """Метод инициализации змейки до исходного состояния"""
        screen.fill(color=BOARD_BACKGROUND_COLOR)
        self.__init__()
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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


def main():
    """Тело игры"""
    # Инициализация PyGame:
    pygame.init()
    # Создаем экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)

        pygame.display.update()

        # Тут опишите основную логику игры.
        if snake.get_head_position() == apple.position:
            # print('Length inc')
            snake.length += 1
            apple = Apple()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.update_direction()
        snake.move()


if __name__ == '__main__':
    main()
