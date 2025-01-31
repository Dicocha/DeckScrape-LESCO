import math
import datetime


class AnkiService:
    def __init__(self, total_words, days=7):
        self.total_words = total_words
        self.days = days
        self.words_per_day = math.ceil(total_words / days)

    def get_schedule(self):
        schedule = {}
        today = datetime.date.today()
        for i in range(self.days):
            day = today + datetime.timedelta(days=i)
            schedule[day.strftime("%Y-%m-%d")] = self.words_per_day
        return schedule
