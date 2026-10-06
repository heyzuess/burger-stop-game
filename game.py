"""Round state: ticket, stack, score, and serve feedback."""

from __future__ import annotations

from enum import Enum

from orders import generate_order

CORRECT_POINTS = 10
WRONG_PENALTY = 2
WRONG_MS = 900
RIGHT_MS = 1200


class Feedback(str, Enum):
    NONE = "none"
    WRONG = "wrong"
    RIGHT = "right"


class Game:
    def __init__(self) -> None:
        self.score = 0
        self.customer = ""
        self.ticket: tuple[str, ...] = ()
        self.stack: list[str] = []
        self.feedback = Feedback.NONE
        self.feedback_ms = 0
        self.new_round()

    def new_round(self) -> None:
        order = generate_order()
        self.customer = order.customer
        self.ticket = order.items
        self.stack = []
        self.feedback = Feedback.NONE
        self.feedback_ms = 0

    def busy(self) -> bool:
        return self.feedback is not Feedback.NONE

    def add_ingredient(self, ingredient_id: str) -> None:
        if self.busy():
            return
        self.stack.append(ingredient_id)

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

    def update(self, dt_ms: int) -> None:
        if self.feedback is Feedback.NONE:
            return
        self.feedback_ms -= dt_ms
        if self.feedback_ms > 0:
            return
        if self.feedback is Feedback.RIGHT:
            self.new_round()
            return
        self.stack.clear()
        self.feedback = Feedback.NONE
        self.feedback_ms = 0
