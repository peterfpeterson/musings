#!/usr/bin/env python
from trainingobjs import (findLengths, TrainingDay, TrainingItem, toRunItem, Week,
                          REST, RACE)


# caloric estimates
# swim ~390 kcal  / 1 mile
# bike ~650 kcal / 12.5 mile
# run  ~450 kcal / 3.1 mile


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


# half ironman training
# https://www.triathlete.com/training/super-simple-ironman-70-3-triathlon-training-plan/

# olympic triathlon
# https://www.californiatriathlon.org/coaching/training-plans/12-week-olympic-training-plan/
triathlon = {'olympic':
             # week 1
             [Week(REST, TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 60 min', 'Easy 60 minute bike ride'),
                   TrainingItem('Run 45 min', 'WU 10 minutes (brisk walk), easy 30 minute run, 5 minute CD'),
                   TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 75 min',
                                'WU 10 minutes (easy spinning), 60 minute medium effort, 5 minute cool down'),
                   TrainingItem('Run 50 min', 'WU 10 minutes (brisk walk), 40 minute easy run')),
              # week 2
              Week(REST, TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 60 min', 'Easy 60 minute bike ride'),
                   TrainingItem('Run 55 min', 'WU 10 minutes (easy jog), easy 40 minute run, 5 minute CD'),
                   TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 75 min',
                                'WU 10 minutes (easy spinning), 60 minute medium effort, 5 minute cool down'),
                   TrainingItem('Run 60 min', 'WU 10 minutes (brisk walk), 50 minute easy run')),
              # week 3
              Week(REST, TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 60 min', 'Easy 60 minute bike ride'),
                   TrainingItem('Run 60 min', 'WU 10 minutes (easy jog), easy 45 minute run, 5 minute CD'),
                   TrainingItem('Swim 40 min', '40 minute easy swim, taking breaks as needed'),
                   TrainingItem('Bike 75 min',
                                'WU 10 minutes (easy spinning), 60 minute medium effort, 5 minute cool down'),
                   TrainingItem('Run 60 min', 'WU 10 minutes (brisk walk), 50 minute easy run')),
              # week 4
              Week(REST, TrainingItem('Swim 60 min',
                                      '10 minute WU, swim 4x 200 at a medium-hard effort with 1 minute recovery '
                                      'between sets, CD 5 minutes easy'),
                   REST, TrainingItem('Bike 75 min',
                                      'WU 10 minutes easy spinning, 60 minutes easy effort, 5 minute CD'),
                   REST, TrainingItem('Run 75 min',
                                      'WU 10 minutes (brisk walk), 60 minutes easy to medium effort, 5 minute CD'),
                   REST),
              # week 5
              Week(REST, TrainingItem('Swim 60 min',
                                      'WU 10 minutes, swim 4x 250 at a medium effort with 1 minute recovery '
                                      'between sets, CD 5 minutes easy'),
                   TrainingItem('Bike 70 min', 'Easy 70 minute bike ride'),
                   TrainingItem('Run 60 min',
                                'WU 10 minutes (easy jog), 45 minute easy run with 10 min hard in the middle, '
                                '5 minute CD'),
                   TrainingItem('Swim 60 min', 'WU 10 minutes, 4x25 sprints, 30 minutes easy spin, CD 5 minutes'),
                   TrainingItem('Bike 115 min',
                                'WU 10 minutes (easy spinning), 100 minute medium effort, 5 minute cool down'),
                   TrainingItem('Run 75 min', 'WU 10 minutes (easy jog), 60 minute easy run, 5 minute CD')),
              # week 6
              Week(REST, TrainingItem('Swim 60 min',
                                      'WU 10 minutes, swim 4x 250 at a medium effort with 1 minute recovery between '
                                      'sets, CD 5 minutes easy'),
                   TrainingItem('Bike 70 min', 'Easy 70 minute bike ride'),
                   TrainingItem('Run 60 min', 'WU 10 minutes (easy jog), 45 minute easy run, 5 minute CD'),
                   TrainingItem('Swim 60 min',
                                'WU 10 minutes, 5x25 sprints, 35 minutes easy spin, CD 5 minutes'),
                   TrainingItem('Bike 135 min',
                                'WU 10 minutes (easy spinning), 120 minute medium effort, 5 minute cool down'),
                   TrainingItem('Run 85 min',
                                'WU 10 minutes (easy jog), 70 minute easy run, 5 minute CD')),
              # week 7
              Week(REST,
                   TrainingItem('Swim 60 min',
                                'WU 10 minutes, swim 4x 250 at a medium effort with 1 minute recovery between sets, '
                                'CD 5 minutes easy'),
                   TrainingItem('Bike 70 min', 'Easy 70 minute bike ride'),
                   TrainingItem('Run 60 min',
                                'WU 10 minutes (easy jog), 45 minute easy run with 10 min hard in the middle, '
                                '5 minute CD'),
                   TrainingItem('Swim 60 min', 'WU 10 minutes, 6x25 sprints, 40 minutes easy spin, CD 5 minutes'),
                   TrainingItem('Bike 160 min',
                                'WU 10 minutes (easy spinning), 140 minutes medium with 10 minutes in the middle at '
                                'hard effort, 5 minutes CD'),
                   TrainingItem('Run 95 min', 'WU 10 minutes (easy jog), 80 minute easy run, 5 minute CD')),
              # week 8
              Week(REST, TrainingItem('Swim 60 min',
                                      'WU 10 minutes, 30 minutes steady race effort, 10 minute easy swim, '
                                      'CD 5 minutes '),
                   REST, TrainingItem('Run 60 min', 'WU 10 minutes (easy jog), 45 minute easy run, 5 minute CD'),
                   REST,
                   TrainingItem('Bike 200 min',
                                'WU 10 minutes (easy spinning), 180 minutes sustained medium effort, 10 minutes CD'),
                   REST),
              # week 9
              Week(REST, TrainingItem('Swim 60 min', 'WU 10 minutes, 4x 300 medium effort with 1 minute recovery '
                                      'between sets, CD 5 minutes'),
                   TrainingItem('Bike 70 min', 'Easy 70 minute bike ride'),
                   TrainingItem('Run 65 min', 'WU 10 minutes (brisk jog), easy 50 minute run, 5 minute CD'),
                   TrainingItem('Swim 60 min', 'WU 10 minutes, 4x50 sprints, 35 minutes easy spin, CD 5 minutes'),
                   TrainingItem('Brick 175 min',
                                'Bike 10 minutes easy spinning, 150 minutes moderated spinning, 5 minute CD. '
                                'Immediately transition to running shoes and run 10 minutes easy'),
                   TrainingItem('Run 40 min', 'WU 10 minutes (brisk walk), 30 minute easy run')),
              # week 10
              Week(REST, TrainingItem('Swim 60 min',
                                      'WU 10 minutes, 4x 350 medium effort with 1 minute recovery between sets, '
                                      'CD 5 minutes'),
                   TrainingItem('Bike 60 min', 'Easy 60 minute bike ride'),
                   TrainingItem('Run 65 min',
                                'WU 10 minutes (brisk jog), easy 50 minute run with 10 minutes hard in the middle, '
                                '5 minute CD'),
                   TrainingItem('Swim 60 min', 'WU 10 minutes, 4x50 sprints, Spin 35 min easy'),
                   TrainingItem('Brick 195 min',
                                'Bike 10 minutes easy spinning, 160 minutes moderated spinning, 10 minute CD. '
                                'Immediately transition to running shoes and run 10 minutes easy'),
                   TrainingItem('Run 50 min', 'WU 10 minutes (brisk walk), 40 minute easy run')),
              # week 11
              Week(REST, TrainingItem('Swim 60 min',
                                      'WU 10 minutes, 4x 300 easy/medium effort with 1 minute recovery between sets, '
                                      'CD 5 minutes'),
                   TrainingItem('Bike 45 min', 'Medium effort 45 minute bike ride'),
                   TrainingItem('Run 55 min', 'WU 10 minutes (easy jog), easy 40 minute run, 5 minute CD'),
                   TrainingItem('Swim 60 min', 'WU 10 minutes, 5x25 sprints, 35 minutes easy spin, CD 5 minutes'),
                   TrainingItem('Brick 130 min',
                                'Bike 10 minutes easy spinning, 120 minutes moderated spinning, 5 minute CD. '
                                'Immediately transition to running shoes and run 10 minutes easy'),
                   TrainingItem('Run 40 min',
                                'WU 10 minutes (brisk walk), 30 minute easy run')),
              # week 12
              Week(REST, TrainingItem('Run 30 min',
                                      '10 minute WU (walk or slow jog), 15 minute easy run, 5 minute CD'),
                   TrainingItem('Bike 45 min', '45 minute easy spinning'),
                   TrainingItem('Swim 60 min',
                                'WU 5 minutes, 4x 200 at easy effort with '
                                '1 minute recovery between sets, 5 minute CD'),
                   REST,
                   TrainingDay([TrainingItem('Easy 10 min swim'),
                                TrainingItem('Easy 30 min bike'),
                                TrainingItem('Easy 15 min run')]),  # not back to back
                   RACE)]}


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


# all the following are tab delimited
running = {'marathon':  # https://www.halhigdon.com/training-programs/marathon-training/intermediate-2-marathon/
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

# convert running to standard form
for name, training in running.items():
    mytraining = parseHal(training)
    mytraining = toFiveDays(mytraining)
    running[name] = mytraining
    del mytraining

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
              REST, RACE,
              REST)]}  # Bike metric century


# put together a single list of training
trainingplans = {**running, **bike, **triathlon}  # type: ignore

# update the length of fields for printing the table
for name in trainingplans.keys():
    lengths = findLengths(trainingplans[name])
    for i in range(len(trainingplans[name])):
        trainingplans[name][i].setTableLengths(lengths)
