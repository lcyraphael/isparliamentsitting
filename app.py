from flask import Flask, render_template
from workalendar.europe import UnitedKingdom
from datetime import datetime, date

cal = UnitedKingdom()
today = date.today()

class recess_period(object):
    def __init__(self,name):
        self.name = name

commons_recess_dates = {
    recess_period("Whitsun"):  ["26 May 2016", "6 June 2016"],
    recess_period("Recess"):   ["15 June 2016", "27 June 2016"],
    recess_period("Summer"):   ["21 July 2016", "5 September 2016"],
    recess_period("Conference"): ["15 September 2016", "10 October 2016"],
    recess_period("November"): ["8 November 2016", "14 November 2016"],
    recess_period("Christmas"):    ["20 December 2016", "9 January 2017"],
    recess_period("February"): ["9 February 2017", "20 February 2017"],
    recess_period("Easter"):   ["30 March 2017", "18 April 2017"],
    recess_period("Whitsun"):  ["25 May 2017", "5 June 2017"],
    recess_period("Summer"): ["20 July 2017", "5 September 2017"],
    recess_period("Conference"): ["14 September 2017", "9 October 2017"],
    recess_period("November"): ["7 November 2017", "13 November 2017"],
    recess_period("Christmas"): ["21 December 2017", "8 January 2018"],
    recess_period("February"): ["8 February 2018", "20 February 2018"],
    recess_period("Easter"):   ["29 March 2018", "16 April 2018"],
    recess_period("May"):   ["3 May 2018", "8 May 2018"],
    recess_period("Whitsun"):  ["24 May 2018", "4 June 2018"],
    recess_period("Summer"): ["24 July 2018", "4 September 2018"],
    recess_period("Conference"): ["13 September 2018", "9 October 2018"],
    recess_period("November"): ["6 November 2018", "12 November 2018"],
    recess_period("Christmas"): ["20 December 2018", "7 January 2019"]
}

lords_recess_dates = {
    recess_period("Whitsun"):  ["26 May 2016", "6 June 2016"],
    recess_period("Referendum"):   ["15 June 2016", "27 June 2016"],
    recess_period("Summer"):   ["21 July 2016", "5 September 2016"],
    recess_period("Summer"): ["15 September 2016", "10 October 2016"],
    recess_period("Autumn"): ["9 November 2016", "15 November 2016"],
    recess_period("Christmas"):    ["21 December 2016", "9 January 2017"],
    recess_period("February"): ["9 February 2017", "20 February 2017"],
    recess_period("Easter"):   ["6 April 2017", "24 April 2017"],
    recess_period("May Bank Holiday"):   ["27 April 2017", "2 May 2017"],
    recess_period("Whitsun"):  ["25 May 2017", "6 June 2017"],
    recess_period("Summer"): ["20 July 2017", "5 September 2017"],
    recess_period("Conference"): ["14 September 2017", "9 October 2017"],
    recess_period("Autumn"): ["7 November 2017", "13 November 2017"],
    recess_period("Christmas"): ["21 December 2017", "8 January 2018"],
    recess_period("February half term"): ["8 February 2018", "20 February 2018"],
    recess_period("Easter"): ["29 March 2018", "16 April 2018"],
    recess_period("May Day"):   ["3 May 2018", "8 May 2018"],
    recess_period("Whitsun"):  ["24 May 2018", "4 June 2018"],
    recess_period("Summer"):  ["24 July 2018", "4 September 2018"],
    recess_period("Summer"):  ["13 September 2018", "9 October 2018"],
    recess_period("Autumn"):  ["6 November 2018", "12 November 2018"]
}

dissolution_dates = {
    recess_period("Dissolution"): ["3 May 2017", "21 June 2017"]
}

def convert_to_dt(recess_dates):
    recess_dates_in_dt = {}
    for recess_period, lst in recess_dates.items():
        recess_pair = []
        for i in lst:
            dt_object = datetime.strptime(i, '%d %B %Y')
            recess_pair.append(datetime.date(dt_object))
        recess_pair = sorted(recess_pair)
        recess_dates_in_dt[recess_period] = recess_pair
    return recess_dates_in_dt

# dictionaries with recess dates as datetime objects
commons_recess = convert_to_dt(commons_recess_dates)
lords_recess = convert_to_dt(lords_recess_dates)
dissolution = convert_to_dt(dissolution_dates)

def is_parliament_dissolved(date):
    sit = {"ans": False}
    for recess_period, dt_pair in dissolution.items():
        if dt_pair[0] < date < dt_pair[1]:
            sit = {"ans": True, "returns_on": dt_pair[1].strftime("%d %B %Y")}
    return sit

def is_commons_sitting(date):
    sit = {"ans": True}
    for recess_period, dt_pair in commons_recess.items():
        if dt_pair[0] < date < dt_pair[1]:
            sit = {"ans": False, "returns_on": dt_pair[1].strftime("%d %B %Y")}
    return sit

def is_lords_sitting(date):
    sit = {"ans": True}
    for recess_period, dt_pair in lords_recess.items():
        if dt_pair[0] < date < dt_pair[1]:
            sit = {"ans": False, "returns_on": dt_pair[1].strftime("%d %B %Y")}
    return sit

def is_parliament_sitting(date):
    commons = is_commons_sitting(date)
    lords = is_lords_sitting(date)
    if is_parliament_dissolved(date)["ans"]:
        sit = {"ans": "No", "info": "Parliament has been dissolved for the General Election. State Opening is scheduled for %s." % is_parliament_dissolved(date)["returns_on"]}
    elif not cal.is_working_day(date):
        sit = {"ans": "No", "info": "Today is not a working day."}
    elif commons["ans"] and lords["ans"]:
        sit = {"ans": "Yes", "info": "Both Houses are sitting. Here are the Orders of Business for the <a href=\"https://www.parliament.uk/business/publications/business-papers/commons/agenda-and-order-of-business\" target=\"_blank\">Commons</a> and <a href=\"https://www.parliament.uk/business/publications/business-papers/lords/lords-business\" target=\"_blank\">Lords</a>."}
    elif commons["ans"] and not lords["ans"]:
        sit = {"ans": "Yes", "info": "Only the House of Commons is sitting (<a href=\"https://www.parliament.uk/business/publications/business-papers/commons/agenda-and-order-of-business\" target=\"_blank\">Order of Business</a>). The House of Lords returns on %s." % lords["returns_on"]}
    elif not commons["ans"] and lords["ans"]:
        sit = {"ans": "Yes", "info": "Only the House of Lords is sitting (<a href=\"https://www.parliament.uk/business/publications/business-papers/lords/lords-business\" target=\"_blank\">Order of Business</a>). The House of Commons returns on %s." % commons["returns_on"]}
    elif commons["returns_on"] == lords["returns_on"]:
        sit = {"ans": "No", "info": "Both Houses have adjourned. They return on %s." % commons["returns_on"]}
    else:
        sit = {"ans": "No", "info": "Both Houses have adjourned. The House of Commons returns on %s and the Lords on %s." % (commons["returns_on"], lords["returns_on"])}
    return sit

sitting = is_parliament_sitting(today)

app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html', data=sitting)

if __name__ == "__main__":
    app.run()
