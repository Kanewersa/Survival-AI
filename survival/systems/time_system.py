from survival import esper
from survival.components.time_component import TimeComponent


class TimeSystem(esper.Processor):
    def process(self, dt):
        for ent, time in self.world.get_component(TimeComponent):
            time.timer += dt
            if time.timer > 1000:
                time.add_time(1)
                time.timer = 0
                print(time)
