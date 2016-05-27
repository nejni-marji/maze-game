#!/usr/bin/python3.5
##
## Entity class
##
from copy import copy
class Entity():
    def __init__(self, board, pos, body):
        self.old_pos, self.pos, self.body = pos, pos, body
        self.board = board
    def get_tile(self, direction):
        tile_pos = copy(self.pos)
        tile_pos[direction[0]] += direction[1]
        return self.board[tile_pos[0]][tile_pos[1]]
    def move(self, direction):
        dest_tile = self.get_tile(direction)
        new_pos = dest_tile.pos
        if dest_tile.attr['solid'] != 'always':
            self.old_pos = self.pos
            self.pos = new_pos