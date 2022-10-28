import datetime


def get_current_academic_week():
    academic_year_start_week = datetime.date(datetime.date.today().year, 9, 1).isocalendar()[1]

    current_date = datetime.datetime.now()
    current_year_week = current_date.isocalendar()[1]

    current_academic_week = current_year_week - academic_year_start_week + 1 # +1 т.к. отсчёт с нуля
    return current_academic_week