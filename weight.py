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

    with open('weight.csv') as weight_file:
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

def polyfit_data(data, graph_start_date, graph_end_date, ):
    polyfit_dates = []
    polyfit_weights = []
    for dat in data:
        if dat[0] >= graph_start_date:
            polyfit_dates.append(dat[0])
            polyfit_weights.append(dat[1])
    polyfit_x = mdates.date2num(polyfit_dates)

    z4 = np.polyfit(polyfit_x, polyfit_weights, 1)
    p4 = np.poly1d(z4)
    xx = np.linspace(polyfit_x.min(), polyfit_x.max(), 100)
    dd = mdates.num2date(xx)

    start_date = mdates.date2num(graph_start_date)
    end_date = mdates.date2num(graph_end_date)
    polyfit_date =  np.linspace(start_date, end_date, 100)

    return p4, polyfit_date
    

def plot_stuff(filename, age, height, is_male, weight_upper, weight_lower, graph_start_date, graph_end_date, lines, polyfit, show_deltas):
    data = get_weight_from_csv_file(filename)

    bmi_lower = bmi_from_weight(weight_lower, height)
    bmi_upper = bmi_from_weight(weight_upper, height)

    dates = [record[0] for record in data]
    y     = [record[1] for record in data]

    x = mdates.date2num(dates)

    fig, host = plt.subplots()
    
    fig.subplots_adjust(top=0.97, bottom=0.05, left=0.12, right=0.86)

    formatter = DateFormatter('%b-%d')
    plt.gcf().axes[0].xaxis.set_major_formatter(formatter)  
    ax2 = host.twinx()

    host.grid()
    host.set_ylim(weight_lower, weight_upper)
    host.set_xlim(graph_start_date, graph_end_date)
    host.plot(dates, y, '-', linewidth=3, color='black')

    if polyfit:
        p4, polyfit_date = polyfit_data(data, graph_start_date, graph_end_date)
        host.plot(polyfit_date, p4(polyfit_date), 'blue')
    # bmi axis
    ax2.set_ylabel("body mass index")
    ax2.set_ylim(bmi_lower, bmi_upper)


    for line in lines:
        ax2.plot([line[0], line[2]], [line[1], line[3]], color='red', linestyle='-', linewidth=1)


    plt.show()

def main():
    _height = 1.80
    plot_stuff(filename = 'weight.csv',
           age = -1,
           height = _height,
           is_male = True,
           weight_upper = 115.0,
           weight_lower = 70.0,
           graph_start_date = DT.datetime(2020,  7, 14),
           graph_end_date   = DT.datetime(2021, 3, 14),
           lines = [[DT.datetime(2020, 7, 14), bmi_from_weight(112.6, _height),
                     DT.datetime(2021, 3, 14), bmi_from_weight(72.6, _height)]
                   ],
           polyfit = True,
           show_deltas = True)

if __name__ == '__main__':
    main()
