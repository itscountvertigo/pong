"""
Pong by Anbiya Popal, made with the Arcade module. 
Includes a start menu, pause menu and an undefeatable bot.
If it doesnt run, make sure you've installed arcade with 'pip install arcade'
"""

import arcade
import random

FONT = 'symtext2.ttf'

# screen properties
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pong by Anbiya Popal"

# speeds
BALL_SPEED = 8
PLAYER_SPEED = 10
BOT_SPEED = 10

# colors
OFF_WHITE = [230,230,230]
OFF_BLACK = [29,29,29]
GRAY = [80, 80, 80]

# what ball.x needs to be before the bot starts moving. 
# making this higher/lower makes the bot weaker/stronger. higher value means weaker bot.
BOT_ACTIVATION_X = SCREEN_WIDTH / 2 + SCREEN_WIDTH / 5 + 1

class LeftPaddle(): # player, left paddle
    def __init__(self):
        self.x = 20
        self.y = SCREEN_HEIGHT / 2

        self.width = 10
        self.height = SCREEN_HEIGHT / 6

        self.color = OFF_WHITE

        self.move_up = False
        self.move_down = False

    def update(self):
        if self.move_up == True:
            if self.y < SCREEN_HEIGHT - (self.height / 2):
                self.y += PLAYER_SPEED

        if self.move_down == True:
            if self.y > (self.height / 2):
                self.y -= PLAYER_SPEED

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)

class RightPaddle(): # bot, right paddle
    def __init__(self):
        self.x = SCREEN_WIDTH - 20
        self.y = SCREEN_HEIGHT / 2

        self.width = 10
        self.height = SCREEN_HEIGHT / 6

        self.color = OFF_WHITE

    def update(self, ball):
        # the bot will only start moving if the ball is at bot_activation_x
        if self.y > ball.y and ball.delta_x > 0 and ball.x > BOT_ACTIVATION_X:
            self.y -= BOT_SPEED
        
        elif self.y < ball.y and ball.delta_x > 0 and ball.x > BOT_ACTIVATION_X:
            self.y += BOT_SPEED

        # move the bot to screen_height / 2 (half way up the screen)
        elif ball.delta_x < 0:
            if self.y < SCREEN_HEIGHT / 2:
                self.y += BOT_SPEED
            if self.y > SCREEN_HEIGHT / 2:
                self.y -= BOT_SPEED

    def draw(self):
        arcade.draw_rectangle_filled(self.x, self.y, self.width, self.height, self.color)

        # draws red guideline on the bot_activation_x, showing from which point the paddle will start moving
        # arcade.draw_rectangle_filled(BOT_ACTIVATION_X, SCREEN_HEIGHT/2, 2, SCREEN_HEIGHT, arcade.color.RED)

class Ball():
    def __init__(self):
        self.x = SCREEN_WIDTH / 2
        self.y = SCREEN_HEIGHT / 2

        self.delta_x = BALL_SPEED
        self.delta_y = BALL_SPEED

        self.size = 10
        self.color = OFF_WHITE

        self.num_segments = 128

        self.score_left = 0
        self.score_right = 0
    
    def update(self, leftpaddle, rightpaddle):

        # letting the ball bounce against top / bottom
        if self.y >= SCREEN_HEIGHT - self.size or self.y - self.size <= 0:
            self.delta_y = -self.delta_y

        # respawning if ball hits left/right walls
        if self.x >= SCREEN_WIDTH:
            self.x = SCREEN_WIDTH / 2
            self.y = SCREEN_HEIGHT / 2
            self.delta_x = -self.delta_x
            self.score_left += 1

            # experiment: random respawn direction to make it a little more difficult
            if random.choice([True, False]) == True:
                self.delta_y = -self.delta_y

        if self.x <= 0:
            self.x = SCREEN_WIDTH / 2
            self.y = SCREEN_HEIGHT / 2
            self.delta_x = -self.delta_x
            self.score_right += 1

            # random respawn direction
            if random.choice([True, False]) == True:
                self.delta_y = -self.delta_y

        self.x += self.delta_x
        self.y += self.delta_y

        # collisions with paddles
        if self.x <= (leftpaddle.x + (leftpaddle.width / 2) + self.size) and self.y >= leftpaddle.y - (leftpaddle.height / 2)  and self.y <= leftpaddle.y + (leftpaddle.height / 2):
            while self.x <= (leftpaddle.x + (leftpaddle.width / 2) + self.size):
                self.x += 1

            self.delta_x = -self.delta_x

        if self.x >= (rightpaddle.x - (rightpaddle.width / 2) - self.size) and self.y >= rightpaddle.y - (rightpaddle.height / 2) and self.y <= rightpaddle.y + (rightpaddle.height /2):
            while self.x >= (rightpaddle.x - (rightpaddle.width / 2) - self.size):
                self.x -= 1
            
            self.delta_x = -self.delta_x
            

    def draw(self):
        arcade.draw_circle_filled(self.x, self.y, self.size, self.color, self.num_segments)

