"""Title, setup, pause, and info screens."""

from __future__ import annotations

from enum import Enum

import pygame

from orders import DEFAULT_DIFFICULTY, DIFFICULTIES, PALETTE

GITHUB_URL = "https://github.com/heyzuess/burger-stop-game"

# Counter props on the title kitchen (left-to-right: burger, book, ketchup).
PLAY_RECT = pygame.Rect(150, 138, 52, 42)
SETUP_RECT = pygame.Rect(210, 140, 48, 40)
EXIT_RECT = pygame.Rect(266, 132, 42, 48)

TITLE_ITEM_RECTS = {
    "play": PLAY_RECT,
    "setup": SETUP_RECT,
    "exit": EXIT_RECT,
}
BACK_RECT = pygame.Rect(96, 208, 128, 20)

SETUP_DIFF_RECT = pygame.Rect(48, 70, 224, 22)
SETUP_HELP_RECT = pygame.Rect(48, 98, 224, 22)
SETUP_ABOUT_RECT = pygame.Rect(48, 126, 224, 22)

DIFF_RECTS = {
    "easy": pygame.Rect(48, 70, 224, 22),
    "medium": pygame.Rect(48, 98, 224, 22),
    "hard": pygame.Rect(48, 126, 224, 22),
}

PAUSE_RESUME_RECT = pygame.Rect(48, 70, 224, 22)
PAUSE_HELP_RECT = pygame.Rect(48, 98, 224, 22)
PAUSE_ABOUT_RECT = pygame.Rect(48, 126, 224, 22)
PAUSE_QUIT_RECT = pygame.Rect(48, 154, 224, 22)

YES_RECT = pygame.Rect(48, 120, 100, 24)
NO_RECT = pygame.Rect(172, 120, 100, 24)

GITHUB_HIT = pygame.Rect(16, 150, 288, 36)


class Screen(str, Enum):
    TITLE = "title"
    SETUP = "setup"
    DIFFICULTY = "difficulty"
    HELP = "help"
    ABOUT = "about"
    PLAYING = "playing"
    PAUSE = "pause"
    PAUSE_HELP = "pause_help"
    PAUSE_ABOUT = "pause_about"
    CONFIRM_QUIT = "confirm_quit"


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
    "PAUSE OPENS THE PAUSE MENU.",
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


