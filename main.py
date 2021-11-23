from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from functools import partial
from random import randint, randrange
from models import *

WIDTH = Window.size[0] / 100
HEIGHT = Window.size[1] / 100
FPS = 0.01
VELOCITY = 1000


class BackGround(Widget):
    def __init__(self, **kwargs):
        super(BackGround, self).__init__(**kwargs)
        self.rect = Image(source='graphics/road_mountain_summer/background.png', size=self.size, pos=self.pos,
                          allow_stretch=True, keep_ratio=False)
        self.bg_rect = Image(source='graphics/road_mountain_summer/road.zip', anim_delay=VELOCITY / 1000 - 0.95,
                             size=self.size, pos=self.pos, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.rect)
        self.add_widget(self.bg_rect)


class GameScreen(Screen):
    def __init__(self, to_lose, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.score = 0
        self.car = Car(pos=(WIDTH * 50, HEIGHT * 5), size_hint=(0.1, 0.17))
        self.main_layout = FloatLayout(size_hint=(1, 1))
        self.start_size = (0.1, 0.1)
        self.offset = [WIDTH * 28.76, 0, WIDTH * -28.76]
        self.offset_objects = [WIDTH * 43, WIDTH * -43]
        self.start_coord = [(WIDTH * 42, HEIGHT * 62.22), (WIDTH * 50, HEIGHT * 62.22),
                            (WIDTH * 58, HEIGHT * 62.22)]  # координаты стратовой позиции препятсвий
        self.start_coord_objects = [(WIDTH * 28, HEIGHT * 62.22), (WIDTH * 72, HEIGHT * 62.22)]
        self.main_layout.add_widget(BackGround(pos=(0, 0), size=(WIDTH * 100, HEIGHT * 100)))
        self.to_lose = to_lose
        self.main_layout.add_widget(self.car)
        btn_left = Button(size_hint=(0.5, 1), pos=(WIDTH * 0, HEIGHT * 0),
                          background_color=(0, 0, 0, 0), on_press=self.on_press_l)
        btn_left.bind(state=self.move_to_left_state)
        btn_right = Button(size_hint=(0.5, 1), pos=(WIDTH * 50, HEIGHT * 0),
                           background_color=(0, 0, 0, 0), on_press=self.on_press_r)
        btn_right.bind(state=self.move_to_right_state)
        self.main_layout.add_widget(btn_left)
        self.main_layout.add_widget(btn_right)
        self.score_label = Label(text=str(self.score), size_hint=(0.2, 0.2), pos=(WIDTH * 40, HEIGHT * 80))
        self.main_layout.add_widget(self.score_label)
        self.add_widget(self.main_layout)

    def build(self):
        global VELOCITY
        self.score = 0
        VELOCITY = 1000  # переменная отвечающая за скорость движения
        self.obstructions = []
        self.obstructions.append(Cow(pos=self.start_coord[0],
                                     size_hint=self.start_size))
        self.obstructions.append(Tractor(pos=self.start_coord[0],
                                         size_hint=self.start_size))
        self.spawner()
        self.spawner_bckgd_objects()
        Clock.schedule_interval(self.collision, FPS)
        self.acc_fun = Clock.schedule_interval(self.acceleration, FPS)
        self.score_label.text = str(self.score)

    def collision(self, *args):
        for obs in self.obstructions:
            if self.car.collide_widget(obs):
                print('game over')
                for obs1 in self.obstructions:
                    self.main_layout.remove_widget(obs1)
                for obj in self.bckgd_objects:
                    self.main_layout.remove_widget(obj)
                for obj in self.right_bckgd_objects:
                    self.main_layout.remove_widget(obj)
                for fun in self.moves:
                    fun.cancel()
                self.acc_fun.cancel()
                self.to_lose()
                return False
        pass

    # Далее блок функций отвечающий за перемещения игрока

    def on_press_r(self, instance):
        self.func_r = Clock.schedule_interval(self.move_to_right, FPS)
        self.car.rect.source = 'graphics/car0_right.png'

    def on_press_l(self, instance):
        self.func_l = Clock.schedule_interval(self.move_to_left, FPS)
        self.car.rect.source = 'graphics/car0_left.png'

    def move_to_right_state(self, instance, state):
        if not state is 'down':
            self.func_r.cancel()
            self.car.rect.source = 'graphics/car0.png'

    def move_to_left_state(self, instance, state):
        if not state is 'down':
            self.func_l.cancel()
            self.car.rect.source = 'graphics/car0.png'

    def move_to_right(self, value):
        if self.car.pos[0] >= 80 * WIDTH:
            return False
        self.car.pos[0] += WIDTH
        self.car.pos[1] += 0
        self.car.size_hint[0] += 0
        self.car.size_hint[1] += 0


    def move_to_left(self, value):
        if self.car.pos[0] <= 10 * WIDTH:
            return False
        self.car.pos[0] -= WIDTH
        self.car.pos[1] -= 0
        self.car.size_hint[0] += 0
        self.car.size_hint[1] += 0


    # Далее блок функций отвечающих за спавн и перемещение препятсвий

    def spawner(self, *args):
        """функция управляет спавном и движением препятсвий"""
        Clock.schedule_once(self.spawn)
        self.moves = []
        for obs in self.obstructions:
            self.moves.append(Clock.schedule_interval(partial(self.move, obs), FPS))

    def spawn(self, *args):
        """стартовый спавн препятсвий"""
        for obs in self.obstructions:
            self.main_layout.add_widget(obs)

    def move(self, obstruction, *args):
        """движение препятвий"""
        if obstruction.pos[1] <= - (HEIGHT * randrange(30, 100, 3)):  # Костыль
            obstruction.num_way = randint(0, 2)
            obstruction.pos = self.start_coord[obstruction.num_way]
            print(obstruction.pos[0])
            obstruction.pos[0] += randrange(-4, 4, 1) * WIDTH
            print(obstruction.pos[0])
            obstruction.size_hint = self.start_size
        obstruction.pos[1] -= HEIGHT * 70.22 / VELOCITY
        obstruction.pos[0] -= self.offset[obstruction.num_way] / VELOCITY
        obstruction.size_hint[0] += 0.1 / VELOCITY
        obstruction.size_hint[1] += 0.1 / VELOCITY
        obstruction.pos[0] -= WIDTH * 5 / VELOCITY
        obstruction.pos[1] -= HEIGHT * 5 / VELOCITY

    def spawner_bckgd_objects(self, *args):
        self.bckgd_objects = []
        self.right_bckgd_objects = []
        x = 0
        for _ in range(4):
            self.bckgd_objects.append(BackgroundObjects(size_hint=(0.1, 0.1), pos=self.start_coord_objects[0]))
        for obj in self.bckgd_objects:
            Clock.schedule_once(partial(self.spawn_bckgd_objects, obj), x)
            Clock.schedule_once(partial(self.move_bckgd_objects, obj), x)
            x += 4

    def spawn_bckgd_objects(self, obj, *args):
        self.main_layout.add_widget(obj)

    def move_bckgd_objects(self, obj, *args):
        self.moves.append(Clock.schedule_interval(partial(self.move_objects, obj), FPS))

    def move_objects(self, obstruction, *args):
        if obstruction.pos[1] <= - (HEIGHT * 20):
            obstruction.num_way = randint(0, 1)
            obstruction.num_sprite = randint(0, 2)
            if obstruction.num_sprite == 1:
                obstruction.rect.source = 'graphics/road_mountain_summer/tree.png'
            elif obstruction.num_sprite == 2:
                obstruction.rect.source = 'graphics/road_mountain_summer/tree1.png'
            else:
                obstruction.rect.source = 'graphics/road_mountain_summer/bush.png'
            obstruction.pos = self.start_coord_objects[obstruction.num_way]
            obstruction.pos[0] += randrange(-4, 4, 1) * WIDTH
            obstruction.size_hint = self.start_size
            self.score += 1
            self.score_label.text = str(self.score)
        obstruction.pos[1] -= HEIGHT * 70.22 / VELOCITY
        obstruction.pos[0] -= self.offset_objects[obstruction.num_way] / VELOCITY
        obstruction.size_hint[0] += 0.1 / VELOCITY
        obstruction.size_hint[1] += 0.1 / VELOCITY
        obstruction.pos[0] -= WIDTH * 5 / VELOCITY
        obstruction.pos[1] -= HEIGHT * 5 / VELOCITY

    def acceleration(self, *args):
        global VELOCITY
        acc = 1.0003  # Подобрать подходящее значение
        VELOCITY /= acc


class MainScreen(Screen):
    def __init__(self, to_game, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        main_layout = FloatLayout()
        main_layout.add_widget(Button(text='play', size_hint=(.2, .2), pos_hint={'x': .4, 'y': .4}, on_press=to_game))
        self.add_widget(main_layout)


class LoseScreen(Screen):
    def __init__(self, to_main, **kwargs):
        super(LoseScreen, self).__init__(**kwargs)
        main_layout = FloatLayout()
        main_layout.add_widget(Button(text='ok', size_hint=(.2, .2), pos_hint={'x': .4, 'y': .4}, on_press=to_main))
        self.add_widget(main_layout)


class MySM(ScreenManager):
    def __init__(self, **kwargs):
        super(MySM, self).__init__(**kwargs)
        self.game_screen = GameScreen(name='game_screen', to_lose=self.go_to_lose)
        self.add_widget(MainScreen(name='main_screen', to_game=self.go_to_game))
        self.add_widget(self.game_screen)
        self.add_widget(LoseScreen(name='lose_menu', to_main=self.go_to_main))

    def go_to_game(self, *args):
        self.current = 'game_screen'
        self.game_screen.build()

    def go_to_main(self, *args):
        self.current = 'main_screen'

    def go_to_lose(self, *args):
        self.current = 'lose_menu'


class GameApp(App):
    def build(self):
        return MySM()


if __name__ == "__main__":
    GameApp().run()
