#!/usr/bin/env python
from __future__ import (absolute_import, division, print_function)
from collections import namedtuple
from datetime import date, datetime, time, timedelta
import pytest
try:
    from icalendar import Alarm, Event
    WITH_ICAL = True
except ImportError:
    print('Testing without icalendar support')
    WITH_ICAL = False

Week = namedtuple('Week', 'mon tue wed thu fri sat sun')
DAY_NAMES = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
DELTA_WEEK = timedelta(days=7)
REST = ' - '
RACE = 'RACE DAY'


class TrainingItem:
    def __init__(self, summary: str, description: str = ''):
        self.summary = summary
        if description:
            self.description = description
        else:
            self.description = str(summary)  # copy the summary

    def __str__(self):
        return self.summary

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.summary)

    def __eq__(self, other):
        # check the summaries
        try:
            if self.summary.strip() != other.summary.strip():
                return False
        except AttributeError:
            if self.summary.strip() != str(other).strip():
                return False
        # check the descriptions
        try:
            if self.description.strip() != other.description.strip():
                return False
        except AttributeError:
            if self.description.strip() != str(other).strip():
                return False

        # they must be the same if it got here
        return True

    def width(self, minimum: int = 3) -> int:
        '''The width of the summary in characters. This is intended for use in printing to the console'''
        return max(len(self.summary.strip()), minimum)

    def __speedInMinutes(self) -> float:
        '''generate speed in minutes per mile'''
        description = self.summary.lower()

        if 'run' in description or 'marathon' in description or 'km race' in description:
            speed = 10.  # 10 minute mile
        elif 'swim' in description:
            speed = 60.  # 1 mph
        elif 'bike' in description:
            speed = 4.  # 15 mph
        else:
            msg = 'Do not have speed for activity "{}"'.format(description)
            raise RuntimeError(msg)

        return speed

    def __toDistanceInMiles(self) -> float:
        '''Convert description to distance in miles'''
        def toFloat(text: str) -> float:
            text = text.lower().replace('run', '').replace('swim', '').replace('bike', '')
            for item in text.split():
                return float(item)
            raise ValueError('failed to convert "{}" to float'.format(text))

        description = self.summary.lower()
        if description.startswith('half'):
            distance = 13.1
        elif description == 'marathon':
            distance = 26.2
        elif 'km' in description:
            # this only appears to be a running event
            distance = toFloat(description) / 1.602
        elif 'metric century' in description:
            distance = 62.
        elif 'century' in description:
            distance = 100.
        else:
            distance = toFloat(description)

        return distance

    def toTimeDelta(self):
        # first try simple static values
        if 'Rest' == self.summary or '-' == self.summary.strip():
            return timedelta(hours=0, minutes=0)
        elif 'min' in self.summary:
            descr = self.summary[:self.summary.index('min')].strip()
            descr = descr.split(' ')[-1]
            return timedelta(hours=0, minutes=int(descr))
        elif 'hour' in self.summary:
            descr = self.summary[:self.summary.index('hour')].strip()
            descr = descr.split(' ')[-1]
            return timedelta(hours=int(descr), minutes=0)
        elif 'cross' in self.summary.lower():
            return timedelta(hours=0, minutes=30)

        # convert the input into something useful
        speed = self.__speedInMinutes()
        distance = self.__toDistanceInMiles()

        minutes = distance*speed
        # print('{} x {} = 0h{}m'.format(distance, int(speed), int(minutes)))
        hours = max(int(minutes)//int(60), 1)
        minutes = max(0., minutes-hours*60.)

        # print('         = {}h{}m'.format(hours, int(minutes)))
        if minutes != 0. and minutes != 30.:
            # round up to the nearest half hour
            if minutes > 30.:
                hours += 1
                minutes = 0.
            elif minutes > 0.:
                minutes = 30.
        # print('         = {}h{}m'.format(hours, int(minutes)))

        return timedelta(hours=hours, minutes=minutes)

    def toICalEvent(self, startdate, dayofweek: int, weeknum: int = 0):
        if not WITH_ICAL:
            raise RuntimeError('Not configured with icalnedar support')

        startweekday = (7, 30)
        startweekend = (8, 0)

        event = Event()
        # add in summary and description
        if dayofweek == 0:
            event.add('summary', 'Week {} - {}'.format(weeknum, self.summary))
        else:
            event.add('summary', self.summary)
        event.add('description', self.description)

        # add in the start
        start = startdate + timedelta(days=dayofweek)
        if dayofweek < 5:  # weekday
            start = datetime.combine(start, time(*startweekday))
        else:  # weekend
            start = datetime.combine(start, time(*startweekend))
        event.add('dtstart', start)

        # add the end
        delta = self.toTimeDelta()
        if delta is not None:
            event.add('dtend', start + delta)

        # add the alarm
        if delta is not None and dayofweek < 5:  # weekday
            alarm = Alarm()
            alarm.add('ACTION', 'DISPLAY')
            alarm.add('DESCRIPTION', 'REMINDER')
            alarm.add('TRIGGER', timedelta(minutes=-15))
            event.add_component(alarm)

        return event


def toRunItem(stuff: str):
    '''Convert some of the random text to standard text'''
    stuff = stuff.strip()
    if stuff.lower() == 'rest':
        return REST
    stuff = stuff.replace('mi run', 'miles')
    stuff = stuff.replace('mi pace', 'miles pace')
    stuff = stuff.replace('-K Race', ' km race')
    stuff = stuff.replace('Half Marathon', 'Half marathon')
    if 'marathon' in stuff.lower() or 'race' in stuff or 'bike' in stuff.lower():
        pass  # TODO should reverse the check
    else:
        stuff = 'Run ' + stuff
    return TrainingItem(stuff)


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


def toDistanceInMiles(description) -> float:
    '''Convert description to distance in miles'''
    def toFloat(text: str) -> float:
        text = text.lower().replace('run', '').replace('swim', '').replace('bike', '')
        for item in text.split():
            return float(item)
        raise ValueError('failed to convert "{}" to float'.format(text))

    description = str(description)
    if description.lower().startswith('half'):
        distance = 13.1
    elif description.lower() == 'marathon':
        distance = 26.2
    elif 'km' in description:
        # this only appears to be a running event
        distance = 1.602 * toFloat(description)
    else:
        distance = toFloat(description)

    return distance


def toTimeDelta(description):
    # convert the input into something useful
    speed = description.speedInMinutes()
    distance = description.toDistanceInMiles()

    minutes = distance*speed
    # print('{} x {} = 0h{}m'.format(distance, int(speed), int(minutes)))
    hours = max(int(minutes)//int(60), 1)
    minutes = max(0., minutes-hours*60.)

    # print('         = {}h{}m'.format(hours, int(minutes)))
    if minutes != 0. and minutes != 30.:
        # round up to the nearest half hour
        if minutes > 30.:
            hours += 1
            minutes = 0.
        elif minutes > 0.:
            minutes = 30.
        # print('         = {}h{}m'.format(hours, int(minutes)))

    return timedelta(hours=hours, minutes=minutes)


def weekToICalGen(week, weeknum, weekdate, startweekday=(11, 30), startweekend=(8, 0)):
    startdate = date(weekdate.year, weekdate.month, weekdate.day)
    for dayofweek, day in enumerate(week):
        day = str(day)  # be smarter than this
        if day.strip() != REST.strip() and day.strip() != RACE:
            event = Event()

            # add in summary and description
            if dayofweek == 0:
                event.add('summary', 'Week {} - {}'.format(weeknum, day))
            else:
                event.add('summary', day)
            event.add('description', day)

            # add in the start
            start = startdate + timedelta(days=dayofweek)
            if dayofweek < 5:  # weekday
                start = datetime.combine(start, time(*startweekday))
            else:  # weekend
                start = datetime.combine(start, time(*startweekend))
            event.add('dtstart', start)

            # add the end
            delta = toTimeDelta(day)
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


@pytest.mark.parametrize('summary, expminutes',
                         [('3 mi run', 60),  # minimum time is 1h
                          ('5 mi run', 60),
                          ('5 mi pace', 60),
                          ('10 miles', 120),  # raw is 100
                          ('4 mi run', 60),
                          ('9 mi run', 90),
                          ('Half Marathon', 150),  # raw is 131
                          ('Marathon', 270),  # raw is 262
                          ('2 mi run', 60),
                          ('10-K Race', 90),  # raw is 62
                          ('5-K Race', 60),
                          ])
def test_running(summary, expminutes):
    obj = toRunItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.
    assert minutes == expminutes, '{} == {}'.format(minutes, expminutes)


@pytest.mark.parametrize('summary, expminutes, expwidth',
                         [('Cross', 30, 5),
                          ('Rest', 0, 4),
                          ('-', 0, 3),
                          ('60 min cross', 60, 12),
                          ('1 hour cross', 60, 12),
                          ])
def test_generic(summary, expminutes, expwidth):
    obj = TrainingItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.
    assert minutes == expminutes, '{} == {}'.format(minutes, expminutes)
    assert obj.width() == expwidth
    if WITH_ICAL:
        assert obj.toICalEvent(startdate=date(2020, 3, 17), dayofweek=2)  # always a Tuesday


@pytest.mark.parametrize('summary, expminutes',
                         [('Bike 60 min', 60),
                          ('Bike 24 miles', 120),
                          ('Bike 54 miles', 240),
                          ('Bike metric century', 270),
                          ])
def test_bike(summary, expminutes):
    obj = TrainingItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.
    assert minutes == expminutes, '{} == {}'.format(minutes, expminutes)


def test_descr():
    summ, descr = ('summary', 'description')

    obj1 = TrainingItem(summ)
    assert obj1.summary == obj1.description == summ

    obj2 = TrainingItem(summ, descr)
    assert obj2.summary == summ
    assert obj2.description == descr

    assert obj1 != obj2


def test_equal():
    assert TrainingItem('blah') == TrainingItem('blah')
    assert TrainingItem(' - ') == TrainingItem('-')
    assert TrainingItem('foo') != TrainingItem('bar')


if __name__ == '__main__':
    pytest.main([__file__])

    for item in ['Cross', '3 mi run', '5 mi run', 'Rest', '5 mi pace', '10 miles',
                 '4 mi run', '9 mi run', 'Half Marathon', 'Marathon', '2 mi run'
                 '60 min cross', '10-K Race', '5-K Race', 'Bike 60 min', 'Bike 30 miles']:
        obj = TrainingItem('item')
