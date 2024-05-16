import time

import customtkinter
from tkinter import *
import random
from PIL import Image, ImageTk
import winsound
import threading
import math
import heapq

GAME_WIDTH = 14 * 40
GAME_HEIGHT = 14 * 40
SPEED = 100
SPACE_SIZE = 40
BODY_PARTS = 3
SNAKE_COLOR = "#0036FF"
SNAKE_HEAD = "black"
FOOD_COLOR = "#C62828"
BACKGROUND_COLOR = "black"
last_direction = "down"
GOLD_APPLE = False
BOMB = False
eye1 = None
eye2 = None
pupil1 = None
pupil2 = None
bomb_counter = 0
animation_counter = 0
first_explode = True
last_moves = 0
walls = []
DIFFICULTY = "medium"

start_image = Image.open("images/start.png")
start_image = start_image.resize((GAME_WIDTH, GAME_HEIGHT), Image.BILINEAR)

apple_image = Image.open("images/apple.png")
apple_image = apple_image.resize((SPACE_SIZE - 5, SPACE_SIZE - 5), Image.BILINEAR)

golden_apple_image = Image.open("images/golden_apple.png")
golden_apple_image = golden_apple_image.resize((SPACE_SIZE - 5, SPACE_SIZE - 5), Image.BILINEAR)

bomb_image = Image.open("images/bomb.png")
bomb_image = bomb_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

red_bomb_image = Image.open("images/red_bomb.png")
red_bomb_image = red_bomb_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

wall_image = Image.open("images/wall.png")
wall_image = wall_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

head_up_image = Image.open("images/head_up.png")
head_up_image = head_up_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

head_down_image = Image.open("images/head_down.png")
head_down_image = head_down_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

head_right_image = Image.open("images/head_right.png")
head_right_image = head_right_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

head_left_image = Image.open("images/head_left.png")
head_left_image = head_left_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

head_images = {
    "up": head_up_image,
    "down": head_down_image,
    "left": head_left_image,
    "right": head_right_image
}

body_bottomleft_image = Image.open("images/body_bottomleft.png")
body_bottomleft_image = body_bottomleft_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_bottomright_image = Image.open("images/body_bottomright.png")
body_bottomright_image = body_bottomright_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_topleft_image = Image.open("images/body_topleft.png")
body_topleft_image = body_topleft_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_topright_image = Image.open("images/body_topright.png")
body_topright_image = body_topright_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_horizontal_image = Image.open("images/body_horizontal.png")
body_horizontal_image = body_horizontal_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_vertical_image = Image.open("images/body_vertical.png")
body_vertical_image = body_vertical_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

body_images = {
    "bottomleft": body_bottomleft_image,
    "bottomright": body_bottomright_image,
    "topleft": body_topleft_image,
    "topright": body_topright_image,
    "horizontal": body_horizontal_image,
    "vertical": body_vertical_image
}

tail_up_image = Image.open("images/tail_up.png")
tail_up_image = tail_up_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

tail_down_image = Image.open("images/tail_down.png")
tail_down_image = tail_down_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

tail_right_image = Image.open("images/tail_right.png")
tail_right_image = tail_right_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

tail_left_image = Image.open("images/tail_left.png")
tail_left_image = tail_left_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)

tail_images = {
    "up": tail_up_image,
    "down": tail_down_image,
    "left": tail_left_image,
    "right": tail_right_image
}

exploation_animation = []
for i in range(10):
    exploation_image = Image.open("images/explosion.png")
    exploation_image = exploation_image.resize((SPACE_SIZE + (i * 12), SPACE_SIZE + (i * 12)),
                                               Image.BILINEAR)  # Resize the image
    exploation_animation.append(exploation_image)

snake_head_image = Image.open("images/snake_head.png")
snake_head_image = snake_head_image.resize((SPACE_SIZE, SPACE_SIZE), Image.BILINEAR)  # Resize the image


