"""Burger Stop — 8-bit order stacking game."""

from __future__ import annotations

import os
from pathlib import Path

# Nearest-neighbor scaling (chunky pixels, no blur)
os.environ.setdefault("SDL_HINT_RENDER_SCALE_QUALITY", "0")

import pygame

from game import Feedback, Game
from orders import INGREDIENTS, PALETTE, TRAY_ORDER

GAME_W, GAME_H = 320, 240
SCALE = 3
WINDOW_W, WINDOW_H = GAME_W * SCALE, GAME_H * SCALE
FPS = 60

ASSETS = Path(__file__).resolve().parent / "assets"
FONT_PATH = ASSETS / "PressStart2P-Regular.ttf"

# Layout in native 320x240 pixels
HUD_RECT = pygame.Rect(0, 0, GAME_W, 18)
TICKET_RECT = pygame.Rect(6, 22, 86, 176)
BUILD_RECT = pygame.Rect(98, 22, 114, 176)
TRAY_RECT = pygame.Rect(218, 22, 96, 176)
MSG_RECT = pygame.Rect(6, 202, 206, 32)


def load_font(size: int) -> pygame.font.Font:
    if FONT_PATH.exists():
        return pygame.font.Font(FONT_PATH, size)
    return pygame.font.Font(None, size + 8)


def draw_text(
    surf: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    pos: tuple[int, int],
    color: tuple[int, int, int],
) -> pygame.Rect:
    image = font.render(text, False, color)
    return surf.blit(image, pos)


def draw_panel(surf: pygame.Surface, rect: pygame.Rect, fill: tuple[int, int, int]) -> None:
    pygame.draw.rect(surf, fill, rect)
    pygame.draw.rect(surf, PALETTE["black"], rect, 2)
    inner = rect.inflate(-4, -4)
    pygame.draw.rect(surf, PALETTE["black"], inner, 1)
    for x in range(inner.left + 2, inner.right, 4):
        surf.set_at((x, inner.top + 1), PALETTE["black"])
        surf.set_at((x, inner.bottom - 2), PALETTE["black"])


def shade(color: tuple[int, int, int], delta: int) -> tuple[int, int, int]:
    return tuple(max(0, min(255, c + delta)) for c in color)


def draw_button(
    surf: pygame.Surface,
    rect: pygame.Rect,
    fill: tuple[int, int, int],
    label: str,
    font: pygame.font.Font,
    label_color: tuple[int, int, int] = PALETTE["black"],
) -> None:
    pygame.draw.rect(surf, fill, rect)
    pygame.draw.rect(surf, PALETTE["black"], rect, 1)
    hi = shade(fill, 40)
    lo = shade(fill, -50)
    pygame.draw.line(surf, hi, (rect.left + 1, rect.top + 1), (rect.right - 2, rect.top + 1))
    pygame.draw.line(surf, hi, (rect.left + 1, rect.top + 1), (rect.left + 1, rect.bottom - 2))
    pygame.draw.line(surf, lo, (rect.left + 1, rect.bottom - 2), (rect.right - 2, rect.bottom - 2))
    pygame.draw.line(surf, lo, (rect.right - 2, rect.top + 1), (rect.right - 2, rect.bottom - 2))
    text = font.render(label, False, label_color)
    tx = rect.x + (rect.w - text.get_width()) // 2
    ty = rect.y + (rect.h - text.get_height()) // 2
    surf.blit(text, (tx, ty))


def draw_customer(surf: pygame.Surface, x: int, y: int) -> None:
    # 16x16 pixel face
    pygame.draw.rect(surf, PALETTE["hair"], (x + 3, y, 10, 4))
    pygame.draw.rect(surf, PALETTE["skin"], (x + 3, y + 3, 10, 9))
    pygame.draw.rect(surf, PALETTE["black"], (x + 5, y + 6, 2, 2))
    pygame.draw.rect(surf, PALETTE["black"], (x + 9, y + 6, 2, 2))
    pygame.draw.rect(surf, PALETTE["black"], (x + 6, y + 9, 4, 1))
    pygame.draw.rect(surf, PALETTE["navy_hi"], (x + 2, y + 12, 12, 6))


def stack_highlight(game: Game) -> tuple[int, int, int] | None:
    if game.feedback is Feedback.WRONG:
        return PALETTE["red"]
    if game.feedback is Feedback.RIGHT:
        return PALETTE["green"]
    return None


