import time
from turtle import Turtle, Screen
import random

SCREEN_WIDTH = 550
SCREEN_HEIGHT = 700
START_BALL_SPEED = 2
SPEED_ACCELERATION = 1

class Game_board(Turtle):
    def __init__(self):
        super(Game_board).__init__()
        self.board_limiters_coordinates = {
            'up_coord': {'x': 0, 'y': 340, 'size_list':[0.5,26,1]},
            'down_coord': {'x': 0, 'y': -340, 'size_list':[0.5,26,1]},
            'left_coord': {'x': -255, 'y': 0, 'size_list':[33,0.5,1]},
            'right_coord': {'x': 255, 'y': 0, 'size_list':[33,0.5,1]},
        }
        self.board_limiters_list=[]

    def put_board_limiters(self):
        for limiter_coord in self.board_limiters_coordinates:
            x = self.put_limiter(x_cor=self.board_limiters_coordinates[limiter_coord]['x'],
                                 y_cor=self.board_limiters_coordinates[limiter_coord]['y'],
                                 size_list=self.board_limiters_coordinates[limiter_coord]['size_list'])
            self.board_limiters_list.append(x)

    def put_limiter(self, x_cor, y_cor, size_list:list):
        x = Turtle()
        x.hideturtle()
        x.penup()
        x.color('white')
        x.shape('square')
        x.shapesize(size_list[0],size_list[1], size_list[2])
        x.setposition(x=x_cor,y=y_cor)
        x.showturtle()
        return x

class Game_Bricks(Turtle):
    def __init__(self):
        super(Game_Bricks).__init__()
        self.row_characteristics = {
            1:
                {'color': 'yellow',
                'points': 1},
            2:
                {'color': 'yellow',
                'points': 1},
            3:
                {'color': 'green',
                'points': 3},
            4:
                {'color': 'green',
                 'points': 3},
            5:
                {'color': 'orange',
                 'points': 5},
            6:
                {'color': 'orange',
                 'points': 5},
            7:
                {'color': 'red',
                 'points': 7},
            8:
                {'color': 'red',
                 'points': 7},
        }
        self.coordinates = {
            "x": [-210, -140, -70, 0, 70, 140, 210],
            'y': {1: 140, 2: 160, 3: 180, 4: 200, 5: 220, 6: 240, 7: 260, 8: 280}
            }
        self.all_bricks_list = []

    def put_game_brick_on_table(self, color:str, x_cor, y_cor):
        new_brick = Turtle()
        new_brick.hideturtle()
        new_brick.penup()
        new_brick.color(color)
        new_brick.setposition(x_cor, y_cor)
        new_brick.shape("square")
        new_brick.shapesize(0.5, 3, 1)
        new_brick.showturtle()
        return new_brick

    def put_all_bricks_on_board(self):
        for y_pos in self.coordinates['y']:
            color = self.row_characteristics[y_pos]['color']
            y_coordinate  = self.coordinates['y'][y_pos]
            for x_pos in self.coordinates['x']:
                x_coordinate = x_pos
                self.all_bricks_list.append(self.put_game_brick_on_table(color, y_cor=y_coordinate,x_cor=x_coordinate))
        print(self.all_bricks_list)

    def destroy_brick(self,brick_obj:Turtle):
        self.all_bricks_list.remove(brick_obj)
        brick_obj.reset()

class Game_paddle():
    def __init__(self):
        super(Game_paddle).__init__()
        self.initial_coordinates = {'x': 0, 'y': -300}
        self.max_x = SCREEN_WIDTH/2 - 50
        self.object = None
        self.paddle_speed = 10

    def put_paddle_on_board(self):
        x = Turtle()
        x.hideturtle()
        x.penup()
        x.shape('square')
        x.shapesize(0.5, 3, 0)
        x.color('white')
        x.heading()
        x.setposition(x=self.initial_coordinates['x'], y=self.initial_coordinates['y'])
        x.showturtle()
        self.object=x
        self.move_paddle_on_key()

    def move_paddle_left(self):
        x = self.object.xcor()
        y = self.object.ycor()
        if -self.max_x < x:
            new_x = x - self.paddle_speed
        else:
            new_x = x
        self.object.goto(x=new_x, y=y)

    def move_paddle_right(self):
        x = self.object.xcor()
        y = self.object.ycor()
        if x < self.max_x:
            new_x = x + self.paddle_speed
        else:
            new_x = x
        self.object.goto(x=new_x, y=y)

    def move_paddle_on_key(self):
        self.object.screen.onkeypress(self.move_paddle_left,"Left")
        self.object.screen.onkeypress(self.move_paddle_right, "Right")
        self.object.screen.listen()

    # def change_size_on_first_ball_to_wall(self):