class Snake:
    def __init__(self, number="1"):
        global eye1, eye2, pupil1, pupil2, head_images, body_images
        head_down_tk = ImageTk.PhotoImage(head_images['down'])
        body_vertical_tk = ImageTk.PhotoImage(body_images['vertical'])
        self.body_size = BODY_PARTS
        self.coordinates = []
        # self.squars = []
        self.images = []

        for i in range(0, BODY_PARTS):
            if number == "1":
                self.coordinates.append([0, 0])
            if number == "2":
                self.coordinates.append([0, SPACE_SIZE * 4])

        for x, y in self.coordinates:
            image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=body_vertical_tk)
            canvas.body_vertical_tk = body_vertical_tk
            self.images.append(image)


class Food:
    def __init__(self):
        self.generate_coordinates()

    def generate_coordinates(self):
        global GOLD_APPLE, BOMB, score

        apple_tk = ImageTk.PhotoImage(apple_image)
        golden_apple_tk = ImageTk.PhotoImage(golden_apple_image)
        bomb_tk = ImageTk.PhotoImage(bomb_image)


        while True:
            x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 3)) * SPACE_SIZE
            y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 3)) * SPACE_SIZE
            new_coordinates = [x, y]

            # Check if the generated coordinates overlap with the snake's body
            is_in = False
            if abs(snake.coordinates[0][0] - x) < SPACE_SIZE * 3 and abs(
                    snake.coordinates[0][1] - y) < SPACE_SIZE * 3 and score < 100:
                is_in = True
            else:
                for body_part in snake.coordinates[1:]:
                # for body_part in snake.coordinates:
                    if x == body_part[0] and y == body_part[1]:
                        is_in = True
                if not is_in:
                    for wall in walls:
                        if wall[0] == x and wall[1] == y:
                            is_in = True
            if not is_in:
                break

        self.coordinates = new_coordinates
        g = random.randint(0, 10)
        print(DIFFICULTY)
        if g == 1:
            golden_apple_item = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=golden_apple_tk,
                                                    tag="gold_food")
            canvas.golden_apple_tk = golden_apple_tk
            GOLD_APPLE = True

        elif g == 2 and DIFFICULTY != 'easy':
            bomb_item = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=bomb_tk, tag="bomb")
            canvas.bomb_tk = bomb_tk
            BOMB = True

        else:
            apple_item = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=apple_tk, tag="food")
            canvas.apple_tk = apple_tk



