# Python Outliers

:lying_face: :lying_face: :bomb: :bomb: :heartbeat: :heartbeat: :butterfly: :butterfly: :dizzy: :dizzy: :helicopter: :helicopter: 

#### *Illustating data and marking outliers*

<hr />

>GUI for graphing **one** set of x values with **multiple** set of y values, adjustable `m` to select how many values are regarded as outliers.

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