class Scoreboard():
    def __init__(self):
           pass

    def draw(self, ball):
        # score left
        arcade.draw_text(str(ball.score_left), (SCREEN_WIDTH / 2) - 100, SCREEN_HEIGHT - 75, OFF_WHITE, font_size=40, anchor_x="center", font_name=FONT)

        # score right
        arcade.draw_text(str(ball.score_right), (SCREEN_WIDTH / 2) + 100, SCREEN_HEIGHT - 75, OFF_WHITE, font_size=40, anchor_x="center", font_name=FONT)

class MenuView(arcade.View): # view for the menu
    def on_show(self):
        arcade.set_background_color(OFF_BLACK)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Pong", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, OFF_WHITE, font_size=50, anchor_x="center", font_name=FONT)
        arcade.draw_text("Press space to start.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75, OFF_WHITE, font_size=20, anchor_x="center", font_name=FONT)
        arcade.draw_text("Use W and S for moving up and down.", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-100, OFF_WHITE, font_size=20, anchor_x="center", font_name=FONT)


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            game = GameView()
            self.window.show_view(game)

class GameView(arcade.View): # view for the game
    def __init__(self):
        super().__init__()
        arcade.set_background_color(OFF_BLACK)

        self.ball = Ball()
        self.leftpaddle = LeftPaddle()
        self.rightpaddle = RightPaddle()

        self.scoreboard = Scoreboard()

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(OFF_BLACK)

        self.ball.draw()
        self.leftpaddle.draw()
        self.rightpaddle.draw()

        self.scoreboard.draw(self.ball)

    def on_update(self, delta_time):
        self.leftpaddle.update()
        self.rightpaddle.update(self.ball)

        self.ball.update(self.leftpaddle, self.rightpaddle)

    def on_key_press(self, key, key_modifiers):
        if key == 119:
            self.leftpaddle.move_up = True

        if key == 115:
            self.leftpaddle.move_down = True

        if key == arcade.key.ESCAPE:
            pause = PauseView(self)
            self.window.show_view(pause)

    def on_key_release(self, key, key_modifiers):
        if key == 119 or 115:
            self.leftpaddle.move_up = False
            self.leftpaddle.move_down = False

class PauseView(arcade.View): # view for pause screen. if esc is pressed, this view will show (it renders the gameview too)
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(GRAY)

        self.game_view.ball.draw()
         
        self.game_view.leftpaddle.draw() # render paused leftpaddle
        self.game_view.rightpaddle.draw() # render paused rightpaddle
        self.game_view.scoreboard.draw(self.game_view.ball)

        arcade.draw_text("PAUSED", SCREEN_WIDTH/2, SCREEN_HEIGHT/2, OFF_WHITE, font_size=50, anchor_x="center", font_name=FONT)
        arcade.draw_text("Press Esc. to return", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-30, OFF_WHITE, font_size=20, anchor_x="center", font_name=FONT)
        arcade.draw_text("Press Enter to reset", SCREEN_WIDTH/2, SCREEN_HEIGHT/2-60, OFF_WHITE, font_size=20, anchor_x="center", font_name=FONT)

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.game_view)
        elif key == arcade.key.ENTER:
            game = GameView()
            self.window.show_view(game)

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    window.set_update_rate(1 / 60)
    # game will start out on whichever view you make this. 
    # pick between MenuView() and GameView(), pause doesnt work (it needs a GameView to render)
    start = MenuView()
    window.show_view(start)

    arcade.run()

if __name__ == "__main__":
    main()