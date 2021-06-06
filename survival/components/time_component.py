class TimeComponent:
    def __init__(self, minute=0, hour=0, day=0, timer=0):
        self.minute = minute
        self.hour = hour
        self.day = day
        self.timer = timer

    def add_time(self, minutes):
        self.minute += minutes
        if self.minute >= 60:
            temp = self.minute - 60
            self.hour += 1
            if self.hour >= 24:
                temp2 = self.hour - 24
                self.day += 1
                self.hour = temp2
            self.minute = temp

    def total_minutes(self):
        return self.minute + self.hour * 60 + self.day * 1440

    def __str__(self):
        return f'Day {self.day}, {self.hour}:{self.minute}'

    def __eq__(self, other):
        return self.total_minutes() == other.total_minutes()

    def __gt__(self, other):
        return self.total_minutes() > other.total_minutes()

    def __lt__(self, other):
        return self.total_minutes() < other.total_minutes()
