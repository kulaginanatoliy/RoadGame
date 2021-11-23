from kivy.uix.widget import Widget
from kivy.graphics import Rectangle


def redraw(self, *args):
    self.rect.pos = self.pos
    self.rect.size = self.size


class Obstruction(Widget):
    def __init__(self, **kwargs):
        super(Obstruction, self).__init__(**kwargs)
        self.rect = Rectangle(source='graphics\\cow.png', size=self.size, pos=self.pos)
        self.canvas.add(self.rect)
        #self.hit_box = Line(points=hit_box_list, close=True)
        #self.canvas.add(self.hit_box)
        self.bind(pos=redraw, size=redraw)
        self.num_way = 0


class Tractor(Obstruction):
    def __init__(self, **kwargs):
        super(Tractor, self).__init__(**kwargs)
        self.rect.source = 'graphics/tractor.png'


class Cow(Obstruction):
    pass


class Car(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rect = Rectangle(source='graphics/car0.png', size=self.size, pos=self.pos)
        self.canvas.add(self.rect)
        self.bind(pos=redraw, size=redraw)


class BackgroundObjects(Obstruction):
    def __init__(self, **kwargs):
        super(BackgroundObjects, self).__init__(**kwargs)
        self.num_sprite = 1
        if self.num_sprite == 1:
            self.rect.source = 'graphics/road_mountain_summer/tree.png'
        elif self.num_sprite == 2:
            self.rect.source = 'graphics/road_mountain_summer/tree1.png'
        else:
            self.rect.source = 'graphics/road_mountain_summer/bush.png'

