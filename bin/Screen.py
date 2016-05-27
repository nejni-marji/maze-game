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
    def draw(self, icon, x, y):
        for height in range(self.bhs):
            self.game.hline(
                y * self.bhs + height,
                x * self.bws,
                icon, self.bws
                )
    def update(self, x, y):
        self.draw(self.board[x][y].attr['icon'], x, y)
    def start_player(self, player):
        self.entity_list = [player]
        return self.entity_list[0]
    def tick(self):
        for i in self.entity_list:
            self.update(*i.pos)
            self.draw(i.body, *i.pos)
            self.game.refresh()