#         Half SIZE!
class Game_ball(Turtle):
    def __init__(self,):
        super(Game_ball).__init__()
        self.initial_coordinates = {'x': 0, 'y': -290}
        self.object=None
        self.initial_heading_list = [70, 80, 100, 110]
        self.paddle_obj = None
        self.brick_list_objs = []
        self.change_of_angle = 0
        self.brick_to_destroy = None
        self.nr_of_hits_paddle = 0
        self.ball_speed = START_BALL_SPEED
        self.paddle_size_corection = 0

    def put_ball_on_board(self,paddle_obj_imported:Turtle, brick_list:list):
        x = Turtle()
        x.hideturtle()
        x.penup()
        x.shape('circle')
        x.shapesize(0.5,)
        x.color('white')
        x.setheading(random.choice(self.initial_heading_list))
        x.setposition(x=self.initial_coordinates['x'], y=self.initial_coordinates['y'])
        x.speed(10)
        x.showturtle()
        self.paddle_obj = paddle_obj_imported
        self.object = x

    def put_ball_in_center(self):
        self.object.setposition(x=self.initial_coordinates['x'], y=self.initial_coordinates['y'])
        self.object.setheading(random.choice(self.initial_heading_list))

    def ball_move(self):
        self.object.forward(self.ball_speed)
        self.monitor_ball_position_to_walls_paddle()

    def ball_refract_from_up_down (self,):
        new_heading = 360 - self.object.heading() + self.change_of_angle
        self.object.setheading(new_heading)
        self.change_of_angle = 0


    def ball_refract_from_wall (self,):
        new_heading = 180 + 360 - self.object.heading() + self.change_of_angle
        self.object.setheading(new_heading)
        self.change_of_angle = 0

    def ball_hits_up(self):
        if self.object.ycor() >= 330:
            return True

    def ball_hits_paddle(self):
        if self.object.ycor() <= -290:
            if self.paddle_obj.xcor() - 35 + self.paddle_size_corection <= self.object.xcor() <= self.paddle_obj.xcor() + 35 - self.paddle_size_corection:
                self.nr_of_hits_paddle += 1
                # print(self.ball_speed)
                return True


    def get_angle_change_on_impact_to_paddle(self):
        angles=[-20, -10,-5, 5, 10, 20]
        if self.paddle_obj.xcor() - 30 <= self.object.xcor() <= self.paddle_obj.xcor() - 10:
            self.change_of_angle += random.choice(angles)
        elif self.paddle_obj.xcor() + 10 <= self.object.xcor() <= self.paddle_obj.xcor() + 30:
            self.change_of_angle += random.choice(angles)

    def ball_hits_the_wall(self):
        if self.object.xcor() >= 245 or self.object.xcor() <= -245:
            return True

    def monitor_ball_position_to_walls_paddle(self):
        if self.ball_hits_up():
            self.ball_refract_from_up_down()
        elif self.ball_hits_paddle():
            self.get_angle_change_on_impact_to_paddle()
            self.ball_refract_from_up_down()
        elif self.ball_hits_the_wall():
            self.ball_refract_from_wall()

