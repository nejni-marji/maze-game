#!/usr/bin/python3.5
##
## Entity class
##
from copy import copy
class Entity():
    def __init__(self, Screen, pos, body):
        self.old_pos, self.pos, self.body = pos, pos, body
        self.Screen = Screen
        self.board = Screen.board
    def get_tile(self, axis, direction):
        tile_pos = copy(self.pos)
        tile_pos[axis] += direction
        return self.board[tile_pos[0]][tile_pos[1]]
    def move(self, axis, direction):
        dest_tile = self.get_tile(axis, direction)
        new_pos = dest_tile.pos
        if dest_tile.attr['solid'] != 'always':
            self.old_pos = self.pos
            self.pos = new_pos
            self.Screen.update(*self.old_pos)
            self.Screen.draw(self.body, *self.pos)
