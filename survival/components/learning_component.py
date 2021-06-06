from survival.components.time_component import TimeComponent


class LearningComponent:
    def __init__(self):
        self.made_step = False
        self.old_state = None
        self.action = None
        self.resource = None

        self.reward = 0
        self.done = False
        self.score = 0
        self.record = 0

    def load_step(self, old_state, action, resource):
        self.old_state = old_state
        self.action = action
        if resource is None:
            self.resource = None
        else:
            self.resource = resource
        self.made_step = True

    def reset(self):
        self.made_step = False
        self.old_state = None
        self.action = None
        self.resource = None

        self.reward = 0
        self.done = False
