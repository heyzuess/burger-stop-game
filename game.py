"""Round state: ticket, stack, score, timer, and serve feedback."""

from __future__ import annotations

import random
from enum import Enum

from orders import generate_order

CORRECT_POINTS = 10
WRONG_PENALTY = 2
WRONG_MS = 900
RIGHT_MS = 1200
LEFT_MS = 1800
ORDER_MS = 30_000

CURSES = ("#@%&!!", "I QUIT!", "TOO SLOW!", "FORGET IT!", "YEESH!!")


class Feedback(str, Enum):
    NONE = "none"
    WRONG = "wrong"
    RIGHT = "right"
    LEFT = "left"


class Game:
    def __init__(self) -> None:
        self.score = 0
        self.customer = ""
        self.ticket: tuple[str, ...] = ()
        self.stack: list[str] = []
        self.feedback = Feedback.NONE
        self.feedback_ms = 0
        self.time_ms = ORDER_MS
        self.curse = ""
        self.new_round()

    def new_round(self) -> None:
        order = generate_order()
        self.customer = order.customer
        self.ticket = order.items
        self.stack = []
        self.feedback = Feedback.NONE
        self.feedback_ms = 0
        self.time_ms = ORDER_MS
        self.curse = ""

    def busy(self) -> bool:
        return self.feedback is not Feedback.NONE

    @property
    def seconds_left(self) -> int:
        return max(0, (self.time_ms + 999) // 1000)

    @property
    def anger(self) -> int:
        if self.feedback is Feedback.LEFT:
            return 3
        elapsed = ORDER_MS - self.time_ms
        if elapsed < 10_000:
            return 0
        if elapsed < 20_000:
            return 1
        return 2

    def add_ingredient(self, ingredient_id: str) -> None:
        if self.busy():
            return
        self.stack.append(ingredient_id)

    def remove_at(self, index: int) -> None:
        if self.busy():
            return
        if 0 <= index < len(self.stack):
            self.stack.pop(index)

    def clear_stack(self) -> None:
        if self.busy():
            return
        self.stack.clear()

    def serve(self) -> None:
        if self.busy():
            return
        if tuple(self.stack) == self.ticket:
            self.score += CORRECT_POINTS
            self.feedback = Feedback.RIGHT
            self.feedback_ms = RIGHT_MS
        else:
            self.score = max(0, self.score - WRONG_PENALTY)
            self.feedback = Feedback.WRONG
            self.feedback_ms = WRONG_MS

    def _time_out(self) -> None:
        self.score = max(0, self.score - WRONG_PENALTY)
        self.feedback = Feedback.LEFT
        self.feedback_ms = LEFT_MS
        self.curse = random.choice(CURSES)

    def update(self, dt_ms: int) -> None:
        if self.feedback is Feedback.NONE:
            self.time_ms -= dt_ms
            if self.time_ms <= 0:
                self.time_ms = 0
                self._time_out()
            return
        if self.feedback is Feedback.WRONG:
            self.time_ms -= dt_ms
            if self.time_ms <= 0:
                self.time_ms = 0
                self._time_out()
                return
        self.feedback_ms -= dt_ms
        if self.feedback_ms > 0:
            return
        if self.feedback in (Feedback.RIGHT, Feedback.LEFT):
            self.new_round()
            return
        self.stack.clear()
        self.feedback = Feedback.NONE
        self.feedback_ms = 0
