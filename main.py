from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from jnius import autoclass


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            bounce_factor = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1.1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + bounce_factor


class PongPaddles(Widget):
    score=NumericProperty(0)

    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx,vy=ball.velocity
            bounce_factor=(ball.center_x-self.center_x)/(self.height/2)
            bounced=Vector(-1*vy,vx)
            vel=bounced*1.01
            ball.velocity=vel.y,vel.x+bounce_factor


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)
    player3 = ObjectProperty(None)
    player4 = ObjectProperty(None)


    def serve_ball(self, vel=(20, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)
        self.player3.bounce_ball(self.ball)
        self.player4.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1.05
        if (self.ball.x<self.x)or(self.ball.top>self.top):
            self.ball.velocity_x*=-1.05

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(20, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-20, 0))
        if self.ball.y > self.height:
            self.player4.score += 1
            self.serve_ball(vel=(0,-20))
        if self.ball.y < self.y:
            self.player3.score += 1
            self.serve_ball(vel=(0,20))

    def on_touch_move(self, touch):
        if (touch.x<self.player1.center_x+149)and(touch.x>self.player1.center_x-149):
            self.player1.center_y = touch.y
        if (touch.x<self.player2.center_x+149)and(touch.x>self.player2.center_x-149):
            self.player2.center_y = touch.y
        if (touch.y<self.player3.center_y+266)and(touch.y>self.player3.center_y-266):
            self.player3.center_x = touch.x
        if (touch.y<self.player4.center_y+266)and(touch.y>self.player4.center_y-266):
            self.player4.center_x = touch.x


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 100.0)
        return game


if __name__ == '__main__':
    PongApp().run()