from survival import esper, GameMap
from survival.components.moving_component import MovingComponent
from survival.components.pathfinding_component import PathfindingComponent
from survival.components.position_component import PositionComponent
from survival.components.resource_component import ResourceComponent


class AutomationComponent:
    pass
    # def __init__(self):
    #     self.resources = []


class AutomationSystem(esper.Processor):
    def __init__(self, game_map: GameMap):
        self.game_map = game_map

    def process(self, dt):
        for ent, (automation, pos) in self.world.get_components(AutomationComponent, PositionComponent):
            if self.world.has_component(ent, PathfindingComponent):
                continue

            resource = self.detect_closest_resource(pos, ent)
            if resource is None:
                # TODO: Check if target position is not out of map bounds
                self.world.add_component(ent, PathfindingComponent((pos.grid_position[0] * 32 + 64, pos.grid_position[1] * 32 + 64)))
                # Move somewhere else
            else:
                target = self.world.component_for_entity(resource, PositionComponent).grid_position
                self.world.add_component(ent, PathfindingComponent((target[0] * 32, target[1] * 32), True))
                # Go collect target resource

    def detect_closest_resource(self, position: PositionComponent, target_entity: int):
        entity_position = position.grid_position
        x_range = [entity_position[0] - 5, entity_position[0] + 5]
        y_range = [entity_position[1] - 5, entity_position[1] + 5]

        # Check if range is not out of map bounds
        if x_range[0] < 0:
            x_range[0] = 0
        if x_range[1] >= self.game_map.width:
            x_range[1] = self.game_map.width - 1
        if y_range[0] < 0:
            y_range[0] = 0
        if y_range[1] >= self.game_map.height:
            y_range[1] = self.game_map.height - 1

        found_resource = [-1, 200000]

        for y in range(y_range[0], y_range[1]):
            for x in range(x_range[0], x_range[1]):
                ent = self.game_map.get_entity([x, y])
                if ent == target_entity:
                    continue
                if ent is not None and self.world.has_component(ent, ResourceComponent):
                    res_position = self.world.component_for_entity(ent, PositionComponent).grid_position
                    distance = abs(entity_position[0] - res_position[0]) + abs(entity_position[1] - res_position[1])
                    if found_resource[1] > distance:
                        found_resource = [ent, distance]

        if found_resource[0] == -1:
            return None
        else:
            return found_resource[0]
