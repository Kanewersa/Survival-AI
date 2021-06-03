from survival import esper
from survival.systems.automation_system import AutomationSystem
from survival.systems.camera_system import CameraSystem
from survival.systems.collection_system import ResourceCollectionSystem
from survival.systems.collision_system import CollisionSystem
from survival.systems.direction_system import DirectionSystem
from survival.systems.draw_system import DrawSystem
from survival.systems.input_system import InputSystem
from survival.systems.movement_system import MovementSystem
from survival.systems.pathfinding_movement_system import PathfindingMovementSystem
from survival.systems.time_system import TimeSystem


class WorldGenerator:

    def create_world(self, camera, game_map):
        world = esper.World()
        world.add_processor(InputSystem(camera, game_map))
        world.add_processor(CameraSystem(camera))
        world.add_processor(MovementSystem(game_map), priority=2)
        world.add_processor(CollisionSystem(game_map), priority=3)
        world.add_processor(DrawSystem(camera))
        world.add_processor(ResourceCollectionSystem(), priority=1)
        world.add_processor(TimeSystem())
        world.add_processor(AutomationSystem(game_map))
        world.add_processor(PathfindingMovementSystem(game_map), priority=4)
        world.add_processor(DirectionSystem())

        return world
