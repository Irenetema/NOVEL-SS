# This software was created by Oregon State University under Army Research
# Office (ARO) Award Number W911NF-22-2-0149. ARO, as the Federal awarding
# agency, reserves a royalty-free, nonexclusive and irrevocable right to
# reproduce, publish, or otherwise use this software for Federal purposes, and
# to authorize others to do so in accordance with 2 CFR 200.315(b).

from astral import LocationInfo
from astral.sun import sun
from datetime import datetime, timedelta, date, time


def partition_capture_time(dt, city):
    assert isinstance(dt, datetime)

    s = sun(city.observer, date=dt.date(), tzinfo=city.timezone)
    dawn = s['dawn']
    dusk = s['dusk']
    sunset = s['sunset']
    sunrise = s['sunrise']

    start_day_time = (sunrise + timedelta(hours=1)).time()
    end_day_time = (sunset - timedelta(hours=1)).time()

    start_dusk_time = sunset.time()
    end_dusk_time = (dusk + timedelta(minutes=30)).time()

    start_night_time = (dusk + timedelta(hours=1)).time()
    end_night_time = (dawn - timedelta(hours=1)).time()

    start_dawn_time = (dawn - timedelta(minutes=30)).time()
    end_dawn_time = sunrise.time()

    if start_day_time <= dt.time() < end_day_time:
        return 'day'
    elif start_dusk_time <= dt.time() < end_dusk_time:
        return 'dusk'
    elif start_night_time <= dt.time() <= time(hour=23, minute=59, second=59) or time(
            hour=0) <= dt.time() < end_night_time:
        return 'night'
    elif start_dawn_time <= dt.time() < end_dawn_time:
        return 'dawn'
    else:
        # not used
        return 'skip'
    
