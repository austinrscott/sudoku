import kivy
from kivy.app import App
from kivy.uix.label import Label

from board import Board

kivy.require('1.9.1')


class SudokuApp(App):
    def build(self):
        return Label(text="Testing")


if __name__ == '__main__':
    board = Board('123456789789123456456789123912345678678912345345678912891234567567891234234567891')
    SudokuApp().run()
