#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from collections import namedtuple
from datetime import date, datetime, time, timedelta
from trainingobjs import TrainingItem, toRunItem
try:
    from icalendar import Alarm, Calendar, Event
    WITH_ICAL = True
except ImportError:
    print('Running without icalendar support')
    WITH_ICAL = False

Week = namedtuple('Week', 'mon tue wed thu fri sat sun')
DAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
DELTA_WEEK = timedelta(days=7)
REST = TrainingItem(' - ')
RACE = 'RACE DAY'


def findLengths(training):
    lengths = [3, 3, 3, 3, 3, 3, 3]
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
        # hard code resting on Thursday if there are too many working days
        restThursday = bool(len([item for item in week
                                 if item != REST]) > 5)
        thursday = week.fri
        # TODO need to be smarter about this
        if restThursday:
            thursday = REST
        week = Week(week.tue, week.wed, week.thu, thursday, week.sat,
                    week.sun, REST)
        adjusted.append(week)
    # remove the race from the last week
    week = list(adjusted[-1])
    week[-2] = RACE
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
        line = [toRunItem(item) for item in line.split('\t')[1:]]
        week = Week(*line)
        program.append(week)
    return program


def weekToICalGen(week, weeknum, weekdate, startweekday=(11, 30), startweekend=(8, 0)):
    startdate = date(weekdate.year, weekdate.month, weekdate.day)
    for dayofweek, day in enumerate(week):
        descr = str(day).strip()  # be smarter than this
        if descr != REST and descr != RACE:
            event = Event()

            # add in summary and description
            if dayofweek == 0:
                event.add('summary', 'Week {} - {}'.format(weeknum, day.summary))
            else:
                event.add('summary', day.summary)
            event.add('description', day.description)

            # add in the start
            start = startdate + timedelta(days=dayofweek)
            if dayofweek < 5:  # weekday
                start = datetime.combine(start, time(*startweekday))
            else:  # weekend
                start = datetime.combine(start, time(*startweekend))
            event.add('dtstart', start)

            # add the end
            delta = day.toTimeDelta()
            if delta is not None:
                event.add('dtend', start + delta)

            # add the alarm
            if delta is not None and dayofweek < 5:  # weekday
                alarm = Alarm()
                alarm.add('ACTION', 'DISPLAY')
                alarm.add('DESCRIPTION', 'REMINDER')
                alarm.add('TRIGGER', timedelta(minutes=-15))
                event.add_component(alarm)

            yield event
        else:
            yield None


def weekToTableGen(week, lengths):
    lengths = ['{:' + str(length) + '}' for length in lengths]
    for day, length in zip(week, lengths):
        yield length.format(str(day))


# half ironman training
# https://www.triathlete.com/training/super-simple-ironman-70-3-triathlon-training-plan/

# all the following are tab delimited
races = {'marathon':  # https://www.halhigdon.com/training-programs/marathon-training/intermediate-2-marathon/
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
17	Cross	4 mi run	6 mi run	4 mi run	Rest	4 mi run	8 miles
18	Cross	3 mi run	4 mi run	Rest	Rest	2 mi run	Marathon
''',  # noqa: E128
'half':  # https://www.halhigdon.com/training-programs/half-marathon-training/intermediate-1-half-marathon/
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
''',
'half-n2':  # https://www.halhigdon.com/training-programs/half-marathon-training/novice-2-half-marathon/
'''
1 	60 min cross	Rest 	3 mi run 	3 mi run 	3 mi run 	Rest 	4 mi run
2 	60 min cross	Rest 	3 mi run 	3 mi pace 	3 mi run 	Rest 	5 mi run
3 	60 min cross	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	6 mi run
4 	60 min cross	Rest 	3 mi run 	4 mi pace 	3 mi run 	Rest 	7 mi run
5 	60 min cross	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	8 mi run
6 	60 min cross	Rest 	3 mi run 	4 mi pace 	3 mi run 	Rest 	5-K Race
7 	60 min cross	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	9 mi run
8 	60 min cross	Rest 	3 mi run 	5 mi pace 	3 mi run 	Rest 	10 mi run
9 	60 min cross	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	10-K Race
10 	60 min cross	Rest 	3 mi run 	5 mi pace 	3 mi run 	Rest 	11 mi run
11 	60 min cross	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	12 mi run
12  	Rest	Rest 	3 mi run 	2 mi pace 	2 mi run 	Rest  	Half Marathon
'''}

# metric century training program
# https://www.endurancemag.com/2014/05/cycling-8-week-metric-training-plan/
bike = {'century':
        [Week(REST, TrainingItem('Bike 60 min', 'Easy ride of 60 minutes at your own pace'),  # week 1
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 20 easy, 20 hard, 20 easy'),
              REST, TrainingItem('Bike 20 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', 'Easy ride of 60 minutes'),  # week 2
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 20 easy, 20 hard, 20 easy'),
              REST, TrainingItem('Bike 24 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills'),  # week 3
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 15 easy, 30 hard, 15 easy'), REST,
              TrainingItem('Bike 30 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills'),  # week 4
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 15 easy, 30 hard, 15 easy'),
              REST, TrainingItem('Bike 34 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills, pushing the last 20 minutes'),  # week 5
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 15 easy, 30 hard, 15 easy'),
              REST, TrainingItem('Bike 41 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills, pushing the last 20 minutes'),  # week 6
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 10 easy, 10 hard, 3 repetitions'),
              REST, TrainingItem('Bike 46 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills, pushing the last 30 minutes'),  # week 7
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 10 easy, 10 hard, 3 repetitions'),
              REST, TrainingItem('Bike 54 miles'), REST),
         Week(REST, TrainingItem('Bike 60 min', '60-minute ride with hills, pushing the last 30 minutes'),  # wkk 8
              REST, TrainingItem('Bike 60 min', 'Bike 60 min - 10 easy, 10 hard, 3 repetitions'),
              REST, TrainingItem(RACE),
              REST)]}  # Bike metric century


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
    race_names = list(races.keys())
    race_names.extend(list(bike.keys()))
    parser.add_argument('--type', dest='racetype', choices=race_names,
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
    if options.racetype in races:
        training = parseHal(races[options.racetype])
        # trim it down to five days per week
        training = toFiveDays(training)
    elif options.racetype in bike:
        training = bike[options.racetype]

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
