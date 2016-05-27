#!/usr/bin/python3.5
##
## Rewriting staticMaze.py from refrence.
##
import argparse, curses
parser = argparse.ArgumentParser()
parser.add_argument(
    '-d', '--debug',
    action = 'store_true',
    default = False,
)
parser.add_argument(
    '-t', '--timeout',
    action = 'store',
    default = 150,
    type = int,
)
parser.add_argument(
    '-m', '--map-file',
    action = 'store',
    default = 'map0',
    type = str,
)
parser.add_argument(
    '--board-scale',
    action = 'store',
    default = '3x2',
    type = str,
)
args = parser.parse_args()

from bin.Map import Map
from bin.Screen import Screen
from bin.Entity import Entity

Map = Map(args)
Map.bws, Map.bhs = list(map(int, args.board_scale.split('x')))
Screen = Screen(args, Map)
spawn = list(map(int, Map.data['spawn']))
player = Entity(Map.board, spawn, 'X')
Screen.player = Screen.start_player(player)
Screen.tick()
Screen.msg_box.getch()
curses.endwin()
