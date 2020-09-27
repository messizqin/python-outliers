"""
Author: Messiz Qin https://github.com/Weilory

find outliers from data
support one set of x values and  multiple sets of y values x & [y, y, y...]

according to Engineering Statistics Handbook, the value m is a control which indicate interplay of purity and efficiency,
which signals sample size, how many measurements are affordable to throw away.

Inspired by
1. Why and When to Optimize Efficiency Time Purity, Benno List, 31/07/2002, https://www.desy.de/~blist/notes/whyeffpur.ps.gz
1. Numpy Builtin Outlier Rejection, Benjamin Bannier, https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
2. Engineering Statistics Handbook, Information Technology Laboratory (ITL), https://www.itl.nist.gov/div898/handbook/eda/section3/eda35h.htm

"""

from regression.regress import regression

import tkinter as tk
import random

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

import numpy as np


""" MAIN """


def to_array(arr: list) -> np.array:
    return np.array(arr)


def main_ploting(
        title_: str,
        xlabel_: str,
        ylabel_: str,
        legends_: [str],
        average_color_: str,
        average_fill_: str,
):

    """
        if you want to edit the information of your graphic, edit this function
    """

    plt.title(title_)
    plt.xlabel(xlabel_)
    plt.ylabel(ylabel_)
    # xy use is the non-outlier data connected by line
    if len(PrivateConstant.XUSE[0]) != 0:
        for i, xs in enumerate(PrivateConstant.XUSE):
            if i == len(PrivateConstant.XUSE) - 1:
                plt.plot(xs, list(PrivateConstant.YUSE[i]), color=average_color_, alpha=0.5, label='average')
                const = np.average(list(PrivateConstant.YUSE[i]))
                plt.axhline(y=const, color=average_color_, linestyle='-.')
                plt.fill_between(xs, const, list(PrivateConstant.YUSE[i]), color=average_fill_, alpha=0.25)
            else:
                plt.plot(xs, list(PrivateConstant.YUSE[i]), color=PrivateConstant.COLORS[i], alpha=0.5,
                         label=legends_[i])
    plt.legend(loc='upper left')
    print('standard deviation: ', PrivateConstant.STDAVG)


class PrivateConstant:
    STDAVG = None
    XUSE = None
    YUSE = None
    SIGMA = None
    COLORS = None


