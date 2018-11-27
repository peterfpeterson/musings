#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from collections import namedtuple
from datetime import date, datetime, timedelta
try:
    from icalendar import Calendar, Event
    WITH_ICAL=True
except ImportError:
    print('Running without icalendar support')
    WITH_ICAL=False

Week = namedtuple('Week', 'mon tue wed thu fri sat sun')
DELTA_WEEK = timedelta(days=7)
REST = ' - '

def standardize(stuff):
    stuff = stuff.strip()
    if stuff.lower() == 'rest':
        return REST
    stuff = stuff.replace('mi run', 'miles')
    stuff = stuff.replace('mi pace', 'miles pace')
    stuff = stuff.replace('-K Race', ' km race')
    stuff = stuff.replace('Half Marathon', 'Half marathon')
    return stuff

def findLengths(training):
    lengths = [3,3,3,3,3,3,3]
    for week in training:
        for i, day in enumerate(week):
            lengths[i] = max(lengths[i], len(day))
    return lengths

def createFormatStr(training):
    lengths = findLengths(training)
    lengths = ['{:' + str(length) + '}' for length in lengths]
    return ' '.join(lengths)

def toFiveDays(training):
    adjusted = []
    for week in training:
        # TODO need to be smarter about this
        week = Week(week.tue, week.wed, week.thu, REST, week.sat, week.sun, REST)
        adjusted.append(week)
    # remove the race from the last week
    week = list(adjusted[-1])
    week[-2] = 'RACE DAY'
    adjusted[-1] = Week(*week)
    return adjusted

def getRaceWeek(racedate):
    DELTA_DAY = timedelta(days=1)
    # monday = 0, sunday =6
    monday = racedate - DELTA_DAY
    while monday.weekday() != 0:
        monday -= DELTA_DAY
    return monday

def parseHal(raw):
    program = []
    for line in raw.split('\n'):
        line = line.strip()
        if not line:
            continue
        line = [standardize(item) for item in line.split('\t')]
        week = Week(*line[1:])
        program.append(week)
    return program

def toICalendar(training):
    calendar = Calendar()

    event = {'summary':'magic summary test',
             'description':'not so magical description',
             'dtstart':date(2018,11,9)}
    event = Event(**event)

    calendar.add_component(event)
    return calendar

def weekToICalGen(week, weeknum, weekdate):
    startdate = date(weekdate.year, weekdate.month, weekdate.day)
    for dayofweek, day in enumerate(week):
        if day.strip() != REST.strip():
            event = {'summary':day,
                     'description':day,
                     'dtstart':startdate + timedelta(days=dayofweek)}
            if dayofweek == 0:
                event['summary'] = 'Week {} - {}'.format(weeknum, day)
            yield Event(**event)
        else:
            yield None

def weekToTableGen(week, lengths):
    lengths = ['{:' + str(length) + '}' for length in lengths]
    for day, length in zip(week, lengths):
        yield length.format(day)

