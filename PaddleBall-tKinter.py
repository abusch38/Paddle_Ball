from tkinter import *
import random
import time


class Ball:
    def __init__(self, canvas, paddle, score, color):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        #names the ball on the canvas
        self.id = canvas.create_oval(10, 10, 25, 25, fill=color)
        #positions the ball at this location
        self.canvas.move(self.id, 245, 100)

        #sets up the inital movement variables of the ball with a random horizontal start value
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -3

        #Lets the Ball class know the dimensions of the canvas.
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

        #a boolean variable we will change if the ball hits the bottom
        self.hit_bottom = False

    #check to see if the ball hits the paddle
    def hit_paddle(self, pos):
        #position variable contains two coordinate pairs: (x1,y1,x2,y2)
        #coordinates of paddle rectangle: top left then bottom right
        paddle_pos = self.canvas.coords(self.paddle.id)

        #ball's position (pos) compared to the paddle's position (paddle_pos)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                self.x += self.paddle.x
                self.score.hit()
                return True
            return False

    #creating the ball on the screen.
    def draw(self):
        #Move: id of variable, horizontal movement added to intial position, vertical movement
        self.canvas.move(self.id, self.x, self.y)

        #creating a variable called "pos" for the position of the ball
        #pos contains 4 numbers or two coordinate pairs: (x1,y1,x2,y2)
        #coordinates of rectangle enclosing the ball: top left then bottom right
        pos = self.canvas.coords(self.id)

        #check the position of the ball on the canvas
        #checks the y1 value on the top of the ball to see if
        #we hit the top of the canvas
        if pos[1] <= 0:
            self.y = 3
        #checks the y2 value on the bottom of the ball to see if
        #we hit the bottom of the canvas
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        #what happens when you hit the bottom of the canvas window
        if self.hit_paddle(pos) == True:
            self.y = -3
        #check to see if the left-side of the ball hits the edge of the canvas
        if pos[0] <= 0:
            self.x = 3
        #check to see if the right-side of the ball hits the edge of the canvas
        if pos[2] >= self.canvas_width:
            self.x = -3

class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        #names the paddle on the canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color)
        #moves the paddle to this location.
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        #makes sure the paddle knows the edges of the canvas
        self.canvas_width = self.canvas.winfo_width()

        
        #binds the movement of the paddle to the left and right arrows.
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        #the game will start once the left-mouse button is pushed.
        self.started = False
        self.canvas.bind_all('<Button-1>', self.start_game)

    def draw(self):
        #moves the paddle left and right by adding self.x to the intital position
        #note: this means the paddle always moves. 
        self.canvas.move(self.id, self.x, 0)
        #position variable for the paddle
        pos = self.canvas.coords(self.id)
        #If the x1 coord (left-side of paddle) is past the canvas stop the movement 
        if pos[0] <= 0:
            self.x = 0
        #If the x2 coord (right-side of paddle) is past the canvas stop the movement
        elif pos[2] >= self.canvas_width:
            self.x = 0

    #left and right functions
    def turn_left(self, evt):
        #the speed of the paddle, which is less than possible speed of ball
        self.x = -2
    def turn_right(self, evt):
        self.x = 2

    #function starts the game
    def start_game(self, evt):
        self.started = True

class Score:
    def __init__(self, canvas, color):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(450, 10, text=self.score, \
                                     fill=color)
    #if the ball hits the paddle, increse the score by 1
    def hit(self):
        self.score += 1
        self.canvas.itemconfig(self.id, text=self.score)




#Normal tkinter intro.
tk = Tk()
#Title of the game
tk.title("Game")
tk.resizable(0, 0)
#window appears on top
tk.wm_attributes("-topmost", 1)
#dimensions of the canvas
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
#tkinter redraws the canvas--just in case
tk.update()

#creating an object instance of our Score Class
score = Score(canvas, 'green')
#creating an object instance of our Paddle Class
paddle = Paddle(canvas, 'blue')
#creating an object instance of our Ball Class
ball = Ball(canvas, paddle, score, 'red')

#creating a "Game Over" text variable
game_over_text = canvas.create_text(250, 200, text='GAME OVER', \
                                    state='hidden')
def animate():
    #This is our animation loop. It will run until the ball hits the bottom.
    if ball.hit_bottom == False and paddle.started == True:
        #draws the ball
        ball.draw()
        #draws the paddle
        paddle.draw()
        
        #force tkinter to redraw the canvas.
        tk.update_idletasks()
        tk.update()
        #Pause between loop cycles to slow the animation down.
        time.sleep(0.01)
        animate()
        
    #if the ball hits the bottom    
    elif ball.hit_bottom == True:
        #stop the animation by no longer calling ball.draw() and paddle.draw()
        #wait 0.5 seconds and then display the text "Game Over"
        time.sleep(0.5)
        canvas.itemconfig(game_over_text, state='normal')
        response = prompt("Would you like to play again? y/n")
        if response == 'y' or 'Y':
            animate()
        else:                      
            print("See you later.")

    else:
        #force tkinter to redraw the canvas.
        tk.update_idletasks()
        tk.update()
        #Pause between loop cycles to slow the animation down.
        time.sleep(0.01)
        animate()
#This is our animation loop. It will run until the ball hits the bottom.
animate()
