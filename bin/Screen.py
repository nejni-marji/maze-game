#!/usr/bin/python3.5
##
## Screen class
##
import curses
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
    def render(self, icon, x, y):
        for height in range(self.bhs):
            self.game.hline(
                y * self.bhs + height,
                x * self.bws,
                icon, self.bws
                )
        self.game.refresh()
    def update(self, x, y):
        self.render(self.board[x][y].attr['icon'], x, y)
