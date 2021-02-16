import numpy as np
import math
from util import *

# This file contains the equations needed to do bias and
# small-signal (linear) analysis on a BJT amplifier with
# feedback from the collector to the base.


# ----- Bias Analysis ----------------------------------------------
#
# Inputs:
#   Vcc - Supply voltage
#   Rcc - From Vcc, low end bypassed to ground
#   Rf - Feedback from collector to base
#   R1 - From base to ground
#   Re - Un-bypassed part from emitter to ground
#   b - Transistor DC beta
#
# Outputs:
#   I1 - Current from Vcc in Amps
#   I2 (from Vb to ground through R1)
#   Ic (Collector current - inwards)
#   Ib (Base current - inwards)
#   Ie (Emitter current - outwards)
#   Vc Voltage at collector
#   Vb Voltage at base
#   Ve Voltage at emitter
#   total_power - Total power in Watts
#   device_power - Power dissipated in device in Watts
#
def calc_bias(Vcc, Rcc, Rf, R1, Re, b0):

    # Equations:
    # #0
    #   Vcc = Rcc * I1 + Vc
    #   Vcc = Rcc * I1 + 1 * Vc
    # #1
    #   Vc = Rf * (I2 + Ib) + Vb
    #   Vc = Rf * I2 + Rf * Ib + Vb
    #   0  = -1 * Vc + Rf * I2 + Rf * Ib + 1 * Vb
    # #2
    #   Vb = R1 * I2
    #    0 = -1 * Vb + R1 * I2
    # #3
    #   Ve = Re * Ie
    #   0  = -1 * Ve + Re * Ie
    # #4
    #   Vb = Ve + 0.7
    #   0.7 = 1 * Vb - 1 * Ve
    # #5
    #   I1 = I2 + Ib + Ic
    #    0 = -1 * I1 + 1 * I2 + 1 * Ib + 1 * Ic
    # #6
    #   Ie = Ib + Ic
    #    0 = -1 * Ie + 1 * Ib + 1 * Ic
    # #7
    #   Ic = b * Ib
    #    0 = -1 * Ic + b0 * Ib

    # Setup the system of equations
    Mbias = np.array([
        # I1   I2   Ic   Ib   Ie   Vc   Vb   Ve
        [Rcc, 0, 0, 0, 0, 1, 0, 0],
        [0, Rf, 0, Rf, 0, -1, 1, 0],
        [0, R1, 0, 0, 0, 0, -1, 0],
        [0, 0, 0, 0, Re, 0, 0, -1],
        [0, 0, 0, 0, 0, 0, 1, -1],
        [-1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 1, 1, -1, 0, 0, 0],
        [0, 0, -1, b0, 0, 0, 0, 0],
    ])
    Y = np.array([Vcc, 0, 0, 0, 0.7, 0, 0, 0])
    # Invert and solve
    Mbias_inv = np.linalg.inv(Mbias)
    a = Mbias_inv.dot(Y)

    result = {
        "I1": a[0],
        "I2": a[1],
        "Ic": a[2],
        "Ib": a[3],
        "Ie": a[4],
        "Vc": a[5],
        "Vb": a[6],
        "Ve": a[7],
        "total_power": Vcc * a[0],
        "device_power": (a[5] - a[7]) * a[4],
        "Rcc_power": (a[0] * a[0]) * Rcc,
        "Rf_power": (a[5] - a[6]) * (a[5] - a[6]) / Rf,
        "R1_power": (a[6] * a[6]) / R1,
        "Re_power": (a[7] * a[7]) / Re
        }

    return result


# ----- Small signal analysis -----

