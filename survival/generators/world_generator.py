from survival import esper, PlayerGenerator, ResourceGenerator, SCREEN_WIDTH, SCREEN_HEIGHT, GameMap, \
    Camera
from survival.components.consumption_component import ConsumptionComponent
from survival.components.direction_component import DirectionChangeComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.learning_component import LearningComponent
from survival.components.moving_component import MovingComponent
from survival.components.pathfinding_component import PathfindingComponent
from survival.components.position_component import PositionComponent
from survival.components.resource_component import ResourceComponent
from survival.components.time_component import TimeComponent
from survival.esper import World
from survival.generators.resource_type import ResourceType
from survival.settings import PLAYER_START_POSITION, STARTING_RESOURCES_AMOUNT
from survival.systems.automation_system import AutomationSystem
from survival.systems.camera_system import CameraSystem
from survival.systems.collision_system import CollisionSystem
from survival.systems.consumption_system import ConsumptionSystem
from survival.systems.direction_system import DirectionSystem
from survival.systems.draw_system import DrawSystem
from survival.systems.input_system import InputSystem
from survival.systems.movement_system import MovementSystem
from survival.systems.neural_system import NeuralSystem
from survival.systems.time_system import TimeSystem
from survival.systems.vision_system import VisionSystem


class WorldGenerator:
    def __init__(self, win, callback):
        self.win = win
        self.callback = callback
        self.world: World = esper.World()
        self.game_map: GameMap = GameMap(int(SCREEN_WIDTH / 32) * 2, 2 * int(SCREEN_HEIGHT / 32) + 1)
        self.camera = Camera(self.game_map.width * 32, self.game_map.height * 32, self.win)
        self.resource_generator: ResourceGenerator = ResourceGenerator(self.world, self.game_map)
        self.player: int = -1

    def create_world(self):
        self.world.add_processor(InputSystem(self.camera, self.game_map))
        self.world.add_processor(CameraSystem(self.camera))
        self.world.add_processor(MovementSystem(self.game_map), priority=20)
        self.world.add_processor(CollisionSystem(self.game_map), priority=30)
        self.world.add_processor(NeuralSystem(self.game_map, self.callback), priority=50)
        self.world.add_processor(DrawSystem(self.camera))
        self.world.add_processor(TimeSystem())
        self.world.add_processor(AutomationSystem(self.game_map))
        # self.world.add_processor(PathfindingMovementSystem(self.game_map), priority=40)
        self.world.add_processor(DirectionSystem())
        self.world.add_processor(ConsumptionSystem(self.callback))
        self.world.add_processor(VisionSystem(self.camera))

        self.player = PlayerGenerator().create_player(self.world, self.game_map)
        self.world.get_processor(DrawSystem).initialize_interface(
            self.world.component_for_entity(self.player, InventoryComponent))

        # BuildingGenerator().create_home(self.world, self.game_map)
        self.resource_generator.generate_resources(self.player)
        return self.game_map, self.world, self.camera

    def reset_world(self):
        for processor in self.world.processors:
            processor.reset()

        self.reset_player()
        self.reset_resources()

    def reset_resources(self):
        for entity in self.world.entities:
            if self.world.has_component(entity, ResourceComponent):
                self.game_map.remove_entity(self.world.component_for_entity(entity, PositionComponent).grid_position)
                self.world.delete_entity(entity)
                continue
        self.resource_generator.generate_resources(self.player)

    def reset_player(self):
        self.world.remove_component(self.player, TimeComponent)
        self.world.add_component(self.player, TimeComponent())

        inv = self.world.component_for_entity(self.player, InventoryComponent)
        inv.clear()
        for resource in ResourceType:
            inv.add_item(resource, STARTING_RESOURCES_AMOUNT)

        if self.world.has_component(self.player, ConsumptionComponent):
            self.world.remove_component(self.player, ConsumptionComponent)
            self.world.add_component(self.player, ConsumptionComponent(inv.total_items_count()))

        pos = self.world.component_for_entity(self.player, PositionComponent)
        old_pos = pos.grid_position

        self.world.remove_component(self.player, PositionComponent)
        self.world.add_component(self.player,
                                 PositionComponent([PLAYER_START_POSITION[0] * 32, PLAYER_START_POSITION[1] * 32],
                                                   PLAYER_START_POSITION))

        self.game_map.move_entity(old_pos, pos.grid_position)

        if self.world.has_component(self.player, MovingComponent):
            self.world.remove_component(self.player, MovingComponent)
        if self.world.has_component(self.player, DirectionChangeComponent):
            self.world.remove_component(self.player, DirectionChangeComponent)
        if self.world.has_component(self.player, PathfindingComponent):
            self.world.remove_component(self.player, PathfindingComponent)
        if self.world.has_component(self.player, LearningComponent):
            learning = self.world.component_for_entity(self.player, LearningComponent)
            learning.reset()
