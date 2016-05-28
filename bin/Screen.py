#!/usr/bin/python3.5
##
## Screen class
##
import curses
from bin.Entity import Entity
class Screen():
    def __init__(self, args, Map):
        self.curses = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        self.board = Map.board
        self.bw, self.bh, self.bws, self.bhs = Map.bw, Map.bh, Map.bws, Map.bhs
        self.game    = curses.newwin(   self.bh * self.bhs, self.bw * self.bws   )
        self.msg_box = curses.newwin(7, self.bw * self.bws, self.bh * self.bhs, 0)
        self.timeout      = args.timeout
        self.game.timeout(  args.timeout)
        for x in range(self.bw):
            for y in range(self.bh):
                self.update(x, y)
                self.game.refresh()
        self.parse_key_file('key_maps/{}'.format(args.key_file))
        spawn = list(map(int, Map.data['spawn']))
        self.player = Entity(Map.board, spawn, 'X')
        self.entity_list = [self.player]
    def parse_key_file(self, key_file):
        self.actions, keys = {}, []
        f = open(key_file, 'r').read()
        for i in f.split('\n'): # \n delimits major sections in key_file
            keys.append(i)
        keys.pop(len(keys)-1) # remove newline from EOF
        # process the rest of the key_file
        self.keys = {}
        for i in keys:
            key = i.split(':') # : delimits minor sections in map_file
            action, key = i.split(':') # : delimits minor sections in map_file
            self.actions[action] = key
            self.keys[key] = action
        assert 'quit' in self.actions
    def draw(self, icon, x, y):
        for height in range(self.bhs):
            self.game.hline(
                y * self.bhs + height,
                x * self.bws,
                icon, self.bws
                )
    def update(self, x, y):
        self.draw(self.board[x][y].attr['icon'], x, y)
    def tick(self):
        for i in self.entity_list:
            self.update(*i.old_pos)
            self.draw(i.body, *i.pos)
            self.game.refresh()
