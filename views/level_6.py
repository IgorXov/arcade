import math
import arcade
from views.level_base import BaseLevel


class Level6(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level6", duration=45.0, player_speed=10.0, attack_speed=8.0, seed=53)

    def build_schedule(self):
        gap_interval = 1.2
        sweep_interval = 3.0

        t = 0.7
        i = 0
        while t < self.duration:
            mid = (self.box_left + self.box_right) / 2
            amp = self.box_width * 0.35
            gap_x = mid + amp * math.sin(i * 0.7)
            self.events.append((t, "hgap", gap_x))
            t += gap_interval
            i += 1

        t = 1.5
        from_left = True
        while t < self.duration:
            y = self.rng.randint(self.box_bottom + 20, self.box_top - 20)
            self.events.append((t, "sweep", y, from_left))
            from_left = not from_left
            t += sweep_interval

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "hgap":
            self.spawn_horizontal_gap(event[2], gap_width=90, bar_height=10, speed=7)
        elif kind == "sweep":
            self.spawn_bone_horizontal(event[2], from_left=event[3], length=180, thickness=8, speed=10, bone_type="white")
