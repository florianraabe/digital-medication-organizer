#!/usr/bin/python

import argparse
import csv

import matplotlib.pyplot as plt
import numpy as np

w = 1920
h = 1080

x = []
y = []
x_clicks = []
y_clicks = []

def create_diagram(filename: str, background: str) -> None:

    with open(filename, newline='') as csvfile:

        spamreader = csv.reader(csvfile)

        row1 = next(spamreader)
        w = int(row1[4])
        h = int(row1[5])

        for row in spamreader:
            if int(row[1]) == 1:
                x_clicks.append(int(row[2]))
                y_clicks.append(int(row[3]))
            x.append(int(row[2]))
            y.append(int(row[3]))


    fig, ax = plt.subplots()

    ax.set_xlim([0, w])
    ax.set_ylim([h, 0])
    ax.set_axis_off()

    img = plt.imread(background)
    ax.imshow(img, extent=[0, 1920, 0, 830], origin='lower')

    plt.plot(np.array(x), np.array(y))
    plt.plot(np.array(x_clicks), np.array(y_clicks), 'ro')

    plt.tight_layout()
    plt.savefig(f"{filename}-result.png", dpi=800)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="csv file containing the data")
    parser.add_argument("background", help="background image")
    args = parser.parse_args()

    create_diagram(args.filename, args.background)