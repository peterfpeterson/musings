#!/usr/bin/env python
from trainingobjs import findLengths, TrainingItem, toRunItem, Week

REST = TrainingItem(' - ')
RACE = TrainingItem('RACE DAY')


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
trainingplans = {**running, **bike}  # type: ignore

# update the length of fields for printing the table
for name in trainingplans.keys():
    lengths = findLengths(trainingplans[name])
    for i in range(len(trainingplans[name])):
        trainingplans[name][i].setTableLengths(lengths)
