from tkinter import *
import random 

#game settings/constants
GAME_WIDTH = 840
GAME_HEIGHT = 840
SPEED = 80 #how often is the canvas update lower=faster snake
GRID_SIZE = 30 #px
BODY_PARTS  = 3
SNAKE_COLOR = 'lawn green'
FOOD_COLOR = 'red4'
BACKGROUND_COLOR = 'black'

class Snake():
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []    
        self.squares = []

        for i in range(0,BODY_PARTS):
            self.coordinates.append([0, 0]) #snake will appear top-left corner
        
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x,y, x + GRID_SIZE, y + GRID_SIZE, fill=SNAKE_COLOR, tags='snake')
            self.squares.append(square)


class Food():
    def __init__(self):
        x = random.randint(0, GAME_WIDTH/GRID_SIZE-1) * GRID_SIZE
        y = random.randint(0, GAME_HEIGHT/GRID_SIZE-1) * GRID_SIZE

        self.coordinates = [x,y]

        canvas.create_rectangle(x,y, x + GRID_SIZE, y + GRID_SIZE, fill= FOOD_COLOR, tag='food')



def next_turn(snake, food):
    x, y = snake.coordinates[0]
    
    if initial_dir == "up":
        y -= GRID_SIZE
    elif initial_dir == "down": 
        y += GRID_SIZE
    elif initial_dir == "left":
        x -= GRID_SIZE
    elif initial_dir == "right":
        x += GRID_SIZE
    
    snake.coordinates.insert(0, (x,y))
    square = canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square) 

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")
        food = Food()
    else: #if we ate food then last square still remains
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake): 
        game_over(snake)
    else:
        window.after(SPEED, next_turn, snake, food)

def change_dir(new_dir):
    global initial_dir

    if new_dir == "left":
        if initial_dir != "right":
            initial_dir = new_dir
    elif new_dir == "right":
        if initial_dir != "left":
            initial_dir = new_dir
    elif new_dir == "up":
        if initial_dir != "down":
            initial_dir = new_dir
    elif new_dir == "down":
        if initial_dir != "up":
            initial_dir = new_dir


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH: 
        return True
    if y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]: #[1:] means body part except head
        if x == body_part[0] and y == body_part[1]:
            return True
        
    return False


def game_over(snake):

    canvas.delete(ALL) #deletes everything

    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=("consolas",70), text="GAME OVER", fill="red", tag="gameover")
    
    


window = Tk()
window.title('Snake')
window.resizable(False, False)

score = 0
initial_dir = 'down'

label = Label(window, text= 'Score:{}'.format(score), font=('consolas',40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenmmwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2)-(window_width/2))
y = int((screen_height/2)-(window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#basic inputs
window.bind('<Left>', lambda event: change_dir("left"))
window.bind('<Right>', lambda event: change_dir("right"))
window.bind('<Up>', lambda event: change_dir("up"))
window.bind('<Down>', lambda event: change_dir("down"))

snake = Snake()
food = Food()

next_turn(snake,food)

window.eval('tk::PlaceWindow . center') #window centered on the screen
window.mainloop()