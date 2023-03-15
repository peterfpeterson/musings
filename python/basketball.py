#!/usr/bin/env python
import random

def winPercent(win: int, lose: int) -> float:
    return float(win)/float(win+ lose)

def calcTerm(team1win: float, team2win: float) -> float:
    return team1win * (1-team2win) / (team1win * (1-team2win) + team2win * (1-team1win))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Predict which team will win based on their records',
                                     epilog="Equations are taken from https://sabr.org/journal/article/probabilities-of-victory-in-head-to-head-team-matchups/")
    parser.add_argument('team1win', type=int, help="Number of games team 1 has won")
    parser.add_argument('team1lose', type=int, help="Number of games team 1 has lost")
    parser.add_argument('team2win', type=int, help="Number of games team 2 has won")
    parser.add_argument('team2lose', type=int, help="Number of games team 2 has lost")
    options = parser.parse_args()

    team1Percent = winPercent(options.team1win, options.team1lose)
    team2Percent = winPercent(options.team2win, options.team2lose)
    expected = calcTerm(team1Percent, team2Percent)
    rando = random.random()

    print('team  W   L   percent')
    print(f'1    {options.team1win:3d} {options.team1lose:3d}  {team1Percent:5.3f}')
    print(f'2    {options.team2win:3d} {options.team2lose:3d}  {team2Percent:5.3f}')

    print('-'*21)
    print(f'EXP={expected:5.3f} RAN={rando:5.3f}')

    # this allows for rolling a 20
    # and further increases the odds by only using 3 digits
    if int(1000*rando) < int(1000*expected):
        print('team 1 wins')
    else:
        print('team 2 wins')