def draw_kitchen(surf: pygame.Surface) -> None:
    """Diner kitchen: tile wall, grill, hood, checkered floor, wood counter."""
    black = PALETTE["black"]
    wall = (212, 156, 108)
    tile_a = (248, 228, 196)
    tile_b = (232, 196, 148)
    hood = (120, 124, 140)
    grill = (56, 52, 60)
    steel = (168, 172, 188)
    floor_a = (168, 116, 64)
    floor_b = (140, 92, 48)
    top = (196, 152, 96)
    face = (120, 76, 40)
    surf.fill(wall)
    pygame.draw.rect(surf, (40, 28, 24), (0, 0, 320, 28))
    for y in range(28, 120, 8):
        for x in range(0, 320, 8):
            pygame.draw.rect(
                surf,
                tile_a if (x // 8 + y // 8) % 2 == 0 else tile_b,
                (x, y, 8, 8),
            )
    pygame.draw.rect(surf, hood, (4, 20, 108, 18))
    pygame.draw.rect(surf, (80, 84, 96), (20, 38, 76, 8))
    pygame.draw.rect(surf, black, (4, 20, 108, 18), 1)
    pygame.draw.rect(surf, grill, (8, 118, 96, 22))
    pygame.draw.rect(surf, steel, (10, 120, 92, 4))
    for gx in range(14, 96, 10):
        pygame.draw.rect(surf, black, (gx, 126, 6, 10))
    pygame.draw.rect(surf, (72, 128, 184), (208, 40, 96, 44))
    pygame.draw.rect(surf, (252, 220, 120), (212, 44, 20, 16))
    pygame.draw.rect(surf, (40, 48, 72), (236, 44, 28, 16))
    pygame.draw.rect(surf, black, (208, 40, 96, 44), 2)
    pygame.draw.rect(surf, (88, 56, 36), (208, 84, 96, 6))
    pygame.draw.rect(surf, (40, 48, 40), (208, 90, 96, 24))
    pygame.draw.rect(surf, black, (208, 90, 96, 24), 1)
    pygame.draw.rect(surf, (72, 48, 32), (240, 118, 64, 36))
    pygame.draw.rect(surf, (160, 112, 64), (248, 124, 20, 24))
    pygame.draw.rect(surf, (160, 112, 64), (276, 124, 20, 24))
    pygame.draw.rect(surf, black, (240, 118, 64, 36), 1)
    for y in range(164, 240, 8):
        for x in range(0, 320, 8):
            pygame.draw.rect(
                surf,
                floor_a if (x // 8 + y // 8) % 2 == 0 else floor_b,
                (x, y, 8, 8),
            )
    pygame.draw.rect(surf, face, (0, 172, 320, 28))
    pygame.draw.rect(surf, top, (0, 164, 320, 10))
    pygame.draw.rect(surf, (232, 196, 132), (0, 164, 320, 3))
    pygame.draw.rect(surf, black, (0, 164, 320, 36), 1)
    pygame.draw.rect(surf, PALETTE["gold"], (72, 4, 176, 34))
    pygame.draw.rect(surf, PALETTE["cream"], (76, 22, 168, 12))
    pygame.draw.rect(surf, black, (72, 4, 176, 34), 1)
    pygame.draw.rect(surf, (48, 40, 36), (8, 176, 12, 8))
    pygame.draw.rect(surf, (48, 40, 36), (300, 176, 12, 8))


def draw_cook(surf: pygame.Surface, ox: int, oy: int) -> None:
    """Pixel cook: hat, mustache, apron, raised spatula, burger on a silver tray."""
    silver = (196, 200, 216)
    silver_dk = (140, 144, 160)
    white = PALETTE["white"]
    black = PALETTE["black"]
    skin = PALETTE["skin"]
    stache = (32, 20, 12)
    shirt = (40, 72, 168)
    handle = (120, 72, 32)
    bun = (232, 168, 72)
    bun_bot = (216, 148, 56)
    patty = (112, 60, 32)
    lettuce = (80, 176, 48)

    pygame.draw.rect(surf, white, (ox + 16, oy, 22, 10))
    pygame.draw.rect(surf, white, (ox + 10, oy + 6, 34, 10))
    pygame.draw.rect(surf, black, (ox + 16, oy, 22, 10), 1)
    pygame.draw.rect(surf, black, (ox + 10, oy + 6, 34, 10), 1)
    pygame.draw.rect(surf, PALETTE["red"], (ox + 12, oy + 16, 30, 4))
    pygame.draw.rect(surf, black, (ox + 12, oy + 18, 10, 8))
    pygame.draw.rect(surf, black, (ox + 32, oy + 18, 10, 8))
    pygame.draw.rect(surf, skin, (ox + 16, oy + 20, 22, 24))
    pygame.draw.rect(surf, black, (ox + 20, oy + 26, 3, 3))
    pygame.draw.rect(surf, black, (ox + 31, oy + 26, 3, 3))
    pygame.draw.rect(surf, stache, (ox + 18, oy + 32, 18, 4))
    pygame.draw.rect(surf, stache, (ox + 16, oy + 34, 5, 3))
    pygame.draw.rect(surf, stache, (ox + 33, oy + 34, 5, 3))
    pygame.draw.rect(surf, black, (ox + 24, oy + 38, 6, 2))
    pygame.draw.rect(surf, skin, (ox + 24, oy + 44, 6, 4))
    pygame.draw.rect(surf, shirt, (ox + 14, oy + 48, 26, 26))
    pygame.draw.rect(surf, PALETTE["cream"], (ox + 18, oy + 52, 18, 30))
    pygame.draw.rect(surf, PALETTE["red"], (ox + 25, oy + 48, 4, 34))
    # Raised arm + spatula held high above the hat.
    pygame.draw.rect(surf, shirt, (ox + 2, oy + 44, 12, 10))
    pygame.draw.rect(surf, skin, (ox - 4, oy + 18, 8, 28))
    pygame.draw.rect(surf, handle, (ox - 1, oy + 4, 4, 16))
    pygame.draw.rect(surf, silver, (ox - 8, oy - 12, 16, 16))
    pygame.draw.rect(surf, black, (ox - 8, oy - 12, 16, 16), 1)
    pygame.draw.rect(surf, black, (ox - 4, oy - 8, 2, 8))
    pygame.draw.rect(surf, black, (ox + 2, oy - 8, 2, 8))
    pygame.draw.rect(surf, shirt, (ox + 38, oy + 50, 12, 8))
    pygame.draw.rect(surf, skin, (ox + 46, oy + 56, 8, 8))
    pygame.draw.rect(surf, silver, (ox + 50, oy + 62, 30, 5))
    pygame.draw.rect(surf, silver_dk, (ox + 52, oy + 66, 26, 3))
    pygame.draw.rect(surf, black, (ox + 50, oy + 62, 30, 8), 1)
    pygame.draw.rect(surf, bun, (ox + 56, oy + 52, 18, 4))
    pygame.draw.rect(surf, lettuce, (ox + 57, oy + 56, 16, 2))
    pygame.draw.rect(surf, patty, (ox + 57, oy + 58, 16, 3))
    pygame.draw.rect(surf, bun_bot, (ox + 56, oy + 61, 18, 3))
    pygame.draw.rect(surf, PALETTE["navy"], (ox + 18, oy + 82, 18, 10))
    pygame.draw.rect(surf, black, (ox + 18, oy + 90, 8, 6))
    pygame.draw.rect(surf, black, (ox + 28, oy + 90, 8, 6))


def draw_item_hover(surf: pygame.Surface, rect: pygame.Rect) -> None:
    glow = pygame.Surface((rect.w + 6, rect.h + 6))
    glow.fill(PALETTE["gold"])
    glow.set_alpha(80)
    surf.blit(glow, (rect.x - 3, rect.y - 3))
    pygame.draw.rect(surf, PALETTE["gold"], rect.inflate(2, 2), 1)
    pygame.draw.rect(surf, PALETTE["white"], rect.inflate(4, 4), 1)


def title_hover_at(pos: tuple[int, int]) -> str | None:
    for name, rect in TITLE_ITEM_RECTS.items():
        if rect.collidepoint(pos):
            return name
    return None


def draw_counter_items(
    surf: pygame.Surface,
    tiny: pygame.font.Font,
    hovered: str | None = None,
) -> None:
    black = PALETTE["black"]
    if hovered in TITLE_ITEM_RECTS:
        draw_item_hover(surf, TITLE_ITEM_RECTS[hovered])
    # PLAY: plated burger
    pygame.draw.rect(surf, PALETTE["white"], (PLAY_RECT.x + 4, PLAY_RECT.y + 20, 40, 8))
    pygame.draw.rect(surf, PALETTE["gray"], (PLAY_RECT.x + 8, PLAY_RECT.y + 26, 32, 4))
    pygame.draw.rect(surf, (232, 168, 72), (PLAY_RECT.x + 12, PLAY_RECT.y + 8, 24, 6))
    pygame.draw.rect(surf, (80, 176, 48), (PLAY_RECT.x + 13, PLAY_RECT.y + 14, 22, 3))
    pygame.draw.rect(surf, (112, 60, 32), (PLAY_RECT.x + 13, PLAY_RECT.y + 17, 22, 4))
    pygame.draw.rect(surf, (216, 148, 56), (PLAY_RECT.x + 12, PLAY_RECT.y + 21, 24, 4))
    pygame.draw.rect(surf, black, (PLAY_RECT.x + 4, PLAY_RECT.y + 20, 40, 10), 1)
    play_color = PALETTE["white"] if hovered == "play" else PALETTE["gold"]
    label = tiny.render("PLAY", False, play_color)
    surf.blit(label, (PLAY_RECT.x + 8, PLAY_RECT.y + 32))
    # SETUP: recipe book
    pygame.draw.rect(surf, (120, 56, 32), SETUP_RECT)
    pygame.draw.rect(surf, PALETTE["cream"], (SETUP_RECT.x + 4, SETUP_RECT.y + 4, 18, 28))
    pygame.draw.rect(surf, PALETTE["paper"], (SETUP_RECT.x + 24, SETUP_RECT.y + 4, 18, 28))
    pygame.draw.rect(surf, black, SETUP_RECT, 1)
    pygame.draw.line(
        surf,
        black,
        (SETUP_RECT.centerx, SETUP_RECT.y + 4),
        (SETUP_RECT.centerx, SETUP_RECT.bottom - 4),
    )
    for ly in range(SETUP_RECT.y + 8, SETUP_RECT.y + 28, 4):
        pygame.draw.rect(surf, PALETTE["gray"], (SETUP_RECT.x + 6, ly, 12, 1))
    setup_color = PALETTE["white"] if hovered == "setup" else PALETTE["gold"]
    book = tiny.render("SETUP", False, setup_color)
    surf.blit(book, (SETUP_RECT.x - 2, SETUP_RECT.bottom - 2))
    # EXIT: ketchup bottle
    pygame.draw.rect(surf, PALETTE["red"], (EXIT_RECT.x + 10, EXIT_RECT.y + 14, 20, 28))
    pygame.draw.rect(surf, (160, 32, 40), (EXIT_RECT.x + 14, EXIT_RECT.y + 6, 12, 10))
    pygame.draw.rect(surf, PALETTE["white"], (EXIT_RECT.x + 16, EXIT_RECT.y + 2, 8, 6))
    pygame.draw.rect(surf, PALETTE["cream"], (EXIT_RECT.x + 12, EXIT_RECT.y + 20, 16, 12))
    pygame.draw.rect(surf, black, (EXIT_RECT.x + 10, EXIT_RECT.y + 14, 20, 28), 1)
    exit_color = PALETTE["white"] if hovered == "exit" else PALETTE["gold"]
    ex = tiny.render("EXIT", False, exit_color)
    surf.blit(ex, (EXIT_RECT.x + 4, EXIT_RECT.bottom - 2))


def draw_title(
    surf: pygame.Surface,
    font: pygame.font.Font,
    tiny: pygame.font.Font,
    difficulty: str,
    draw_btn,
    draw_text,
    hovered: str | None = None,
) -> None:
    draw_kitchen(surf)
    title = font.render("BURGER STOP", False, PALETTE["black"])
    surf.blit(title, ((surf.get_width() - title.get_width()) // 2, 8))
    sub = tiny.render("STACK EM RIGHT", False, PALETTE["navy"])
    surf.blit(sub, ((surf.get_width() - sub.get_width()) // 2, 24))
    label = DIFFICULTIES.get(difficulty, DIFFICULTIES[DEFAULT_DIFFICULTY]).label
    diff = tiny.render(label, False, PALETTE["green"])
    surf.blit(diff, (216, 98))
    draw_cook(surf, 40, 62)
    draw_counter_items(surf, tiny, hovered)


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
    url_lines = wrap_to_width(GITHUB_URL.upper(), tiny, 288)
    _blit_lines(surf, tiny, url_lines, 16, 152, PALETTE["gold"], gap=10)
    draw_text(surf, tiny, "CLICK URL TO OPEN", (12, 188), PALETTE["gray"])
    draw_btn(surf, BACK_RECT, PALETTE["gray"], "BACK", tiny, PALETTE["white"])


def draw_pause_overlay(
    surf: pygame.Surface,
    tiny: pygame.font.Font,
    draw_btn,
    draw_text,
) -> None:
    veil = pygame.Surface(surf.get_size())
    veil.fill(PALETTE["black"])
    veil.set_alpha(160)
    surf.blit(veil, (0, 0))
    draw_text(surf, tiny, "PAUSED", (8, 8), PALETTE["gold"])
    draw_btn(surf, PAUSE_RESUME_RECT, PALETTE["green"], "RESUME", tiny, PALETTE["black"])
    draw_btn(surf, PAUSE_HELP_RECT, PALETTE["cream"], "HOW TO PLAY", tiny)
    draw_btn(surf, PAUSE_ABOUT_RECT, PALETTE["cream"], "ABOUT / GITHUB", tiny)
    draw_btn(surf, PAUSE_QUIT_RECT, PALETTE["red"], "QUIT GAME", tiny, PALETTE["white"])


def draw_confirm_quit(
    surf: pygame.Surface,
    tiny: pygame.font.Font,
    draw_btn,
    draw_text,
) -> None:
    veil = pygame.Surface(surf.get_size())
    veil.fill(PALETTE["black"])
    veil.set_alpha(180)
    surf.blit(veil, (0, 0))
    draw_text(surf, tiny, "QUIT TO TITLE?", (72, 80), PALETTE["gold"])
    draw_text(surf, tiny, "PROGRESS IS LOST", (64, 96), PALETTE["cream"])
    draw_btn(surf, YES_RECT, PALETTE["red"], "YES", tiny, PALETTE["white"])
    draw_btn(surf, NO_RECT, PALETTE["green"], "NO", tiny, PALETTE["black"])
