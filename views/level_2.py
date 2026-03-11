import arcade
from views.level_base import BaseLevel


class Level2(BaseLevel):

    def __init__(self):
        super().__init__(level_key="level2", duration=45.0, player_speed=10.0, attack_speed=9.0, seed=17)

    def build_schedule(self):
        lanes = 5
        margin = 40
        spacing = (self.box_width - margin * 2) / (lanes - 1)
        lane_x = [self.box_left + margin + i * spacing for i in range(lanes)]

        block_interval = 0.3
        sweep_interval = 2.8

        t = 0.4
        last_lane = -1
        while t < self.duration:
            lane = self.rng.randint(0, lanes - 1)
            if lane == last_lane and lanes > 1:
                lane = (lane + self.rng.randint(1, lanes - 1)) % lanes
            last_lane = lane
            self.events.append((t, "lane_bone", lane_x[lane]))
            t += block_interval

        t = 1.2
        from_left = True
        while t < self.duration:
            y = self.rng.randint(self.box_bottom + 30, self.box_top - 30)
            self.events.append((t, "sweep", y, from_left))
            from_left = not from_left
            t += sweep_interval

        self.events.sort(key=lambda e: e[0])

    def spawn_event(self, event):
        kind = event[1]
        if kind == "lane_bone":
            self.spawn_bone_vertical(event[2], length=26, thickness=8, speed=self.attack_speed, bone_type="white")
        elif kind == "sweep":
            self.spawn_bone_horizontal(event[2], from_left=event[3], length=220, thickness=10, speed=11, bone_type="white")