def graph(
        xs: list,
        ys: list,
        title: str,
        xlabel: str,
        ylabel: str,
        legends: [str],
        left_shift: float or int = 0,
        upper_shift: float or int = 0,
        shift_rate: float or int = 0,
        average_color: str = 'blue',
        average_fill: str = 'cyan',
):
    x_val = list(map(to_array, [xs for xx in range(len(ys))]))
    y_val = list(map(to_array, ys))
    formulas = []

    for iq, xv in enumerate(x_val):
        yv = y_val[iq]
        expr = regression(x=xv.tolist(), y=yv.tolist())
        formulas.append(expr.formula)

    x_val = np.concatenate((x_val, [x_val[-1].copy()]))

    y_avg = []
    for ho in range(len(y_val[0])):
        co = 0
        pl = 0
        for ve in range(len(y_val)):
            co += 1
            pl += y_val[ve][ho]
        y_avg.append(float(pl / co))

    y_val.append(np.array(y_avg))
    formulas.append(regression(x=x_val[-1].tolist(), y=y_avg).formula)

    # linear regression = (x_var:number, *args):y_var
    # return 2 * np.pi * np.sqrt(float(x_var) / k)

    def concat1(arr):
        res = []
        for i in arr:
            res.append(i)
        return np.array(res)

    def concat2(arr):
        res = []
        for brr in arr:
            res.append(concat1(brr))
        return res

    PrivateConstant.YUSE = concat2(y_val)
    PrivateConstant.XUSE = concat2(x_val)
    PrivateConstant.STDAVG = 0

    matplotlib.use('TkAgg')
    plt.style.use('ggplot')
    root = tk.Tk()

    fig = plt.figure(1)
    plt.ion()

    PrivateConstant.SIGMA = 0
    PrivateConstant.COLORS = ["#%06x" % random.randint(0, 0xFFFFFF) for x in range(len(y_val) - 1)]

    def generator():
        a = -1
        while True:
            a += 1
            yield a

    g = generator()

    def gen():
        return int(g.__next__())

    def to_abs(num):
        return abs(num)

    # [[useful<dict>, outliers<dict>]...]
    def reject_outliers(y_data_frame, x_data_frame, fo_data_frame, m=1):
        res = []
        for iq, y_raw_data in enumerate(y_data_frame):
            x_raw_data = x_data_frame[iq]
            fo = fo_data_frame[iq]
            y_should = np.array(list(map(fo, x_raw_data)))
            data = np.array(list(map(to_abs, y_should - y_raw_data)))
            PrivateConstant.STDAVG = np.std(data)
            mean = np.mean(data)
            res.append([{}, {}])
            for i, d in enumerate(data):
                if abs(d - mean) < float(m) * PrivateConstant.STDAVG:
                    res[-1][0][i] = y_raw_data[i]
                else:
                    res[-1][1][i] = y_raw_data[i]
        return res

    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()

    def update():
        PrivateConstant.XUSE = []
        PrivateConstant.YUSE = []
        plt.clf()
        con = reject_outliers(y_data_frame=y_val, x_data_frame=x_val, fo_data_frame=formulas, m=PrivateConstant.SIGMA)
        for i, uo in enumerate(con):
            u_ys = uo[0].values()
            o_ys = uo[1].values()
            u_xs = []
            o_xs = []

            for k in uo[0].keys():
                u_xs.append(x_val[i][k])

            for j, k in enumerate(uo[1].keys()):
                o_xs.append(x_val[i][k])
                plt.annotate(
                    s='  (%.2f, %.2f)' % (x_val[i][k], y_val[i][k]),
                    xy=[float(x_val[i][k]) - left_shift * (j + 1) * shift_rate,
                        float(y_val[i][k]) + upper_shift * (j + 1) * shift_rate]
                )

            if i == len(con) - 1:
                plt.scatter(u_xs, u_ys, color=average_color, alpha=.4, linewidth=2)
                plt.scatter(o_xs, o_ys, color=average_color, linewidth=4)
            else:
                plt.scatter(u_xs, u_ys, color=PrivateConstant.COLORS[i], alpha=.4, linewidth=2)
                plt.scatter(o_xs, o_ys, color=PrivateConstant.COLORS[i], linewidth=4)

            PrivateConstant.XUSE.append(u_xs)
            PrivateConstant.YUSE.append(u_ys)
        fig.canvas.draw()

        main_ploting(
            title_=title,
            xlabel_=xlabel,
            ylabel_=ylabel,
            legends_=legends,
            average_color_=average_color,
            average_fill_=average_fill,
        )

    entry_var = tk.StringVar(root, 'graph')

    def save():
        plt.savefig(entry_var.get())

    def deviation(m):
        PrivateConstant.SIGMA = float(m)
        var.set(PrivateConstant.SIGMA)

    def re_color():
        PrivateConstant.COLORS = ["#%06x" % random.randint(0, 0xFFFFFF) for x in range(len(y_val))]
        update()

    var = tk.DoubleVar(root, 0)
    plot_widget.grid(row=gen(), column=0)
    tk.Button(root, text='color', command=re_color).grid(row=gen(), column=0)
    tk.Label(root, text='save file name').grid(row=gen(), column=0)
    tk.Entry(root, textvariable=entry_var).grid(row=gen(), column=0)
    tk.Button(root, text='Save', command=save).grid(row=gen(), column=0)
    tk.Button(root, text="Update", command=update).grid(row=gen(), column=0)
    scale_widget = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, resolution=0.01, length=400, command=deviation)
    scale_widget.grid(row=gen(), column=0)
    entry_widget = tk.Entry(root, textvariable=var)
    entry_widget.grid(row=gen(), column=0)

    def entry_event(the_val):
        the_val = float(the_val)
        if 0 <= the_val <= 10:
            scale_widget.set(the_val)
            update()

    entry_widget.bind("<Return>", lambda event: entry_event(var.get()))
    update()

    root.mainloop()


if __name__ == '__main__':

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

