from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty,ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            bounce_factor = (ball.center_y - self.center_y) / (self.height / 2)
            bounced_back = Vector(-1.1 * vx, vy)
            vel = bounced_back * 1.1
            ball.velocity = vel.x, vel.y + bounce_factor


class PongPaddles(Widget):
    score=NumericProperty(0)

    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx,vy=ball.velocity
            bounce_factor=(ball.center_x-self.center_x)/(self.height/2)
            bounced_back=Vector(-1.1*vy,vx)
            vel=bounced_back*1.1
            ball.velocity=vel.y,vel.x+bounce_factor


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player_l = ObjectProperty(None)
    player_r = ObjectProperty(None)
    player_u = ObjectProperty(None)
    player_d = ObjectProperty(None)


    def ball_again(self, vel=(20, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update_function(self, dt):
        self.ball.move()

        self.player_l.bounce_ball(self.ball)
        self.player_r.bounce_ball(self.ball)
        self.player_u.bounce_ball(self.ball)
        self.player_d.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1.05
        if (self.ball.x<self.x)or(self.ball.top>self.top):
            self.ball.velocity_x*=-1.05

        if self.ball.x < self.x:
            self.player_r.score += 1
            self.ball_again(vel=(20, 0))
        if self.ball.x > self.width:
            self.player_l.score += 1
            self.ball_again(vel=(-20, 0))
        if self.ball.y > self.height:
            self.player_d.score += 1
            self.ball_again(vel=(0,-20))
        if self.ball.y < self.y:
            self.player_u.score += 1
            self.ball_again(vel=(0,20))

    def on_touch_move(self, touch):
        if (touch.x<self.player_l.center_x+149)and(touch.x>self.player_l.center_x-149):
            self.player_l.center_y = touch.y
        if (touch.x<self.player_r.center_x+149)and(touch.x>self.player_r.center_x-149):
            self.player_r.center_y = touch.y
        if (touch.y<self.player_u.center_y+266)and(touch.y>self.player_u.center_y-266):
            self.player_u.center_x = touch.x
        if (touch.y<self.player_d.center_y+266)and(touch.y>self.player_d.center_y-266):
            self.player_d.center_x = touch.x


class PongApp(App):
    def build(self):
        game_pong = PongGame()
        game_pong.ball_again()
        Clock.schedule_interval(game_pong.update_function, 1.0 / 100.0)
        return game_pong


if __name__ == "__main__":
    PongApp().run()