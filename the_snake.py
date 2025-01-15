from random import randint

import pygame

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


""" Класс Объекта """
# Базовый класс для игровых объектов


class GameObject:
    """функция"""

    def __init__(self, x=0, y=0):  # Исправлено на __init__
        self.position = (x, y)
        self.body_color = "default_color"  # Добавьте атрибут body_color

    def draw(self, color):
        """Функция рисования Объекта."""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def handle_keys(snake):
    """Ручное управление."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        """Змея-начало."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.last = None
        self.position = [0, 0]  # Начальная позиция змеи
        self.body_color = "green"  # Цвет тела змеи
        self.direction = UP
        self.next_direction = UP

    def handle_keys(self):
        """Ручное управление"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update(self):
        """апдейт"""
        self.last = self.positions[-1]
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = (head_x + delta_x, head_y + delta_y)
        self.positions.insert(0, new_head)
        self.positions.pop()

    def move(self, direction):
        """запуск"""
        if direction == 'up':
            self.position[1] += 1
        elif direction == 'down':
            self.position[1] -= 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1

    def get_head_position(self):
        """позиция головы змеи"""
        return self.position

    def reset(self):
        """сброс позиции головы змеи"""
        self.position = [0, 0]  # Сброс к начальной позиции

    def grow(self):
        """гров"""
        self.positions.append(self.last)

    def draw(self):
        """рисование"""
        for position in self.positions:
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def update_direction(self):
        """апдейт"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, direction):
        """рисование"""
        # Логика перемещения змеи
        if direction == 'up':
            self.position[1] += 1
        elif direction == 'down':
            self.position[1] -= 1
        elif direction == 'left':
            self.position[0] -= 1
        elif direction == 'right':
            self.position[0] += 1

    def reset(self):
        """сброс"""
        # Логика сброса состояния змеи
        self.position = [0, 0]  # Сброс к начальной позиции


class Apple(GameObject):
    """класс яблочка"""

    def __init__(self):
        """инит"""
        self.body_color = APPLE_COLOR  # Определяем атрибут body_color
        self.randomize_position()  # Случайная позиция при создании

    def randomize_position(self):
        """рандомная позиция"""
        self.position = (
            randint(0, GRID_WIDTH - 1),
            randint(0, GRID_HEIGHT - 1)
        )

    def draw(self):
        """рисование"""
        super().draw(self.body_color)


def main():
    """основная функция"""
    # Инициализация PyGame:
    pygame.init()

    # Создание экземпляров классов
    snake = Snake()
    apple = Apple()

    # пока верно
    while True:

        # Обработка действий игрока
        snake.handle_keys()
        snake.update_direction()
        snake.update()

        # Проверка на движеие к яблоку
        if snake.positions[0] == apple.position:
            snake.grow()
            apple.respawn()

        # Отрисовка экрана
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.flip()

        # Ограничение частоты кадров
        clock.tick(60)  # Ограничение до 60 кадров в секунду


""" вызываем функцию """
# вызываем
if __name__ == '__main__':
    main()
