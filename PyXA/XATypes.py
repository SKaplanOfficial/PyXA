from collections import namedtuple

XAPoint = namedtuple('XAPoint', ['x', 'y'])
"""A named tuple representing an (x, y) coordinate.
"""

XARectangle = namedtuple('XARectangle', ['x', 'y', 'width', 'height'])
"""A named tuple representing a rectangle with an origin point (x, y) and dimensions width x height.
"""

