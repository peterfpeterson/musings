#!/usr/bin/env python
from copy import deepcopy
from trainingobjs import (
    findLengths,
    TrainingDay,
    TrainingItem,
    toRunItem,
    Week,
    REST,
    RACE,
)
from typing import Dict, List

# caloric estimates
# swim ~390 kcal  / 1 mile
# bike ~650 kcal / 12.5 mile
# run  ~450 kcal / 3.1 mile


# friendly names for typing
TrainingPlan = List[Week]
TrainingCollection = Dict[str, TrainingPlan]


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


# #### half ironman training
# SWIM 1.9 km
# BIKE 90 km
# RUN 21.1 km

# https://www.triathlete.com/training/super-simple-ironman-70-3-triathlon-training-plan/

# #### olympic triathlon
# SWIM 1.5 km = 0.93 mile
# BIKE 40 km = 24.8 mile
# RUN 10 km = 6.2 mile

# http://www.chicotriathlonclub.com/Documents/Olympic_Distance_Program.pdf
triathlon: TrainingCollection = {
    "olympic":
    # week 1
    [
        Week(
            REST,
            TrainingItem("Run 25 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 500 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 30 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 20 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 45 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 60 min", "Long RPE 6"),
            TrainingItem("Run 30 min", "Long RPE 6"),
        ),
        # week 2
        Week(
            REST,
            TrainingItem("Run 30 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 500 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 30 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 20 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1000 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 45 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 70 min", "Long RPE 6"),
            TrainingItem("Run 40 min", "Long RPE 6"),
        ),
        # week 3
        Week(
            REST,
            TrainingItem("Run 30 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 35 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1000 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 50 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 75 min", "Long RPE 6"),
            TrainingItem("Run 40 min", "Long RPE 6"),
        ),
        # week 4
        Week(
            REST,
            TrainingItem("Run 25 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 500 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 25 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 20 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1000 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 40 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 60 min", "Long RPE 6"),
            TrainingItem("Run 30 min", "Long RPE 6"),
        ),
        # week 5
        Week(
            REST,
            TrainingItem("Run 30 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 30 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 20 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1000 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 45 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 70 min", "Long RPE 6"),
            TrainingItem("Run 35 min", "Long RPE 6"),
        ),
        # week 6
        Week(
            REST,
            TrainingItem("Run 35 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 35 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1250 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 50 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 80 min", "Long RPE 6"),
            TrainingItem("Run 45 min", "Long RPE 6"),
        ),
        # week 7
        Week(
            REST,
            TrainingItem("Run 40 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 40 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1500 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 55 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 90 min", "Long RPE 6"),
            TrainingItem("Run 50 min", "Long RPE 6"),
        ),
        # week 8
        Week(
            REST,
            TrainingItem("Run 25 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 25 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 20 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1250 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 40 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 60 min", "Long RPE 6"),
            TrainingItem("Run 35 min", "Long RPE 6"),
        ),
        # week 9
        Week(
            REST,
            TrainingItem("Run 35 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 30 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1250 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 50 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 85 min", "Long RPE 6"),
            TrainingItem("Run 45 min", "Long RPE 6"),
        ),
        # week 10
        Week(
            REST,
            TrainingItem("Run 40 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 35 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1500 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 60 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 100 min", "Long RPE 6"),
            TrainingItem("Run 50 min", "Long RPE 6"),
        ),
        # week 11
        Week(
            REST,
            TrainingItem("Run 35 min", "Moderate RPE 6-7"),
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7 + strength"),
                    TrainingItem("Bike 40 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Run 25 min", "Tempo RPE 7"),
            TrainingDay(
                [
                    TrainingItem("Swim 1500 m", "Long RPE 6 + strength"),
                    TrainingItem("Bike 45 min", "Tempo RPE 6-7"),
                ]
            ),
            TrainingItem("Bike 75 min", "Long RPE 6"),
            TrainingItem("Run 40 min", "Long RPE 6"),
        ),
        # week 12
        Week(
            REST,
            TrainingDay(
                [
                    TrainingItem("Swim 750 m", "Tempo RPE 7"),
                    TrainingItem("Run 20 min", "Tempo RPE 7"),
                ]
            ),
            TrainingItem("Bike 30 min", "Tempo RPE 7"),
            REST,
            REST,
            TrainingDay(
                [
                    TrainingItem("Bike 20 min", "Easy RPE 6-7"),
                    TrainingItem("Run 15 min", "Easy with pick-ups RPE 6"),
                ]
            ),
            RACE,
        ),
    ],
    # https://www.californiatriathlon.org/coaching/training-plans/12-week-olympic-training-plan/
    "olympic2":
    # week 1
    [
        Week(
            REST,
            TrainingItem("Swim 40 min", "40 minute easy swim, taking breaks as needed"),
            TrainingItem("Bike 60 min", "Easy 60 minute bike ride"),
            TrainingItem(
                "Run 45 min",
                "WU 10 minutes (brisk walk), easy 30 minute run, 5 minute CD",
            ),
            TrainingItem("Swim 40 min", "40 minute easy swim, taking breaks as needed"),
            TrainingItem(
                "Bike 75 min",
                "WU 10 minutes (easy spinning), 60 minute medium effort, "
                "5 minute cool down",
            ),
            TrainingItem(
                "Run 50 min", "WU 10 minutes (brisk walk), 40 minute easy run"
            ),
        ),
        # week 2
        Week(
            REST,
            TrainingItem("Swim 40 min", "40 minute easy swim, taking breaks as needed"),
            TrainingItem("Bike 60 min", "Easy 60 minute bike ride"),
            TrainingItem(
                "Run 55 min",
                "WU 10 minutes (easy jog), easy 40 minute run, " "5 minute CD",
            ),
            TrainingItem("Swim 40 min", "40 minute easy swim, taking breaks as needed"),
            TrainingItem(
                "Bike 75 min",
                "WU 10 minutes (easy spinning), 60 minute medium effort, "
                "5 minute cool down",
            ),
            TrainingItem(
                "Run 60 min", "WU 10 minutes (brisk walk), 50 minute easy run"
            ),
        ),
        # week 3
        Week(
            REST,
            TrainingItem(
                "Swim 40 min", "40 minute easy swim, taking breaks " "as needed"
            ),
            TrainingItem("Bike 60 min", "Easy 60 minute bike ride"),
            TrainingItem(
                "Run 60 min",
                "WU 10 minutes (easy jog), easy 45 minute run, " "5 minute CD",
            ),
            TrainingItem("Swim 40 min", "40 minute easy swim, taking breaks as needed"),
            TrainingItem(
                "Bike 75 min",
                "WU 10 minutes (easy spinning), 60 minute medium effort, "
                "5 minute cool down",
            ),
            TrainingItem(
                "Run 60 min", "WU 10 minutes (brisk walk), 50 minute easy run"
            ),
        ),
        # week 4
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "10 minute WU, swim 4x 200 at a medium-hard effort with "
                "1 minute recovery between sets, CD 5 minutes easy",
            ),
            REST,
            TrainingItem(
                "Bike 75 min",
                "WU 10 minutes easy spinning, 60 minutes easy effort, " "5 minute CD",
            ),
            REST,
            TrainingItem(
                "Run 75 min",
                "WU 10 minutes (brisk walk), 60 minutes easy to medium "
                "effort, 5 minute CD",
            ),
            REST,
        ),
        # week 5
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, swim 4x 250 at a medium effort with 1 minute"
                " recovery between sets, CD 5 minutes easy",
            ),
            TrainingItem("Bike 70 min", "Easy 70 minute bike ride"),
            TrainingItem(
                "Run 60 min",
                "WU 10 minutes (easy jog), 45 minute easy run with 10 min hard in"
                " the middle, 5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 4x25 sprints, 30 minutes easy spin," " CD 5 minutes",
            ),
            TrainingItem(
                "Bike 115 min",
                "WU 10 minutes (easy spinning), 100 minute medium effort, "
                "5 minute cool down",
            ),
            TrainingItem(
                "Run 75 min",
                "WU 10 minutes (easy jog), 60 minute easy run, " "5 minute CD",
            ),
        ),
        # week 6
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, swim 4x 250 at a medium effort with 1 minute"
                " recovery between sets, CD 5 minutes easy",
            ),
            TrainingItem("Bike 70 min", "Easy 70 minute bike ride"),
            TrainingItem(
                "Run 60 min",
                "WU 10 minutes (easy jog), 45 minute easy run, " "5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 5x25 sprints, 35 minutes easy spin, CD 5 minutes",
            ),
            TrainingItem(
                "Bike 135 min",
                "WU 10 minutes (easy spinning), 120 minute medium effort, "
                "5 minute cool down",
            ),
            TrainingItem(
                "Run 85 min",
                "WU 10 minutes (easy jog), 70 minute easy run, 5 minute CD",
            ),
        ),
        # week 7
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, swim 4x 250 at a medium effort with 1 minute "
                "recovery between sets, CD 5 minutes easy",
            ),
            TrainingItem("Bike 70 min", "Easy 70 minute bike ride"),
            TrainingItem(
                "Run 60 min",
                "WU 10 minutes (easy jog), 45 minute easy run with 10 min hard in "
                "the middle, 5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 6x25 sprints, 40 minutes easy spin," " CD 5 minutes",
            ),
            TrainingItem(
                "Bike 160 min",
                "WU 10 minutes (easy spinning), 140 minutes medium with 10 minutes"
                " in the middle at hard effort, 5 minutes CD",
            ),
            TrainingItem(
                "Run 95 min",
                "WU 10 minutes (easy jog), 80 minute easy run, " "5 minute CD",
            ),
        ),
        # week 8
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 30 minutes steady race effort, 10 minute "
                "easy swim, CD 5 minutes ",
            ),
            REST,
            TrainingItem(
                "Run 60 min",
                "WU 10 minutes (easy jog), 45 minute easy run," " 5 minute CD",
            ),
            REST,
            TrainingItem(
                "Bike 200 min",
                "WU 10 minutes (easy spinning), 180 minutes sustained medium "
                "effort, 10 minutes CD",
            ),
            REST,
        ),
        # week 9
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 4x 300 medium effort with 1 "
                "minute recovery between sets, CD 5 minutes",
            ),
            TrainingItem("Bike 70 min", "Easy 70 minute bike ride"),
            TrainingItem(
                "Run 65 min",
                "WU 10 minutes (brisk jog), easy 50 minute run, " "5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 4x50 sprints, 35 minutes easy " "spin, CD 5 minutes",
            ),
            TrainingItem(
                "Brick 175 min",
                "Bike 10 minutes easy spinning, 150 minutes moderated spinning, "
                "5 minute CD. Immediately transition to running shoes and "
                "run 10 minutes easy",
            ),
            TrainingItem(
                "Run 40 min", "WU 10 minutes (brisk walk), 30 minute easy run"
            ),
        ),
        # week 10
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 4x 350 medium effort with 1 minute recovery "
                "between sets, CD 5 minutes",
            ),
            TrainingItem("Bike 60 min", "Easy 60 minute bike ride"),
            TrainingItem(
                "Run 65 min",
                "WU 10 minutes (brisk jog), easy 50 minute run with 10 minutes "
                "hard in the middle, 5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min", "WU 10 minutes, 4x50 sprints, Spin 35 min easy"
            ),
            TrainingItem(
                "Brick 195 min",
                "Bike 10 minutes easy spinning, 160 minutes moderated spinning, "
                "10 minute CD. Immediately transition to running shoes and "
                "run 10 minutes easy",
            ),
            TrainingItem(
                "Run 50 min", "WU 10 minutes (brisk walk), 40 minute easy run"
            ),
        ),
        # week 11
        Week(
            REST,
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 4x 300 easy/medium effort with 1 minute "
                "recovery between sets, CD 5 minutes",
            ),
            TrainingItem("Bike 45 min", "Medium effort 45 minute bike ride"),
            TrainingItem(
                "Run 55 min",
                "WU 10 minutes (easy jog), easy 40 minute run, " "5 minute CD",
            ),
            TrainingItem(
                "Swim 60 min",
                "WU 10 minutes, 5x25 sprints, 35 minutes easy spin," " CD 5 minutes",
            ),
            TrainingItem(
                "Brick 130 min",
                "Bike 10 minutes easy spinning, 120 minutes moderated spinning,"
                " 5 minute CD. Immediately transition to running shoes and run "
                "10 minutes easy",
            ),
            TrainingItem(
                "Run 40 min", "WU 10 minutes (brisk walk), 30 minute easy run"
            ),
        ),
        # week 12
        Week(
            REST,
            TrainingItem(
                "Run 30 min",
                "10 minute WU (walk or slow jog), 15 minute easy run, " "5 minute CD",
            ),
            TrainingItem("Bike 45 min", "45 minute easy spinning"),
            TrainingItem(
                "Swim 60 min",
                "WU 5 minutes, 4x 200 at easy effort with "
                "1 minute recovery between sets, 5 minute CD",
            ),
            REST,
            TrainingDay(
                [
                    TrainingItem("Easy 10 min swim"),
                    TrainingItem("Easy 30 min bike"),
                    TrainingItem("Easy 15 min run"),
                ]
            ),  # not back to back
            RACE,
        ),
    ],
}


