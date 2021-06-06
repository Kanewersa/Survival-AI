from survival import esper
from survival.components.position_component import PositionComponent
from survival.components.vision_component import VisionComponent


class VisionSystem(esper.Processor):
    def __init__(self, camera):
        self.camera = camera

    def process(self, dt):
        pos: PositionComponent
        vision: VisionComponent
        for ent, (pos, vision) in self.world.get_components(PositionComponent, VisionComponent):
            vision.update_positions(pos.position)
            self.camera.window.blit(vision.surface_l, self.camera.apply(vision.l_pos))
            self.camera.window.blit(vision.surface_r, self.camera.apply(vision.r_pos))
            self.camera.window.blit(vision.surface_t, self.camera.apply(vision.t_pos))
            self.camera.window.blit(vision.surface_b, self.camera.apply(vision.b_pos))