def next_turn(snake, food):
    global direction, bomb_counter, exploation_image, exploation_animation, first_explode, head_images, body_images, tail_images, last_direction, last_moves

    if snake.body_size <= 0:
        game_over()
        return


    if snake.body_size == int((GAME_WIDTH / SPACE_SIZE) * (GAME_HEIGHT / SPACE_SIZE)):
        canvas.delete('food')
        label.configure(text="you won!")
        return

    exploation_tk = []
    for i in range(10):
        exploation_tk.append(ImageTk.PhotoImage(exploation_animation[i]))

    red_bomb_tk = ImageTk.PhotoImage(red_bomb_image)
    head_down_tk = ImageTk.PhotoImage(head_images['down'])
    head_up_tk = ImageTk.PhotoImage(head_images['up'])
    head_right_tk = ImageTk.PhotoImage(head_images['right'])
    head_left_tk = ImageTk.PhotoImage(head_images['left'])
    tail_down_tk = ImageTk.PhotoImage(tail_images['down'])
    tail_up_tk = ImageTk.PhotoImage(tail_images['up'])
    tail_right_tk = ImageTk.PhotoImage(tail_images['right'])
    tail_left_tk = ImageTk.PhotoImage(tail_images['left'])
    body_vertical_tk = ImageTk.PhotoImage(body_images['vertical'])
    body_horizontal_tk = ImageTk.PhotoImage(body_images['horizontal'])
    body_topleft_tk = ImageTk.PhotoImage(body_images['topleft'])
    body_topright_tk = ImageTk.PhotoImage(body_images['topright'])
    body_bottomleft_tk = ImageTk.PhotoImage(body_images['bottomleft'])
    body_bottomright_tk = ImageTk.PhotoImage(body_images['bottomright'])

    x, y = snake.coordinates[0]

    # cycle(snake, food)

    # direction = AI(snake, food)
    # if (AI(snake, food)) == None:
    #     direction = "up"

    if direction == 'up':
        y -= SPACE_SIZE

    elif direction == 'down':
        y += SPACE_SIZE

    elif direction == 'left':
        x -= SPACE_SIZE

    elif direction == 'right':
        x += SPACE_SIZE


    snake.coordinates.insert(0, (x, y))

    for coor in range(len(snake.coordinates) - 1):

        if coor == 0:
            if direction == 'up':
                image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=head_up_tk, tag='head')
                canvas.head_up_tk = head_up_tk

            elif direction == 'down':
                image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=head_down_tk, tag='head')
                canvas.head_down_tk = head_down_tk

            elif direction == 'left':
                image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=head_left_tk, tag='head')
                canvas.head_left_tk = head_left_tk

            elif direction == 'right':
                image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=head_right_tk, tag='head')
                canvas.head_right_tk = head_right_tk

            snake.images.insert(0, image)


        else:

            if snake.coordinates[coor][0] == snake.coordinates[coor - 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_vertical_tk)
                canvas.body_vertical_tk = body_vertical_tk

            if snake.coordinates[coor][1] == snake.coordinates[coor - 1][1]:
                canvas.itemconfig(snake.images[coor], image=body_horizontal_tk)
                canvas.body_horizontal_tk = body_horizontal_tk

            if (snake.coordinates[coor + 1][0] < snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] <
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor - 1][0]):
                canvas.itemconfig(snake.images[coor], image=body_bottomleft_tk)
                canvas.body_bottomleft_tk = body_bottomleft_tk

            if snake.coordinates[coor + 1][0] < snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] < \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor + 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_topright_tk)
                canvas.body_topright_tk = body_topright_tk

            if snake.coordinates[coor + 1][0] < snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] > \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor - 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_topleft_tk)
                canvas.body_topleft_tk = body_topleft_tk

            if snake.coordinates[coor + 1][0] < snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] > \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor + 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_bottomright_tk)
                canvas.body_bottomright_tk = body_bottomright_tk

            if snake.coordinates[coor + 1][0] > snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] > \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor + 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_bottomleft_tk)
                canvas.body_bottomleft_tk = body_bottomleft_tk

            if snake.coordinates[coor + 1][0] > snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] < \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor + 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_topleft_tk)
                canvas.body_topleft_tk = body_topleft_tk

            if snake.coordinates[coor + 1][0] > snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] < \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor - 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_bottomright_tk)
                canvas.body_bottomright_tk = body_bottomright_tk

            if snake.coordinates[coor + 1][0] > snake.coordinates[coor - 1][0] and snake.coordinates[coor + 1][1] > \
                    snake.coordinates[coor - 1][1] and snake.coordinates[coor][0] == snake.coordinates[coor - 1][0]:
                canvas.itemconfig(snake.images[coor], image=body_topright_tk)
                canvas.body_topright_tk = body_topright_tk

        if snake.coordinates[coor] == snake.coordinates[-2]:
            if snake.coordinates[-2][0] < snake.coordinates[-3][0]:
                canvas.itemconfig(snake.images[-2], image=tail_left_tk)
                canvas.tail_left_tk = tail_left_tk

            if snake.coordinates[-2][0] > snake.coordinates[-3][0]:
                canvas.itemconfig(snake.images[-2], image=tail_right_tk)
                canvas.tail_right_tk = tail_right_tk

            if snake.coordinates[-2][1] < snake.coordinates[-3][1]:
                canvas.itemconfig(snake.images[-2], image=tail_up_tk)
                canvas.tail_up_tk = tail_up_tk

            if snake.coordinates[-2][1] > snake.coordinates[-3][1]:
                canvas.itemconfig(snake.images[-2], image=tail_down_tk)
                canvas.tail_down_tk = tail_down_tk

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, SPEED, GOLD_APPLE, BOMB
        snake.body_size += 1
        if GOLD_APPLE:
            play_sound("audio/gold_eat.wav")
            score += 5
            GOLD_APPLE = False
            last_moves = 0
        elif BOMB:
            play_sound("audio/exploation.wav")
            # canvas.create_image(food.coordinates[0] + SPACE_SIZE // 2, food.coordinates[1] + SPACE_SIZE // 2,
            #                     image=exploation_tk[0], tag="exploation_image")
            # canvas.exploation_tk = exploation_tk
            window.update()
            for i in range(1, 6):
                if len(snake.images) <= 2:
                    game_over()
                    return
                else:
                    del snake.coordinates[-1]
                    # canvas.delete(snake.squars[-1])
                    # del snake.squars[-1]
                    canvas.delete(snake.images[-1])
                    del snake.images[-1]
            BOMB = False
            score -= 5
            if score < 0:
                score = 0
        else:
            play_sound('audio/eat.wav')
            score += 1
            last_moves = 0
        label.configure(text="score:{}".format(score))

        canvas.delete('food')
        canvas.delete('gold_food')
        canvas.delete('bomb')
        canvas.delete('red_bomb')

        food = Food()
        if DIFFICULTY == 'hard':
            w = random.randint(0,5)
            if w == 1:
                create_wall(snake, food)
        window.update()

    else:
        if BOMB:
            # if bomb_counter == 10:
            #     play_sound("ticking_bomb.wav")
            bomb_counter += 1
            if bomb_counter >= 20 and bomb_counter < 30:
                if bomb_counter % 2 == 0:
                    threading.Thread(target=winsound.Beep, args=(1000, 100)).start()
                    red_bomb_item = canvas.create_image(food.coordinates[0] + SPACE_SIZE // 2,
                                                        food.coordinates[1] + SPACE_SIZE // 2, image=red_bomb_tk,
                                                        tag="red_bomb")
                    canvas.red_bomb_tk = red_bomb_tk
                else:
                    canvas.delete('red_bomb')
                window.update()

            if bomb_counter == 30:
                canvas.delete('bomb')
                canvas.delete('red_bomb')
                play_sound("audio/exploation.wav")
            if bomb_counter >= 30:
                canvas.create_image(food.coordinates[0] + SPACE_SIZE // 2, food.coordinates[1] + SPACE_SIZE // 2,
                                    image=exploation_tk[bomb_counter - 30], tag="exploation_image")
                canvas.exploation_tk = exploation_tk
                window.update()
                if explode(snake, food) and first_explode:
                    first_explode = False
                    for i in range(1, 6):
                        if len(snake.images) <= 2:
                            game_over()
                            return
                        else:
                            del snake.coordinates[-1]
                            # canvas.delete(snake.squars[-1])
                            # del snake.squars[-1]
                            canvas.delete(snake.images[-1])
                            del snake.images[-1]

                    score -= 5
                    if score < 0:
                        score = 0

                if bomb_counter == 37:
                    canvas.delete('exploation_image')
                    BOMB = False
                    bomb_counter = 0
                    first_explode = True
                    food = Food()
                    window.update()

        del snake.coordinates[-1]

        # canvas.delete(snake.squars[-1])
        # del snake.squars[-1]

        canvas.delete(snake.images[-1])
        del snake.images[-1]

    if check_collisions(snake):
        game_over()

    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction, changing_direction

    if changing_direction != snake.coordinates[0]:
        if new_direction == 'left' and direction != 'right':
            direction = new_direction

        elif new_direction == 'right' and direction != 'left':
            direction = new_direction


        elif new_direction == 'up' and direction != 'down':
            direction = new_direction

        elif new_direction == 'down' and direction != 'up':
            direction = new_direction


    changing_direction = snake.coordinates[0]


