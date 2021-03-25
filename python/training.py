#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from datetime import date, datetime, timedelta
from trainingplans import trainingplans, REST, RACE
try:
    from icalendar import Calendar
    WITH_ICAL = True
except ImportError:
    print('Running without icalendar support')
    WITH_ICAL = False

DAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
DELTA_WEEK = timedelta(days=7)


def findLengths(training):
    lengths = [3] * len(DAY_NAMES)
    for week in training:
        for i, day in enumerate(week):
            if day == REST:
                continue
            lengths[i] = max(lengths[i], day.width())
    return lengths


def createFormatStr(training):
    lengths = findLengths(training)
    lengths = ['{:' + str(length) + '}' for length in lengths]
    return ' '.join(lengths)


def getRaceWeek(racedate):
    DELTA_DAY = timedelta(days=1)
    # monday = 0, sunday =6
    monday = racedate - DELTA_DAY
    while monday.weekday() != 0:
        monday -= DELTA_DAY
    return monday


def weekToICalGen(week, weeknum, weekdate, startweekday=(11, 30), startweekend=(8, 0)):
    startdate = date(weekdate.year, weekdate.month, weekdate.day)
    for dayofweek, day in enumerate(week):
        descr = str(day).strip()  # be smarter than this
        if descr != REST and descr != RACE:
            yield day.toICalEvent(weeknum=weeknum, startdate=startdate, dayofweek=dayofweek)
        else:
            yield None


def weekToTableGen(week, lengths):
    lengths = ['{:' + str(length) + '}' for length in lengths]
    for day, length in zip(week, lengths):
        yield length.format(str(day))


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
    parser.add_argument('--type', dest='racetype', choices=list(trainingplans.keys()),
                        default='marathon',
                        help='type of race default=%(default)s [%(choices)s]')
    parser.add_argument('--date', type=valid_date, help='date of the race')
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
    lengths = findLengths(training)
    print('{:19}'.format(''), ' '.join(weekToTableGen(DAY_NAMES, lengths)))
    for num, week in enumerate(training):
        weeknum = len(training) - num
        weekdate = raceweek - (weeknum - 1) * DELTA_WEEK

        # this creates the calendar
        if ical is not None:
            for day in weekToICalGen(week, weeknum, weekdate, startweekday=(7, 30)):
                if day is not None:
                    ical.add_component(day)

        # this prints the table version
        label = '{:%Y-%m-%d} Week {:2}:'.format(weekdate, weeknum)
        print(label, ' '.join(weekToTableGen(week, lengths)))

    # write the calendar to disk
    if ical is not None:
        # write to disk
        FILENAME = 'training.ics'
        with open(FILENAME, 'wb') as handle:
            handle.write(ical.to_ical())
        print('Wrote training calendar to "{}"'.format(FILENAME))
