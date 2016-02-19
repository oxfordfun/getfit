from __future__ import print_function
import csv, math

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as DT
from matplotlib.patches import Rectangle
from matplotlib.dates import DateFormatter

#font = { 'size' : 8 }

#mpl.rc('font', **font)

def kg_to_lbs(kg):
    return kg * 2.20462

def lbs_to_kg(lbs):
    return lbs / 2.20462

def bmi_from_weight(weight, height):
    return weight / (height * height)

def get_weight_from_csv_file(filename):
    data = []

    with open('weight.csv', 'rb') as weight_file:
        weight_reader = csv.reader(weight_file)

        for row in weight_reader:
            year   = int(row[0])
            month  = int(row[1])
            day    = int(row[2])
            weight = float(row[3])
            data.append((DT.datetime(year, month, day), weight))

    return data

def feet_inches_to_meters(feet, inches):
    return (feet * 12.0 + inches) * 2.54 / 100.0

def meters_to_feet_inches(meters):
    total_inches = meters * 100 / 2.54
    feet = int(math.floor(total_inches / 12))
    inches = int(math.floor(total_inches % 12))
    return feet, inches

# TODO
def absi(weight, height, waist_circumferance):
    return waist_circumferance / (bmi_from_weight(weight, height) ** (2.0/3.0) * height ** (1.0/2.0))

def estimate_bfp(bmi, age, is_male):
    if is_male:
        return 1.20 * bmi + 0.23 * age - 10.8 - 5.4
    else:
        return 1.20 * bmi + 0.23 * age + 5.4

def plot_stuff(filename, age, height, is_male, weight_upper, weight_lower, graph_start_date, graph_end_date, lines, polyfit, show_deltas):
    data = get_weight_from_csv_file(filename)

    bmi_lower = bmi_from_weight(weight_lower, height)
    bmi_upper = bmi_from_weight(weight_upper, height)

    dates = [record[0] for record in data]
    y     = [record[1] for record in data]

    x = mdates.date2num(dates)

    fig, host = plt.subplots()
    #fig.set_size_inches(5.8, 5.8, forward=True)
    fig.subplots_adjust(top=0.97, bottom=0.05, left=0.12, right=0.86)
    #plt.xticks(rotation = 90)
    formatter = DateFormatter('%b-%d')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)  
    ax2 = host.twinx()
    ax3 = host.twinx()
    ax4 = host.twinx()

    ax2.add_patch(Rectangle((x[0], 30),   x[-1], 50.0, facecolor="red",       alpha=0.2))
    ax2.add_patch(Rectangle((x[0], 25),   x[-1], 5.0,  facecolor="yellow",    alpha=0.2))
    ax2.add_patch(Rectangle((x[0], 18.5), x[-1], 6.5,  facecolor="green",     alpha=0.2))
    ax2.add_patch(Rectangle((x[0], 16),   x[-1], 2.5,  facecolor="steelblue", alpha=0.2))
    ax2.add_patch(Rectangle((x[0], 0),    x[-1], 16,   facecolor="blue",      alpha=0.2))

    #ax2.text(graph_start_date, 30.1, r' obese',       fontsize=15)
    #ax2.text(graph_start_date, 25.1, r' overweight',  fontsize=15)
    #ax2.text(graph_start_date, 18.6, r' normal',      fontsize=15)
    #ax2.text(graph_start_date, 16.1, r' underweight', fontsize=15)

    # weight axis
    # host.set_title("weight and BMI (height = {0}m)".format(height))
    # host.set_xlabel("date")
    host.grid()
    host.set_ylim(weight_lower, weight_upper)
    host.set_xlim(graph_start_date, graph_end_date)
    host.plot(dates, y, '-', linewidth=3, color='black')

    if polyfit:
        polyfit_dates = []
        polyfit_weights = []
        for dat in data:
            if dat[0] >= lines[0][0]:
                polyfit_dates.append(dat[0])
                polyfit_weights.append(dat[1])
        polyfit_x = mdates.date2num(polyfit_dates)

        z4 = np.polyfit(polyfit_x, polyfit_weights, 1)
        p4 = np.poly1d(z4)
        xx = np.linspace(polyfit_x.min(), polyfit_x.max(), 100)
        dd = mdates.num2date(xx)
        host.plot(dd, p4(xx), '-g')

    # bmi axis
    ax2.set_ylabel("body mass index")
    ax2.set_ylim(bmi_lower, bmi_upper)

    ax4.set_ylabel("change per day [kg]")
    ax4.yaxis.set_label_position('right')
    ax4.yaxis.set_ticks_position('right')
    ax4.spines["right"].set_position(("axes", 1.08))
    ax4.set_ylim(-0.5,0.5)
    # ax4.set_ylim(estimate_bfp(bmi_lower, age, is_male), estimate_bfp(bmi_upper, age, is_male))

    if show_deltas:
        changes = []
        days_length = []
        dd = mdates.date2num(dates)
        for i, d in enumerate(data):
            if i == 0:
                changes.append(0)
                days_length.append(0)
            else:
                date = d[0]
                weight = float(d[1])
                prev_date = data[i - 1][0]
                prev_weight = float(data[i - 1][1])
                days = float((date - prev_date).days)
                change = (weight - prev_weight) / days
                print(change, days)
                changes.append((weight - prev_weight) / days)
                days_length.append(dd[i - 1] - dd[i])
        ax4.bar(dates, changes, align = 'edge', linewidth = 0, width = days_length, alpha = 0.3, color = 'black')

    # draw weight-loss line
    for line in lines:
        ax2.plot([line[0], line[2]], [line[1], line[3]], color='red', linestyle='-', linewidth=1)

    #ax2.plot([line_start[0], line_end[0]], [line_start[1], line_end[1]], color='red', linestyle='-', linewidth=1)

    # lbs axis
    ax3.yaxis.set_label_position('left')
    ax3.yaxis.set_ticks_position('left')
    ax3.set_ylabel('weight [lbs/kg]')
    ax3.spines["left"].set_position(("axes", -0.055))
    ax3.set_ylim(kg_to_lbs(weight_lower), kg_to_lbs(weight_upper))

    plt.show()

def main():
    _height = 1.79

    plot_stuff(filename = 'weight.csv',
               age = -1,
               height = _height,
               is_male = True,
               weight_upper = 105,
               weight_lower = 69,
               #graph_start_date = DT.datetime(2015, 12, 1),
               graph_start_date = DT.datetime(2015,  7, 20),
               #graph_start_date = DT.datetime(2009,  8, 17),
               graph_end_date   = DT.datetime(2016, 4, 1),
               lines = [[DT.datetime(2015, 7, 24), bmi_from_weight(104.5, _height),
                         DT.datetime(2015,12, 31), bmi_from_weight( 80.0, _height)],
                        [DT.datetime(2015,12, 31), bmi_from_weight( 80.0, _height),
                         DT.datetime(2016, 3, 31), bmi_from_weight( 70.0, _height)]
                       ],
               polyfit = True,
               show_deltas = True)

if __name__ == '__main__':
    main()
