from survival import esper
from survival.systems.camera_system import CameraSystem
from survival.systems.collision_system import CollisionSystem
from survival.systems.draw_system import DrawSystem
from survival.systems.input_system import InputSystem
from survival.systems.movement_system import MovementSystem
from survival.systems.time_system import TimeSystem


class WorldGenerator:

    def create_world(self, camera, game_map):
        world = esper.World()
        world.add_processor(InputSystem())
        world.add_processor(CameraSystem(camera))
        world.add_processor(MovementSystem(), priority=1)
        world.add_processor(CollisionSystem(game_map), priority=2)
        world.add_processor(DrawSystem(camera))
        world.add_processor(TimeSystem())

        return world
