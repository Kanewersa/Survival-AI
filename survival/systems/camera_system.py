from survival import esper
from survival.components.camera_target_component import CameraTargetComponent
from survival.components.position_component import PositionComponent


class CameraSystem(esper.Processor):
    def __init__(self, camera):
        self.camera = camera

    def process(self, dt):
        for ent, (camera_target, pos) in self.world.get_components(CameraTargetComponent, PositionComponent):
            self.camera.update(pos)
