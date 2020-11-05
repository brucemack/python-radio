import numpy as np
import math
from util import *

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
    vars = Mbias_inv.dot(Y)

    result = {
        "I1": vars[0],
        "I2": vars[1],
        "Ic": vars[2],
        "Ib": vars[3],
        "Ie": vars[4],
        "Vc": vars[5],
        "Vb": vars[6],
        "Ve": vars[7],
        "total_power": Vcc * vars[0],
        "device_power": (vars[5] - vars[7]) * vars[4]
        }

    return result


