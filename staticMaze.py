#!/usr/bin/python2.7
# ugly messy reworking of maze.py to separate render and map
from copy import copy
import curses, argparse, time, random
if True:
    parser = argparse.ArgumentParser(
    description = 'A simple maze program, started while learning how to use the curses library.'
    )
    parser.add_argument('-d', '--debug',
    dest = 'debugEnabled',
    action = 'store_true',
    default = False,
    )
    parser.add_argument('-t', '--time',
    dest = 'timeout',
    action = 'store',
    default = 150,
    type = int,
    )
    parser.add_argument('-m', '--map',
    dest = 'mapFile',
    action = 'store',
    default = 'map0',
    )
    parser.add_argument('-s', '--board-scale',
    dest = 'boardScale',
    action = 'store',
    default = '3x2',
    )
    parser.add_argument('-k', '--keys',
    dest = 'keys',
    action = 'store',
    default = 'qwerty',
    )
    args = parser.parse_args()
    bws, bhs = map(int, args.boardScale.split('x'))
    right, left = +1, -1
    
if args.keys in ('q', 'qwerty'):
    binds = {
        'quit'  : 'q',
        'right' : 'd',
        'left'  : 'a',
        'jump'  : 'o',
        'break' : ';',
        'turn'  : 'k',
    }
if args.keys in ('d', 'dvk', 'dvorak'):
    binds = {
        'grab'  : 'c',
        'down'  : 'o',
        'up'    : ',',
        # testing
        'quit'  : '\'',
        'right' : 'e',
        'left'  : 'a',
        'jump'  : 'r',
        'break' : 's',
        'turn'  : 't',
    }
    
class Map():
    def __init__(self):
        self.parseMapFile(args.mapFile)
        self.bw, self.bh, self.bws, self.bhs = map(int, self.info['size'] + [bws, bhs])
        self.loadMap(self.mapString)
        self.loadBoard()
    # preloading
    def parseMapFile(self, mapFile):
        self.info, info = {}, []
        f = open(mapFile, 'r').read()
        for i in f.split('\n::'):
            info.append(i)
        info.pop(len(info)-1) # removing newline at EOF
        self.mapString = info.pop(0)
        # automaticly process remaining lines
        for i in info:
            j = i.split(':')
            k = j.pop(0)
            self.info[k] = j
    # loading
    def loadMap(self, mapString):
        mapRows = mapString.split('\n')
        self.keyMap = [] # 2D list of the map
        for y in range(self.bw): # y is first for a reason
            yRow = []
            self.keyMap.append(yRow)
            for x in range(self.bh):
                yRow.append(list(mapRows[x])[y])
    def loadBoard(self):
        self.board, self.spawn = [], {}
        for x in range(self.bw):
            self.board.append([])
            for y in range(self.bh):
                self.board[x].append(None)
                self.loadTile(x, y, self.keyMap[x][y])
    def loadTile(self, x, y, mapKey):
        self.board[x][y] = Tile(x, y, mapKey)
    def getTile(self, x, y):
        return self.board[x][y]
class Tile():
    def __init__(self, x, y, mapKey = ' '):
        self.mapKey = mapKey
        self.pos = [x, y]
        self.special = []
        if mapKey == ' ':
            self.attr = {
            'name': 'empty',
            'phase': False,
            'icon': ' ',
            }
        elif mapKey == '=':
            self.attr = {
            'name': 'ladder',
            #'phase': self.makePhase(down = True, up = True, left = True, right = True),
            'phase': False,
            'icon': '=',
            }
            self.special.append('sticky')
        elif mapKey == '#':
            self.attr = {
            'name': 'wall',
            'phase': self.makePhase(),
            'icon': '#',
            }
        elif mapKey == 'V':
            self.attr = {
            'name': 'arrow',
            'phase': False,
            'icon': 'V',
            }
        elif mapKey == '<':
            self.attr = {
            'name': 'one_way_left',
            'phase': self.makePhase(right = True), # left->right because movement direction
            'icon': '<'
            }
        elif mapKey == '>':
            self.attr = {
            'name': 'one_way_right',
            'phase': self.makePhase(left = True), # right->left because movement direction
            'icon': '>'
            }
        elif mapKey == 'O':
            self.attr = {
            'name': 'fakeWall',
            'phase': False,
            'icon': '#',
            }
        elif mapKey in ('+', '-', '|'):
            self.attr = {
            'name': 'border',
            'phase': self.makePhase(),
            'icon': mapKey,
            }
        else: # to catch any undefined characters in mapFile
            self.attr = {
            'name': 'unassigned',
            'phase': self.makePhase(),
            'icon': mapKey,
            }
        if not self.attr['phase']:
            self.attr['phase'] = self.makePhase(True, True, True, True)
    def makePhase(self, left = False, right = False, down = False, up = False):
        return {
            0: { +1: left, -1: right },
            1: { +1: down, -1: up    },
        }
    def getPhase(self, direction):
        return self.attr['phase'][direction[0]][direction[1]]
