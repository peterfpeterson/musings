---
layout: presentation
title: Lotka–Volterra
---

name: inverse
layout: true
class: center, middle, inverse
---
template: inverse
background-image: url(whiteboard.jpg)
background-position: center
background-size: cover

# Lotka–Volterra predator–prey equations

## &#x1F43A; vs &#x1F430;

???

Markdown cheatsheet https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
font awesome        http://fontawesome.io/icons/
Emoji unicode table http://apps.timwhitlock.info/emoji/tables/unicode

also see http://mathworld.wolfram.com/Lotka-VolterraEquations.html
https://stackoverflow.com/questions/28332217/solve-lotka-volterra-model-using-scipy
http://mathinsight.org/applet/lotka_volterra_versus_time
http://www.math.ku.dk/~moller/e04/bio/maple/lotka_volterra.html
http://epubs.siam.org/doi/pdf/10.1137/080723715

---
layout: false
class:
# Some acknowledgements

* [<i class="fa fa-wikipedia-w" aria-hidden="true"></i>ikipedia](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)
* [remark.js](https://remarkjs.com/) for browser based presentations
* [KaTex](https://github.com/Khan/KaTeX) is a browser based relative to [LaTex](https://www.latex-project.org/)
* <i class="fa fa-github" aria-hidden="true"></i> [GitHub](https://github.com/)

---
# Who am I?

* PhD in Condensed Matter Phyics
* Work at Spallation Neutron Source at Oak Ridge National Laboratory

.center[![Who are you?](https://swanshadow.files.wordpress.com/2013/10/alwaysbeyourself.jpg)]

---
background-image: url(https://neutrons.ornl.gov/sites/default/files/styles/splash_image_800x360/public/splash/SNS-aerial_0.jpg)
background-position: center
background-size: cover

# Spallation Neutron Source

---
# http://www.mantidproject.org <img alt="logo" src="https://docs.mantidproject.org/nightly/_images/Mantid_Logo_Transparent.png" width="15%"/>

.center[<img alt="pretty picture" src="https://docs.mantidproject.org/nightly/_images/release39.png" width="90%"/>]

.center[\\([h,k,0]\\) plane in slice viewer]

---
template: inverse

background-image: url(http://neutrons.ornl.gov/sites/default/files/Shull_Wollan_history-750.jpg)
background-position: center

.left[[Nobel prize in 1994](http://www.nobelprize.org/nobel_prizes/physics/laureates/1994/illpres/)]

.left[http://neutrons.ornl.gov]

???
Work was done in the 1950s
---
# Structure - How atoms are arranged

.center[<img alt="structure" src="http://www.nobelprize.org/nobel_prizes/physics/laureates/1994/illpres/3_are.gif" width="100%"/>]

---
# Dynamics - How atoms move

.center[<img alt="dynamics" src="http://www.nobelprize.org/nobel_prizes/physics/laureates/1994/illpres/5_do.gif" width="100%"/>]

---

# Public Service Announcement (PSA)

--
[Tau manifesto](http://tauday.com/tau-manifesto)

$$\tau = \frac{circumference}{radius}$$

--
Euler's identity:

$$e^{i\pi} + 1 = 0$$

--
...but using \\(\tau = 2 \pi\\)

$$e^{i\tau} = 1 + 0$$

---
# What is a Mathematical Model?

*n.* An abstract mathematical representation of a process, device or concept; it uses a number of variables to represent inputs, outputs and internal states, and sets of equations and inequalities to describe their interaction.

.right[via [wordnik](https://www.wordnik.com/words/mathematical%20model)]

---
# The model

The **Lotka–Volterra** equations, also known as the predator–prey
equations, are a pair of first-order, non-linear, differential
equations frequently used to describe the dynamics of biological
systems in which two species interact, one as a predator and the other
as prey. The populations change through time according to the pair of
equations:

$$\frac{dx}{dt} = \alpha x - \beta x y$$

$$\frac{dy}{dt} = \delta x y - \gamma y$$

where \\(x\\) is the number of prey \\(y\\) is the number of some
predator \\(\tfrac {dy}{dt}\\) and \\(\tfrac {dx}{dt}\\) represent the
growth rates of the two populations over time; \\(t\\) represents
time; and α, β, γ, δ are positive real parameters describing the
interaction of the two species.
--

.center[**It's all greek to me!**]

---
# [Greek Alphabet](https://en.wikipedia.org/wiki/Greek_alphabet) Cheat Sheet!

<center><table width="80%">
<tr>
  <td>&alpha;</td><td>alpha</td>
  <td>&beta;</td><td>beta</td>
  <td>&gamma;</td><td>gamma</td>
</tr>
<tr>
  <td>&delta;</td><td>delta</td>
  <td>&epsilon;</td><td>epsilon</td>
  <td>&zeta;</td><td>zeta</td>
</tr>
<tr>
  <td>&eta;</td><td>eta</td>
  <td>&theta;</td><td>theta</td>
  <td>&iota;</td><td>iota</td>
</tr>
<tr>
  <td>&kappa;</td><td>kappa</td>
  <td>&lambda;</td><td>lambda</td>
  <td>&mu;</td><td>mu</td>
</tr>
  <td>&nu;</td><td>nu</td>
  <td>&xi;</td><td>xi</td>
  <td>&omicron;</td><td>omicron</td>
</tr>
<tr>
  <td>&pi;</td><td>pi</td>
  <td>&rho;</td><td>rho</td>
  <td>&sigma;</td><td>sigma</td>
</tr>
<tr>
  <td>&tau;</td><td>tau</td>
  <td>&upsilon;</td><td>upsilon</td>
  <td>&phi;</td><td>phi</td>
</tr>
<tr>
  <td>&chi;</td><td>chi</td>
  <td>&psi;</td><td>psi</td>
  <td>&omega;</td><td>omega</td>
</tr>
</table></center>

--


.center[One more letter that the [latin alphabet](https://en.wikipedia.org/wiki/Latin_alphabet)]

---
#Very brief introduction to calculus

.center[![The guys](http://www.todayifoundout.com/wp-content/uploads/2016/12/leibniz-and-newton-340x211.png)]


.center[[Who invented calculus](http://www.todayifoundout.com/index.php/2016/12/really-invented-calculus/)?]

--
* Newton in 1665-1666

--
* Leibniz in 1675-1676

--
* Acta Eruditorium article was published in 1684

--
* Principia Mathematica was published in 1687

---
# Derivatives - Newton

.center[<img alt='derivatives are cool' src='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Tangent_derivative_calculusdia.svg/561px-Tangent_derivative_calculusdia.svg.png' width='500'/>]

---
# Derivatives are slope

$$y = m~x + b$$

--
Derivative with respect to \\(x\\)

$$y' = \frac{dy}{dx} = m$$

---
# Integrals - Leibniz

.center[<img alt="integrals are just area" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Integral_as_region_under_curve.svg/744px-Integral_as_region_under_curve.svg.png" width='500'/>]

Related: [Riemann sum](https://en.wikipedia.org/wiki/Riemann_sum)

---
# Integrals are area under a curve

$$y = m~x + b$$

--
Integrate from zero to \\(a\\)

$$\int_0^a m~x + b~dx = \frac{m}{2} a^2 + b~a = \frac{a}{2}\left\( m~a + 2~b \right\)$$

--
[Area of a trapezoid](http://www.mathgoodies.com/lessons/vol1/area_trapezoid.html) is

$$A = \frac{h}{2}\left\( b_1 + b_2 \right\)$$

with \\(h = a\\), \\(b_1 = b\\), and \\(b_2 = m~a+b\\)

--

Area of a recangle: integral of \\(y=b\\) is \\(A = a~b\\)

---
# What does that all mean?

$$\frac{dx}{dt} = \alpha x - \beta x y$$

$$\frac{dy}{dt} = \delta x y - \gamma y$$

* \\(x\\) is the number of prey (&#x1F430;)
* \\(y\\) is the number of predators (&#x1F43A;)
* α is related to prey birth rate (+ &#x1F430;)
* β is related to how often predators eat prey (- &#x1F430;)
* δ is related to predator population growth (+ &#x1F43A;)
* γ is related to predator death/emigration rate (- &#x1F43A;)

--
## Range and Domain

--
* &#x1F430; \\(x \in\\) [0, &#x221E;)
* &#x1F43A; \\(y \in\\) [0, &#x221E;)

---
# How do you "solve" that?

--
**Stability points:** Points where the population is stable

$$\frac{dx}{dt} = 0 = \alpha x - \beta x y$$

$$\frac{dy}{dt} = 0 = \delta x y - \gamma y$$

---
# There are no animals

$$(x,y) = (0,0)$$

.center[![tombstone](https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fi.imgur.com%2FwWfAm3S.jpg&f=1)]
---
# There are no animals

$$\frac{dx}{dt} = \alpha \times 0 - \beta \times 0 \times 0 = 0$$

$$\frac{dy}{dt} = \delta \times 0 \times 0 - \gamma \times 0 = 0$$

.center[![tombstone](https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fi.imgur.com%2FwWfAm3S.jpg&f=1)]
---
# One is missing

--
## There are no predators

$$\frac{dx}{dt} = \alpha x$$

$$\frac{dy}{dt} = 0$$

--
## There are no prey

$$\frac{dx}{dt} = 0$$

$$\frac{dy}{dt} = - \gamma y$$
---
# Is there another stability point?

$$\frac{dx}{dt} = 0 = \alpha x - \beta x y$$

$$\frac{dy}{dt} = 0 = \delta x y - \gamma y$$

--
solve prey equation for \\(y\\)

$$x y = \frac{\alpha x}{\beta} \Rightarrow y = \frac{\alpha}{\beta}$$

--
solve the predator equation for \\(x\\)

$$x y = \frac{\gamma y}{\delta} \Rightarrow x = \frac{\gamma}{\delta}$$

---
# Is there another? (pt 2)

$$(x,y) = (\frac{\gamma}{\delta}, \frac{\alpha}{\beta})$$

Check our math by substituting in for \\(x\\) and \\(y\\) yields

$$\frac{dx}{dt} = \alpha \frac{\gamma}{\delta} - \beta \frac{\gamma}{\delta} \frac{\alpha}{\beta} = \frac{\alpha \gamma}{\delta} - \frac{\alpha \gamma}{\delta} = 0$$

$$\frac{dy}{dt} = \delta \frac{\gamma}{\delta} \frac{\alpha}{\beta} - \gamma \frac{\alpha}{\beta} = \frac{\alpha \gamma}{\beta} - \frac{\alpha \gamma}{\beta} = 0$$

--
The two fixed points are \\((x,y) = (0,0)\\) and \\((x,y) = (\frac{\gamma}{\delta}, \frac{\alpha}{\beta})\\)

.center[[plot of the two stable points](quiverplot_py.html)]

---
# Quiver plot

.center[![quiver](http://matplotlib.org/_images/quiver_demo_00.png)]

---
# Various values

<center><table width="100%" text-align="center">
<tr bgcolor="#aaaaaa"><th>&alpha; (+ &#x1F430;)</th><th>&beta; (- &#x1F430;)</th><th>&delta; (+ &#x1F43A;)</th><th>&gamma; (- &#x1F43A;)</th><th>&gamma;/&delta;</th><th>&alpha;/&beta;</th><th>&nbsp;</th></tr>
<tr><td>100</td><td>5</td><td>1</td><td>10</td><td>10</td><td>20</td><td><a href='quiverplot_100_5_1_10.html'>quiver</a></td></tr>
<tr bgcolor="#dddddd"><td>10</td><td>50</td><td>1</td><td>10</td><td>10</td><td>0.2</td><td><a href='quiverplot_10_50_1_10.html'>quiver</a></td></tr>
<tr><td>10</td><td>5</td><td>1</td><td>10</td><td>10</td><td>2</td><td><a href='quiverplot_10_5_1_10.html'>quiver</a></td></tr>
<tr bgcolor="#dddddd"><td>10</td><td>1</td><td>10</td><td>1</td><td>0.1</td><td>10</td><td><a href='quiverplot_10_1_10_1.html'>quiver</a></td></tr>
<tr><td>10</td><td>5</td><td>10</td><td>1</td><td>0.1</td><td>2</td><td><a href='quiverplot_10_5_10_1.html'>quiver</a></td></tr>
</table></center>


.center[Generated with a [python script](https://github.com/peterfpeterson/musings/blob/master/docs/lotka_volterra/quiver.py)]