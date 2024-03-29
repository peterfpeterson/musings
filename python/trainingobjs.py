#!/usr/bin/env python
from __future__ import absolute_import, division, print_function
from copy import deepcopy
from datetime import date, datetime, time, timedelta
import numpy as np
import pytest  # type: ignore

try:
    from icalendar import Alarm, Event  # type: ignore

    WITH_ICAL = True
except ImportError:
    print("Testing without icalendar support")
    WITH_ICAL = False

DAY_NAMES = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DELTA_WEEK = timedelta(days=7)
KM_PER_MILE = 1.609344
YARD_PER_MILE = 1760


class Pace:
    def __init__(self, minutes_per_mile):
        self.speed = float(minutes_per_mile)

    def __float__(self) -> float:
        return self.speed

    def __mul__(self, other) -> float:
        return float(self) * other

    def __rmul__(self, other) -> float:
        return self * other


class BikePace(Pace):
    def __init__(self, miles_per_hour: float):
        super().__init__(60 / miles_per_hour)


class RunPace(Pace):
    def __init__(self, minutes_per_mile):
        try:
            pace = float(minutes_per_mile)
        except ValueError:
            values = minutes_per_mile.split(":")
            pace = timedelta(minutes=float(values[0]), seconds=float(values[1])) / timedelta(minutes=1)
        super().__init__(pace)


class SwimPace(Pace):
    def __init__(self, minutes_per_100m: float):
        super().__init__(minutes_per_100m * YARD_PER_MILE / 100)


SPEED_RUN = RunPace(10.0)  # 10 minute mile
SPEED_SWIM = SwimPace(3.0)  # 1 minutes per 100 yard
SPEED_BIKE = BikePace(15.0)  # 15 mph


