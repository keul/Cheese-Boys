# -*- coding: utf-8 -

from cheeseboys.ai import State, StateMachine
from cheeseboys.ai.base_brain import BaseStateExploring, BaseStateWaiting
from cheeseboys import cblocals
from cheeseboys.cbrandom import cbrandom


class PresentationStateExploring(BaseStateExploring):
    """Exploring state. The character will move to a position then wait"""

    def do_actions(self, time_passed):
        self.character.moveBasedOnNavPoint(time_passed)

    def check_conditions(self):
        character = self.character
        if not character.navPoint:
            return "waiting"

        return None

    def entry_actions(self, old_state_name):
        pass


class PresentationStateWaiting(BaseStateWaiting):
    """The character simply do nothing until he has a navPoint"""

    def do_actions(self, time_passed):
        pass

    def check_conditions(self):
        character = self.character
        if self.character.navPoint:
            return "exploring"

        return None

    def entry_actions(self, old_state_name):
        pass


class PresentationStateMachine(StateMachine):
    """State machine used for non AI.
    During presentation time all AI and intelligence must be negated, so every character use
    an instance of this brain instead of other.
    """

    def __init__(self, character):
        self._character = character
        states = (
            PresentationStateWaiting(character),
            PresentationStateExploring(character),
        )
        StateMachine.__init__(self, states)
