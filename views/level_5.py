import math
from views.level_base import BaseLevel


class Level5(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level5", duration=45.0, player_speed=10.0, attack_speed=9.0, seed=41)

    def build_schedule(self):
        block_interval = 0.55
        wall_interval = 1.4

        t = 0.5
        while t < self.duration:
            x = self.rng.randint(self.box_left, self.box_right)
            self.events.append((t, "bone", x))
            t += block_interval

        t = 0.9
        i = 0
        while t < self.duration:
            mid = (self.box_bottom + self.box_top) / 2
            amp = self.box_height * 0.35
            gap_y = mid + amp * math.sin(i * 0.6)
            from_left = (i % 2 == 0)
            self.events.append((t, "wall", gap_y, from_left))
            t += wall_interval
            i += 1

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "bone":
            self.spawn_bone_vertical(event[2], length=24, thickness=8, speed=self.attack_speed, bone_type="white")
        elif kind == "wall":
            self.spawn_wall_gap(event[2], event[3], gap_half=45, tile=20, speed=5)
