from views.level_base import BaseLevel


class Level1(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level1", duration=45.0, player_speed=10.0, attack_speed=10.0, seed=7)

    def build_schedule(self):
        block_interval = 0.35
        wall_interval = 1.8

        t = 0.5
        while t < self.duration:
            x = self.rng.randint(self.box_left, self.box_right)
            self.events.append((t, "bone", x))
            t += block_interval

        t = 1.0
        while t < self.duration:
            gap_y = self.rng.randint(self.box_bottom + 50, self.box_top - 50)
            from_left = self.rng.choice([True, False])
            self.events.append((t, "wall", gap_y, from_left))
            t += wall_interval

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "bone":
            self.spawn_bone_vertical(event[2], length=28, thickness=8, speed=self.attack_speed, bone_type="white")
        elif kind == "wall":
            self.spawn_wall_gap(event[2], event[3], gap_half=40, tile=20, speed=4)
