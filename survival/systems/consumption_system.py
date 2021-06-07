from survival import esper
from survival.components.consumption_component import ConsumptionComponent
from survival.components.inventory_component import InventoryComponent
from survival.components.learning_component import LearningComponent
from survival.generators.resource_type import ResourceType


class ConsumptionSystem(esper.Processor):
    def __init__(self, callback):
        self.callback = callback

    def process(self, dt):
        for ent, (cons, inventory) in self.world.get_components(ConsumptionComponent, InventoryComponent):
            cons.timer -= dt
            if cons.timer > 0:
                continue
            cons.timer = cons.timer_value

            if self.world.has_component(ent, LearningComponent):
                # If no item was picked up
                if cons.last_inventory_state == inventory.total_items_count():
                    learning: LearningComponent = self.world.component_for_entity(ent, LearningComponent)
                    learning.reward += -10
                    learning.done = True
                cons.last_inventory_state = inventory.total_items_count()
            else:
                if inventory.has_item(ResourceType.FOOD):
                    inventory.remove_item(ResourceType.FOOD, 1)
                else:
                    self.callback()
