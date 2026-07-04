from pyluach import dates

from datetime import datetime
import pandas as pd

from collections import defaultdict

import json

def check_link(address):
    import httplib2
    h = httplib2.Http()
    resp = h.request(address, 'HEAD')
    return int(resp[0]['status']) < 400

class Course:
    def __init__(self):

        self._template = {}
        self._template["class"] = """
        <TR>
           <TD> ~~~DATE~~~ </TD> <TD> ~~~SUBJECT~~~ </TD>
           <TD></TD>
        </TR>

        <TR>
          <TD BGCOLOR="DDDDDD"></TD>
          <TD COLSPAN="3" BGCOLOR="DDDDDD">
              ~~~CONTENT~~~
          </TD>
        </TR>
        """
        
        self._template["homework"] = """
        <TR>
            <TD> ~~~DATE~~~ </TD> <TD> Homework Due </TD> <TD> <A HREF="~~~CONTENT~~~">~~~SUBJECT~~~</TD> <TD></TD>
        </TR>
        """

        self._template["holiday"] = """
        <TR>
          <TD> ~~~DATE~~~ </TD> <TD BGCOLOR="#FF0000"> ~~~SUBJECT~~~ </TD> <TD>   <TD>
        </TD>
        </TR>  

        """


    def load_holidays(self, path):
        with open(path, 'r') as infile:
            self._noclass = json.loads(infile.read())
        self._noclass = dict((datetime.strptime(x[0], "%Y-%m-%d").date(), x[1]) for x in self._noclass)

    def render_topic(self, topic):
        if topic not in self._topics:
            return ""

        html = ""
        for category in self._topics[topic]:
            html += "\t\t<B>%s</B>\n" % category
            html += "\t\t<UL>\n"

            for resource in self._topics[topic][category]:
                try:
                    name, link = resource
                except ValueError:
                    name = resource
                    link = ""

                if link:
                    html += '\t\t\t<LI> <A HREF="%s">%s</A>\n' % (link, name)
                else:
                    html += '\t\t\t<LI> %s\n' % name

            html += '\t\t</UL>\n'

        return html
                
        
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
            contribution = self.date_range(self.start, self.end, day)
            instruction_days += contribution

        noclass = [x for x in instruction_days if x in self._noclass]
        instruction_days = [x for x in instruction_days if x not in self._noclass]
        instruction_days += [datetime.strptime(x, "%Y-%m-%d").date() for x in self._specials]
        
        print(instruction_days)        
        print("NOCLASS", noclass)

        homework_days = self.date_range(self.start, self.end, self.hw_day)
        homework_days = [x for x in homework_days if x not in self._noclass]

        days = [(x, "class") for x in instruction_days] + \
               [(x, "holiday") for x in noclass] + \
               [(x, "homework") for x in homework_days]

        
            
        days.sort()

        day_lookup = defaultdict(dict)

        for day, homework in zip(homework_days, self._hw_sequence):
            if homework is not None:
                day_lookup[day]["homework"] = homework

        for day, lecture_material in zip(sorted(instruction_days), self._class_sequence):
            day_lookup[day]["class"] = lecture_material

        for day in noclass:
            day_lookup[day]["holiday"] = self._noclass[day]
        
        return day_lookup

    def pretty_date(self, day):
        """
        Create 
        """
        
        hebrew = dates.HebrewDate.from_pydate(day)        
        jewish_holiday = hebrew.holiday()

        hebrew_fmt = hebrew.hebrew_date_string()
        gregorian_fmt = day.strftime("%A, %d. %B %Y")
        
        if jewish_holiday:
            template = '<div title="%s">%s [%s]</div>' % (hebrew_fmt, gregorian_fmt, jewish_holiday)
        else:
            template = '<div title="%s">%s</div>' % (hebrew_fmt, gregorian_fmt)
        return template
    
    def render(self):
        html = ""

        days = self.class_dates()
        
        day_keys = list(days.keys())
        day_keys.sort()

        html = ""
        for day in day_keys:
            for element_type in days[day]:
                formatted_date = self.pretty_date(day)

                print(days[day][element_type])
                if days[day][element_type] == "":
                    continue

                try:
                    subject, content = days[day][element_type]
                except ValueError:
                    subject = days[day][element_type]
                    content = ""

                if element_type == "class":
                    content = self.render_topic(content)

                try:
                    contribution = self._template[element_type].replace("~~~SUBJECT~~~", subject)
                    contribution = contribution.replace("~~~DATE~~~", formatted_date)
                    contribution = contribution.replace("~~~CONTENT~~~", content)
                except:
                    print("Contribution got messed up:\n\tSubject: %s\n\tDate: %s\n\t Content: %s" % (subject, formatted_date, content))

                html += contribution
        return html

if __name__ == "__main__":
    from glob import glob
    
    c = Course()
    c.load_holidays("teaching/holidays.json")
    
    for ii in glob("teaching/*/index.json"):
        print("*******\n%s\n*******\n" % ii)
        c.load_json(ii)
        
        print(c.class_dates())

        print(c.render())