def parseHal(raw):
    program = []
    for line in raw.split("\n"):
        line = line.strip()
        if not line:
            continue
        line = [toRunItem(item) for item in line.split("\t")[1:]]
        week = Week(*line)
        program.append(week)
    return program


# all the following are tab delimited
runningraw = {
    "marathon-i2":  # https://www.halhigdon.com/training-programs/marathon-training/intermediate-2-marathon/
    """
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
""",  # noqa: E128
    "marathon-i1":  # https://www.halhigdon.com/training-programs/marathon-training/intermediate-1-marathon/
    """
1 	Cross 	3 mi run 	5 mi run 	3 mi run 	Rest 	5 mi pace 	8
2 	Cross 	3 mi run 	5 mi run 	3 mi run 	Rest 	5 mi run 	9
3 	Cross 	3 mi run 	5 mi run 	3 mi run 	Rest 	5 mi pace 	6
4 	Cross 	3 mi run 	6 mi run 	3 mi run 	Rest 	6 mi pace 	11
5 	Cross 	3 mi run 	6 mi run 	3 mi run 	Rest 	6 mi run 	12
6 	Cross 	3 mi run 	5 mi run 	3 mi run 	Rest 	6 mi pace 	9
7 	Cross 	4 mi run 	7 mi run 	4 mi run 	Rest 	7 mi pace 	14
8 	Cross 	4 mi run 	7 mi run 	4 mi run 	Rest 	7 mi run 	15
9 	Cross 	4 mi run 	5 mi run 	4 mi run 	Rest 	Rest 	Half Marathon
10 	Cross 	4 mi run 	8 mi run 	4 mi run 	Rest 	8 mi pace 	17
11 	Cross 	5 mi run 	8 mi run 	5 mi run 	Rest 	8 mi run 	18
12 	Cross 	5 mi run 	5 mi run 	5 mi run 	Rest 	8 mi pace 	13
13 	Cross 	5 mi run 	8 mi run 	5 mi run 	Rest 	5 mi pace 	20
14 	Cross 	5 mi run 	5 mi run 	5 mi run 	Rest 	8 mi run 	12
15 	Cross 	5 mi run 	8 mi run 	5 mi run 	Rest 	5 mi pace 	20
16 	Cross 	5 mi run 	6 mi run 	5 mi run 	Rest 	4 mi pace 	12
17 	Cross 	4 mi run 	5 mi run 	4 mi run 	Rest 	3 mi run 	8
18 	Cross 	3 mi run 	4 mi run 	Rest 	Rest 	2 mi run 	Marathon
""",  # noqa: E128
    "marathon-n1":  # https://www.halhigdon.com/training-programs/marathon-training/novice-1-marathon/
    """
1 	Rest	Rest 	3 mi run 	3 mi run 	3 mi run 	Rest 	6 mi run
2 	Rest	Rest 	3 mi run 	3 mi run 	3 mi run 	Rest 	7 mi run
3 	Rest	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	5 mi run
4 	Rest	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	9 mi run
5 	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	10 mi run
6 	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	7 mi run
7 	Rest	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	12 mi run
8 	Rest	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	Half Marathon
9 	Rest	Rest 	3 mi run 	7 mi run 	4 mi run 	Rest 	10 mi run
10 	Rest	Rest 	3 mi run 	7 mi run 	4 mi run 	Rest 	15 mi run
11 	Rest	Rest 	4 mi run 	8 mi run 	4 mi run 	Rest 	16 mi run
12 	Rest	Rest 	4 mi run 	8 mi run 	5 mi run 	Rest 	12 mi run
13 	Rest	Rest 	4 mi run 	9 mi run 	5 mi run 	Rest 	18 mi run
14 	Rest	Rest 	5 mi run 	9 mi run 	5 mi run 	Rest 	14 mi run
15 	Rest	Rest 	5 mi run 	10 mi run 	5 mi run 	Rest 	20 mi run
16 	Rest	Rest 	5 mi run 	8 mi run 	4 mi run 	Rest 	12 mi run
17 	Rest	Rest 	4 mi run 	6 mi run 	3 mi run 	Rest 	8 mi run
18 	Rest	Rest 	3 mi run 	4 mi run 	2 mi run 	Rest 	Marathon
""",  # noqa: E128
    "marathon-n2":  # https://www.halhigdon.com/training-programs/marathon-training/novice-2-marathon/
    """
1 	Rest	Rest 	3 mi run 	5 m pace 	3 mi run 	Rest 	8
2 	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	9
3 	Rest	Rest 	3 mi run 	5 m pace 	3 mi run 	Rest 	6
4 	Rest	Rest 	3 mi run 	6 m pace 	3 mi run 	Rest 	11
5 	Rest	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	12
6 	Rest	Rest 	3 mi run 	6 m pace 	3 mi run 	Rest 	9
7 	Rest	Rest 	4 mi run 	7 m pace 	4 mi run 	Rest 	14
8 	Rest	Rest 	4 mi run 	7 mi run 	4 mi run 	Rest 	15
9 	Rest	Rest 	4 mi run 	7 m pace 	4 mi run 	Rest 	Half Marathon
10 	Rest	Rest 	4 mi run 	8 m pace 	4 mi run 	Rest 	17
11 	Rest	Rest 	5 mi run 	8 mi run 	5 mi run 	Rest 	18
12 	Rest	Rest 	5 mi run 	8 m pace 	5 mi run 	Rest 	13
13 	Rest	Rest 	5 mi run 	5 m pace 	5 mi run 	Rest 	19
14 	Rest	Rest 	5 mi run 	8 mi run 	5 mi run 	Rest 	12
15 	Rest	Rest 	5 mi run 	5 m pace 	5 mi run 	Rest 	20
16 	Rest	Rest 	5 mi run 	4 m pace 	5 mi run 	Rest 	12
17 	Rest	Rest 	4 mi run 	3 mi run 	4 mi run 	Rest 	8
18 	Rest	Rest 	3 mi run 	2 mi run 	Rest 	2 mi run 	Marathon
""",  # noqa: E128
    "half":  # https://www.halhigdon.com/training-programs/half-marathon-training/intermediate-1-half-marathon/
    """
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
""",
    "half-n2":  # https://www.halhigdon.com/training-programs/half-marathon-training/novice-2-half-marathon/
    """
1 	Rest	Rest 	3 mi run 	3 mi run 	3 mi run 	Rest 	4 mi run
2 	Rest	Rest 	3 mi run 	3 mi pace 	3 mi run 	Rest 	5 mi run
3 	Rest	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	6 mi run
4 	Rest	Rest 	3 mi run 	4 mi pace 	3 mi run 	Rest 	7 mi run
5 	Rest	Rest 	3 mi run 	4 mi run 	3 mi run 	Rest 	8 mi run
6 	Rest	Rest 	3 mi run 	4 mi pace 	3 mi run 	Rest 	5-K Race
7 	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	9 mi run
8 	Rest	Rest 	3 mi run 	5 mi pace 	3 mi run 	Rest 	10 mi run
9 	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	10-K Race
10	Rest	Rest 	3 mi run 	5 mi pace 	3 mi run 	Rest 	11 mi run
11	Rest	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	12 mi run
12  	Rest	Rest 	3 mi run 	2 mi pace 	2 mi run 	Rest  	Half Marathon
""",
    "ultra-hal":  # https://www.halhigdon.com/training-programs/more-training/ultramarathon-50k/
    """
1 	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	5 mi pace 	10 mi run
2 	Rest 	3 mi run 	5 mi run 	3 mi run 	Rest 	5 mi run 	1.5 hr run
3 	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	6 mi pace 	8 mi run
4 	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	6 mi pace 	13 mi run
5 	Rest 	3 mi run 	7 mi run 	3 mi run 	Rest 	7 mi run 	2 hr run
6 	Rest 	3 mi run 	7 mi run 	3 mi run 	Rest 	7 mi pace 	10 mi run
7 	Rest 	4 mi run 	8 mi run 	4 mi run 	Rest 	5 mi pace 	16 mi run
8 	Rest 	4 mi run 	8 mi run 	4 mi run 	Rest 	8 mi run 	2.5 hr run
9 	Rest 	4 mi run 	9 mi run 	4 mi run 	Rest 	Rest 	13.1 mi
10 	Rest 	4 mi run 	9 mi run 	4 mi run 	Rest 	9 mi pace 	3 hr run
11 	Rest 	5 mi run 	10 mi run 	5 mi run 	Rest 	10 mi run 	20 mi run
12 	Rest 	5 mi run 	6 mi run 	5 mi run 	Rest 	6 mi pace 	2 hr run
13 	Rest 	5 mi run 	10 mi run 	5 mi run 	Rest 	10 mi pace 	20 mi run
14 	Rest 	5 mi run 	6 mi run 	5 mi run 	Rest 	6 mi run 	2.5 hr run
15 	Rest 	5 mi run 	10 mi run 	5 mi run 	Rest 	10 mi pace 	20 mi run
16 	Rest 	5 mi run 	8 mi run 	5 mi run 	Rest 	10 mi pace 	3 hr run
17 	Rest 	4 mi run 	6 mi run 	4 mi run 	Rest 	4 mi pace 	8 mi run
18 	Rest 	3 mi run 	4 mi run 	Rest 	Rest 	2 mi run 	26.2 mi
19 	Rest 	Rest 	Rest 	3 mi run 	Rest 	1.0 hr run 	1.0 hr run
20 	Rest 	3 mi run 	10 mi run 	3 mi run 	Rest 	1.0 hr pace 	3.0 hr run
21 	Rest 	3 mi run 	6 mi run 	3 mi run 	Rest 	1.5 hr run 	2.0 hr run
22 	Rest 	3 mi run 	10 mi run 	3 mi run 	Rest 	1.5 hr pace 	4.0 hr run
23 	Rest 	4 mi run 	7 mi run 	4 mi run 	Rest 	2.0 hr run 	3.0 hr run
24 	Rest 	4 mi run 	10 mi run 	4 mi run 	Rest 	2.0 hr pace 	5.0 hr run
25 	Rest 	4 mi run 	8 mi run 	4 mi run 	Rest 	1.0 hr run 	1.0 hr run
26 	Rest 	4 mi run 	4 mi run 	Rest 	Rest 	2 mi run 	31.1 mi
""",
}