# Inputs:
#   Rs - Input source impedance
#   Rf - Total feedback resistance
#   R1 - From Vb to ground
#   Re - Total resistance from Ve to ground
#   Rl - Load resistance
#   Ie - Bias current in Amps
#   b - Small signal beta
#
# Outputs:
#   Iin - Input current from source
#   I1 - From Vb to ground via R1
#   Ib - Into Vb
#   I3 - From Vc to Vb via Rf
#   Il - Current into the load
#   Vc
#   Vb
#   Ve
#   Ie - Current out of emitter towards ground via Re
#
def calc_small_signal(Rs, Rf, R1, Re, Rl, Ie, b):

    Vin = 1
    # Emitter resistor (26 / Ie_ma)
    re = 26 / (Ie * 1000)

    # Equations
    #
    # 0: Vin = Rs * Iin + R1 * I1
    # 1: Vb = R1 * I1
    #    0 = -Vb + R1 * I1
    # 2: Vb = re * Ib + b * re * Ib + Ve
    #    0  = -Vb + (re + b * re) * Ib + Ve
    # 3: Vc = Rf * I3 + Vb
    #    0 = -Vc + Rf * I3 + Vb
    # 4: Ve = Re * Ib + (Re * b) * Ib
    #    0 = -Ve + (Re + Re * b) * Ib
    # 5: Vc = Rl * I4
    #    0 = -Vc + Rl * I4
    # 6: -I4 = I3 + b * Ib
    #    0 = I4 + I3 + b * Ib
    # 7: Iin + I3 = Ib + I1
    #    0 = -Iin -I3 + Ib + I1

    Mss = np.array([
    # Iin, I1,  Ib,  I3,  I4,  Vc,  Vb,  Ve

    [ Rs,  R1,  0,   0,   0,   0,   0,   0 ],
    [ 0,   R1,  0,   0,   0,   0,   -1,  0 ],
    [ 0,   0, re+re*b, 0, 0,   0,   -1,  1 ],
    [ 0,   0,   0,   Rf,  0,   -1,  1,   0 ],
    [ 0,   0, Re+Re*b, 0, 0,   0,   0,   -1 ],
    [ 0,   0,   0,   0,   Rl,  -1,  0,   0  ],
    [ 0,   0,   b,   1,   1,   0,   0,   0  ],
    [ -1,  1,   1,   -1,  0,   0,   0,   0  ]
    ])

    yss = np.array([ Vin, 0, 0, 0, 0, 0, 0, 0 ])
    Mss_inv = np.linalg.inv(Mss)
    v = Mss_inv.dot(yss)

    # Available power (assuming load is matched with source resistance)
    Pav = ((Vin / (Rs + Rs)) ** 2) * Rs
    # Power delivered to load
    Pout = ((v[5] / Rl) ** 2) * Rl
    # Gain in dB
    g = 10.0 * math.log10(Pout / Pav)
    # Implied Re
    re_implied = v[7] / (v[2] + b * v[2]);

    result = {
        "Iin": v[0],
        "I1": v[1],
        "Ib": v[2],
        "I3": v[3],
        "Il": v[4],
        "Vc": v[5],
        "Vb": v[6],
        "Ve": v[7],
        "Ie": v[2] + b * v[2],
        "gain": g,
        "zin": v[6] / v[0],
        "re_implied": re_implied
    }
    return result


# Computes the small-signal limit of the amplifier input,
# taking into account device limitations.
#
# Inputs:
#   vgap - The minimum required forward-bias voltage between
#     the collector and the base of the device.
#
def small_signal_limit(bias_result, ss_result, vgap):

    # Calculate the largest Vin can swing before the collector/base junction
    # goes inside of the forward-bias gap
    vin_max_0 = (vgap - bias_result["Vc"] + bias_result["Vb"]) / (ss_result["Vc"] - ss_result["Vb"])
    vin_max_0 = math.fabs(vin_max_0)

    # Calculate the largest Vin can swing before the bias current is
    # turned off.
    vin_max_1 = bias_result["Ie"] / ss_result["Ie"]
    vin_max_1 = math.fabs(vin_max_1)

    return min(vin_max_0, vin_max_1)
