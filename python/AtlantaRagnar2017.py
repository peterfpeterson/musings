
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import matplotlib
get_ipython().magic(u'matplotlib notebook')
import matplotlib.pyplot as plt
plt.xkcd()


# In[2]:

legs = np.array([3.8, 4.8, 6.7])
print('short', legs)
legs_full  = np.tile(legs,8)
legs_ultra = legs_full[:12]+legs_full[1:13]
legs_full  = np.insert(legs_full, 0, 0.)
legs_ultra = np.insert(legs_ultra, 0, 0.)
print('full ', legs_full, legs_full.size, legs_full.sum())
print('ultra', legs_ultra, legs_ultra.size, legs_ultra.sum())

runner = np.array([1,2,3,4])
runner = np.repeat(runner,2)
runner = np.tile(runner,3)
runner = np.insert(runner, 0, 0)
print('runner', runner, runner.size)


# In[3]:

race = pd.DataFrame({'leg':np.arange(25),
                     'distance':legs_full,
                     'runner': runner,
                  })
race['distance_accum'] = np.add.accumulate(race['distance'])

race


# In[4]:

fig, axes  = plt.subplots()
axes.plot(np.arange(legs_full.size)+1, np.add.accumulate(legs_full), label='full')
axes.plot(np.arange(legs_ultra.size)+1, np.add.accumulate(legs_ultra), label='ultra')
axes.legend()


# In[5]:

runners = pd.DataFrame({'runner':np.arange(5),
                        'name':['NA', 'Dan', 'Josh', 'Pete', 'Ross'],
                        'pace':[np.timedelta64(int(0), 's'),
                                np.timedelta64(int(9*60+45), 's'),
                                np.timedelta64(int(10*60), 's'),
                                np.timedelta64(int(9*60+30), 's'),
                                np.timedelta64(int(7*60), 's')]})
runners = runners.set_index('runner') # must be a better way
runners


# In[6]:

# taken from https://www.timeanddate.com/sun/usa/atlanta
sunset = np.datetime64('2017-04-21T20:13')
sunrise = np.datetime64('2017-04-22T06:57')


# In[7]:

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
race


# In[8]:

time_start = np.datetime64('2017-04-21T12:00')
for label in ['time_accum', 'time_accum_fast', 'time_accum_slow']:
    race[label] = [ time_start+time_accum for time_accum in race[label]]
race


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


# In[ ]:



