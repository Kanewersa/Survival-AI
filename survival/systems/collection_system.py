from survival import esper
from survival.components.direction_component import DirectionChangeComponent
from survival.components.moving_component import MovingComponent
from survival.components.position_component import PositionComponent
from survival.graph_search import Action
from survival.systems.pathfinding_movement_system import CollectingResourceComponent


class ResourceCollectionSystem(esper.Processor):
    def __init__(self):
        pass

    def process(self, dt):
        for ent, (collect, pos) in self.world.get_components(CollectingResourceComponent, PositionComponent):
            if self.world.has_component(ent, MovingComponent) or self.world.has_component(ent, DirectionChangeComponent):
                continue

            if collect.action == Action.MOVE:
                self.world.remove_component(ent, CollectingResourceComponent)
                self.world.add_component(ent, MovingComponent())