def check_collisions(snake):
    global walls
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    for wall in walls:
        if wall[0] == snake.coordinates[0][0] and wall[1] == snake.coordinates[0][1]:
            return True


    return False


def create_wall(snake, food):
    wall_tk = ImageTk.PhotoImage(wall_image)

    while True:
        x = random.randint(0, int((GAME_WIDTH / SPACE_SIZE) - 3)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT / SPACE_SIZE) - 3)) * SPACE_SIZE

        # Check if the generated coordinates overlap with the snake's body
        is_in = False
        if abs(snake.coordinates[0][0] - x) < SPACE_SIZE * 3 and abs(
                snake.coordinates[0][1] - y) < SPACE_SIZE * 3 and score < 100:
            is_in = True
        else:
            for body_part in snake.coordinates[1:]:
                # for body_part in snake.coordinates:
                if x == body_part[0] and y == body_part[1]:
                    is_in = True
                if x == food.coordinates[0] and y == food.coordinates[1]:
                    is_in = True
        if not is_in:
            break

    # wall = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=wall_tk)
    # canvas.wall_tk = wall_tk
    wall = [x, y]

    walls.append(wall)

    for x, y in walls:
        image = canvas.create_image(x + SPACE_SIZE // 2, y + SPACE_SIZE // 2, image=wall_tk)
        canvas.wall_tk = wall_tk





def game_over():
    play_sound("audio/game_over.wav")
    canvas.delete(ALL)
    canvas.config(bg="black")
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 100, font=('consolas', 70), text="GAME OVER",
                       fill="red", tag="game_over")
    button_rect = canvas.create_rectangle(canvas.winfo_width() / 2 - 100, canvas.winfo_height() / 2,
                                          canvas.winfo_width() / 2 + 100, canvas.winfo_height() / 2 + 50, fill="red")
    button_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 25, text="play again",
                                     font=('consolas', 20), fill="black")
    canvas.tag_bind(button_rect, "<Button-1>", play_again)
    canvas.tag_bind(button_text, "<Button-1>", play_again)

    # Create the Easy button
    easy_button_rect = canvas.create_rectangle(
        canvas.winfo_width() / 2 - 198, canvas.winfo_height() / 2 + 115,
        canvas.winfo_width() / 2 - 108, canvas.winfo_height() / 2 + 146,
        fill="#37B1BC"
    )
    easy_button_text = canvas.create_text(
        canvas.winfo_width() / 2 - 151, canvas.winfo_height() / 2 + 130,
        text="Easy", font=('consolas', 15), fill="white"
    )
    canvas.tag_bind(easy_button_rect, "<Button-1>", lambda event: set_difficulty('easy'))
    canvas.tag_bind(easy_button_text, "<Button-1>", lambda event: set_difficulty('easy'))

    # Create the Medium button
    medium_button_rect = canvas.create_rectangle(
        canvas.winfo_width() / 2 - 50, canvas.winfo_height() / 2 + 104,
        canvas.winfo_width() / 2 + 45, canvas.winfo_height() / 2 + 144,
        fill="#FCD24F"
    )
    medium_button_text = canvas.create_text(
        canvas.winfo_width() / 2 - 3, canvas.winfo_height() / 2 + 124,
        text="Medium", font=('consolas', 15), fill="white"
    )
    canvas.tag_bind(medium_button_rect, "<Button-1>", lambda event: set_difficulty('medium'))
    canvas.tag_bind(medium_button_text, "<Button-1>", lambda event: set_difficulty('medium'))

    # Create the Hard button
    hard_button_rect = canvas.create_rectangle(
        canvas.winfo_width() / 2 + 105, canvas.winfo_height() / 2 + 115,
        canvas.winfo_width() / 2 + 198, canvas.winfo_height() / 2 + 146,
        fill="#FC5658"
    )
    hard_button_text = canvas.create_text(
        canvas.winfo_width() / 2 + 151, canvas.winfo_height() / 2 + 130,
        text="Hard", font=('consolas', 15), fill="white"
    )
    canvas.tag_bind(hard_button_rect, "<Button-1>", lambda event: set_difficulty('hard'))
    canvas.tag_bind(hard_button_text, "<Button-1>", lambda event: set_difficulty('hard'))


