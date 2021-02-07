# Python Outliers

:lying_face: :lying_face: :bomb: :bomb: :heartbeat: :heartbeat: :butterfly: :butterfly: :dizzy: :dizzy: :helicopter: :helicopter: 

#### *Illustating data and marking outliers*

<hr />

>GUI for graphing **one** set of x values with **multiple** set of y values, adjustable `m` to select how many values are regarded as outliers.

<hr />

* refers to https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list#comment114785064_11686720

## Get Started

```
git clone https://github.com/Weilory/python-outliers
```

place `outliers` folder to base level directory

<hr />

```python
from outliers.variance import graph

xs = [1, 2, 3, 4, 5]
ys1 = [3.2, 4.2, 5.3, 6.2, 7.1]
ys2 = [3.1, 4.3, 5.4, 6.4, 7.2]
ys3 = [3.2, 4.1, 5.1, 6.1, 7]

graph(
    xs=xs,
    ys=[ys1, ys2, ys3],
    title='Test title',
    xlabel='Test xlabel',
    ylabel='Test ylabel',
    legends=['x', '2x-3', '0.5x^2+2x+1'],
    average_color='red',
    average_fill='magenta',
)
```

![exp](https://github.com/Weilory/python-outliers/blob/master/docs/img/exp2.png)

<hr />

```python
from outliers.variance import graph

rts = [
        [280.5, 280.5, 280.6, 280.5, 280.6, 280.5, 280.5, 300.6],
        [280.5, 280.2, 279.9, 279.5, 279, 278, 279.5, 295.4],
        [280.4, 279.9, 279.2, 278.6, 277.5, 275.7, 278.5, 290.9],
        [280.3, 279.6, 278.6, 277.7, 276.1, 273.6, 277.6, 287.3],
        [280.3, 279.4, 278, 276.9, 274.8, 272.7, 276.9, 285.9],
        [280.2, 280.2, 277.4, 276.2, 274, 272, 276.2, 285],
        [280.2, 279, 276.9, 275.6, 273.4, 271.7, 275.5, 284.3],
        [280.1, 278.8, 276.4, 275, 272.9, 271.7, 274.9, 283.7],
        [280.1, 278.7, 275.9, 274.5, 272.6, 271.7, 274.4, 283.4],
        [280.1, 278.6, 277.5, 274.1, 272.4, 271.7, 274, 283.4],
    ]

dts = []
for ii in range(len(rts[0])):
    mts = []
    for dd in range(len(rts)):
        mts.append(rts[dd][ii])
    dts.append(mts)

x_val = [30 * x for x in range(10)]
y_val = dts

graph(
    xs=x_val,
    ys=y_val,
    title='CaCO3 HCl Reaction',
    xlabel='time(s)',
    ylabel='mass(g)',
    legends=['trial %d' % int(il + 1) for il in range(8)],
)
```

![exp](https://github.com/Weilory/python-outliers/blob/master/docs/img/exp.png)


# How does it work?

### standard deviation is defined as:

><a href="https://www.codecogs.com/eqnedit.php?latex=S&space;=&space;\sqrt{\frac{\sum{(x-\bar{x})^2}}{N}}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?S&space;=&space;\sqrt{\frac{\sum{(x-\bar{x})^2}}{N}}" title="S = \sqrt{\frac{\sum{(x-\bar{x})^2}}{N}}" /></a>

>where S is the standard deviation of a sample, x is each value in the data set, x bar is the mean of all values in the data set, N is the number of values in the data set. 

By this formula, we can work out the outlier of a stablized data. For example: 

>[38.2, 38.1, 38, 40, 39, 37.2, 25] -> 25



however, when exponential gets involved, for instance. if the equation is

><a href="https://www.codecogs.com/eqnedit.php?latex=y&space;=&space;kx&space;&plus;&space;b" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y&space;=&space;kx&space;&plus;&space;b" title="y = kx + b" /></a>

whereas the data follows a specific pattern, `standard error` becomes less efficient since it does not consider gradient of the polynomial.

To be specific, consider following data:

>[1, 3, 5.5, 7, 9, 12, 15]

by `standard deviation`, the result will always be the edge values

> [1, 15]

Although it actually should be

> [5.5]

**Therefore, we regress the data into an formula at first, then evaulate how far each value is from the formula, to decide which one should be outliers**

By using this module, we handle all postive integer exponential equation for you, whatever it is

> <a href="https://www.codecogs.com/eqnedit.php?latex=y&space;=&space;ax^3&space;&plus;&space;bx^2&space;&plus;&space;cx&space;&plus;&space;d" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y&space;=&space;ax^3&space;&plus;&space;bx^2&space;&plus;&space;cx&space;&plus;&space;d" title="y = ax^3 + bx^2 + cx + d" /></a>

even 

><a href="https://www.codecogs.com/eqnedit.php?latex=y&space;=&space;\frac{1}{(4x&plus;1)^2}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y&space;=&space;\frac{1}{(4x&plus;1)^2}" title="y = \frac{1}{(4x+1)^2}" /></a>

or 

><a href="https://www.codecogs.com/eqnedit.php?latex=y^4&space;=&space;\frac{9}{(2x&plus;1)^5}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?y^4&space;=&space;\frac{9}{(2x&plus;1)^5}" title="y^4 = \frac{9}{(2x+1)^5}" /></a>

In addition, all feature of `standard deviation` is inherited, which you can modify `m` to adjust `the propotion of data can be regarded as outlier`.

