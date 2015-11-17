from datetime import datetime, timedelta

# returns the earliest following date, based on a day (1=monday, 7=sunday)
# offset of 1 day, because saving 0 is hard for Odoo
def _get_next_date_for_day(dt, day):
    #day = 1 (monday), dt.weekday() = 1 (tuesday), days ahead = -1, return 6
    days_ahead = day - dt.weekday() - 1 # difference in count weekday days ahead = 0
    if days_ahead < 1: # Target day already happened this week
        days_ahead += 7 # days ahead = 8
    return dt + timedelta(days_ahead)

# same as _get_next_date_for_day, but always returns a date in the future
def _get_future_next_date_for_day(olddt, day): #olddt = datetime.datetime(2015, 11, 23, 13, 32, 47), day = 4
    now = datetime.utcnow()
    if now >= olddt:
        while(now >= olddt):
            olddt = _get_next_date_for_day(olddt, day)
        return olddt
    return _get_next_date_for_day(olddt, day)