def draw_burger_layer(
    surf: pygame.Surface,
    ingredient_id: str,
    cx: int,
    top: int,
    width: int,
) -> int:
    meta = INGREDIENTS[ingredient_id]
    h = meta["height"]
    color = meta["color"]
    if ingredient_id == "top_bun":
        pygame.draw.rect(surf, color, (cx - width // 2 + 4, top, width - 8, h))
        pygame.draw.rect(surf, color, (cx - width // 2, top + 4, width, h - 3))
        pygame.draw.rect(surf, PALETTE["black"], (cx - width // 2 + 4, top, width - 8, h), 1)
        pygame.draw.rect(surf, PALETTE["black"], (cx - width // 2, top + 4, width, h - 3), 1)
    elif ingredient_id == "bottom_bun":
        pygame.draw.rect(surf, color, (cx - width // 2, top, width, h - 2))
        pygame.draw.rect(surf, shade(color, -30), (cx - width // 2 + 2, top + h - 4, width - 4, 4))
        pygame.draw.rect(surf, PALETTE["black"], (cx - width // 2, top, width, h), 1)
    else:
        pygame.draw.rect(surf, color, (cx - width // 2, top, width, h))
        pygame.draw.rect(surf, PALETTE["black"], (cx - width // 2, top, width, h), 1)
        pygame.draw.line(
            surf,
            shade(color, 40),
            (cx - width // 2 + 1, top + 1),
            (cx + width // 2 - 2, top + 1),
        )
    return h


def layer_width(ingredient_id: str) -> int:
    if ingredient_id in ("top_bun", "bottom_bun"):
        return 72
    if ingredient_id == "cheese":
        return 70
    return 64


def draw_stack(
    surf: pygame.Surface,
    items: list[str] | tuple[str, ...],
    area: pygame.Rect,
    outline: tuple[int, int, int] | None,
) -> None:
    if not items:
        return
    widths = [layer_width(item) for item in items]
    total_h = sum(INGREDIENTS[item]["height"] for item in items)
    cx = area.centerx
    top = area.bottom - 10 - total_h
    if outline:
        max_w = max(widths)
        burger_box = pygame.Rect(cx - max_w // 2 - 3, top - 3, max_w + 6, total_h + 6)
        flash = pygame.Surface((burger_box.w, burger_box.h))
        flash.fill(outline)
        flash.set_alpha(90)
        surf.blit(flash, burger_box.topleft)
        pygame.draw.rect(surf, outline, burger_box, 2)
    y = area.bottom - 10
    for item, w in zip(items, widths):
        y -= INGREDIENTS[item]["height"]
        draw_burger_layer(surf, item, cx, y, w)


def make_tray_buttons() -> dict[str, pygame.Rect]:
    buttons: dict[str, pygame.Rect] = {}
    x, y = TRAY_RECT.x + 4, TRAY_RECT.y + 14
    for ingredient_id in TRAY_ORDER:
        buttons[ingredient_id] = pygame.Rect(x, y, TRAY_RECT.w - 8, 16)
        y += 18
    return buttons


SERVE_RECT = pygame.Rect(218, 204, 46, 28)
CLEAR_RECT = pygame.Rect(268, 204, 46, 28)


def draw_scene(
    surf: pygame.Surface,
    game: Game,
    font: pygame.font.Font,
    tiny: pygame.font.Font,
    tray_buttons: dict[str, pygame.Rect],
) -> None:
    surf.fill(PALETTE["navy"])
    for ty in range(HUD_RECT.bottom, GAME_H, 8):
        for tx in range(0, GAME_W, 8):
            if (tx // 8 + ty // 8) % 2 == 0:
                pygame.draw.rect(surf, PALETTE["navy_hi"], (tx, ty, 8, 8))
    pygame.draw.rect(surf, PALETTE["navy_hi"], HUD_RECT)
    pygame.draw.line(surf, PALETTE["black"], (0, HUD_RECT.bottom), (GAME_W, HUD_RECT.bottom))
    draw_text(surf, font, "BURGER STOP", (6, 5), PALETTE["gold"])
    score = f"SCORE {game.score:04d}"
    draw_text(surf, font, score, (GAME_W - 8 - tiny.size(score)[0], 5), PALETTE["white"])

    draw_panel(surf, TICKET_RECT, PALETTE["paper"])
    draw_text(surf, tiny, "ORDER", (TICKET_RECT.x + 8, TICKET_RECT.y + 6), PALETTE["black"])
    draw_customer(surf, TICKET_RECT.x + 34, TICKET_RECT.y + 16)
    draw_text(surf, tiny, game.customer, (TICKET_RECT.x + 8, TICKET_RECT.y + 36), PALETTE["black"])
    y = TICKET_RECT.y + 50
    # Ticket shows the finished stack top-to-bottom; build from the plate up.
    for item in reversed(game.ticket):
        meta = INGREDIENTS[item]
        pygame.draw.rect(surf, meta["color"], (TICKET_RECT.x + 8, y, 8, 8))
        pygame.draw.rect(surf, PALETTE["black"], (TICKET_RECT.x + 8, y, 8, 8), 1)
        draw_text(surf, tiny, meta["label"], (TICKET_RECT.x + 20, y + 1), PALETTE["black"])
        y += 12

    pygame.draw.rect(surf, PALETTE["navy_hi"], BUILD_RECT)
    pygame.draw.rect(surf, PALETTE["black"], BUILD_RECT, 2)
    draw_text(surf, tiny, "BUILD", (BUILD_RECT.x + 6, BUILD_RECT.y + 4), PALETTE["white"])
    # plate
    pygame.draw.rect(surf, PALETTE["gray"], (BUILD_RECT.x + 12, BUILD_RECT.bottom - 12, BUILD_RECT.w - 24, 6))
    pygame.draw.rect(surf, PALETTE["black"], (BUILD_RECT.x + 12, BUILD_RECT.bottom - 12, BUILD_RECT.w - 24, 6), 1)
    draw_stack(surf, game.stack, BUILD_RECT, stack_highlight(game))

    pygame.draw.rect(surf, PALETTE["navy_hi"], TRAY_RECT)
    pygame.draw.rect(surf, PALETTE["black"], TRAY_RECT, 2)
    draw_text(surf, tiny, "TRAY", (TRAY_RECT.x + 6, TRAY_RECT.y + 4), PALETTE["white"])
    for ingredient_id, rect in tray_buttons.items():
        meta = INGREDIENTS[ingredient_id]
        draw_button(surf, rect, meta["color"], meta["label"], tiny)

    pygame.draw.rect(surf, PALETTE["navy_hi"], MSG_RECT)
    pygame.draw.rect(surf, PALETTE["black"], MSG_RECT, 2)
    if game.feedback is Feedback.WRONG:
        msg, color = "TRY AGAIN", PALETTE["red"]
    elif game.feedback is Feedback.RIGHT:
        msg, color = "ORDER COMPLETE!", PALETTE["green"]
    else:
        msg, color = "STACK THE ORDER", PALETTE["cream"]
    draw_text(surf, tiny, msg, (MSG_RECT.x + 8, MSG_RECT.y + 12), color)

    draw_button(surf, SERVE_RECT, PALETTE["green"], "SERVE", tiny, PALETTE["black"])
    draw_button(surf, CLEAR_RECT, PALETTE["red"], "CLEAR", tiny, PALETTE["white"])


def to_game_pos(pos: tuple[int, int]) -> tuple[int, int]:
    return pos[0] // SCALE, pos[1] // SCALE


def handle_click(game: Game, pos: tuple[int, int], tray_buttons: dict[str, pygame.Rect]) -> None:
    gx, gy = to_game_pos(pos)
    if SERVE_RECT.collidepoint(gx, gy):
        game.serve()
        return
    if CLEAR_RECT.collidepoint(gx, gy):
        game.clear_stack()
        return
    for ingredient_id, rect in tray_buttons.items():
        if rect.collidepoint(gx, gy):
            game.add_ingredient(ingredient_id)
            return


def main() -> None:
    pygame.init()
    pygame.display.set_caption("BURGER STOP")
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    game_surf = pygame.Surface((GAME_W, GAME_H))
    clock = pygame.time.Clock()
    font = load_font(8)
    tiny = load_font(8)
    tray_buttons = make_tray_buttons()
    game = Game()
    running = True

    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_click(game, event.pos, tray_buttons)

        game.update(dt)
        draw_scene(game_surf, game, font, tiny, tray_buttons)
        scaled = pygame.transform.scale_by(game_surf, SCALE)
        window.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
