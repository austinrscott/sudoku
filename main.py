import kivy
from kivy.app import App
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from board import Board

kivy.require('1.9.1')


class Cell(Button):
    table = ObjectProperty(None)

    def __init__(self, xy, char, table, **kwargs):
        self.xy = xy
        self.value = char
        super().__init__(**kwargs)
        self.table = table

    def clicked(self):
        self.table.popup(NumPad(target_cell=self))


class NumKey(Button):
    pass


class SpaceKey(NumKey):
    pass


class NumPad(Bubble):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.numgrid = GridLayout(cols=3, spacing=0)

        for i in range(1, 10):
            self.numgrid.add_widget(NumKey(text=str(i)))
        self.add_widget(self.numgrid)
        self.add_widget(SpaceKey(text='_'))


class GridSpace(Widget):
    pass

class Grid(GridLayout):
    table = ObjectProperty(None)

    def __init__(self, **kwargs):
        self.board = Board()
        super().__init__(**kwargs)
        for i, c in enumerate(self.board.cells):
            widget = Cell(self.board.idx_to_xy(i), c, self.table)
            self.add_widget(widget)
        with self.canvas:
            Color(0, 0, 0)
            self.lines_h = [Line() for _ in range(8)]
            self.lines_v = [Line() for _ in range(8)]
        self.redraw()
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *args):
        x, y, top, right, cell_width = self.x, self.y, self.top, self.right, self.width / 9
        for i in range(8):
            cur_width = 1.0 if (i + 1) % 3 else 2.0
            cur_y = y + (i + 1) * cell_width
            self.lines_h[i].points = x, cur_y, right, cur_y
            self.lines_h[i].width = cur_width
            cur_x = x + (i + 1) * cell_width
            self.lines_v[i].points = cur_x, y, cur_x, top
            self.lines_v[i].width = cur_width
        for c in self.children:
            c.font_size = self.width * 0.06

    @staticmethod
    def get_grid_size(table, button_bar_width):
        w, h, orientation = table
        long, short = (w, h) if orientation == 'horizontal' else (h, w)
        if long <= short + button_bar_width:
            mid = long - button_bar_width
            return mid, mid
        else:
            return short, short


class Shade(Button):
    pass


class GameTable(FloatLayout):
    shade = ObjectProperty(Shade())
    orientation = StringProperty('')
    cur_popup = ObjectProperty(None)

    def popup(self, widget, cutout=None, clickaway=None):
        self.add_widget(self.shade)
        self.add_widget(widget)
        self.cur_popup = widget

    def clear_popup(self):
        self.remove_widget(self.cur_popup)
        self.remove_widget(self.shade)
        self.cur_popup = None

class SudokuApp(App):
    def build(self):
        return GameTable()


if __name__ == '__main__':
    SudokuApp().run()
