#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from datetime import datetime, timedelta
from trainingplans import trainingplans
try:
    from icalendar import Calendar  # type: ignore
    WITH_ICAL = True
except ImportError:
    print('Running without icalendar support')
    WITH_ICAL = False

DELTA_WEEK = timedelta(days=7)


def getRaceWeek(racedate):
    DELTA_DAY = timedelta(days=1)
    # monday = 0, sunday =6
    monday = racedate - DELTA_DAY
    while monday.weekday() != 0:
        monday -= DELTA_DAY
    return monday


# ####################################################################
# tips on swimming technique
# https://www.californiatriathlon.org/swim-workouts/
# https://www.snackinginsneakers.com/12-week-olympic-triathlon-training-plan/
# ####################################################################

if __name__ == '__main__':
    def valid_date(s):
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    # set up optparse
    import argparse     # for command line options
    parser = argparse.ArgumentParser(description='Create training schedule')
    parser.add_argument('-t', '--type', dest='racetype', choices=list(trainingplans.keys()),
                        default='marathon',
                        help='type of race default=%(default)s [%(choices)s]')
    parser.add_argument('-d', '--date', type=valid_date, help='date of the race')
    # TODO add option to set start time on weekdays

    # parse the command line
    options = parser.parse_args()
    if options.racetype == 'full':
        options.racetype = 'marathon'
    if options.date is None:
        parser.error('--date is required')
    raceweek = getRaceWeek(options.date)

    # create the training program
    training = trainingplans[options.racetype]

    # trim down the training weeks as appropriate
    today = datetime.today()
    weeks_util_race = float((options.date - today).days) / 7.
    weeks_util_training = float((options.date - today - DELTA_WEEK*len(training)).days) / 7.
    print('{:4.1f} weeks until the race'.format(weeks_util_race))
    if weeks_util_training > 0:
        print('{:4.1f} weeks until training starts'.format(weeks_util_training))
    else:
        print('training has already started, '
              'trimming to the last {} weeks'.format(int(weeks_util_race)+1))
        training = training[-1*int(weeks_util_race)-1:]

    ical = None if not WITH_ICAL else Calendar()

    # print the results
    print(training[0].tableHeader())
    for num, week in enumerate(training):
        weeknum = len(training) - num
        weekdate = raceweek - (weeknum - 1) * DELTA_WEEK

        # this creates the calendar
        if ical is not None:
            for day in week.toICalGen(weeknum, weekdate, startweekday=(7, 30)):
                if day is not None:
                    ical.add_component(day)

        # this prints the table version
        print(week.tableRows(weekdate, weeknum))

    # write the calendar to disk
    if ical is not None:
        # write to disk
        FILENAME = 'training.ics'
        with open(FILENAME, 'wb') as handle:
            handle.write(ical.to_ical())
        print('Wrote training calendar to "{}"'.format(FILENAME))