races = {'marathon': #https://www.halhigdon.com/training-programs/marathon-training/intermediate-2-marathon/
'''
1	Cross	3 mi run	5 mi run	3 mi run	Rest	5 mi pace	10 miles
2	Cross	3 mi run	5 mi run	3 mi run	Rest	5 mi run	11 miles
3	Cross	3 mi run	6 mi run	3 mi run	Rest	6 mi pace	8 miles
4	Cross	3 mi run	6 mi run	3 mi run	Rest	6 mi pace	13 miles
5	Cross	3 mi run	7 mi run	3 mi run	Rest	7 mi run	14 miles
6	Cross	3 mi run	7 mi run	3 mi run	Rest	7 mi pace	10 miles
7	Cross	4 mi run	8 mi run	4 mi run	Rest	8 mi pace	16 miles
8	Cross	4 mi run	8 mi run	4 mi run	Rest	8 mi run	17 miles
9	Cross	4 mi run	9 mi run	4 mi run	Rest	Rest	Half Marathon
10	Cross	4 mi run	9 mi run	4 mi run	Rest	9 mi pace	19 miles
11	Cross	5 mi run	10 mi run	5 mi run	Rest	10 mi run	20 miles
12	Cross	5 mi run	6 mi run	5 mi run	Rest	6 mi pace	12 miles
13	Cross	5 mi run	10 mi run	5 mi run	Rest	10 mi pace	20 miles
14	Cross	5 mi run	6 mi run	5 mi run	Rest	6 mi run	12 miles
15	Cross	5 mi run	10 mi run	5 mi run	Rest	10 mi pace	20 miles
16	Cross	5 mi run	8 mi run	5 mi run	Rest	4 mi pace	12 miles
17	Cross	4 mi run	6 mi run	4 mi run	Rest	4 mi run	8
18	Cross	3 mi run	4 mi run	Rest	Rest	2 mi run	Marathon
''',
'half': #https://www.halhigdon.com/training-programs/half-marathon-training/intermediate-1-half-marathon/
'''
1	30 min cross	3 mi run	4 mi run	3 mi run	Rest	3 mi run	4 mi run
2	30 min cross	3 mi run	4 mi pace	3 mi run	Rest	3 mi pace	5 mi run
3	40 min cross	3.5 mi run	5 mi run	3.5 mi run	Rest	Rest	6 mi run
4	40 min cross	3.5 mi run	5 mi pace	3.5 mi run	Rest	3 mi run	7 mi run
5	40 min cross	4 mi run	6 mi run	4 mi run	Rest	3 mi pace	8 mi run
6	50 min cross	4 mi run	6 mi pace	4 mi run	Rest or easy run	Rest	5-K Race
7	Rest	4.5 mi run	7 mi run	4.5 mi run	Rest	4 mi pace	9 mi run
8	50 min cross	4.5 mi run	7 mi pace	4.5 mi run	Rest	5 mi pace	10 mi run
9	60 min cross	5 mi run	8 mi run	5 mi run	Rest or easy run	Rest	10-K Race
10	Rest	5 mi run	8 mi pace	5 mi run	Rest	5 mi pace	11 mi run
11	60 min cross	5 mi run	6 mi run	4 mi run	Rest	3 mi pace	12 mi run
12	Rest	4 mi run	4 mi pace	2 mi run	Rest	Rest	Half Marathon
'''}

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
    parser.add_argument('--type', dest='racetype', choices=['marathon', 'full', 'half'], default='marathon',
                        help='type of race default=%(default)s')
    parser.add_argument('--date', type=valid_date, help='date of the race')

    # parse the command line
    options = parser.parse_args()
    if options.racetype == 'full':
        options.racetype = 'marathon'

    if options.date is None:
        parser.error('--date is required')
    raceweek = getRaceWeek(options.date)

    # create the training program
    training = parseHal(races[options.racetype])

    # trim it down to five days per week
    training = toFiveDays(training)

    # trim down the training weeks as appropriate
    today = datetime.today()
    weeks_util_race = float((options.date - today).days) / 7.
    weeks_util_training = float((options.date - today - DELTA_WEEK*len(training)).days) / 7.
    print('{:4.1f} weeks until the race'.format(weeks_util_race))
    if weeks_util_training > 0:
        print('{:4.1f} weeks until training starts'.format(weeks_util_training))
    else:
        print('training has already started, trimming to the last {} weeks'.format(int(weeks_util_race)+1))
        training = training[-1*int(weeks_util_race)-1:]

    ical = None if not WITH_ICAL else Calendar()

    # print the results
    lengths = findLengths(training)
    print('{:19}'.format(''), ' '.join(weekToTableGen(('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'), lengths)))
    for num, week in enumerate(training):
        weeknum = len(training) - num
        weekdate = raceweek - (weeknum - 1) * DELTA_WEEK

        # this creates the calendar
        if ical is not None:
            for day in weekToICalGen(week, weeknum, weekdate):
                if day is not None:
                    ical.add_component(day)

        # this prints the table version
        label = '{:%Y-%m-%d} Week {:2}:'.format(weekdate, weeknum)
        print(label, ' '.join(weekToTableGen(week, lengths)))

    # write the calendar to disk
    if ical is not None:
        # write to disk
        filename = 'training.ics'
        with open(filename, 'wb') as handle:
            handle.write(ical.to_ical())
        print('Wrote training calendar to "{}"'.format(filename))
