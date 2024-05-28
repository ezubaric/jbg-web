
from datetime import datetime
import pandas as pd
import json

class Course:
    def __init__(self):
        None

    def load_holidays(self, path):
        with open(path, 'r') as infile:
            self._noclass = json.loads(infile.read())
        self._noclass = set(datetime.strptime(x, "%Y-%m-%d").date() for x in self._noclass)
        
    def load_json(self, path):
        with open(path, 'r') as infile:
            raw = json.loads(infile.read())
            self._config = raw["config"]
            self._topics = raw["topics"]
            self._class_sequence = raw["class_sequence"]
            self._hw_sequence = raw["hw_sequence"]
            self._specials = raw["specials"]

        self.start = datetime.strptime(raw["config"]["start"], "%Y-%m-%d").date()
        self.end = datetime.strptime(raw["config"]["end"], "%Y-%m-%d").date()
        self.class_days = raw["config"]["days"]
        self.hw_day = raw["config"]["hw_day"]

    def class_dates(self):
        instruction_days = []
        for day in self.class_days:
            instruction_days += list(pd.date_range(self.start, end=self.end, freq=day))

        noclass = [x for x in instruction_days if x in self._noclass]

        homework_days = list(pd.date_range(self.start, end=self.end, freq=self.hw_day))
        homework_days = [x for x in homework_days if x not in self._noclass]

        days = [(x, "INST") for x in instruction_days] + \
               [(x, "HOL") for x in noclass] + \
               [(x, "HW") for x in hw]

               
        
        days.sort()
        return days
        
    def render(self, class_template, hw_template):
        html = ""
        for day, topic in zip(self.class_dates(), self._sequence):
            html += ""
        


if __name__ == "__main__":
    c = Course()
    c.load_holidays("teaching/holidays.json")
    c.load_json("teaching/GRAD_IND/index.json")

    print(c.class_dates())
