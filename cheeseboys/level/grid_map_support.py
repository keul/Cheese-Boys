# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from cheeseboys import cblocals, utils
from cheeseboys.ai.pathfinder import GridMap


class GridMapSupport(object):
    """An object that behave all method for support the usage of a GridMap object and pathfinding features"""

    def __init__(self):
        self.grip_map = None

    def computeGridMap(self):
        """Fill the grid_map attribute with a GridMap instance, to be used in pathfinding
        Call this method after init the level the first time and also when something is changed
        """
        tile_size_x, tile_size_y = cblocals.PATHFINDING_GRID_SIZE
        w, h = self.levelSize
        self.grid_map = GridMap(int(w / tile_size_x), int(h / tile_size_y))
        collideGroups = (self["physical"],)
        for group in collideGroups:
            for sprite in group.sprites():
                self.grid_map.set_blocked_multi(sprite.collide_grid)

    def toGridCoord(self, coord):
        """Transforms a level coordinate to a grid point"""
        tile_size_x, tile_size_y = cblocals.PATHFINDING_GRID_SIZE
        x, y = coord
        x /= tile_size_x
        y /= tile_size_y
        return int(x), int(y)

    def fromGridCoord(self, coord):
        """Transforms a grid coordinate to a level absolute ones"""
        tile_size_x, tile_size_y = cblocals.PATHFINDING_GRID_SIZE
        x, y = coord
        return int(x * tile_size_x + tile_size_x / 2), int(
            y * tile_size_y + tile_size_y / 2
        )

    def drawGridMapSquares(self, surface):
        """Draw on a surface the gridmap areas, for debug purposes"""
        gw, gh = cblocals.PATHFINDING_GRID_SIZE
        w, h = self.levelSize
        transformToScreenCoordinate = self.transformToScreenCoordinate
        for x in range(0, w, gw):
            pygame.draw.line(
                surface,
                (255, 255, 255),
                transformToScreenCoordinate((x, 0)),
                transformToScreenCoordinate((x, h)),
                1,
            )
        for y in range(0, h, gh):
            pygame.draw.line(
                surface,
                (255, 255, 255),
                transformToScreenCoordinate((0, y)),
                transformToScreenCoordinate((w, y)),
                1,
            )

    def isPointOnFreeSlot(self, point):
        """Check if a given point is placed on a free slot.
        This can be different from GameLevel.checkPointIsFree, beacuse a point can be free (don't collide with anything) but placed
        on a occupied slot.
        """
        grid_point = self.toGridCoord(point)
        try:
            return not self.grid_map.isBlocked(grid_point)
        except IndexError:
            return False

    def getFreeNearSlot(self, point):
        """This method check for a free slot near the point passed. The free slot can be the point itself (if it's free).
        @return: The free slot coord, or None if no free slot is found.
        """
        grid_map = self.grid_map
        try:
            if not grid_map.isBlocked(point):
                return point
        except IndexError:
            blocked = True
        px, py = point
        for y, x in (
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ):
            try:
                blocked = grid_map.isBlocked((px + x, py + y))
            except IndexError:
                blocked = True
            if not blocked:
                return (px + x, py + y)
        return None

    # ******* methods needed to init a PathFinder object *******
    def grid_map_successors(self, point):
        """Given a point get all possible successors where you can freely move into from the given point.
        Freepoint are all non blocked point near the point itself.
        Also no diagonal movement is possible if one of the two near non-diagolan point is blocked.
        @return: a list of successors, free points
        """
        successors = []
        grid_map = self.grid_map
        px, py = point

        # linear near points
        for y, x in (
            (-1, 0),
            (0, 1),
            (1, 0),
            (0, -1),
        ):
            try:
                blocked = grid_map.isBlocked((px + x, py + y))
            except IndexError:
                blocked = True
            if not blocked:
                successors.append((px + x, py + y))
        # diagonal movements
        for y, x in (
            (-1, -1),
            (-1, 1),
            (1, 1),
            (1, -1),
        ):
            try:
                blocked = grid_map.isBlocked((px + x, py + y))
            except IndexError:
                blocked = True
            if not blocked:
                # must check near non-diag points also
                if (0, x) in successors and (y, 0) in successors:
                    successors.append((px + x, py + y))
        return successors

    def grid_map_move_cost(self, point_a, point_b):
        """Get the numeric cost of moving from the first point to the second.

        Euclidean distance is:
        h(n) = D * sqrt((n.x-goal.x)^2 + (n.y-goal.y)^2)

        Diagonal distance (if diagonal movements cost like straight ones) is:
        h(n) = D * max(abs(n.x-goal.x), abs(n.y-goal.y))

        Diagonal distance (if diagonal movements cost more than straight ones) is:
        h_diagonal(n) = min(abs(n.x-goal.x), abs(n.y-goal.y))
        h_straight(n) = (abs(n.x-goal.x) + abs(n.y-goal.y))
        h(n) = D2 * h_diagonal(n) + D * (h_straight(n) - 2*h_diagonal(n)))
        """
        d = 1
        d2 = 1.25
        ax, ay = point_a
        bx, by = point_b
        h_diagonal = min(abs(ax - bx), abs(ay - by))
        h_straight = abs(ax - bx) + abs(ay - by)
        return d2 * h_diagonal + d * (h_straight - 2 * h_diagonal)

    def grid_map_heuristic_to_goal(self, point, goal):
        """Given a point and a goal point,
        obtains the numeric heuristic estimation of
        the cost of reaching the goal from the point.
        """
        return self.grid_map_move_cost(point, goal)

    # ******* *******
