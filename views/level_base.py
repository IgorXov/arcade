import arcade
import math
import random
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    asset_path,
    lerp_color,
    COLOR_BG_TOP,
    COLOR_BG_BOTTOM,
    COLOR_ARENA_GLOW,
    COLOR_ARENA_OUTLINE,
    COLOR_TEXT,
    COLOR_ACCENT,
    BACKGROUND_STEPS,
)
from stats import record_win, record_loss

DESPAWN_MARGIN = 60
INVUL_DURATION = 2.5

BONE_COLORS = {
    "white": arcade.color.WHITE,
    "blue": (0, 170, 255),
    "orange": (255, 170, 0),
}

BONE_RULES = {
    "white": "always",
    "blue": "blue",
    "orange": "orange",
}


class BaseLevel(arcade.View):

    def __init__(
        self,
        level_key: str,
        duration: float = 45.0,
        player_speed: float = 10.0,
        attack_speed: float = 10.0,
        seed: int = 7,
    ):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.level_key = level_key
        self.duration = duration
        self.player_speed = player_speed
        self.attack_speed = attack_speed

        # arena bounds
        self.box_left = SCREEN_WIDTH // 2 - 200
        self.box_right = SCREEN_WIDTH // 2 + 200
        self.box_bottom = 80
        self.box_top = 380
        self.box_width = self.box_right - self.box_left
        self.box_height = self.box_top - self.box_bottom

        # soul setup
        self.soul = arcade.Sprite(asset_path("player", "soul.png"), scale=1)
        self.soul.center_x = SCREEN_WIDTH // 2
        self.soul.center_y = 150

        self.soul_list = arcade.SpriteList()
        self.soul_list.append(self.soul)

        self.attacks = arcade.SpriteList()
        self.particles = arcade.SpriteList()

        # state flags
        self.max_hp = 5
        self.hp = 5
        self.game_over = False
        self.result = None
        self.result_recorded = False
        self.hit_flash_timer = 0.0
        self.invul_time = 0.0

        self.level_timer = 0.0

        # screen shake
        self.shake_timer = 0.0
        self.shake_strength = 0

        # pause menu
        self.paused = False
        self.pause_selected = 0

        self.hp_text = arcade.Text(
            f"HP: {self.hp}",
            30,
            SCREEN_HEIGHT - 40,
            COLOR_ACCENT,
            20
        )

        self.timer_text = arcade.Text(
            "",
            SCREEN_WIDTH - 150,
            SCREEN_HEIGHT - 40,
            COLOR_TEXT,
            20
        )

        self.win_text = arcade.Text(
            "YOU WIN\nPress SPACE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            COLOR_ACCENT,
            40,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400
        )

        self.lose_text = arcade.Text(
            "GAME OVER\nPress SPACE",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.RED,
            40,
            anchor_x="center",
            anchor_y="center",
            multiline=True,
            width=400
        )

        self.pause_title_text = arcade.Text(
            "PAUSED",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2 + 80,
            COLOR_TEXT,
            32,
            anchor_x="center",
            anchor_y="center",
        )
        self.pause_menu_items = ["Restart Level", "Main Menu"]

        # hit sound
        self.hit_sound = None
        self.sound_ready = False
        try:
            self.hit_sound = arcade.load_sound(asset_path("sounds", "hit.mp3"))
            self.sound_ready = True
        except Exception:
            self.sound_ready = False

        # starfield
        self.star_rng = random.Random(seed + 1000)
        self.stars = []
        for _ in range(70):
            self.stars.append({
                "x": self.star_rng.uniform(0, SCREEN_WIDTH),
                "y": self.star_rng.uniform(0, SCREEN_HEIGHT),
                "r": self.star_rng.uniform(1.0, 2.2),
                "a": self.star_rng.randint(60, 140),
                "tw": self.star_rng.uniform(0.4, 1.2),
            })

        # event schedule
        self.rng = random.Random(seed)
        self.events = []
        self.event_index = 0
        self.build_schedule()

    def build_schedule(self):
        raise NotImplementedError

    def spawn_event(self, event):
        raise NotImplementedError

    def on_draw(self):
        self.clear()
        self.draw_background()

        offset_x = 0
        offset_y = 0

        if self.shake_timer > 0:
            offset_x = random.randint(-self.shake_strength, self.shake_strength)
            offset_y = random.randint(-self.shake_strength, self.shake_strength)

        arcade.draw_lrbt_rectangle_filled(
            self.box_left - 4 + offset_x,
            self.box_right + 4 + offset_x,
            self.box_bottom - 4 + offset_y,
            self.box_top + 4 + offset_y,
            COLOR_ARENA_GLOW,
        )

        arcade.draw_lrbt_rectangle_outline(
            self.box_left + offset_x,
            self.box_right + offset_x,
            self.box_bottom + offset_y,
            self.box_top + offset_y,
            COLOR_ARENA_OUTLINE,
            border_width=3
        )

        self.attacks.draw()
        self.particles.draw()

        # blink invul
        if self.invul_time <= 0 or int(self.invul_time * 10) % 2 == 0:
            self.soul_list.draw()

        self.hp_text.draw()
        self.timer_text.draw()

        if self.game_over:
            if self.result == "win":
                self.win_text.draw()
            else:
                self.lose_text.draw()

        if self.hit_flash_timer > 0:
            alpha = int(120 * (self.hit_flash_timer / 0.12))
            arcade.draw_lrbt_rectangle_filled(
                0,
                SCREEN_WIDTH,
                0,
                SCREEN_HEIGHT,
                (255, 255, 255, max(0, min(120, alpha)))
            )

        if self.paused:
            self.draw_pause_menu()

    def draw_pause_menu(self):
        arcade.draw_lrbt_rectangle_filled(
            0,
            SCREEN_WIDTH,
            0,
            SCREEN_HEIGHT,
            (0, 0, 0, 180)
        )
        self.pause_title_text.draw()

        base_y = SCREEN_HEIGHT // 2 + 10
        for i, text in enumerate(self.pause_menu_items):
            color = COLOR_ACCENT if i == self.pause_selected else COLOR_TEXT
            arcade.draw_text(
                text,
                SCREEN_WIDTH // 2,
                base_y - i * 36,
                color,
                22,
                anchor_x="center",
                anchor_y="center",
            )

    def draw_background(self):
        step_h = SCREEN_HEIGHT / BACKGROUND_STEPS
        for i in range(BACKGROUND_STEPS):
            t = i / max(1, BACKGROUND_STEPS - 1)
            color = lerp_color(COLOR_BG_BOTTOM, COLOR_BG_TOP, t)
            arcade.draw_lrbt_rectangle_filled(
                0,
                SCREEN_WIDTH,
                i * step_h,
                (i + 1) * step_h,
                color
            )

        for star in self.stars:
            arcade.draw_circle_filled(
                star["x"],
                star["y"],
                star["r"],
                (255, 255, 255, star["a"])
            )

    def on_update(self, delta_time):
        if self.paused or self.game_over:
            return

        self.level_timer += delta_time
        remaining = max(0, int(self.duration - self.level_timer))
        self.timer_text.text = f"Time: {remaining}"

        if self.level_timer >= self.duration:
            self.game_over = True
            if not self.result_recorded:
                self.result = "win"
                record_win(self.level_key, self.duration)
                self.result_recorded = True
            return

        if self.shake_timer > 0:
            self.shake_timer -= delta_time

        self.hit_flash_timer = max(0.0, self.hit_flash_timer - delta_time)
        self.invul_time = max(0.0, self.invul_time - delta_time)

        self.soul_list.update()
        self.attacks.update()
        self.particles.update()

        # arena clamp
        half_w = self.soul.width / 2
        half_h = self.soul.height / 2

        self.soul.center_x = max(
            self.box_left + half_w,
            min(self.soul.center_x, self.box_right - half_w)
        )

        self.soul.center_y = max(
            self.box_bottom + half_h,
            min(self.soul.center_y, self.box_top - half_h)
        )

        # event spawn
        while self.event_index < len(self.events) and self.level_timer >= self.events[self.event_index][0]:
            self.spawn_event(self.events[self.event_index])
            self.event_index += 1

        for attack in list(self.attacks):
            if (
                attack.top < self.box_bottom - DESPAWN_MARGIN or
                attack.bottom > self.box_top + DESPAWN_MARGIN or
                attack.right < self.box_left - DESPAWN_MARGIN or
                attack.left > self.box_right + DESPAWN_MARGIN
            ):
                attack.remove_from_sprite_lists()

        for p in list(self.particles):
            p.alpha -= 12
            if p.alpha <= 0:
                p.remove_from_sprite_lists()

        # damage check
        if self.invul_time <= 0:
            hit_list = arcade.check_for_collision_with_list(self.soul, self.attacks)
            damage_taken = False
            for obj in hit_list:
                if self.should_take_damage(obj):
                    damage_taken = True
                    obj.remove_from_sprite_lists()
            if damage_taken:
                self.hp -= 1
                self.hp_text.text = f"HP: {self.hp}"
                self.spawn_particles(self.soul.center_x, self.soul.center_y)
                self.shake_timer = 0.2
                self.shake_strength = 8
                self.hit_flash_timer = 0.12
                self.invul_time = INVUL_DURATION
                if self.sound_ready:
                    arcade.play_sound(self.hit_sound)

        if self.hp <= 0:
            self.game_over = True
            if not self.result_recorded:
                self.result = "lose"
                record_loss(self.level_key, self.level_timer)
                self.result_recorded = True

        for star in self.stars:
            star["a"] += star["tw"] * delta_time * 60
            if star["a"] > 160 or star["a"] < 50:
                star["tw"] *= -1

    # bone rules
    def is_player_moving(self):
        return abs(self.soul.change_x) > 0 or abs(self.soul.change_y) > 0

    def should_take_damage(self, attack):
        rule = getattr(attack, "damage_rule", "always")
        if rule == "blue":
            return self.is_player_moving()
        if rule == "orange":
            return not self.is_player_moving()
        return True

    def apply_bone_rule(self, sprite, bone_type: str):
        rule = BONE_RULES.get(bone_type, "always")
        sprite.damage_rule = rule

    # spawn helpers
    def spawn_block(self, x, y=None, size=15, dx=0, dy=None, color=arcade.color.WHITE):
        block = arcade.SpriteSolidColor(size, size, color)
        block.center_x = x
        block.center_y = y if y is not None else self.box_top + size
        block.change_x = dx
        block.change_y = dy if dy is not None else -self.attack_speed
        self.attacks.append(block)

    def spawn_bone_horizontal(
        self,
        y,
        length=180,
        thickness=8,
        from_left=True,
        speed=12,
        bone_type="white",
    ):
        color = BONE_COLORS.get(bone_type, arcade.color.WHITE)
        line = arcade.SpriteSolidColor(length, thickness, color)
        if from_left:
            line.center_x = self.box_left - length / 2
            line.change_x = speed
        else:
            line.center_x = self.box_right + length / 2
            line.change_x = -speed
        line.center_y = y
        self.apply_bone_rule(line, bone_type)
        self.attacks.append(line)

    def spawn_bone_vertical(
        self,
        x,
        length=180,
        thickness=8,
        from_top=True,
        speed=12,
        bone_type="white",
    ):
        color = BONE_COLORS.get(bone_type, arcade.color.WHITE)
        line = arcade.SpriteSolidColor(thickness, length, color)
        if from_top:
            line.center_y = self.box_top + length / 2
            line.change_y = -speed
        else:
            line.center_y = self.box_bottom - length / 2
            line.change_y = speed
        line.center_x = x
        self.apply_bone_rule(line, bone_type)
        self.attacks.append(line)

    def spawn_radial(self, center_x, center_y, count=12, speed=5.0, size=10, bone_type="white"):
        color = BONE_COLORS.get(bone_type, arcade.color.WHITE)
        for i in range(count):
            angle = (math.pi * 2 * i) / count
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            proj = arcade.SpriteSolidColor(size, size, color)
            proj.center_x = center_x
            proj.center_y = center_y
            proj.change_x = dx
            proj.change_y = dy
            self.apply_bone_rule(proj, bone_type)
            self.attacks.append(proj)

    def spawn_spiral_shot(self, center_x, center_y, angle, speed=5.0, size=10, bone_type="white"):
        color = BONE_COLORS.get(bone_type, arcade.color.WHITE)
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        proj = arcade.SpriteSolidColor(size, size, color)
        proj.center_x = center_x
        proj.center_y = center_y
        proj.change_x = dx
        proj.change_y = dy
        self.apply_bone_rule(proj, bone_type)
        self.attacks.append(proj)

    def spawn_wall_gap(self, gap_y, from_left, gap_half=40, tile=20, speed=4):
        for y in range(self.box_bottom, self.box_top, tile):
            if gap_y - gap_half < y < gap_y + gap_half:
                continue

            wall = arcade.SpriteSolidColor(tile, tile, arcade.color.WHITE)
            if from_left:
                wall.center_x = self.box_left - tile
                wall.change_x = speed
            else:
                wall.center_x = self.box_right + tile
                wall.change_x = -speed
            wall.center_y = y
            self.attacks.append(wall)

    def spawn_line_horizontal(
        self,
        y,
        from_left=True,
        length=200,
        thickness=8,
        speed=12,
        color=arcade.color.CYAN,
    ):
        line = arcade.SpriteSolidColor(length, thickness, color)
        if from_left:
            line.center_x = self.box_left - length / 2
            line.change_x = speed
        else:
            line.center_x = self.box_right + length / 2
            line.change_x = -speed
        line.center_y = y
        self.attacks.append(line)

    def spawn_line_vertical(
        self,
        x,
        from_top=True,
        length=200,
        thickness=8,
        speed=12,
        color=arcade.color.CYAN,
    ):
        line = arcade.SpriteSolidColor(thickness, length, color)
        if from_top:
            line.center_y = self.box_top + length / 2
            line.change_y = -speed
        else:
            line.center_y = self.box_bottom - length / 2
            line.change_y = speed
        line.center_x = x
        self.attacks.append(line)

    def spawn_horizontal_gap(self, gap_x, gap_width=80, bar_height=8, speed=6):
        left_width = max(0, gap_x - gap_width / 2 - self.box_left)
        right_width = max(0, self.box_right - (gap_x + gap_width / 2))

        if left_width > 0:
            left_bar = arcade.SpriteSolidColor(int(left_width), bar_height, arcade.color.WHITE)
            left_bar.center_x = self.box_left + left_width / 2
            left_bar.center_y = self.box_top + bar_height
            left_bar.change_y = -speed
            self.attacks.append(left_bar)

        if right_width > 0:
            right_bar = arcade.SpriteSolidColor(int(right_width), bar_height, arcade.color.WHITE)
            right_bar.center_x = (gap_x + gap_width / 2) + right_width / 2
            right_bar.center_y = self.box_top + bar_height
            right_bar.change_y = -speed
            self.attacks.append(right_bar)

    def spawn_diagonal(self, x, y, dx, dy, size=12, color=arcade.color.YELLOW):
        proj = arcade.SpriteSolidColor(size, size, color)
        proj.center_x = x
        proj.center_y = y
        proj.change_x = dx
        proj.change_y = dy
        self.attacks.append(proj)

    def spawn_particles(self, x, y):
        for _ in range(20):
            p = arcade.SpriteSolidColor(6, 6, arcade.color.RED)
            p.center_x = x
            p.center_y = y
            p.change_x = random.uniform(-3, 3)
            p.change_y = random.uniform(-3, 3)
            self.particles.append(p)

    # input handling
    def on_key_press(self, key, modifiers):
        if self.paused:
            if key == arcade.key.UP:
                self.pause_selected = (self.pause_selected - 1) % len(self.pause_menu_items)
            elif key == arcade.key.DOWN:
                self.pause_selected = (self.pause_selected + 1) % len(self.pause_menu_items)
            elif key == arcade.key.ENTER:
                if self.pause_selected == 0:
                    self.window.show_view(self.__class__())
                else:
                    from views.overworld import OverworldView
                    self.window.show_view(OverworldView())
            elif key == arcade.key.ESCAPE:
                self.paused = False
            return

        if self.game_over:
            if key == arcade.key.SPACE:
                from views.level_select import LevelSelectView
                self.window.show_view(LevelSelectView())
            return

        if key == arcade.key.ESCAPE:
            self.paused = True
            return

        if key == arcade.key.W:
            self.soul.change_y = self.player_speed
        elif key == arcade.key.S:
            self.soul.change_y = -self.player_speed
        elif key == arcade.key.A:
            self.soul.change_x = -self.player_speed
        elif key == arcade.key.D:
            self.soul.change_x = self.player_speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.soul.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.soul.change_x = 0