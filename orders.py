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

TRAY_ORDER = [
    "bottom_bun",
    "patty",
    "cheese",
    "lettuce",
    "tomato",
    "onion",
    "pickle",
    "top_bun",
]

FILLINGS = ["patty", "cheese", "lettuce", "tomato", "onion", "pickle"]

CUSTOMERS = ["BOB", "LISA", "MIKE", "AMY", "TED", "NINA", "JOE", "KIM"]


@dataclass(frozen=True)
class Order:
    customer: str
    items: tuple[str, ...]


def generate_order() -> Order:
    filling_count = random.randint(2, 4)
    fillings = [random.choice(FILLINGS) for _ in range(filling_count)]
    items = ("bottom_bun", *fillings, "top_bun")
    return Order(customer=random.choice(CUSTOMERS), items=items)
