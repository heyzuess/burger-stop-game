"""Title, setup, and info screens."""

from __future__ import annotations

from enum import Enum

import pygame

from orders import DEFAULT_DIFFICULTY, DIFFICULTIES, PALETTE

GITHUB_URL = "https://github.com/heyzuess/burger-stop-game"

PLAY_RECT = pygame.Rect(96, 140, 128, 22)
SETUP_RECT = pygame.Rect(96, 168, 128, 22)
BACK_RECT = pygame.Rect(96, 208, 128, 20)

SETUP_DIFF_RECT = pygame.Rect(48, 70, 224, 22)
SETUP_HELP_RECT = pygame.Rect(48, 98, 224, 22)
SETUP_ABOUT_RECT = pygame.Rect(48, 126, 224, 22)

DIFF_RECTS = {
    "easy": pygame.Rect(48, 70, 224, 22),
    "medium": pygame.Rect(48, 98, 224, 22),
    "hard": pygame.Rect(48, 126, 224, 22),
}

GITHUB_HIT = pygame.Rect(16, 150, 288, 24)


class Screen(str, Enum):
    TITLE = "title"
    SETUP = "setup"
    DIFFICULTY = "difficulty"
    HELP = "help"
    ABOUT = "about"
    PLAYING = "playing"


HELP_LINES = [
    "MATCH THE TICKET IN 30S.",
    "+10 CORRECT SERVE",
    "-2 WRONG SERVE OR TIMEOUT",
    "SCORE NEVER GOES BELOW 0.",
    "",
    "CLICK TRAY TO ADD",
    "CLICK A LAYER TO PULL IT",
    "SERVE CHECKS THE STACK",
    "CLEAR DUMPS THE STACK",
    "ESC RETURNS TO TITLE.",
    "",
    "MOOD: CALM, MAD, IRATE.",
    "AT 0S THEY CURSE AND GO.",
    "HARDER = MORE TRAY ITEMS.",
]

ABOUT_LINES = [
    "BURGER STOP IS AN 8-BIT",
    "PYGAME-CE GAME. TAKE ORDERS",
    "STACK BURGERS, AND BEAT THE",
    "TIMER. SOURCE, LICENSE, AND",
    "DOCS LIVE ON GITHUB.",
    "",
    "CLICK THE LINK TO OPEN:",
]


def wrap_to_width(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    words = text.split(" ")
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if font.size(trial)[0] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_checker(surf: pygame.Surface, game_w: int, game_h: int) -> None:
    surf.fill(PALETTE["navy"])
    for ty in range(0, game_h, 8):
        for tx in range(0, game_w, 8):
            if (tx // 8 + ty // 8) % 2 == 0:
                pygame.draw.rect(surf, PALETTE["navy_hi"], (tx, ty, 8, 8))


def _blit_lines(
    surf: pygame.Surface,
    font: pygame.font.Font,
    lines: list[str],
    x: int,
    y: int,
    color: tuple[int, int, int],
    gap: int = 10,
) -> None:
    for line in lines:
        if line:
            image = font.render(line, False, color)
            surf.blit(image, (x, y))
        y += gap


def draw_title(
    surf: pygame.Surface,
    font: pygame.font.Font,
    tiny: pygame.font.Font,
    difficulty: str,
    draw_btn,
    draw_text,
) -> None:
    title = font.render("BURGER STOP", False, PALETTE["gold"])
    surf.blit(title, ((surf.get_width() - title.get_width()) // 2, 36))
    sub = tiny.render("STACK EM RIGHT", False, PALETTE["cream"])
    surf.blit(sub, ((surf.get_width() - sub.get_width()) // 2, 54))
    label = DIFFICULTIES.get(difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY]).label
    diff = tiny.render(f"DIFFICULTY {label}", False, PALETTE["gray"])
    surf.blit(diff, ((surf.get_width() - diff.get_width()) // 2, 110))
    draw_btn(surf, PLAY_RECT, PALETTE["green"], "PLAY", tiny, PALETTE["black"])
    draw_btn(surf, SETUP_RECT, PALETTE["gold"], "SETUP", tiny, PALETTE["black"])
    draw_text(surf, tiny, "ESC QUITS", (8, 228), PALETTE["gray"])


def draw_setup(surf: pygame.Surface, tiny: pygame.font.Font, draw_btn, draw_text) -> None:
    draw_text(surf, tiny, "SETUP", (8, 8), PALETTE["gold"])
    draw_btn(surf, SETUP_DIFF_RECT, PALETTE["cream"], "DIFFICULTY", tiny)
    draw_btn(surf, SETUP_HELP_RECT, PALETTE["cream"], "HOW TO PLAY", tiny)
    draw_btn(surf, SETUP_ABOUT_RECT, PALETTE["cream"], "ABOUT / GITHUB", tiny)
    draw_btn(surf, BACK_RECT, PALETTE["gray"], "BACK", tiny, PALETTE["white"])


def draw_difficulty(
    surf: pygame.Surface,
    tiny: pygame.font.Font,
    selected: str,
    draw_btn,
    draw_text,
) -> None:
    draw_text(surf, tiny, "DIFFICULTY", (8, 8), PALETTE["gold"])
    draw_text(surf, tiny, "STAYS UNTIL YOU CHANGE IT", (8, 24), PALETTE["gray"])
    for key, rect in DIFF_RECTS.items():
        spec = DIFFICULTIES[key]
        fill = PALETTE["gold"] if key == selected else PALETTE["cream"]
        mark = "*" if key == selected else " "
        extra = f" {len(spec.fillings)} FILLINGS"
        draw_btn(surf, rect, fill, f"{mark}{spec.label}{extra}", tiny)
    draw_btn(surf, BACK_RECT, PALETTE["gray"], "BACK", tiny, PALETTE["white"])


def draw_help(surf: pygame.Surface, tiny: pygame.font.Font, draw_btn, draw_text) -> None:
    draw_text(surf, tiny, "HOW TO PLAY", (8, 8), PALETTE["gold"])
    _blit_lines(surf, tiny, HELP_LINES, 12, 24, PALETTE["cream"], gap=10)
    draw_btn(surf, BACK_RECT, PALETTE["gray"], "BACK", tiny, PALETTE["white"])


def draw_about(surf: pygame.Surface, tiny: pygame.font.Font, draw_btn, draw_text) -> None:
    draw_text(surf, tiny, "ABOUT", (8, 8), PALETTE["gold"])
    _blit_lines(surf, tiny, ABOUT_LINES, 12, 28, PALETTE["cream"], gap=12)
    # URL may be wider than 320; split for the pixel font.
    url_lines = wrap_to_width(GITHUB_URL.upper(), tiny, 288)
    _blit_lines(surf, tiny, url_lines, 16, 152, PALETTE["gold"], gap=10)
    draw_text(surf, tiny, "CLICK URL TO OPEN", (12, 188), PALETTE["gray"])
    draw_btn(surf, BACK_RECT, PALETTE["gray"], "BACK", tiny, PALETTE["white"])