def explode(snake, food):
    for body_part in snake.coordinates:
        if abs(body_part[0] - food.coordinates[0]) < SPACE_SIZE * 2 and abs(body_part[1] - food.coordinates[1]) < SPACE_SIZE * 2:
            return True
    return False


def play_sound(sound_file):
    threading.Thread(target=winsound.PlaySound, args=(sound_file, 0)).start()



def estimated_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x1 - x2) + abs(y1 - y2)



def AI(snake, food):
    global score, last_moves

    x, y = snake.coordinates[0]
    food_position = food.coordinates

    # Calculate the possible moves.
    moves = ["up", "down", "left", "right"]

    # Filter out invalid moves (collisions or going back).
    valid_moves = []
    for move in moves:
        if (move == "up" and direction != "down") or \
                (move == "down" and direction != "up") or \
                (move == "left" and direction != "right") or \
                (move == "right" and direction != "left"):
            new_x, new_y = make_move((x, y), move)
            snake.coordinates.insert(0, (new_x, new_y))
            if not check_collisions(snake):
                valid_moves.append(move)
            snake.coordinates.pop(0)

    # Find the move that brings the snake closest to the food.
    closest_move = None
    closest_distance = float('inf')
    farthest_move = None
    farthest_distance = float('-inf')

    for move in valid_moves:
        new_x, new_y = make_move((x, y), move)
        distance = estimated_distance((new_x, new_y), food_position)
        if distance < closest_distance:
            closest_distance = distance
            closest_move = move
        if distance > farthest_distance:
            farthest_distance = distance
            farthest_move = move

    return closest_move



