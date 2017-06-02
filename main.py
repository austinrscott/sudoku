import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from board import Board

kivy.require('1.9.1')


class Cell(Button):
    def __init__(self, board, char, **kwargs):
        self._b = board
        self.value = char
        super().__init__(**kwargs)


class Grid(GridLayout):
    def __init__(self, **kwargs):
        self.board = Board()
        super().__init__(**kwargs)
        for c in self.board.cells:
            self.add_widget(Cell(self.board, c))

    def get_grid_size(self, table, button_bar_width):
        w, h, orientation = table
        long, short = (w, h) if orientation == 'horizontal' else (h, w)
        if long <= short + button_bar_width:
            mid = long - button_bar_width
            return (mid, mid)
        else:
            return (short, short)


class GameTable(BoxLayout):
    pass


class SudokuApp(App):
    def build(self):
        return GameTable()


if __name__ == '__main__':
    SudokuApp().run()
