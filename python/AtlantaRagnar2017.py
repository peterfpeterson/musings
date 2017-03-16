#!/usr/bin/env python3
from __future__ import (absolute_import, division, print_function)

import json
import numpy as np
import pandas as pd
from datetime import datetime
### plotly
from plotly import tools as toolsly
from plotly.offline import plot
import plotly.graph_objs as go
### matplotlib
#import matplotlib
#import matplotlib.pyplot as plt
#plt.xkcd()

# setup list of legs
legs = np.array([3.8, 4.8, 6.7])
#print('short', legs)
legs_full  = np.tile(legs,8)
legs_ultra = legs_full[:12]+legs_full[1:13]
legs_full  = np.insert(legs_full, 0, 0.)
legs_ultra = np.insert(legs_ultra, 0, 0.)
#print('full ', legs_full, legs_full.size, legs_full.sum())
#print('ultra', legs_ultra, legs_ultra.size, legs_ultra.sum())

# setup list of all runners
runner = np.array([1,2,3,4])
runner = np.repeat(runner,2) # since it is an ultra each runner is twice in a row
runner = np.tile(runner,3) # and three of those
runner = np.insert(runner, 0, 0) # get a slot for the time
#print('runner', runner, runner.size)

# accumulate a list of distances
race = pd.DataFrame({'leg':np.arange(25),
                     'distance':legs_full,
                     'runner': runner,
                  })
race['distance_accum'] = np.add.accumulate(race['distance'])
#print(race)
# debug matplotlib plot
#fig, axes  = plt.subplots()
#axes.plot(np.arange(legs_full.size)+1, np.add.accumulate(legs_full), label='full')
#axes.plot(np.arange(legs_ultra.size)+1, np.add.accumulate(legs_ultra), label='ultra')
#axes.legend()

# setup times for runners
runners = pd.DataFrame({'runner':np.arange(5),
                        'name':['NA', 'Josh', 'Ross', 'Dan', 'Pete'],
                        'pace':[np.timedelta64(int(0), 's'),
                                np.timedelta64(int(8*60), 's'),
                                np.timedelta64(int(7*60), 's'),
                                np.timedelta64(int(6*60+45), 's'),
                                np.timedelta64(int(9*60), 's')]})
runners = runners.set_index('runner') # must be a better way
#print(runners)

# taken from https://www.timeanddate.com/sun/usa/atlanta
sunset = np.datetime64('2017-04-21T20:13')
sunrise = np.datetime64('2017-04-22T06:57')

# calculate the leg times for the actual races
time_error = np.timedelta64(int(30), 's')
time_zero = np.timedelta64(int(0), 's')
leg_time = []
leg_time_fast = []
leg_time_slow = []
for index, row in race.iterrows():
    if row.runner == 0:
        leg_time.append(time_zero)
        leg_time_fast.append(time_zero)
        leg_time_slow.append(time_zero)
    else:
        leg_time.append(row.distance*runners.loc[row.runner].pace)
        leg_time_fast.append(row.distance*(runners.loc[row.runner].pace-time_error))
        leg_time_slow.append(row.distance*(runners.loc[row.runner].pace+time_error))
race['time'] = leg_time
race['time_fast'] = leg_time_fast
race['time_slow'] = leg_time_slow
race['time_accum'] = np.add.accumulate(race['time'])
race['time_accum_fast'] = np.add.accumulate(race['time_fast'])
race['time_accum_slow'] = np.add.accumulate(race['time_slow'])
#print(race)

# set a start time and calculate when the magic happens
time_start = np.datetime64('2017-04-21T12:00')
for label in ['time_accum', 'time_accum_fast', 'time_accum_slow']:
    race[label] = [ time_start+time_accum for time_accum in race[label]]
#print(race)

# load in the actual times
with open('../docs/AtlantaRagnar2017/actual.json', 'r') as handle:
    actual = json.load(handle)
    actual = [np.datetime64(item) for item in actual]
while len(actual) < 12: # magic number related to number of legs
    actual.append(None)

# put together the json document
leg_descr = {0:'gre/yel',
             1:'red/gre',
             2:'yel/red'}