def make_move(position, move):
    x, y = position
    if move == "up":
        return x, y - SPACE_SIZE
    elif move == "down":
        return x, y + SPACE_SIZE
    elif move == "left":
        return x - SPACE_SIZE, y
    elif move == "right":
        return x + SPACE_SIZE, y


def cycle(snake, food):
    global direction



    if direction == "down" and snake.coordinates[0][1] + SPACE_SIZE == GAME_HEIGHT:
        direction = "right"
        return

    if direction == "right":
        if (snake.coordinates[0][0] / SPACE_SIZE) % 2 == 0:
            direction = "down"
            return
        else:
            direction = "up"
            return

    if direction == "up":
        if snake.coordinates[0][0] + SPACE_SIZE == GAME_WIDTH:
            if snake.coordinates[0][1] == 0:
                direction = "left"
            else:
                return
        if snake.coordinates[0][1] - SPACE_SIZE == 0:
            direction = "right"
            return

    if direction == "left" and snake.coordinates[0][0] == 0:
        direction = "down"


def draw_background(canvas):
    for row in range(int(GAME_WIDTH / SPACE_SIZE)):
        for col in range(int(GAME_HEIGHT / SPACE_SIZE)):
            x1 = col * SPACE_SIZE
            y1 = row * SPACE_SIZE
            x2 = x1 + SPACE_SIZE
            y2 = y1 + SPACE_SIZE
            color = "#91F58E" if (row + col) % 2 == 0 else "#7BD578"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=color)

play_sound("audio/new_game.wav")

def set_difficulty(new_difficulty):
    global DIFFICULTY
    DIFFICULTY = new_difficulty
    difficulty_label.configure(text="difficulty:{}".format(DIFFICULTY))




def play_again(event):
    global score, direction, changing_direction, snake, food, BOMB, bomb_counter, walls

    canvas.delete(ALL)  # Clear the canvas

    score = 0
    direction = 'down'
    changing_direction = [0, 0]
    BOMB = False
    bomb_counter = 0
    walls = []

    label.config(text="score:{}".format(score))  # Update the score label

    draw_background(canvas)  # Redraw the checkerboard

    snake = Snake()
    food = Food()

    next_turn(snake, food)

window = Tk()
window.title("Snake")
window.resizable(False, False)

