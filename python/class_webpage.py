
from datetime import datetime
import pandas as pd

from collections import defaultdict

import json

class Course:
    def __init__(self):
        None

    def load_holidays(self, path):
        with open(path, 'r') as infile:
            self._noclass = json.loads(infile.read())
        self._noclass = dict((datetime.strptime(x[0], "%Y-%m-%d").date(), x[1]) for x in self._noclass)
        
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

    @staticmethod
    def date_range(start, stop, day):
        days = list(pd.date_range(start, end=stop, freq=day))
        return [x.to_pydatetime().date() for x in days]
        
    def class_dates(self):
        instruction_days = []

        for day in self.class_days:
            instruction_days += self.date_range(self.start, self.end, day)

        print(instruction_days, self._noclass)
        noclass = [x for x in instruction_days if x in self._noclass]
        print("NOCLASS", noclass)

        homework_days = self.date_range(self.start, self.end, self.hw_day)
        homework_days = [x for x in homework_days if x not in self._noclass]

        days = [(x, "INST") for x in instruction_days] + \
               [(x, "HOL") for x in noclass] + \
               [(x, "HW") for x in homework_days]
            
        days.sort()

        day_lookup = defaultdict(dict)

        for day, homework in zip(homework_days, self._hw_sequence):
            if homework is not None:
                day_lookup[day]["HW"] = homework

        for day, lecture_material in zip(instruction_days, self._class_sequence):
            day_lookup[day]["INST"] = lecture_material

        for day in noclass:
            day_lookup[day]["HOL"] = self._noclass[day]
        
        return day_lookup
        
    def render(self, class_template, hw_template, hol_template):
        html = ""

        days = self.class_dates()
        
        day_keys = days.keys()
        day_keys.sort()

        for day in day_keys:
            for element_type in days:
                if element_type == "INST":
                    html += ""
                elif element_type == "HW":
                    html += ""
                elif element_type == "HOL":
                    html += ""
        return html

if __name__ == "__main__":
    c = Course()
    c.load_holidays("teaching/holidays.json")
    c.load_json("teaching/GRAD_IND/index.json")

    print(c.class_dates())
