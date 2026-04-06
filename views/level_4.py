import arcade
from views.level_base import BaseLevel


class Level4(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level4", duration=45.0, player_speed=10.0, attack_speed=7.0, seed=31)

    def build_schedule(self):
        diag_interval = 2.2
        burst_interval = 3.6
        ring_interval = 4.2

        t = 0.8
        while t < self.duration:
            self.events.append((t, "diag_burst"))
            t += diag_interval

        t = 1.6
        while t < self.duration:
            self.events.append((t, "center_burst"))
            t += burst_interval

        t = 2.0
        while t < self.duration:
            self.events.append((t, "ring", 10, 4.6))
            t += ring_interval

        t = 12.0
        angle = 0.0
        while t < 22.0:
            self.events.append((t, "spiral", angle))
            t += 0.25
            angle += 0.55

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "diag_burst":
            speed = 6
            self.spawn_diagonal(self.box_left - 10, self.box_bottom - 10, speed, speed, size=12, color=arcade.color.ORANGE)
            self.spawn_diagonal(self.box_left - 10, self.box_top + 10, speed, -speed, size=12, color=arcade.color.ORANGE)
            self.spawn_diagonal(self.box_right + 10, self.box_bottom - 10, -speed, speed, size=12, color=arcade.color.ORANGE)
            self.spawn_diagonal(self.box_right + 10, self.box_top + 10, -speed, -speed, size=12, color=arcade.color.ORANGE)
        elif kind == "center_burst":
            speed = 4.5
            cx = (self.box_left + self.box_right) / 2
            cy = (self.box_bottom + self.box_top) / 2
            directions = [
                (1, 0), (-1, 0), (0, 1), (0, -1),
                (1, 1), (1, -1), (-1, 1), (-1, -1),
            ]
            for dx, dy in directions:
                self.spawn_diagonal(cx, cy, dx * speed, dy * speed, size=10, color=arcade.color.YELLOW)
        elif kind == "ring":
            cx = (self.box_left + self.box_right) / 2
            cy = (self.box_bottom + self.box_top) / 2
            self.spawn_radial(cx, cy, count=event[2], speed=event[3], size=10, bone_type="white")
        elif kind == "spiral":
            cx = (self.box_left + self.box_right) / 2
            cy = (self.box_bottom + self.box_top) / 2
            self.spawn_spiral_shot(cx, cy, event[2], speed=5.2, size=9, bone_type="white")