class TrainingItem:
    def __init__(self, summary: str, description: str = ""):
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
        return 1

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

    def __iter__(self):
        return iter([self])

    def __add__(self, other):
        day = []
        if self != REST:
            day.append(self)
        if other != REST:
            if isinstance(other, TrainingItem):
                day.append(other)
            elif isinstance(other, TrainingDay):
                day.extend(other)
            else:
                raise ValueError(f'Cannot add "{other}"')
        if len(day) == 0:
            day.append(REST)

        if len(day) == 1:
            return day[0]
        else:
            return TrainingDay(day)

    def itemInRow(self, rowNum: int):
        if rowNum >= 1:
            return ""
        else:
            return self

    def width(self, minimum: int = 3) -> int:
        """The width of the summary in characters. This is intended for use in printing to the console"""
        return max(len(self.summary.strip()), minimum)

    def __speedInMinutes(self) -> float:
        """generate speed in minutes per mile"""
        description = self.summary.lower()

        speed: Pace  # speed will end up being a pace object
        if "run" in description or "marathon" in description or "km race" in description:
            speed = SPEED_RUN
        elif "swim" in description:
            speed = SPEED_SWIM  # 3 minutes per 100 yards
        elif "bike" in description:
            speed = SPEED_BIKE  # 15 mph
        else:
            msg = 'Do not have speed for activity "{}"'.format(description)
            raise RuntimeError(msg)

        return float(speed)

    def __toDistanceInMiles(self) -> float:
        """Convert description to distance in miles"""

        def toFloat(text: str) -> float:
            replaced_text = text.lower().replace("run", "").replace("swim", "").replace("bike", "")
            for item in replaced_text.split():
                return float(item)
            raise ValueError('failed to convert "{}" to float'.format(text))

        description = self.summary.lower()
        if description.startswith("half"):
            distance = 13.1
        elif description == "marathon":
            distance = 26.2
        elif "km" in description:
            # this only appears to be a running event
            distance = toFloat(description) / KM_PER_MILE
        elif "swim" in description:
            if " m" in description:
                distance = toFloat(description) * 0.001 / KM_PER_MILE
            else:
                raise ValueError(f'Do not know how to convert "{description}" to miles')
        elif "metric century" in description:
            distance = 62.0
        elif "century" in description:
            distance = 100.0
        else:
            distance = toFloat(description)

        return distance

    def toTimeDelta(self, roundUp: bool = True) -> timedelta:
        # first try simple static values
        if "Rest" == self.summary or "-" == self.summary.strip() or "RACE DAY" == self.summary:
            return timedelta(hours=0, minutes=0)
        elif "min" in self.summary:
            descr = self.summary[: self.summary.index("min")].strip()
            descr = descr.split(" ")[-1]
            return timedelta(hours=0, minutes=int(descr))
        elif "hour" in self.summary:
            descr = self.summary[: self.summary.index("hour")].strip()
            descr = descr.split(" ")[-1]
            return timedelta(hours=int(descr), minutes=0)
        elif "hr" in self.summary:
            descr = self.summary[: self.summary.index("hr")].strip()
            descr = descr.split(" ")[-1]
            return timedelta(hours=float(descr), minutes=0)
        elif "cross" in self.summary.lower():
            return timedelta(hours=0, minutes=30)

        # convert the input into something useful
        speed = self.__speedInMinutes()
        distance = self.__toDistanceInMiles()

        hours = 0
        minutes = distance * speed
        # print('{} x {} = 0h{}m'.format(distance, int(speed), int(minutes)))

        if roundUp:
            hours = max(int(minutes) // int(60), 1)
            minutes = max(0.0, minutes - hours * 60.0)
            if minutes != 0.0 and minutes != 30.0:
                # print('         = {}h{}m'.format(hours, int(minutes)))
                # round up to the nearest half hour
                if minutes > 30.0:
                    hours += 1
                    minutes = 0.0
                elif minutes > 0.0:
                    minutes = 30.0
            # print('         = {}h{}m'.format(hours, int(minutes)))

        return timedelta(hours=hours, minutes=int(minutes))

    def volume(self) -> timedelta:
        return self.toTimeDelta(roundUp=False)

    def shouldConvertToICal(self) -> bool:
        descr = str(self).strip()  # be smarter than this
        return descr != REST and descr != RACE

    def toICalEvents(self, startdate, dayofweek: int, weeknum: int = 0):
        if not WITH_ICAL:
            raise RuntimeError("Not configured with icalnedar support")

        startweekday = (7, 30)
        startweekend = (8, 0)

        event = Event()
        # add in summary and description
        if dayofweek == 0:
            event.add("summary", "Week {} - {}".format(weeknum, self.summary))
        else:
            event.add("summary", self.summary)
        event.add("description", self.description)

        # add in the start
        start = startdate + timedelta(days=dayofweek)
        if dayofweek < 5:  # weekday
            start = datetime.combine(start, time(*startweekday))
        else:  # weekend
            start = datetime.combine(start, time(*startweekend))
        event.add("dtstart", start)

        # add the end
        delta = self.toTimeDelta()
        if delta is not None:
            event.add("dtend", start + delta)

        # add the alarm
        if delta is not None and dayofweek < 5:  # weekday
            alarm = Alarm()
            alarm.add("ACTION", "DISPLAY")
            alarm.add("DESCRIPTION", "REMINDER")
            alarm.add("TRIGGER", timedelta(minutes=-15))
            event.add_component(alarm)

        return event


REST = TrainingItem(" - ")
RACE = TrainingItem("RACE DAY")


class TrainingDay:
    def __init__(self, *args):
        self.__items = []
        for item in args:
            self.__items.extend(item)

    def __str__(self):
        return " ".join([str(item) for item in self.__items])

    def __repr__(self):
        return str(self)

    def __len__(self):
        return len(self.__items)

    def __eq__(self, other):
        if len(self) != len(other):
            return False
        else:
            pass  # TODO compare items
        return True  # TODO this is wrong

    def __iter__(self):
        return iter(self.__items)

    def __add__(self, other) -> "TrainingDay":
        day = deepcopy(self.__items)
        if other != REST:
            if isinstance(other, TrainingItem):
                day.append(other)
            elif isinstance(other, TrainingDay):
                day.extend(other)
            else:
                raise ValueError(f'Cannot add "{other}"')

        return TrainingDay(day)

    def volume(self) -> timedelta:
        total = timedelta(hours=0, minutes=0)
        for item in self.__items:
            total += item.volume()

        return total

    def shouldConvertToICal(self):
        for item in self.__items:
            if item.shouldConvertToICal():
                return True
        return False  # none of these should be ical

    def toICalEvents(self, startdate, dayofweek: int, weeknum: int = 0):
        if not WITH_ICAL:
            raise RuntimeError("Not configured with icalnedar support")
        raise NotImplementedError("like it says")  # TODO

    def itemInRow(self, rowNum: int):
        if rowNum >= len(self):
            return ""
        else:
            return self.__items[rowNum]

    def width(self, minimum: int = 3) -> int:
        width: int = minimum
        for item in self.__items:
            width = max(width, item.width())
        return width


def toRunItem(stuff: str):
    """Convert some of the random text to standard text"""
    stuff = stuff.strip()
    if stuff.lower() == "rest" or stuff == "-":
        return REST
    stuff = stuff.replace("mi run", "miles")
    stuff = stuff.replace("mi pace", "miles pace")
    stuff = stuff.replace("-K Race", " km race")
    stuff = stuff.replace("Half Marathon", "Half marathon")
    details = ""
    if "marathon" in stuff.lower() or "race" in stuff or "bike" in stuff.lower():
        pass  # TODO should reverse the check
    else:
        if "pace" in stuff:
            details = stuff
            stuff = stuff.replace("pace", "").strip()
        stuff = "Run " + stuff
    return TrainingItem(stuff, details)


def toFiveDays(training):
    adjusted = []
    for week in training:
        # hard code resting on Thursday if there are too many working days
        restThursday = bool(len([item for item in week if item != REST]) > 5)
        thursday = week.fri
        # TODO need to be smarter about this
        if restThursday:
            thursday = REST
        week = Week(week.tue, week.wed, week.thu, thursday, week.sat, week.sun, REST)
        adjusted.append(week)
    # remove the race from the last week
    week = list(adjusted[-1])
    week[-2] = RACE
    adjusted[-1] = Week(*week)
    return adjusted


class Week:
    def __init__(self, mon, tue, wed, thu, fri, sat, sun):
        self.mon = mon
        self.tue = tue
        self.wed = wed
        self.thu = thu
        self.fri = fri
        self.sat = sat
        self.sun = sun
        self._lengths = None

    def __iter__(self):
        return iter([self.mon, self.tue, self.wed, self.thu, self.fri, self.sat, self.sun])

    def setTableLengths(self, lengths):
        if len(lengths) != len(DAY_NAMES):
            raise RuntimeError("Wrong number of lengths {} != {}".format(len(lengths), len(DAY_NAMES)))
        self._lengths = deepcopy(lengths)

    def volume(self) -> timedelta:
        total = timedelta(hours=0, minutes=0)
        for item in self:
            total += item.volume()
        return total

    def toICalGen(self, weeknum, weekdate, startweekday=(11, 30), startweekend=(8, 0)):
        startdate = date(weekdate.year, weekdate.month, weekdate.day)
        for dayofweek, day in enumerate(self):
            if day != REST and day.shouldConvertToICal():
                for item in day:  # loop through each item in the object
                    yield item.toICalEvents(weeknum=weeknum, startdate=startdate, dayofweek=dayofweek)
            else:
                yield None

    def tableHeader(self):
        return "{:20}".format("") + " ".join(_tableGen(DAY_NAMES, self._lengths))

    def __itemsInRow(self, rowNum):
        return [item.itemInRow(rowNum) for item in self]

    def __add__(self, other: "Week") -> "Week":
        week = []

        for us, them in zip(self, other):
            week.append(us + them)

        return Week(*week)

    def tableRows(self, weekdate, weeknum):
        numRow = 1
        for item in self:
            numRow = max(numRow, len(item))

        # this prints the table version
        label = "{:%Y-%m-%d} Week {:2}: ".format(weekdate, weeknum)
        result = (
            label + " ".join(_tableGen(self.__itemsInRow(0), self._lengths)) + " vol=" + timeDeltaToStr(self.volume())
        )
        for i in range(1, numRow):
            result += "\n" + " " * len(label) + " ".join(_tableGen(self.__itemsInRow(i), self._lengths))
        return result


def timeDeltaToStr(value: timedelta, withHours=True, withSeconds: bool = False) -> str:
    # TODO improve this
    returnable = ""
    if withSeconds:
        result = str(value).split(":")[0:3]
        result[2] = "{:.1f}".format(float(result[2]))
        returnable = f"{result[0]}h{result[1]}m{result[2]}s"
    else:
        result = str(value).split(":")[0:2]
        returnable = f"{result[0]}h{result[1]}m"

    if not withHours:
        returnable = returnable.split("h")[-1]

    return returnable


def _tableGen(week, lengths):
    lengths = ["{:" + str(length) + "}" for length in lengths]
    for day, length in zip(week, lengths):
        yield length.format(str(day))


def findLengths(training):
    lengths = [3] * len(DAY_NAMES)
    for week in training:
        for i, day in enumerate(week):
            if day == REST:
                continue
            try:
                lengths[i] = max(lengths[i], day.width())
            except AttributeError as e:
                raise TypeError(str(day) + " is of wrong type") from e
    return lengths


@pytest.mark.parametrize(
    "summary, expminutes",
    [
        ("3 mi run", 60),  # minimum time is 1h
        ("5 mi run", 60),
        ("5 mi pace", 60),
        ("10 miles", 120),  # raw is 100
        ("4 mi run", 60),
        ("9 mi run", 90),
        ("Half Marathon", 150),  # raw is 131
        ("Marathon", 270),  # raw is 262
        ("2 mi run", 60),
        ("10-K Race", 90),  # raw is 62
        ("5-K Race", 60),
        ("3.0 hr run", 180),
        ("1.5 hr run", 90),
    ],
)
def test_running(summary, expminutes):
    obj = toRunItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.0
    assert minutes == expminutes, "{} == {}".format(minutes, expminutes)


@pytest.mark.parametrize(
    "summary, expminutes, expwidth",
    [
        ("Cross", 30, 5),
        ("Rest", 0, 4),
        ("-", 0, 3),
        ("60 min cross", 60, 12),
        ("1 hour cross", 60, 12),
    ],
)
def test_generic(summary, expminutes, expwidth):
    obj = TrainingItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.0
    assert minutes == expminutes, "{} == {}".format(minutes, expminutes)
    assert obj.width() == expwidth
    if WITH_ICAL:
        assert obj.toICalEvents(startdate=date(2020, 3, 17), dayofweek=2)  # always a Tuesday


def test_pace():
    assert float(Pace(10.0)) == 10.0  # 10 minutes per mile
    assert float(RunPace(10.0)) == 10.0  # 10 minutes per mile
    assert float(BikePace(15.0)) == 4.0  # 15 mph = 4 minutes per mile
    pytest.approx(float(SwimPace(3.0)), 48.28)  # 3 minutes per 100m = 48 minutes per mile
    assert float(RunPace("9:30")) == 9.5  # 9m30s


@pytest.mark.parametrize(
    "summary, expminutes, expminutesround",
    [
        ("Bike 60 min", 60, 60),
        ("Bike 24 miles", 24 * SPEED_BIKE, 120),
        ("Bike 54 miles", 54 * SPEED_BIKE, 240),
        ("Bike metric century", SPEED_BIKE * 62, 270),
        ("Swim 60 min", 60, 60),
        ("Swim 500 m", int(0.5 * SPEED_SWIM / KM_PER_MILE), 60),
        ("Swim 1602 m", 52, 60),
        ("Swim 3204 m", 105, 120),
    ],
)
def test_timing(summary, expminutes, expminutesround):
    obj = TrainingItem(summary)
    assert obj  # sucessfully created an object
    minutes = obj.toTimeDelta().total_seconds() / 60.0
    assert minutes == expminutesround, "toTimeDelta(round) {} == {}".format(minutes, expminutes)
    minutes = obj.toTimeDelta(roundUp=False).total_seconds() / 60.0
    assert minutes == expminutes, "toTimeDelta(raw) {} == {}".format(minutes, expminutes)
    minutes = obj.volume().total_seconds() / 60.0
    assert minutes == expminutes, "volume {} == {}".format(minutes, expminutes)


def test_descr():
    summ, descr = ("summary", "description")

    obj1 = TrainingItem(summ)
    assert obj1.summary == obj1.description == summ

    obj2 = TrainingItem(summ, descr)
    assert obj2.summary == summ
    assert obj2.description == descr

    assert obj1 != obj2


def test_equal():
    assert TrainingItem("blah") == TrainingItem("blah")
    assert TrainingItem(" - ") == TrainingItem("-")
    assert TrainingItem("foo") != TrainingItem("bar")


def test_training_day():
    # setup training items
    item1 = TrainingItem("summary", "description")
    item2 = TrainingItem("summary2", "description")
    assert item1
    assert item2

    # create TrainingDay with only 1 item
    day = TrainingDay([item1])

    assert day
    assert len(day) == 1
    for item in day:
        assert item == item1  # there is only one item \in the day

    # create TrainingDay with 2 items
    day = TrainingDay([item1, item2])
    assert day
    assert len(day) == 2
    for obs, exp in zip(day, [item1, item2]):
        assert obs == exp  # there is only one item \in the day


def test_triathlon():
    MINUTES = (10, 30, 15)
    swim = TrainingItem("Easy 10 minute swim")
    bike = TrainingItem("Easy 30 minute bike")
    run = TrainingItem("Easy 15 minute run")
    day = TrainingDay([swim, bike, run])  # not back to back

    assert day
    assert len(day) == 3
    for obs, exp in zip(day, MINUTES):
        assert obs.toTimeDelta() == timedelta(hours=0, minutes=exp)

    assert day.itemInRow(0) == swim
    assert day.itemInRow(1) == bike
    assert day.itemInRow(2) == run
    assert day.itemInRow(3) == ""
    minutes = day.volume().total_seconds() / 60.0
    assert minutes == np.sum(MINUTES), "volume {} == {}".format(minutes, np.sum(MINUTES))


def test_have_plans():
    # test object existance
    for item in [
        "Cross",
        "3 mi run",
        "5 mi run",
        "Rest",
        "5 mi pace",
        "10 miles",
        "4 mi run",
        "9 mi run",
        "Half Marathon",
        "Marathon",
        "2 mi run" "60 min cross",
        "10-K Race",
        "5-K Race",
        "Bike 60 min",
        "Bike 30 miles",
    ]:
        assert TrainingItem("item")


def test_add_day():
    RUN_DAY = TrainingItem("Run 5 km")

    result = REST + REST
    assert result == REST

    result = REST + RUN_DAY
    assert result == RUN_DAY

    day = TrainingDay(RUN_DAY, RUN_DAY)

    result = REST + day
    assert result == day

    result = day + REST
    assert result == day

    result = day + day
    assert len(result) == 4


def test_add_week():
    rest_week = Week(REST, REST, REST, REST, REST, REST, REST)
    run_day = TrainingItem("Run 5 km")
    run_week = Week(run_day, run_day, run_day, run_day, run_day, run_day, run_day)

    # lots of rest
    result = rest_week + rest_week
    assert result
    for day in result:
        assert day == REST

    # add rest to running
    result = run_week + rest_week
    assert result
    for day in result:
        assert day == run_day

    # add running to rest
    result = rest_week + run_week
    assert result
    for day in result:
        assert day == run_day

    # lots of running
    tons_of_run = TrainingDay(run_day, run_day)
    result = run_week + run_week
    assert result
    for day in result:
        assert day == tons_of_run


if __name__ == "__main__":
    import sys

    sys.exit(pytest.main([__file__]))
