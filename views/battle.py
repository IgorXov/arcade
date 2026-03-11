import random
import arcade
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

BATTLE_DURATION = 30.0
INVUL_DURATION = 2.5


class BattleView(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.box_width = 400
        self.box_height = 300
        self.box_center_x = SCREEN_WIDTH // 2
        self.box_center_y = SCREEN_HEIGHT // 2

        self.box_left = self.box_center_x - self.box_width / 2
        self.box_bottom = self.box_center_y - self.box_height / 2
        self.box_right = self.box_left + self.box_width
        self.box_top = self.box_bottom + self.box_height

        self.soul = arcade.Sprite(asset_path("player", "soul.png"), scale=1.0)
        self.soul.center_x = self.box_center_x
        self.soul.center_y = self.box_center_y

        self.soul_list = arcade.SpriteList()
        self.soul_list.append(self.soul)

        self.soul_speed = 6

        self.hp = 3
        self.invul_time = 0.0
        self.hit_flash_timer = 0.0
        self.result_recorded = False

        self.hit_sound = arcade.load_sound(asset_path("sounds", "hit.mp3"))
        self.sound_ready = self.hit_sound is not None

        self.lines = arcade.SpriteList()
        self.projectiles = arcade.SpriteList()
        self.walls = arcade.SpriteList()
        self.particles = arcade.SpriteList()

        self.attack_pattern = ["line", "projectile", "wall"]
        self.attack_index = 0

        self.elapsed_time = 0.0
        self.spawn_timer = 0.0
        self.spawn_interval = 0.25

        self.timer_text = arcade.Text(
            "",
            SCREEN_WIDTH - 160,
            SCREEN_HEIGHT - 40,
            COLOR_TEXT,
            18
        )

        self.stars = []
        for _ in range(60):
            self.stars.append({
                "x": random.uniform(0, SCREEN_WIDTH),
                "y": random.uniform(0, SCREEN_HEIGHT),
                "r": random.uniform(1.0, 2.5),
                "a": random.randint(60, 140),
                "tw": random.uniform(0.4, 1.2),
            })

    def on_draw(self):
        self.clear()
        self.draw_background()

        arcade.draw_lbwh_rectangle_filled(
            self.box_left - 4,
            self.box_bottom - 4,
            self.box_width + 8,
            self.box_height + 8,
            COLOR_ARENA_GLOW,
        )

        arcade.draw_lbwh_rectangle_outline(
            self.box_left,
            self.box_bottom,
            self.box_width,
            self.box_height,
            COLOR_ARENA_OUTLINE,
            3,
        )

        self.lines.draw()
        self.projectiles.draw()
        self.walls.draw()
        self.particles.draw()

        if self.invul_time <= 0 or int(self.invul_time * 10) % 2 == 0:
            self.soul_list.draw()

        arcade.draw_text(
            f"HP: {self.hp}",
            20,
            SCREEN_HEIGHT - 40,
            COLOR_ACCENT,
            20
        )
        self.timer_text.draw()

        if self.hit_flash_timer > 0:
            alpha = int(120 * (self.hit_flash_timer / 0.12))
            arcade.draw_lrbt_rectangle_filled(
                0,
                SCREEN_WIDTH,
                0,
                SCREEN_HEIGHT,
                (255, 255, 255, max(0, min(120, alpha)))
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

        self.elapsed_time += delta_time
        self.invul_time = max(0.0, self.invul_time - delta_time)
        self.spawn_timer += delta_time
        self.hit_flash_timer = max(0.0, self.hit_flash_timer - delta_time)

        remaining = max(0, int(BATTLE_DURATION - self.elapsed_time))
        self.timer_text.text = f"Time: {remaining}"

        if self.elapsed_time >= BATTLE_DURATION:
            if not self.result_recorded:
                record_win("battle", BATTLE_DURATION)
                self.result_recorded = True
            from views.overworld import OverworldView
            self.window.show_view(OverworldView())
            return

        if self.hp <= 0:
            if not self.result_recorded:
                record_loss("battle", self.elapsed_time)
                self.result_recorded = True
            from views.overworld import OverworldView
            self.window.show_view(OverworldView())
            return

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_attack()
            self.spawn_timer = 0.0

        self.lines.update(delta_time)
        self.projectiles.update(delta_time)
        self.walls.update(delta_time)
        self.soul_list.update(delta_time)

        half_w = self.soul.width / 2
        half_h = self.soul.height / 2

        self.soul.center_x = max(
            self.box_left + half_w,
            min(self.box_right - half_w, self.soul.center_x)
        )

        self.soul.center_y = max(
            self.box_bottom + half_h,
            min(self.box_top - half_h, self.soul.center_y)
        )

        for p in list(self.particles):
            p.center_x += p.change_x * delta_time
            p.center_y += p.change_y * delta_time
            p.alpha -= 200 * delta_time
            if p.alpha <= 0:
                p.remove_from_sprite_lists()

        if self.invul_time <= 0:
            if (
                arcade.check_for_collision_with_list(self.soul, self.lines) or
                arcade.check_for_collision_with_list(self.soul, self.projectiles) or
                arcade.check_for_collision_with_list(self.soul, self.walls)
            ):
                self.hp -= 1
                self.invul_time = INVUL_DURATION
                self.hit_flash_timer = 0.12
                if self.sound_ready:
                    arcade.play_sound(self.hit_sound)
                self.spawn_particles()

        for spr_list in [self.lines, self.projectiles, self.walls]:
            for obj in list(spr_list):
                if (
                    obj.center_x < self.box_left - 100 or
                    obj.center_x > self.box_right + 100 or
                    obj.center_y < self.box_bottom - 100
                ):
                    obj.remove_from_sprite_lists()

        for star in self.stars:
            star["a"] += star["tw"] * delta_time * 60
            if star["a"] > 160 or star["a"] < 50:
                star["tw"] *= -1

    def spawn_attack(self):

        attack_type = self.attack_pattern[self.attack_index]
        self.attack_index = (self.attack_index + 1) % len(self.attack_pattern)

        if attack_type == "line":
            self.spawn_line()
        elif attack_type == "projectile":
            self.spawn_projectile()
        elif attack_type == "wall":
            self.spawn_wall()

    def spawn_line(self):
        line = arcade.SpriteSolidColor(200, 8, arcade.color.CYAN)
        line.center_x = self.box_left - 100
        line.center_y = random.uniform(self.box_bottom + 20, self.box_top - 20)
        line.change_x = 20
        self.lines.append(line)

    def spawn_projectile(self):
        proj = arcade.SpriteSolidColor(14, 14, arcade.color.YELLOW)
        proj.center_x = random.uniform(self.box_left, self.box_right)
        proj.center_y = self.box_top + 50
        proj.change_y = -25
        self.projectiles.append(proj)

    def spawn_wall(self):

        gap_size = 50
        wall_width = 5

        gap_y = random.uniform(
            self.box_bottom + gap_size,
            self.box_top - gap_size
        )

        top_wall = arcade.SpriteSolidColor(
            wall_width,
            self.box_top - (gap_y + gap_size / 2),
            arcade.color.WHITE
        )

        bottom_wall = arcade.SpriteSolidColor(
            wall_width,
            (gap_y - gap_size / 2) - self.box_bottom,
            arcade.color.WHITE
        )

        for wall in (top_wall, bottom_wall):
            wall.center_x = self.box_right + 10
            wall.change_x = -20

        top_wall.center_y = self.box_top - top_wall.height / 2
        bottom_wall.center_y = self.box_bottom + bottom_wall.height / 2

        self.walls.append(top_wall)
        self.walls.append(bottom_wall)

    def spawn_particles(self):
        for _ in range(10):
            p = arcade.SpriteSolidColor(4, 4, arcade.color.WHITE)
            p.center_x = self.soul.center_x
            p.center_y = self.soul.center_y
            p.change_x = random.uniform(-80, 80)
            p.change_y = random.uniform(-80, 80)
            p.alpha = 255
            self.particles.append(p)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.soul.change_y = self.soul_speed
        elif key == arcade.key.S:
            self.soul.change_y = -self.soul_speed
        elif key == arcade.key.A:
            self.soul.change_x = -self.soul_speed
        elif key == arcade.key.D:
            self.soul.change_x = self.soul_speed

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.soul.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.soul.change_x = 0
