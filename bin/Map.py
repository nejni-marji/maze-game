#!/usr/bin/python3.5
##
## Map class
##
from bin.Tile import Tile
class Map():
    def __init__(self, args):
        self.parse_map_file(args.map_file)
        self.load_map(self.map_string)
        self.load_board()
    def parse_map_file(self, map_file):
        self.data, data = {}, []
        f = open('map_files/{}'.format(map_file), 'r').read()
        for i in f.split('\n::'): # :: delimits major sections in map_file
            data.append(i)
        data.pop(len(data)-1) # remove newline from EOF
        self.map_string = data.pop(0)
        # process the rest of the map_file
        for i in data:
            value = i.split(':') # : delimits minor sections in map_file
            key = value.pop(0)
            self.data[key] = value
        assert 'size' in self.data and 'spawn' in self.data
        self.bw, self.bh = map(int, self.data['size'])
    def load_map(self, map_string):
        map_rows = map_string.split('\n')
        self.map_keys = [] # 2d list of tile keys
        for y in range(self.bw): ## y is first for a reason
            y_row = []
            self.map_keys.append(y_row)
            for x in range(self.bh):
                y_row.append(list(map_rows[x])[y]) ## this works, apparently
    def load_board(self):
        self.board = []
        for x in range(self.bw):
            self.board.append([])
            for y in range(self.bh):
                self.board[x].append(Tile(x, y, self.map_keys[x][y]))
