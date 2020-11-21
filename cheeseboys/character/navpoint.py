# -*- coding: utf-8 -

from cheeseboys.vector2 import Vector2


class NavPoint(object):
    """A class for store the target of movement action of GameCharacter sprites,
    and manage the path to follow.
    """

    def __init__(self, character):
        self._character = character
        self._v = None
        self.computed_path = []

    def set(self, value):
        if type(value) == tuple:
            value = Vector2(value)
        self._character.moving(True)
        value_t = value.as_tuple()
        if self._character.hasNoFreeMovementTo(value_t):
            self.compute_path(value)
        else:
            self.computed_path = [
                value_t,
            ]
        next(self)

    def get(self):
        return self._v

    def reset(self):
        self._v = None
        self._character.moving(False)

    def __next__(self):
        """Get the next navPoint from the computed_path list"""
        # BBB: check there if with the new navPoint we can now move freely to the target
        try:
            self._v = Vector2(self.computed_path.pop(0))
        except IndexError:
            self.reset()

    def reroute(self):
        """Re-compute the route to the target"""
        try:
            if self.computed_path:
                self.compute_path(Vector2(self.computed_path[-1]))
            else:
                self.compute_path(self._v)
        except IndexError:
            pass
        next(self)

    def as_tuple(self):
        return self._v.as_tuple()

    def compute_path(self, target=None):
        """Call PathFinder.compute_path using the character position as start point
        and his navPoint as goal.
        First and last path elements are ignored (last element only sometimes) so we get:
        [path2, path3, ... pathn-1, navPoint]
        @target: an optional Vector2 instance; the current navPoint is used as default
        @return: the computed path itself (that can be an empty list)
        """
        character = self._character
        level = character.currentLevel
        if not target:
            target = self.get()
        if target:
            target_tuple = target.as_tuple()
            target_is_free_point = level.checkPointIsFree(target_tuple)
            target_is_free_slot = level.isPointOnFreeSlot(target_tuple)
            # Checking for a free slot on the grid, to be the target of the pathfinding
            free_near_slot = None
            if not target_is_free_slot and target_is_free_point:
                # The target is on a non free slot but is a free point: I need to move to a free near slot
                free_near_slot = level.getFreeNearSlot(level.toGridCoord(target_tuple))
            if not target_is_free_point or (
                not target_is_free_slot and not free_near_slot
            ):
                # The character wanna move on a non-free point, or onto a free point but in a non free gridmap slot: no path computed!
                self.computed_path = [
                    target_tuple,
                ]
                return self.computed_path
            fromGridCoord = level.fromGridCoord
            if free_near_slot:
                goal = free_near_slot
            else:
                goal = level.toGridCoord(target_tuple)
            temp_computed_path = [
                fromGridCoord(x)
                for x in character.pathfinder.compute_path(
                    character.position_grid, goal
                )
            ]
            # For a better animation I like to cut the last pathfinding step before the real navPoint;
            # this can lead to collision sometimes.
            if len(temp_computed_path) > 2 and character.hasNoFreeMovementTo(
                target_tuple, source=temp_computed_path[-2]
            ):
                self.computed_path = temp_computed_path[1:] + [
                    target_tuple,
                ]
            else:
                self.computed_path = temp_computed_path[1:-1] + [
                    target_tuple,
                ]
        else:
            self.computed_path = []
        return self.computed_path

    def __bool__(self):
        if self._v is None:
            return False
        return True

    def __str__(self):
        st = "to %s" % self._v
        if self.computed_path:
            st += " (" + ", ".join([str(x) for x in self.computed_path]) + ")"
        return st
