#!/usr/bin/python3.5
##
## Tile class
##
class Tile():
    def __init__(self, x, y, map_key = ' '):
        self.pos = [x, y]
        self.map_key = map_key
        try:
            self.attr = self.types(map_key)
        except:
            self.attr = self.types('?')
    def types(self, key):
        if key == ' ': return {
            'name': 'empty',
            'solid': 'never',
            'icon': ' ',
            }
        if key == '?': return {
            'name': 'unknown',
            'solid': 'never',
            'icon': '?',
            }
        if key == '#': return {
            'name': 'wall',
            'solid': 'always',
            'icon': '#',
            }
        if key in ('+', '-', '|'): return {
            'name': 'border',
            'solid': 'always',
            'icon': key,
            }
        if key == '=': return {
            'name': 'ladder',
            'solid': 'never',
            'icon': '=',
            }
        return self.types('?')