class Game_score(Turtle):
    def __init__(self):
        super(Game_score).__init__()
        self.initial_coordinates = {'x': 0, 'y': 300}
        self.object=None
        self.score = 0

    def put_score_on_board(self):
        x = Turtle()
        x.hideturtle()
        x.penup()
        x.color('white')
        x.setposition(x=self.initial_coordinates['x'], y=self.initial_coordinates['y'])
        x.write(self.score, align='center', font=('Arial',20,'bold'))
        self.object = x

    def update_score_board(self,):
        self.object.clear()
        self.object.write(self.score, align='center', font=('Arial',20,'bold'))

class Game_writer(Turtle):
    def __init__(self):
        super(Game_writer).__init__()
        self.initial_coordinates = {'x': 0, 'y': 0}
        self.object=None

    def put_writer(self):
        x = Turtle()
        x.hideturtle()
        x.penup()
        x.color('white')
        x.setposition(x=self.initial_coordinates['x'], y=self.initial_coordinates['y'])
        x.write('Ready?', align='center', font=('Arial',30,'bold'))
        self.object = x

    def write_something_center(self, text_to_write:str):
        self.object.clear()
        self.object.hideturtle()
        self.object.write(text_to_write, align='center', font=('Arial',20,'bold'))

class Game_play(Turtle):
    def __init__(self):
        super(Game_play).__init__()
        self.bricks = Game_Bricks()
        self.paddle = Game_paddle()
        self.score_obj = Game_score()
        self.writer = Game_writer()
        self.ball = Game_ball()
        self.walls = Game_board()
        self.screen = Screen()
        self.game_on = True
        self.color_of_brick = None
        self.lives = 3
        self.nr_of_hits_paddle = 0
        self.change_speed_red_brick_hit_nr = 1
        self.change_speed_orange_brick_hit_nr = 1
        self.red_brick_hitted = False
        self.orange_brick_hitted = False
        self.change_of_paddle_size_nr = 1


    def screen_setup(self):
        # Screen setup:
        self.screen.title("Brickout Game")
        self.screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.screen.bgcolor("black")
        self.screen.tracer(0)

    def board_initial_set_up(self):
        # Game Board setup
        self.walls.put_board_limiters()
        self.screen.update()
        time.sleep(0.5)
        self.score_obj.put_score_on_board()
        self.screen.update()
        time.sleep(0.5)
        self.bricks.put_all_bricks_on_board()
        self.screen.update()
        time.sleep(0.5)
        self.paddle.put_paddle_on_board()
        self.ball.put_ball_on_board(self.paddle.object,self.bricks.all_bricks_list)
        self.screen.update()
        time.sleep(0.5)
        self.writer.put_writer()
        self.writer.write_something_center("Ready?")
        self.screen.update()
        time.sleep(1.5)
        self.writer.write_something_center("GO!")
        self.screen.update()
        time.sleep(2)
        self.writer.write_something_center("")
        self.screen.update()

    def update_score(self, color):
        if color == "yellow":
            self.score_obj.score +=1
        elif color == "green":
            self.score_obj.score += 3
        elif color == "orange":
            self.score_obj.score += 5
        elif color == "red":
            self.score_obj.score += 7
        self.score_obj.update_score_board()

    def ball_hits_brick(self):
        if 140-10 <= self.ball.object.ycor() <= 280 +10:
            for brick in self.bricks.all_bricks_list:
                if brick.ycor()-10 <= self.ball.object.ycor() <= brick.ycor()+10:
                    if brick.xcor()-35 <= self.ball.object.xcor() <= brick.xcor()+35:
                        self.ball.ball_refract_from_up_down()
                        self.update_score(brick.color()[0])
                        if brick.color()[0] == "red" and self.change_speed_red_brick_hit_nr > 0:
                                self.red_brick_hitted = True
                                self.change_speed_red_brick_hit_nr -=1
                        if brick.color()[0] == "orange" and self.change_speed_orange_brick_hit_nr > 0:
                                self.orange_brick_hitted = True
                                self.change_speed_orange_brick_hit_nr -=1
                        self.bricks.destroy_brick(brick)


    def check_if_game_on(self):
    #     ball is under the paddle
        if len(self.bricks.all_bricks_list) == 0:
            self.game_on = False
            self.writer.write_something_center(f"YOU WON! \nYour total score is {self.score_obj.score}")
            self.screen.update()
            answer = self.screen.textinput("Do you want to play again?", "Y - for YES, N - for NO")
            if answer.lower() == "y":
                self.reset_all()
                self.game_on = True
                self.new_game()
            else:
                self.writer.write_something_center("Thank you for playing!")

        else:
            if self.ball.object.ycor() < -300:
                self.lives -= 1
                if self.lives > 0:
                    self.game_on = False
                    self.writer.write_something_center(f"You have {self.lives} more")
                    self.screen.update()
                    self.ball.put_ball_in_center()
                    time.sleep(1)
                    self.writer.write_something_center("GO!")
                    self.screen.update()
                    time.sleep(1)
                    self.writer.object.clear()
                    self.screen.update()
                    self.game_on = True

                else:
                    self.game_on = False
                    self.writer.write_something_center(f"YOU LOST! \nYour total score is {self.score_obj.score}")
                    self.screen.update()
                    answer = self.screen.textinput("Do you want to play again?", "Y - for YES, N - for NO")
                    if answer.lower() == "y":
                        self.reset_all()
                        self.game_on = True
                        self.new_game()
                    else:
                        self.writer.write_something_center("Thank you for playing!")

    def reset_all(self):
        for brick in self.bricks.all_bricks_list:
            brick.reset()
        self.bricks.all_bricks_list = []
        self.color_of_brick = None
        self.score_obj.score = 0
        self.ball.ball_speed = 1
        self.ball.nr_of_hits_paddle = 0
        self.change_speed_orange_brick_hit_nr = 1
        self.change_speed_red_brick_hit_nr = 1
        self.lives = 3
        self.ball.paddle_size_corection = 0
        self.change_of_paddle_size_nr = 1
        self.ball.object.reset()
        self.paddle.object.reset()
        self.screen.clear()


    def game_play(self):
        while self.game_on:
            self.ball.ball_move()
            self.paddle.move_paddle_on_key()
            self.ball_hits_brick()
            self.check_if_game_on()
            self.speed_monitor()
            self.screen.update()

    def new_game(self):
        self.screen_setup()
        self.board_initial_set_up()
        self.score_obj.score = 0

        # Game play
        # self.screen.tracer(n=0)
        self.game_play()

        self.screen.mainloop()


    def speed_monitor(self):
        if self.red_brick_hitted == True:
            self.ball.ball_speed += SPEED_ACCELERATION
            self.ball.object.speed(self.ball.ball_speed)
            self.red_brick_hitted = False
            # self.screen.tracer(self.ball.ball_speed)
            print('RED!!!')
            print(self.ball.ball_speed)
        elif self.orange_brick_hitted == True:
            self.ball.ball_speed += SPEED_ACCELERATION
            self.ball.object.speed(self.ball.ball_speed)
            self.orange_brick_hitted = False

            # self.screen.tracer(self.ball.ball_speed)
            print('ORANGE!!!')
            print(self.ball.ball_speed)
        elif self.ball.nr_of_hits_paddle == 4:
            self.ball.ball_speed += SPEED_ACCELERATION
            self.ball.nr_of_hits_paddle += 1
            self.ball.object.speed(self.ball.ball_speed)

            # self.screen.tracer(self.ball.ball_speed)
            print(self.ball.ball_speed)
            print("4 hits paddle")
            print(self.ball.object.speed())

        elif self.ball.nr_of_hits_paddle == 13:
            self.ball.ball_speed += SPEED_ACCELERATION
            self.ball.nr_of_hits_paddle += 1
            self.ball.object.speed(self.ball.ball_speed)

            # self.screen.tracer(self.ball.ball_speed)
            print("12 hits paddle")
            print(self.ball.ball_speed)
            print(self.ball.object.speed())
        elif self.ball.ball_hits_up() and self.change_of_paddle_size_nr >0:
            self.ball.paddle_size_corection = 15
            self.paddle.object.shapesize(0.5, 3-(self.ball.paddle_size_corection/20), 0)
            self.change_of_paddle_size_nr -=1
            print("CHANGED PADDLE")