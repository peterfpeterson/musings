#!/usr/bin/env python3
from plotly import tools as toolsly
from plotly.offline import plot
import plotly.graph_objs as go
import numpy as np

##### parameters for everything

alpha = 10 # prey growth
beta  = 1 # predator eat
delta = 10. # predator growth
gamma = 1 # predator death

# second fixed point
(xfixed, yfixed) = (gamma /delta, alpha / beta)

# plotting parameters
xmax = 2. * xfixed
ymax = 2. * yfixed
numarrows = 20.

# grid for everything
x,y = np.meshgrid(np.arange(0, xmax, xmax/numarrows), np.arange(0, ymax, ymax/numarrows))

# vector of arrows
u = alpha * x - beta * x * y
v = delta * x * y - gamma * y

####################

title = 'alpha=%.1f beta=%.1f delta=%.1f gamma=%.1f' % (alpha, beta, delta, gamma)
ext = '_'.join([str(item) for item in [alpha, beta, delta, gamma]])
filename='quiverplot_'+ext+'.html'

htmlline = '</td><td>'.join([str(item) for item in [alpha, beta, delta, gamma]])
htmlline = '<tr><td>' + htmlline + '</td><a href=\'' + filename + '\'>link</a></td></tr>'
print(htmlline)

# fixed points
points = go.Scatter(x=[0, xfixed], y=[0, yfixed],
                    mode='markers',
                    marker=dict(size=12),
                    name='fixed points',)

options = {}
if len(ext) <= 0:
    options['visible'] = 'legendonly'


fig = toolsly.FigureFactory.create_quiver(x, y, u, v,
                                          scale=.01, arrow_scale=.1,
                                          name='density', **options)

fig['data'].append(points)
fig['layout']['xaxis'] = dict(range=[0., xmax])
fig['layout']['yaxis'] = dict(range=[0., ymax])
fig['layout']['title'] = title
plot(fig, show_link=False, filename='lotka_volterra/'+ filename)

# http://tributary.io/inlet/5211034