leg_miles = {0:8.6,
             1:10.5,
             2:11.5}
json_data = []
for index, row in race.iterrows():
    if index%2 != 0: # it is an ultra
        continue
    if index == 0:
        continue

    runner = ''
    if row.runner != 0:
        runner = runners.loc[row.runner]['name']

    leg_type = int(row.leg/2-1)%3

    start = race.iloc[index-2]['time_accum']
    real = actual[int(row.leg/2-1)]
    if real is None:
        real = ''
    else:
        diff = start - real
        diff = str(diff).split(' ')[-1]
        diff = 'h'.join(diff.split(':')[:2]) + 'm'
        if real <= start:
            real = '%s (-%s)' % (real.astype(datetime).strftime('%H:%M'), diff)
        else:
            real = '%s (+%s)' % (real.astype(datetime).strftime('%H:%M'), diff)
    start = race.iloc[index-2]['time_accum'].strftime('%H:%M')

    time = str(race.iloc[index-1]['time'] + race.iloc[index]['time']).split(' ')[-1]
    time = 'h'.join(time.split(':')[:2]) + 'm'

    json_data.append({'leg':int(row['leg']/2),
                      'runner':runner,
                      'descr':leg_descr[leg_type],
                      'miles':leg_miles[leg_type],
                      'start':start,
                      'elapse':time,
                      'actual':real})
# write out the json doc
#print(json.dumps(json_data, indent=2))
with open('../docs/AtlantaRagnar2017/data.json', 'w') as handle:
    json.dump(json_data, handle, sort_keys=True)

# generate the plotly plot
plotly_args = {'filename': '../docs/AtlantaRagnar2017/plot.html',
               #'output_type': 'div',
               #'include_plotlyjs': False
               }

# define various useful colors
color = dict(cone='#aaaaaa',
             predicted='#555555',
             actual='#7777ff',
             easy='#bbfb9d',
             medium='#fbf59b',
             hard='#fbae9d')

# only the legs that matter
mask = race['leg']%2 == 0
mask[0] = True
def magic(race, label):
    return race[label][mask]

# bounding box
distance_bounds = [race.distance_accum[0], race.distance_accum[race.distance_accum.size-1]]
time_bounds = [race.time_accum_slow[0], race.time_accum_slow[race.distance_accum.size-1]]

# ultra race distance array
distance = magic(race, 'distance_accum')

# color bar for difficulties of doubles
doubles_pos = time_start + np.timedelta64(15,'m') # minutes offset

