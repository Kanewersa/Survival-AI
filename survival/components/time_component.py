class TimeComponent:
    def __init__(self, minute, hour, day, timer):
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

    def __str__(self):
        return f'Day {self.day}, {self.hour}:{self.minute}'
