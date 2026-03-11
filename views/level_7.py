import arcade
from views.level_base import BaseLevel


class Level7(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level7", duration=45.0, player_speed=10.0, attack_speed=9.0, seed=61)

    def build_schedule(self):

        phase1_end = 15.0
        phase2_end = 30.0

        t = 0.6
        while t < phase1_end:
            x = self.rng.randint(self.box_left, self.box_right)
            self.events.append((t, "bone_rain", x))
            t += 0.32

        t = 1.2
        from_left = True
        while t < phase1_end:
            y = self.rng.randint(self.box_bottom + 20, self.box_top - 20)
            self.events.append((t, "sweep", y, from_left))
            from_left = not from_left
            t += 2.6

        t = phase1_end + 0.6
        from_left = True
        while t < phase2_end:
            y = self.rng.randint(self.box_bottom + 20, self.box_top - 20)
            self.events.append((t, "blue_side", from_left, y))
            from_left = not from_left
            t += 0.45

        t = phase1_end + 1.1
        from_left = False
        while t < phase2_end:
            y = self.rng.randint(self.box_bottom + 20, self.box_top - 20)
            self.events.append((t, "orange_side", from_left, y))
            from_left = not from_left
            t += 0.6

        t = phase2_end + 0.6
        while t < self.duration:
            gap_y = self.rng.randint(self.box_bottom + 60, self.box_top - 60)
            from_left = self.rng.choice([True, False])
            self.events.append((t, "wall", gap_y, from_left))
            t += 2.2

        t = phase2_end + 1.2
        while t < self.duration:
            self.events.append((t, "diag_pair"))
            t += 1.9

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "bone_rain":
            self.spawn_bone_vertical(event[2], length=24, thickness=8, speed=self.attack_speed, bone_type="white")
        elif kind == "sweep":
            self.spawn_bone_horizontal(event[2], from_left=event[3], length=200, thickness=10, speed=11, bone_type="white")
        elif kind == "blue_side":
            self.spawn_bone_horizontal(event[3], from_left=event[2], length=30, thickness=8, speed=9, bone_type="blue")
        elif kind == "orange_side":
            self.spawn_bone_horizontal(event[3], from_left=event[2], length=30, thickness=8, speed=9, bone_type="orange")
        elif kind == "wall":
            self.spawn_wall_gap(event[2], event[3], gap_half=50, tile=20, speed=5)
        elif kind == "diag_pair":
            speed = 5.5
            self.spawn_diagonal(self.box_left - 10, self.box_top + 10, speed, -speed, size=12, color=arcade.color.ORANGE)
            self.spawn_diagonal(self.box_right + 10, self.box_bottom - 10, -speed, speed, size=12, color=arcade.color.ORANGE)