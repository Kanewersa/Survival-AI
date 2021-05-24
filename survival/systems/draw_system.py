from survival import esper
from survival.components.position_component import PositionComponent
from survival.components.sprite_component import SpriteComponent
from survival.user_interface import UserInterface


class DrawSystem(esper.Processor):
    def __init__(self, camera):
        self.camera = camera
        self.ui = None

    def initialize_interface(self, inventory):
        self.ui = UserInterface(self.camera.window, inventory)

    def process(self, dt):
        for ent, (sprite, pos) in self.world.get_components(SpriteComponent, PositionComponent):
            sprite.image.pos = pos.position
            sprite.image.origin = (32 * pos.direction.value, 0)
            self.camera.draw(sprite.image)
            self.ui.update()
            self.ui.draw()
