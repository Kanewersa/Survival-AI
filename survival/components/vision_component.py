from pygame import Surface

from survival.settings import AGENT_VISION_RANGE, SCREEN_WIDTH, SCREEN_HEIGHT


class VisionComponent:
    def __init__(self):
        self.agent_vision = AGENT_VISION_RANGE * 32 * 2
        self.width = SCREEN_WIDTH * 2
        self.height = SCREEN_HEIGHT * 2
        self.surface_l = Surface(((self.width - self.agent_vision) / 2, self.height))
        self.surface_r = Surface(((self.width - self.agent_vision) / 2, self.height))
        self.surface_t = Surface((self.agent_vision, (self.height - self.agent_vision) / 2))
        self.surface_b = Surface((self.agent_vision, (self.height - self.agent_vision) / 2))
        self.surface_l.fill((0, 0, 0))
        self.surface_l.set_alpha(200)
        self.surface_r.fill((0, 0, 0))
        self.surface_r.set_alpha(200)
        self.surface_t.fill((0, 0, 0))
        self.surface_t.set_alpha(200)
        self.surface_b.fill((0, 0, 0))
        self.surface_b.set_alpha(200)
        self.l_pos = (0, 0)
        self.r_pos = (0, 0)
        self.t_pos = (0, 0)
        self.b_pos = (0, 0)

    def update_positions(self, position: [int, int]):
        new_position = (position[0] - self.width / 2 + 16, position[1] - self.height / 2 + 16)
        self.l_pos = new_position
        self.r_pos = (new_position[0] + (self.width + self.agent_vision) / 2, new_position[1])
        self.t_pos = (new_position[0] + (self.width - self.agent_vision) / 2, new_position[1])
        self.b_pos = (new_position[0] + (self.width - self.agent_vision) / 2,
                            new_position[1] + (self.height + self.agent_vision) / 2)