score = 0
direction = 'down'
changing_direction = [0, 0]

difficulty_label = Label(window, text="difficulty:{}".format(DIFFICULTY), font=('consolas', 20))
difficulty_label.pack()

label = Label(window, text="score:{}".format(score), font=('consolas', 20))
label.pack()


canvas = Canvas(window, bg="black", height=GAME_HEIGHT, width=GAME_WIDTH)

canvas.pack()



draw_background(canvas)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{0}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))

window.bind('<A>', lambda event: change_direction('left'))
window.bind('<D>', lambda event: change_direction('right'))
window.bind('<W>', lambda event: change_direction('up'))
window.bind('<S>', lambda event: change_direction('down'))

new_game_rect = canvas.create_rectangle(canvas.winfo_width() / 2 - 120, canvas.winfo_height() / 2 - 150,
                                      canvas.winfo_width() / 2 + 120, canvas.winfo_height() / 2 + 150, fill="#4D71F7")
new_game_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 100, text="SNAKE GAME",
                                 font=('consolas', 30), fill="black")
name_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 - 65, text="by Ohad Amoyal",
                                 font=('consolas', 15), fill="black")

start_tk = ImageTk.PhotoImage(start_image)
canvas.create_image(GAME_WIDTH // 2, GAME_HEIGHT // 2, image=start_tk)
canvas.start_tk = start_tk

# Create the Easy button
easy_button_rect = canvas.create_rectangle(
    canvas.winfo_width() / 2 - 198, canvas.winfo_height() / 2 + 115,
    canvas.winfo_width() / 2 - 108, canvas.winfo_height() / 2 + 146,
    fill="#37B1BC"
)
easy_button_text = canvas.create_text(
    canvas.winfo_width() / 2 - 151, canvas.winfo_height() / 2 + 130,
    text="Easy", font=('consolas', 15), fill="white"
)
canvas.tag_bind(easy_button_rect, "<Button-1>", lambda event: set_difficulty('easy'))
canvas.tag_bind(easy_button_text, "<Button-1>", lambda event: set_difficulty('easy'))



# Create the Medium button
medium_button_rect = canvas.create_rectangle(
    canvas.winfo_width() / 2 - 50, canvas.winfo_height() / 2 + 104,
    canvas.winfo_width() / 2 + 45, canvas.winfo_height() / 2 + 144,
    fill="#FCD24F"
)
medium_button_text = canvas.create_text(
    canvas.winfo_width() / 2 - 3, canvas.winfo_height() / 2 + 124,
    text="Medium", font=('consolas', 15), fill="white"
)
canvas.tag_bind(medium_button_rect, "<Button-1>", lambda event: set_difficulty('medium'))
canvas.tag_bind(medium_button_text, "<Button-1>", lambda event: set_difficulty('medium'))

# Create the Hard button
hard_button_rect = canvas.create_rectangle(
    canvas.winfo_width() / 2 + 105, canvas.winfo_height() / 2 + 115,
    canvas.winfo_width() / 2 + 198, canvas.winfo_height() / 2 + 146,
    fill="#FC5658"
)
hard_button_text = canvas.create_text(
    canvas.winfo_width() / 2 + 151, canvas.winfo_height() / 2 + 130,
    text="Hard", font=('consolas', 15), fill="white"
)
canvas.tag_bind(hard_button_rect, "<Button-1>", lambda event: set_difficulty('hard'))
canvas.tag_bind(hard_button_text, "<Button-1>", lambda event: set_difficulty('hard'))


button_rect = canvas.create_rectangle(canvas.winfo_width() / 2 - 120, canvas.winfo_height() / 2 + 80,
                                      canvas.winfo_width() / 2 + 120, canvas.winfo_height() / 2 + 20, fill="#1B103A")
button_text = canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2 + 50, text="start",
                                 font=('consolas', 40), fill="white")
canvas.tag_bind(button_rect, "<Button-1>", play_again)
canvas.tag_bind(button_text, "<Button-1>", play_again)






window.mainloop()
