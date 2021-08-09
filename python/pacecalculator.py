from datetime import (datetime, timedelta)
from trainingobjs import (KM_PER_MILE, BikePace, Pace, RunPace, SwimPace, timeDeltaToStr)


def to_time_of_day(epoch) -> str:
    return epoch.strftime("%H:%M")


def generate_miles(size: float):
    count: int = 0
    while count <= int(size):
        yield count
        count += 1
    yield size


def print_running(starttime, distance: float, pace: Pace):
    for distance in generate_miles(distance):
        label = 'start' if distance == 0 else '{:5s}'.format(str(distance))
        print(label,
              to_time_of_day(starttime + timedelta(minutes=pace * distance)),
              timeDeltaToStr(timedelta(minutes=float(pace)), withHours=False, withSeconds=True))
    print('total:    ', timeDeltaToStr(timedelta(minutes=pace * distance), withSeconds=True))


def print_olympic(starttime, swimpace: Pace,
                  bikepace: Pace,
                  runpace: Pace):
    labels = ('swim', 'T1  ', 'bike', 'T2  ', 'run ')

    deltas = (timedelta(minutes=swimpace * 1.5 / KM_PER_MILE),  # swim
              timedelta(minutes=5),
              timedelta(minutes=bikepace * 40. / KM_PER_MILE),  # bike
              timedelta(minutes=2),
              timedelta(minutes=runpace * 10. / KM_PER_MILE))   # run

    total = timedelta(minutes=0)
    for (label, delta) in zip(labels, deltas):
        print(label, to_time_of_day(starttime + total), timeDeltaToStr(delta))
        total += delta
    print('    ', to_time_of_day(starttime + total))
    print('total:    ', timeDeltaToStr(total))


if __name__ == '__main__':
    # set up optparse
    import argparse     # for command line options
    parser = argparse.ArgumentParser(description='Calculate timing for a race')
    parser.add_argument('-s', '--starttime', default='7:00',
                        help='race start time default=%(default)s')
    parser.add_argument('-t', '--type', dest='racetype', choices=['full', 'half', 'marathon', 'olympic'],
                        default='marathon',
                        help='type of race default=%(default)s choices=[%(choices)s]')
    parser.add_argument('--swimpace', default=3.0,
                        help='Swiming pace in minutes per 100 yard (default=%(default)s)')
    parser.add_argument('--bikepace', default=15.5,
                        help='Cycling pace in miles per hour (default=%(default)s)')
    parser.add_argument('--runpace', default=9.5,
                        help='Running pace in minutes per mile (default=%(default)s)')
    parser.add_argument('--totaltime',
                        help='Total time for running race')
    # parse the command line
    options = parser.parse_args()

    # convert starttime to proper object
    starttime = datetime.strptime(options.starttime, '%H:%M')
    starttime = datetime.combine(datetime.now(), starttime.time())

    # convert 'full' to 'marathon'
    if options.racetype == 'full':
        options.racetype = 'marathon'

    # determine running pace if totaltime was specified
    if options.totaltime:
        print(f'--totaltime={options.totaltime} overrides value of --runpace')
        if ':' in options.totaltime:
            hours, minutes = options.totaltime.split(':')[:2]
        elif 'h' in options.totaltime:
            hours = options.totaltime.split('h')[0]
            minutes = 0
            if 'm' in options.totaltime:
                minutes = options.totaltime[len(hours) + 1: -1]
        else:
            raise ValueError(f'Cannot convert {options.totaltime} to hours and minutes')
        totaltime = timedelta(hours=float(hours), minutes=float(minutes))

        if options.racetype == 'half':
            miletime = totaltime / 13.1
        elif options.racetype == 'marathon':
            miletime = totaltime / 26.2
        else:
            raise ValueError(f'Do not know how to calculate pace for type="{options.racetype}"')
        print('converted {} to {} minutes per mile'.format(timeDeltaToStr(totaltime),
                                                           timeDeltaToStr(miletime, withHours=False,
                                                                          withSeconds=True)))
        options.runpace = miletime / timedelta(minutes=1.)

    # print the table that was requested
    if options.racetype == 'olympic':
        print_olympic(starttime, swimpace=SwimPace(options.swimpace),
                      bikepace=BikePace(options.bikepace),
                      runpace=RunPace(options.runpace))
    elif options.racetype == 'half':
        print_running(starttime, 13.1, RunPace(options.runpace))
    elif options.racetype == 'marathon':
        print_running(starttime, 26.2, RunPace(options.runpace))
    else:
        raise ValueError(f'Do not know how to calculate pace for type="{options.racetype}"')
