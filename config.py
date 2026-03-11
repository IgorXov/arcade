from pathlib import Path

ROOT_DIR = Path(__file__).parent
ASSETS_DIR = ROOT_DIR / "assets"


def asset_path(*parts: str) -> str:
    return str(ASSETS_DIR.joinpath(*parts))


def lerp_color(color_a, color_b, t: float):
    return (
        int(color_a[0] + (color_b[0] - color_a[0]) * t),
        int(color_a[1] + (color_b[1] - color_a[1]) * t),
        int(color_a[2] + (color_b[2] - color_a[2]) * t),
    )


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SCREEN_TITLE = "CLONEEEE"

PLAYER_SPEED = 4
BATTLE_BOX_WIDTH = 300
BATTLE_BOX_HEIGHT = 200

COLOR_BG_TOP = (24, 20, 40)
COLOR_BG_BOTTOM = (8, 8, 16)
COLOR_ARENA_GLOW = (90, 180, 255, 80)
COLOR_ARENA_OUTLINE = (230, 230, 230)
COLOR_TEXT = (230, 230, 230)
COLOR_TEXT_DIM = (170, 170, 170)
COLOR_ACCENT = (255, 210, 80)
BACKGROUND_STEPS = 36
