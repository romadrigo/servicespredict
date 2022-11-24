import datetime
WEEKDAYS = {'Monday': 1, 'Tuesday': 2, 'Wednesday': 3, 'Thursday': 4, 'Friday': 5, 'Saturday': 6, 'Sunday': 7}

now = datetime.datetime.strptime('2019-10-26', "%Y-%m-%d").date()
day = now.strftime("%A")
print(day)
print(WEEKDAYS[day])