y = np.array([doubles_pos, doubles_pos, None])
y = np.tile(y, 4)
doubles_g = go.Scatter(x=distance,
                       y=y,
                       line=dict(shape='spline', color=color['easy'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

y = np.array([None, doubles_pos, doubles_pos])
y = np.tile(y, 4)
doubles_y = go.Scatter(x=distance,
                       y=y,
                       line=dict(shape='spline', color=color['medium'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

y = np.array([doubles_pos, None, doubles_pos])
y = np.tile(y, 5) # just keep the pattern going
y[:3] = [None, None, doubles_pos]
doubles_r = go.Scatter(x=distance,
                       y=y,
                       line=dict(shape='spline', color=color['hard'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

# color bar for difficulties of singles
singles_pos = time_start + np.timedelta64(0,'m') # minutes offset

y = np.array([singles_pos, singles_pos, None])
y = np.tile(y, 8)
singles_g = go.Scatter(x=race['distance_accum'],
                       y=y,
                       line=dict(shape='spline', color=color['easy'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

y = np.array([None, singles_pos, singles_pos])
y = np.tile(y, 8)
singles_y = go.Scatter(x=race['distance_accum'],
                       y=y,
                       line=dict(shape='spline', color=color['medium'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

y = np.array([singles_pos, None, singles_pos])
y = np.tile(y, 9) # just keep the pattern going
y[:3] = [None, None, singles_pos]
singles_r = go.Scatter(x=race['distance_accum'],
                       y=y,
                       line=dict(shape='spline', color=color['hard'], width=10),
                       mode='lines',
                       hoverinfo='skip',
                       showlegend=False)

# prediction cone
fast = go.Scatter(x=distance,
                  y=magic(race,'time_accum_fast'),
                  name='fast',
                  line=dict(shape='spline', color='transparent'),
                  mode='lines',
                  showlegend=False,
                  hoverinfo='skip',
                  fill='tonextx',
                  fillcolor=color['cone'])
slow = go.Scatter(x=distance,
                  y=magic(race, 'time_accum_slow'),
                  name='slow',
                  line=dict(shape='spline', color='transparent'),
                  mode='lines',
                  hoverinfo='skip',
                  showlegend=False)

# actual times
actual = [item for item in actual
          if item is not None]
actual = go.Scatter(x=distance[:len(actual)],
                    y=actual,
                    name='actual',
                    line=dict(shape='spline', color=color['actual'], width=2),
                    mode='lines',
                    #hoverinfo='skip',
                    showlegend=False)

# predicted line
pred_text = []
for x, y, leg in zip(distance, magic(race,'time_accum'), magic(race,'leg')):
    leg_type = leg%3
    leg = int((leg+1)/2)+1
    runner = leg%4
    if runner == 0:
        runner = 4
    runner = runners.iloc[runner]['name']

    if leg == 13: # finish line
        text = 'finish'
    else:
        text = 'leg %d - %.1f miles' % (leg, leg_miles[leg_type])
        text += '<br>%s - %s' % (runner, leg_descr[leg_type])
    pred_text.append(text)
prediction = go.Scatter(x=distance,
                        y=magic(race,'time_accum'),
                        text=pred_text,
                        name='prediction',
                        line=dict(shape='spline', color=color['predicted'], width=2),
                        mode='lines',
                        showlegend=False)




# add some annotations
annotations = []
if sunrise < time_bounds[-1]:
    annotations.append(dict(x=0, y=sunrise, text='\u263C sunrise', showarrow=False, xanchor='left'))
annotations.append(dict(x=0, y=sunset, text='\u263D sunset', showarrow=False, xanchor='left'))

# put together the final plot
layout = go.Layout(xaxis={'title': 'miles',
                          'showgrid':False,'showline':False},
                   yaxis={'showgrid':False,'showline':False,
                          'zeroline':False},
                   margin={'r':0,'t':0},
                   annotations=annotations
)
fig = go.Figure(data=[singles_g, singles_y, singles_r,
                      doubles_g,doubles_y,doubles_r,
                      slow,fast,prediction,
                      actual],
                layout=layout)
plot(fig, show_link=False, **plotly_args)

"""
# In[9]:

distance_bounds = [race.distance_accum[0], race.distance_accum[race.distance_accum.size-1]]
time_bounds = [race.time_accum_slow[0], race.time_accum_slow[race.distance_accum.size-1]]


# In[10]:
fig, axes  = plt.subplots(figsize=(5,7))

# color the legs
colors = ['#bbfb9d', '#fbf59b', '#fbae9d']
for i in range(race.distance_accum.size-1):
    axes.fill_between([race.distance_accum[i], race.distance_accum[i+1]], time_bounds[0], time_bounds[1],
                      facecolor=colors[i%3], linewidth=0)

# sunrise/sunset
axes.fill_between(distance_bounds, [sunset, sunset],
                  [sunrise, sunrise], facecolor='#666666', linewidth=0, alpha=.2)

# predict range of times
axes.fill_between(race.distance_accum,
                  race['time_accum_slow'].values, race['time_accum_fast'].values,
                  facecolor='#aaaaaa', linewidth=0)

# format the y-axis
axes.yaxis.set_major_locator(matplotlib.dates.HourLocator(interval=2))
axes.yaxis.set_major_formatter(matplotlib.dates.DateFormatter('%H:%M'))
axes.invert_yaxis()

# format the x-axis
axes.set_xlim(distance_bounds[0], distance_bounds[1])
axes.xaxis.set_major_locator(matplotlib.ticker.FixedLocator([0.,30.,60.,90.,120.]))

#axes.set_aspect(200)

fig.savefig('docs/AtlantaRagnar2017/race.svg')
"""

# In[ ]:
