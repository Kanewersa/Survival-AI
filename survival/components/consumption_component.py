class ConsumptionComponent:
    def __init__(self, inventory_state=0):
        self.timer_value: float = 2000
        self.timer: float = self.timer_value
        self.last_inventory_state = inventory_state
