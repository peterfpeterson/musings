---
layout: presentation
title: Lotka–Volterra
---

name: inverse
layout: true
class: center, middle, inverse
---
template: inverse

# Lotka–Volterra predator–prey equations

## &#x1F43A; vs &#x1F430;

More information on [<i class="fa fa-wikipedia-w" aria-hidden="true"></i>ikipedia](https://en.wikipedia.org/wiki/Lotka%E2%80%93Volterra_equations)

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

# What to cover - delete this

1. Who am I?
2. This doesn't *feel* like algebra
3. Lotka-Volterra equations
   1. Gentle introducion
   1. What is a model
   2. The actual equations
   3. Our simplification

---
# Who am I?

* PhD in Condensed Matter Phyics
* Work at Spallation Neutron Source at Oak Ridge National Laboratory

.center[![Who are you?](https://swanshadow.files.wordpress.com/2013/10/alwaysbeyourself.jpg)]

---
template: inverse

background-image: url(http://neutrons.ornl.gov/sites/default/files/Shull_Wollan_history-750.jpg)

.right[http://neutrons.ornl.gov]

???

Brief overview of what neutron scattering is/what it is used for
---

# Display and Inline

1. This is an inline integral: \(\int_a^bf(x)dx\)
2. More \\(x={a \over b}\\) formulae.

Display formula:

$$e^{i\pi} + 1 = 0$$

---

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
#Very brief introduction to calculus

.center[![The guys](http://www.todayifoundout.com/wp-content/uploads/2016/12/leibniz-and-newton-340x211.png)]


.center[[Who invented calculas](http://www.todayifoundout.com/index.php/2016/12/really-invented-calculus/)?]

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
# Integrals - Leibniz

.center[<img alt="integrals are just area" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Integral_as_region_under_curve.svg/744px-Integral_as_region_under_curve.svg.png" width='500'/>]

Related: [Riemann sum](https://en.wikipedia.org/wiki/Riemann_sum)

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
* \\(x \in\\) [0, &#x1F430;, &#x221E;)
* \\(y \in\\) [0, &#x1F43A;, &#x221E;)

---
# How do you "solve" that?

--
**Stability points:** Points where the population is stable

$$\frac{dx}{dt} = 0$$

$$\frac{dy}{dt} = 0$$
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
# Is there another?

$$\frac{dx}{dt} = \alpha x - \beta x y = 0$$

$$\frac{dy}{dt} = \delta x y - \gamma y = 0$$

--
solve prey equation for \\(y\\)

$$x y = \frac{\alpha x}{\beta} \Rightarrow y = \frac{\alpha}{\beta}$$

--
solve the preditor equation for \\(x\\)

$$x y = \frac{\gamma y}{\delta} \Rightarrow x = \frac{\gamma}{\delta}$$

---
# Is there another? (pt 2)

$$(x,y) = (\frac{\gamma}{\delta}, \frac{\alpha}{\beta})$$

Check our math by substituting in for \\(x\\) and \\(y\\) yields

$$\frac{dx}{dt} = \alpha \frac{\gamma}{\delta} - \beta \frac{\gamma}{\delta} \frac{\alpha}{\beta} = \frac{\alpha \gamma}{\delta} - \frac{\alpha \gamma}{\delta} = 0$$

$$\frac{dy}{dt} = \delta \frac{\gamma}{\delta} \frac{\alpha}{\beta} - \gamma \frac{\alpha}{\beta} = \frac{\alpha \gamma}{\beta} - \frac{\alpha \gamma}{\beta} = 0$$

--
The two fixed points are \\((x,y) = (0,0)\\) and \\((x,y) = (\frac{\gamma}{\delta}, \frac{\alpha}{\beta})\\)
---
.center[[plot of the two stable points](quiverplot_py.html)]

---
# One is missing

## There are no preditors

$$\frac{dx}{dt} = \alpha x$$

$$\frac{dy}{dt} = 0$$

## There are no prey

$$\frac{dx}{dt} = 0$$

$$\frac{dy}{dt} = - \gamma y$$
---
# Various values

<center><table>
<tr><th>alpha</th><th>beta</th><th>delta</th><th>gamma</th><th>&nbsp;</th></tr>
<tr><td>100</td><td>5</td><td>1</td><td>10</td><td><a href='quiverplot_100_5_1_10.html'>link</a></td></tr>
<tr><td>10</td><td>50</td><td>1</td><td>10</td><td><a href='quiverplot_10_50_1_10.html'>link</a></td></tr>
<tr><td>10</td><td>5</td><td>1</td><td>10</td><td><a href='quiverplot_10_5_1_10.html'>link</a></td></tr>
<tr><td>10</td><td>1</td><td>10</td><td>1</td><td><a href='quiverplot_10_1_10_1.html'>link</a></td></tr>
<tr><td>10</td><td>5</td><td>10</td><td>1</td><td><a href='quiverplot_10_5_10_1.html'>link</a></td></tr>
</table></center>

.center[&#x1F43A; &#x1F430;]