class Screen():
    def __init__(self):
        # curses
        self.curses = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        # window
        for i in Map.bw, Map.bh, Map.bws, Map.bhs:
            print(i)
        self.game   = curses.newwin(Map.bh * Map.bhs, Map.bw * Map.bws)
        self.msgBox = curses.newwin(5, Map.bw * Map.bws, Map.bh * Map.bhs, 0) # 5 is msgBox height
        self.timeout = args.timeout
        self.game.timeout(self.timeout)
        for x in range(Map.bw):
            for y in range(Map.bh):
                self.update(x, y)
        # entities
        self.entityList = []
        self.Player = Entity(map(int, Map.info['spawn']), 'X', '@')
        self.entityList.append(self.Player)
    def renderEntity(self, entity):
        icon, head, bearing = entity.icon, entity.head, entity.bearing
        entityString = entity.eyeCon
        if entity.bearing == -1:
            entityString = entityString[::-1]
        for h in range(Map.bhs):
            self.game.addstr(entity.pos[1] * Map.bhs + h, entity.pos[0] * Map.bws, entityString)
    def render(self, icon, x, y):
        for h in range(Map.bhs): # [h]eight
            self.game.hline(y * Map.bhs + h, x * Map.bws, icon, Map.bws)
        self.game.refresh()
    def update(self, x, y):
        self.render(Map.getTile(x, y).attr['icon'], x, y)
    def keyInput(self, action = 'move'):
        key = self.game.getch()
        for i in binds:
            if key == ord(binds[i]):
                key = i
        if key == 'quit':
            curses.endwin()
            exit()
        if key == 'right':
            self.Player.move([0, right])
        if key == 'left':
            self.Player.move([0, left])
        if key == 'down':
                self.Player.move([1, +1])
        if key == 'jump':
            self.Player.state['jump'] = False
            self.Player.lastPos = copy(self.Player.pos)
            if self.Player.isStable():
                self.Player.state['jump'] = True
                self.Player.move([1, -1])
                self.Player.move([1, -1])
        self.Player.action(key) # run other actions, BEFORE FALL
        for entity in self.entityList: # !!! execute this on all entities
            if entity == self.Player:
                if key in ('jump', 'down', 'up'): # list of NO_FALL
                    if not entity.state['jump']: # if already jumped, drop anyway
                        entity.drop()
                else: entity.drop()
            else: entity.drop()
            self.renderEntity(entity)
        if args.debugEnabled: # debug stuff
            self.msgBox.hline(0, 0, ' ', Map.bw * Map.bws) 
            self.msgBox.addstr('{}: {} {}'.format(self.Player.pos, self.Player.bearing, action))
            self.msgBox.hline(1, 0, ' ', Map.bw * Map.bws) 
            self.msgBox.addstr(1, 0, str(self.Player.state['grab']))
            self.msgBox.refresh()
class Entity():
    def __init__(self, pos, icon, head): # pos must be list, not tuple
        self.pos, self.icon, self.head = pos, icon, head
        self.bearing = right
        self.eyeCon = self.icon * (Map.bws - 1) + self.head
        self.state = {'grav': True, 'grab': False}
    def slide(self, direction):
        newPos = copy(self.pos)
        newPos[direction[0]] += direction[1]
        destTile = Map.getTile(*newPos)
        return destTile
    def isStable(self):
        return not self.slide([1, +1]).getPhase([1, +1]) or ('sticky' in self.slide([0, 0]).special and self.state['grab'])
    def drop(self):
        if not ('sticky' in self.slide([0, 0]).special and self.state['grab']):
            self.move([1, +1])
    def move(self, direction):
        if direction[0] == 0: self.bearing = direction[1] # set bearing if needed
        oldPos = self.pos # new variable oldPos
        newPos = self.slide(direction).pos # new variable newPos
        destTile = self.slide(direction)
        if destTile.getPhase(direction):
            self.pos = newPos # moving entity to newPos
            if not oldPos == newPos: Screen.update(*oldPos) # updating oldPos tile if needed
    def action(self, action):
        pos = copy(self.pos)
        pos[0] += self.bearing
        if action == 'break':
            Map.loadTile(pos[0], pos[1], ' ')
            Screen.update(*pos)
        if action == 'turn':
            self.bearing = -1 * self.bearing
            Screen.renderEntity(self)
        if action == 'grab':
            self.state['grab'] = not self.state['grab']
#
Map = Map()
print(Map.info)
try:
    Screen = Screen()
    Screen.renderEntity(Screen.Player)
    while True:
        Screen.keyInput()
finally:
    curses.endwin()
