from define_objects import *
import os
import random 
import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd



def convert_to_db(power):
    return 10*math.log10(power)

def convert_back_to_watt(db_value):
    return pow(10, float(db_value/10))

def snr(pt, gt, g_r, sigma_b, wavelength, total_pulses, Rt, Rr, Lb, N0):

    snr = 1.0
    snr = snr*(pt*gt*sigma_b*g_r*pow(wavelength, 2.0)*total_pulses)
    try :
        snr = snr/(pow(math.pi*2, 3)*Lb*N0*pow(Rt*Rr, 2.0))
    except ZeroDivisionError:
        return 1
    return snr

# SOurce http://dsp-book.narod.ru/RSAD/C1828_PDF_C02.pdf
#  Page NUmber 14
def rcs_sphere(radius, wavelength):
    k = 2*math.pi/wavelength
    if radius/wavelength < 0.01:
        return (9*math.pi*radius**2*pow((k*radius), 4))
    elif radius/wavelength > 100:
        return math.pi*pow(radius, 2)
    else:
        print('VERY Hard to solve analytically')

def find_current_snr(current_Rr, current_Rt):
    pt = convert_back_to_watt(30)
    gt = convert_back_to_watt(40)
    wavelength = 0.001
    Lb = convert_back_to_watt(20)
    N0 = convert_back_to_watt(-140)
    number_pulses = 10
    pulse_length = 8e-6
    minimum_snr_required = convert_back_to_watt(12)
    radius_of_incoming_target = 0.5

    # Caclulate the SNR 
    current_snr = snr(pt, gt, gt, rcs_sphere(radius = 0.5, wavelength = wavelength), wavelength,  number_pulses, \
        current_Rt, current_Rr, Lb, N0)
    
    if current_snr < minimum_snr_required:
        return False, current_snr
    else:
        return True, current_snr

if __name__ == "__main__":
    l = simulate()
    Rr, Rt = l[3], l[4]
    if os.path.isfile("results.txt"):
        os.remove("results.txt")
    f = open("results.txt", "a")
    snr_values = []
    for i in range(len(Rr)):
        transmitter_location = l[0][i]
        receiver_location = l[1][i]
        target_location = l[2][i]
        current_snr = find_current_snr(Rr[i], Rt[i])
        snr_values.append(convert_to_db(current_snr[1]))
        final = ["TRANSMITTER_COORDINATES : " + str(transmitter_location), "RECEIVER_COORDINATES : " + str(receiver_location), "TARGET_COORDINATES : " + str(target_location), "CURRENT_SNR : " + str(current_snr)]
        f.write(" ".join(final))
        f.write("\n")
    # plt.plot()
    columns = ["Rr", "Rt", "Snr_Values"]
    df = pd.DataFrame(columns= columns)
    df["Rr"] = l[3]
    df["Rt"] = l[4]
    df["Snr_Values"] = snr_values
    print(df.head())
    # sns.relplot(x="Rr", y="Rt", data=df["Snr_Values"])
    # plt.show()    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(df['Rr'], df['Rt'], df['Snr_Values'], c='blue', s=6)
    print(len(df["Rr"]) == len(df["Rt"]))
    # ax.view_init(30, 185)
    plt.xlabel('Receiver-Target-Distance')
    plt.ylabel('Transmitter-Target-Distance')
    # plt.zlabel('Snr')
    plt.show()

