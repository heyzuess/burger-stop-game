"""Ingredient catalog and random tickets."""

from __future__ import annotations

import random
from dataclasses import dataclass

# NES-like palette
PALETTE = {
    "navy": (20, 16, 52),
    "navy_hi": (36, 32, 80),
    "cream": (252, 236, 196),
    "paper": (236, 216, 164),
    "black": (8, 8, 16),
    "white": (248, 248, 248),
    "gray": (120, 120, 136),
    "red": (208, 48, 64),
    "green": (48, 184, 80),
    "gold": (248, 208, 64),
    "skin": (248, 184, 136),
    "skin_mad": (248, 120, 96),
    "skin_rage": (232, 72, 72),
    "hair": (88, 56, 32),
}

INGREDIENTS: dict[str, dict] = {
    "bottom_bun": {"label": "BOT BUN", "color": (216, 148, 56), "height": 10},
    "patty": {"label": "PATTY", "color": (112, 60, 32), "height": 8},
    "cheese": {"label": "CHEESE", "color": (248, 200, 40), "height": 4},
    "lettuce": {"label": "LETTUCE", "color": (80, 176, 48), "height": 5},
    "tomato": {"label": "TOMATO", "color": (208, 56, 48), "height": 5},
    "onion": {"label": "ONION", "color": (200, 168, 216), "height": 4},
    "pickle": {"label": "PICKLE", "color": (72, 152, 56), "height": 4},
    "top_bun": {"label": "TOP BUN", "color": (232, 168, 72), "height": 10},
}

# Top of tray = top of burger.
TRAY_ORDER = [
    "top_bun",
    "pickle",
    "onion",
    "tomato",
    "lettuce",
    "cheese",
    "patty",
    "bottom_bun",
]

FILLINGS = ["patty", "cheese", "lettuce", "tomato", "onion", "pickle"]

CUSTOMERS = ["BOB", "LISA", "MIKE", "AMY", "TED", "NINA", "JOE", "KIM"]

DEFAULT_DIFFICULTY = "easy"


@dataclass(frozen=True)
class Difficulty:
    key: str
    label: str
    fillings: tuple[str, ...]
    filling_min: int
    filling_max: int


DIFFICULTIES: dict[str, Difficulty] = {
    "easy": Difficulty("easy", "EASY", ("patty", "cheese"), 1, 2),
    "medium": Difficulty(
        "medium",
        "MEDIUM",
        ("patty", "cheese", "lettuce", "tomato"),
        2,
        3,
    ),
    "hard": Difficulty(
        "hard",
        "HARD",
        ("patty", "cheese", "lettuce", "tomato", "onion", "pickle"),
        2,
        4,
    ),
}


@dataclass(frozen=True)
class Order:
    customer: str
    items: tuple[str, ...]


def tray_ids(difficulty: str = DEFAULT_DIFFICULTY) -> tuple[str, ...]:
    fillings = set(DIFFICULTIES[difficulty].fillings)
    return tuple(
        item
        for item in TRAY_ORDER
        if item in ("top_bun", "bottom_bun") or item in fillings
    )


def generate_order(difficulty: str = DEFAULT_DIFFICULTY) -> Order:
    spec = DIFFICULTIES[difficulty]
    filling_count = random.randint(spec.filling_min, spec.filling_max)
    fillings = [random.choice(spec.fillings) for _ in range(filling_count)]
    items = ("bottom_bun", *fillings, "top_bun")
    return Order(customer=random.choice(CUSTOMERS), items=items)