# convert running to standard form
running: TrainingCollection = dict()
for name, training in runningraw.items():
    mytraining = parseHal(training)
    mytraining = toFiveDays(mytraining)
    running[name] = mytraining
    del mytraining
del runningraw
# copy Hal's intermediate-2 to be the default marathon training
running["marathon"] = running["marathon-i1"]

# one suggestion for ultras said that your weekly volume should be 20-30% higher than expected race finish

# add in bonus programs
# https://www.jennyhadfield.com/wp-content/uploads/2016/01/Coach-Jennys-First-50K-Training-Plan.pdf

# 50 minutes
SPEED_10X1 = """Speed Workout 10 x 1
Warm up walking for 3 minutes, starting easy and build to a brisk pace by the end.
Run 15 minutes in your easy yellow zone effort.
Repeat 10 times:
Run 1 minute at your Red Zone Effort (Zone 5)
Follow with 2 minutes of very easy jogging or walking to catch your breath.
Run 5 minutes in your easy yellow zone effort.
Cool down walking for 3 minutes, starting at a brisk pace and slowing by the end."""
SPEED_6X2 = """Warm up walking for 3 minutes, starting easy and build to a brisk pace by the end.
Run 10 minutes in your easy yellow zone effort.
Repeat 6 times:
Run 2 minute at your Red Zone Effort (Zone 5)
Follow with 3 minutes of very easy jogging or walking to catch your breath.
Run 5 minutes in your easy yellow zone effort.
Cool down walking for 3 minutes, starting at a brisk pace and slowing by the end."""
TEMPO_5X5 = """Warm up walking for 3 minutes, starting easy and build to a brisk pace by the end.
Run 10 minutes in your easy yellow zone effort (Zone 1-2).
Repeat 5 times:
Run 5 minutes at the top of your Orange Zone Effort (Zone 4)
Follow with 2 minutes of very easy jogging or walking to catch your breath.
Run 10 minutes in your easy yellow zone effort.
Cool down walking for 3 minutes, starting at a brisk pace and slowing by the end."""
HILL_TEMPO = """Warm up walking for 3 minutes, starting easy and build to a brisk pace by the end.
Run 10 minutes in your easy yellow zone effort (Zone 1-2).
Run 25 minutes on a rolling hilly course (outside or treadmill) and focus on adjusting your speed to stay at the top of your Orange Zone Effort (Zone 4).
This means slowing on the uphill, and increasing speed on the downhill.
This incredible workout teaches you how to run by the terrain, by your body and with the flow. This will be a game-changer on race day!
Run 5 minutes in your easy yellow zone effort.
Cool down walking for 3 minutes, starting at a brisk pace and slowing by the end"""
running["ultra-a"] = [
    Week(
        TrainingItem("Run 45 min", "Easy Run 45-50 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes orange zone"),
        TrainingItem("Run 45 min", "Easy run 45-50 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes orange zone"),
        TrainingItem("Run 4 miles", "Easy run 4 miles yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
        REST,
    ),
    # week 2
    Week(
        TrainingItem("Run 45 min", "Easy Run 45-50 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes orange zone"),
        TrainingItem("Run 45 min", "Easy run 45-50 minutes yellow zone"),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
        TrainingItem("Run 4 miles", "Easy run 4 miles yellow zone"),
    ),
    # week 3
    Week(
        REST,
        TrainingItem("Run 50 min", "Easy Run 50-60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes orange zone"),
        TrainingItem("Run 50 min", "Easy Run 50-60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes orange zone"),
        TrainingItem("Run 10 miles", "Long run 10 miles yellow zone"),
        REST,
    ),
    # week 4
    Week(
        TrainingItem("Run 50 min", "Easy Run 50-60 minutes yellow zone"),
        TrainingItem("Cross 50 min", "Cross-training 50 minutes orange zone"),
        TrainingItem("Run 45 min", "Easy run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy run 4 miles yellow zone"),
        TrainingItem("Run 7 miles", "Long run 8 miles yellow zone"),
        REST,
    ),
    # week 5
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill run 90 min", "Hill run orange zone\nlots of details in pdf"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy run 4 miles yellow zone"),
        TrainingItem("Run 12 miles", "Long run 12 miles yellow zone"),
        REST,
    ),
    # week 6
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill run 90 min", "Hill run orange zone\nlots of details in pdf"),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 10 miles", "Long run 10 miles yellow zone"),
        TrainingItem("Run 5 miles", "Run 5 miles yellow zone"),
    ),
    # week 7
    Week(
        REST,
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill run 90 min", "Hill run orange zone\nlots of details in pdf"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 14 miles", "Long run 14 miles yellow zone"),
        REST,
    ),
    # week 8
    Week(
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 3 miles", "Easy Run 3 miles yellow zone"),
        TrainingItem("Run 7 miles", "Long run 7 miles yellow zone"),
        REST,
    ),
    # week 9
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill run 90 min", "Hill run orange zone\nlots of details in pdf"),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy Run 4 miles yellow zone"),
        TrainingItem("Run 16 miles", "Long run 16 miles yellow zone"),
        REST,
    ),
    # week 10
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Speed 10x1 50 min", "Speed workout 10x1 red zone\n" + SPEED_10X1),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 12 miles", "Long run 12 miles yellow zone"),
        TrainingItem("Run 6 miles", "Long run 6 miles yellow zone"),
    ),
    # week 11
    Week(
        REST,
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Speed 10x1 50 min", "Speed workout 10x1 red zone\n" + SPEED_10X1),
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 18 miles", "Long run 18 miles yellow zone"),
        REST,
    ),
    # week 12
    Week(
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 3 miles", "Easy Run 3 miles yellow zone"),
        TrainingItem("Run 7 miles", "Long run 7 miles yellow zone"),
        REST,
    ),
    # week 13
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Speed 6x2 60 min", "Speed workout 6x2 red zone\n" + SPEED_6X2),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy Run 4 miles yellow zone"),
        TrainingItem("Run 20 miles", "Long run 20 miles yellow zone"),
        REST,
    ),
    # week 14
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Speed 6x2 60 min", "Speed workout 6x2 red zone\n" + SPEED_6X2),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 14 miles", "Long run 14 miles yellow zone"),
        TrainingItem("Run 7 miles", "Long run 7 miles yellow zone"),
    ),
    # week 15
    Week(
        REST,
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 7 miles", "Long run 7 miles yellow zone"),
        REST,
    ),
    # week 16
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 55 min", "Tempo Workout 5x5\n" + TEMPO_5X5),
        TrainingItem("Cross 45 min", "Cross-training 45 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy Run 4 miles yellow zone"),
        TrainingItem("Run 22 miles", "Long run 22 miles yellow zone"),
        REST,
    ),
    # week 17
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 55 min", "Tempo Workout 5x5\n" + TEMPO_5X5),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 16 miles", "Long run 16 miles yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
    ),
    # week 18
    Week(
        REST,
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
        REST,
    ),
    # week 19
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill tempo 45 min", HILL_TEMPO),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy run 4 miles yellow zone"),
        TrainingItem("Run 23 miles", "Long run 23 miles yellow zone"),
        REST,
    ),
    # week 20
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 55 min", "Tempo Workout 5x5\n" + TEMPO_5X5),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 18 miles", "Long run 18 miles yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
    ),
    # week 21
    Week(
        REST,
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Run 3 miles", "Easy run 3 miles yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
        REST,
    ),
    # week 22
    Week(
        TrainingItem("Run 60 min", "Easy Run 60 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Run 55 min", "Tempo Workout 5x5\n" + TEMPO_5X5),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30-40 minutes yellow zone"),
        TrainingItem("Run 12 miles", "Long run 12 miles yellow zone"),
        TrainingItem("Run 6 miles", "Long run  miles yellow zone"),
    ),
    # week 23
    Week(
        REST,
        TrainingItem("Run 50 min", "Easy Run 50 minutes yellow zone"),
        TrainingItem("Cross 45 min", "Cross-training 45-60 minutes yellow zone"),
        TrainingItem("Hill tempo 45 min", HILL_TEMPO),
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        TrainingItem("Run 8 miles", "Long run 8 miles yellow zone"),
        TrainingItem("Run 3 miles", "Easy run 3 miles yellow zone"),
    ),
    # week 24
    Week(
        REST,
        TrainingItem("Run 40 min", "Easy Run 40 minutes yellow zone"),
        TrainingItem("Run 30 min", "Easy Run 30 minutes yellow zone"),
        REST,
        TrainingItem("Run 20 min", "Easy Run 20 minutes yellow zone"),
        RACE,
        REST,
    ),
    # recovery weeks
    # week 25
    Week(
        REST,
        TrainingItem("Run 20 min", "Easy Run 20 minutes yellow zone"),
        REST,
        TrainingItem("Run 30 min", "Easy Run 30 minutes yellow zone"),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        TrainingItem("Run 3 miles", "Easy run 3 miles yellow zone"),
    ),
    # week 26
    Week(
        REST,
        TrainingItem("Run 30 min", "Easy Run 30 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        REST,
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        TrainingItem("Run 3 miles", "Easy run 3-5 miles yellow zone"),
        REST,
    ),
    # week 27
    Week(
        REST,
        TrainingItem("Run 30 min", "Easy Run 30 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        TrainingItem("Run 45 min", "Easy Run 45 minutes yellow zone"),
        TrainingItem("Cross 30 min", "Cross-training 30 minutes yellow zone"),
        TrainingItem("Run 4 miles", "Easy run 4-6 miles yellow zone"),
        REST,
    ),
]

# blue and white png ultra plan
# https://relentlessforwardcommotion.com/wp-content/uploads/2019/05/Beginner-50K-training-plan-Relentless-Forward-Commotion_Hart-Strength-Endurance-1-1024x576.png

#

# metric century training program
# https://www.endurancemag.com/2014/05/cycling-8-week-metric-training-plan/
bike: TrainingCollection = {
    "century":
    # week 1
    [
        Week(
            REST,
            TrainingItem("Bike 60 min", "Easy ride of 60 minutes at your own pace"),
            REST,
            TrainingItem("Bike 60 min", "Bike 60 min - 20 easy, 20 hard, 20 easy"),
            REST,
            TrainingItem("Bike 20 miles"),
            REST,
        ),
        Week(
            REST,
            TrainingItem("Bike 60 min", "Easy ride of 60 minutes"),  # week 2
            REST,
            TrainingItem("Bike 60 min", "Bike 60 min - 20 easy, 20 hard, 20 easy"),
            REST,
            TrainingItem("Bike 24 miles"),
            REST,
        ),
        Week(
            REST,
            TrainingItem("Bike 60 min", "60-minute ride with hills"),  # week 3
            REST,
            TrainingItem("Bike 60 min", "Bike 60 min - 15 easy, 30 hard, 15 easy"),
            REST,
            TrainingItem("Bike 30 miles"),
            REST,
        ),
        Week(
            REST,
            TrainingItem("Bike 60 min", "60-minute ride with hills"),  # week 4
            REST,
            TrainingItem("Bike 60 min", "Bike 60 min - 15 easy, 30 hard, 15 easy"),
            REST,
            TrainingItem("Bike 34 miles"),
            REST,
        ),
        # week 5
        Week(
            REST,
            TrainingItem(
                "Bike 60 min", "60-minute ride with hills, pushing the last 20 minutes"
            ),
            REST,
            TrainingItem("Bike 60 min", "Bike 60 min - 15 easy, 30 hard, 15 easy"),
            REST,
            TrainingItem("Bike 41 miles"),
            REST,
        ),
        # week 6
        Week(
            REST,
            TrainingItem(
                "Bike 60 min", "60-minute ride with hills, pushing the last 20 minutes"
            ),
            REST,
            TrainingItem(
                "Bike 60 min", "Bike 60 min - 10 easy, 10 hard, 3 repetitions"
            ),
            REST,
            TrainingItem("Bike 46 miles"),
            REST,
        ),
        # week 7
        Week(
            REST,
            TrainingItem(
                "Bike 60 min", "60-minute ride with hills, pushing the last 30 minutes"
            ),
            REST,
            TrainingItem(
                "Bike 60 min", "Bike 60 min - 10 easy, 10 hard, 3 repetitions"
            ),
            REST,
            TrainingItem("Bike 54 miles"),
            REST,
        ),
        # week 8
        Week(
            REST,
            TrainingItem(
                "Bike 60 min", "60-minute ride with hills, pushing the last 30 minutes"
            ),
            REST,
            TrainingItem(
                "Bike 60 min", "Bike 60 min - 10 easy, 10 hard, 3 repetitions"
            ),
            REST,
            RACE,
            REST,
        ),
    ]
}  # Bike metric century

# #### custom plan for 2021 - raw version
rawWacky = deepcopy(triathlon["olympic"])
# pad with rest
for i in range(8):
    rawWacky.append(Week(REST, REST, REST, REST, REST, REST, REST))
# merge with a marathon starting 2 weeks later
for i in range(len(running["marathon"])):
    newweek = list(running["marathon"][i])
    newweek.insert(0, REST)
    del newweek[-1]
    newweek[4], newweek[5] = newweek[5], newweek[4]
    rawWacky[i + 2] = Week(*newweek) + rawWacky[i + 2]


# function to aid making wacky
def makeWacky(left, right, sunday):
    newweek = [REST]
    newweek.append(left.mon)
    newweek.append(right.wed)
    newweek.append(left.wed)
    newweek.append(right.fri)
    newweek.append(right.sat)
    if isinstance(sunday, str):
        newweek.append(TrainingItem(sunday))
    else:
        newweek.append(sunday)
    return Week(*newweek)


# #### custom plan for 2021 - reduced version
wacky = triathlon["olympic"][:2]  # copy first weeks from triathlon
assert wacky[0].tue == triathlon["olympic"][0].tue

# overlap weeks
for i, descr in enumerate(
    (
        "Run 7 miles",
        "Run 7 miles",
        "Run 5.5 miles",
        "Run 9 miles",
        "Run 9.5 miles",
        "Run 6.5 miles",
        "Run 10 miles",
        "Run 11 miles",
        "Run 8.5 miles",
    )
):
    wacky.append(makeWacky(running["marathon"][i], triathlon["olympic"][i + 2], descr))
# race week
wacky.append(deepcopy(triathlon["olympic"][-1]))
# copy over the remainder of the marathon weeks
wacky.extend(deepcopy(running["marathon"][-8:-1]))
# final week is special
finalweek = deepcopy(running["marathon"][-1])
wacky.append(Week(REST, finalweek.mon, finalweek.tue, REST, finalweek.fri, REST, RACE))


# put together a single list of training
trainingplans: TrainingCollection = {**running, **bike, **triathlon}  # type: ignore
trainingplans["rawwacky"] = rawWacky
trainingplans["wacky"] = wacky

# update the length of fields for printing the table
for name in trainingplans.keys():
    lengths = findLengths(trainingplans[name])
    for i in range(len(trainingplans[name])):
        trainingplans[name][i].setTableLengths(lengths)
