import arcade
from views.level_base import BaseLevel


class Level3(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level3", duration=45.0, player_speed=10.0, attack_speed=8.0, seed=23)

    def build_schedule(self):
        side_interval = 0.32
        line_interval = 2.2

        t = 0.6
        from_left = True
        while t < self.duration:
            y = self.rng.randint(self.box_bottom + 10, self.box_top - 10)
            self.events.append((t, "side", from_left, y))
            from_left = not from_left
            t += side_interval

        t = 1.5
        while t < self.duration:
            x = self.rng.randint(self.box_left + 20, self.box_right - 20)
            self.events.append((t, "vline", x))
            t += line_interval

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "side":
            from_left = event[2]
            y = event[3]
            x = self.box_left - 10 if from_left else self.box_right + 10
            dx = 6 if from_left else -6
            self.spawn_bone_horizontal(y, from_left=from_left, length=26, thickness=8, speed=abs(dx), bone_type="blue")
        elif kind == "vline":
            self.spawn_bone_vertical(event[2], length=140, thickness=10, speed=8, bone_type="white")
