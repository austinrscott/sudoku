from functools import partial
from random import shuffle

import kivy
from kivy.app import App
from kivy.factory import Factory
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Line
from kivy.properties import ObjectProperty, StringProperty, DictProperty, Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.bubble import Bubble
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget

from board import Board
from solve import solve_one

kivy.require('1.9.1')


class NumPadKey(Button):
    value = StringProperty('')

    def __init__(self, value, **kwargs):
        self.text = value
        self.value = value
        super(NumPadKey, self).__init__(**kwargs)


class SpaceKey(NumPadKey):
    def __init__(self, **kwargs):
        super(SpaceKey, self).__init__(value='0', text='', **kwargs)


class NumPad(Bubble):
    cur_cell = ObjectProperty(None)
    last_press = StringProperty('')

    def __init__(self, init_cell, **kwargs):
        super(NumPad, self).__init__(**kwargs)
        self.numgrid = GridLayout(cols=3, spacing=0)
        init_cell.bind(size=self._resize)

        for i in range(1, 10):
            numpadkey = Factory.NumPadKey(value=str(i))
            numpadkey.bind(on_press=partial(self._pressed, numpadkey))
            self.numgrid.add_widget(numpadkey)
        self.add_widget(self.numgrid)

        spacekey = SpaceKey()
        spacekey.bind(on_press=partial(self._pressed, spacekey))
        self.add_widget(spacekey)

    def _resize(self, instance, new_size):
        w, h = new_size
        self.size = (w * 3, h * 4)

    def focus(self, cell):
        self.cur_cell = cell
        x, y = cell.xy

        # NOTE: Sudoku board is (0,0) in the top-left but Kivy is (0,0) in the bottom-right. Inverted Y axis
        cell_h_align = cell.x if x >= 4 else cell.right
        cell_v_align = cell.y if y >= 4 else cell.top
        np_arrow_pos = '{}_{}'.format('right' if x >= 4 else 'left', 'bottom' if y >= 4 else 'top')

        if x >= 4:
            self.right = cell_h_align
        else:
            self.x = cell_h_align

        if y >= 4:
            self.y = cell_v_align
        else:
            self.top = cell_v_align

        self.arrow_pos = np_arrow_pos

    def _pressed(self, key, *args, **kwargs):
        self.last_press = key.value
        if self.cur_cell:
            self.cur_cell.value = key.value


class Shade(ButtonBehavior, Widget):
    pass


class GameTable(FloatLayout):
    orientation = StringProperty('')
    numpad = ObjectProperty(None)
    shade = ObjectProperty(None)
    ng_dialog = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(GameTable, self).__init__(**kwargs)
        self.shade = Factory.Shade()
        for cell in self.ids.grid.children:
            cell.bind(on_press=self.numpad_popup)
        self.numpad = Factory.NumPad(self.ids.grid.children[0])
        self.numpad.bind(last_press=self.numpad_close)
        self.remove_widget(self.ng_dialog)

    def ng_popup(self, *args, **kwargs):
        self.add_widget(self.shade)
        self.add_widget(self.ng_dialog)
        self.shade.bind(on_press=self.ng_close)

    def ng_close(self, *args, **kwargs):
        self.remove_widget(self.shade)
        self.shade.unbind(on_press=self.ng_close)
        self.remove_widget(self.ng_dialog)

    def numpad_popup(self, cell, *args, **kwargs):
        self.numpad.focus(cell)
        self.add_widget(self.shade)
        self.add_widget(self.numpad)
        self.shade.bind(on_press=self.numpad_close)

    def numpad_close(self, *args, **kwargs):
        self.remove_widget(self.numpad)
        self.shade.unbind(on_press=self.numpad_close)
        self.remove_widget(self.shade)


class GridSpace(Widget):
    pass


class Cell(Button):
    value = StringProperty('')

    def __init__(self, idx, xy, char, **kwargs):
        self.idx = idx
        self.xy = xy
        self.value = char
        super(Cell, self).__init__(**kwargs)


class Grid(GridLayout):
    table = ObjectProperty(None)
    cells = DictProperty({})

    def __init__(self, **kwargs):
        self.board = Board()
        super(Grid, self).__init__(**kwargs)
        for i, c in enumerate(self.board.cells):
            xy = self.board.idx_to_xy(i)
            cell = Factory.Cell(i, xy, c)
            cell.bind(value=self._value_changed)
            self.add_widget(cell)
            self.cells[xy] = cell
        with self.canvas:
            Color(0, 0, 0)
            self.lines_h = [Line() for _ in range(8)]
            self.lines_v = [Line() for _ in range(8)]
        self.redraw()
        self.bind(pos=self.redraw, size=self.redraw)

    def new_board(self):
        self.board = Board()
        for cell in self.cells.values():
            cell.value = '0'

    def generate(self, number_of_blanks):
        print("Generating a board with {} blanks on it.".format(int(number_of_blanks)))
        self.table.ng_close()

        self.new_board()

        solution = solve_one(self.board)
        shuffle(solution)

        for i in range(81 - number_of_blanks):
            xy, value = solution[i]
            Clock.schedule_once(partial(self.fill, xy, value), 2 + 0.05 * i)

    def fill(self, xy, value, *args, **kwargs):
        self.cells[xy].value = value

    def _value_changed(self, cell, new_value):
        self.board[cell.xy] = new_value

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


class SudokuApp(App):
    def build(self):
        game_table = GameTable()
        return game_table


if __name__ == '__main__':
    SudokuApp().run()
