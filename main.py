import numpy as np
import math
from util import *

# This file contains the equations needed to do bias and
# small-signal (linear) analysis on a BJT amplifier with
# feedback from the collector to the base.

# ----- Bias Analysis ----------------------------------------------
#
# Constants:
#   Vcc - Supply voltage
#   Rcc - From Vcc, low end bypassed to ground
#   Rf - Feedback from collector to base
#   R1 - From base to ground
#   Re - Un-bypassed part from emitter to ground
#   b - Transistor DC beta
#
# Variables:
#   0: I1 (from Vcc through Rcc)
#   1: I2 (from Vb to ground through R1)
#   2: Ic (Collector current - inwards)
#   3: Ib (Base current - inwards)
#   4: Ie (Emitter current - outwards)
#   5: Vc
#   6: Vb
#   7: Ve

# These are settings from the amplifier on EMRFD page 5.14
Vcc = 12
Rcc = 22
Rf = 1500
R1 = 680
Re = 47
b0 = 100

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
[ Rcc, 0,   0,   0,   0,   1,   0,   0 ],
[ 0,   Rf,  0,   Rf,  0,  -1,   1,   0 ],
[ 0,   R1,  0,   0,   0,   0,  -1,   0 ],
[ 0,   0,   0,   0,  Re,   0,   0,  -1 ],
[ 0,   0,   0,   0,   0,   0,   1,  -1 ],
[-1,   1,   1,   1,   0,   0,   0,   0 ],
[ 0,   0,   1,   1,  -1,   0,   0,   0 ],
[ 0,   0,  -1,   b0,  0,   0,   0,   0 ],
])
Y = np.array([ Vcc, 0, 0, 0, 0.7, 0, 0, 0])

# Invert and solve
Mbias_inv = np.linalg.inv(Mbias)
vars = Mbias_inv.dot(Y)

print("Bias Analysis:")
print()
print("I1 = ", vars[0])
print("I2 = ", vars[1])
print("Ic = ", vars[2])
print("Ib = ", vars[3])
print("Ie = ", vars[4])
print("Vc = ", vars[5])
print("Vb = ", vars[6])
print("Ve = ", vars[7])
print("Power usage (W):", Vcc * vars[0])

# Create the bias current in mA
Ie_ma = vars[4] * 1000.0
print("Transistor bias current (mA):", Ie_ma)
print("Transistor power (W):", (vars[5] - vars[7]) * vars[4])

# ----- Small signal analysis -----

# Constants
# Re - From Ve to ground
# Ft - Unity gain frequency
# Fop - Operating frequency

# Variables
# 0: Iin - Input from source via Rs
# 1: I1 - From Vb to ground via R1
# 2: Ib - Into Vb
# 3: I3 - From Vc to Vb via Rf
# 4: I4 - Current into the load
# 5: Vc
# 6: Vb
# 7: Ve

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


# NOTE: There is a bypassed emitter resistor
Re = parallel_r(47, 8.2)
Vin = 1
Rs = 50
# Transformer
Rl = 200
Ft = 300
Fop = 6
b = Ft / Fop
re = 26 / Ie_ma
print("re = ", re, " Re = ", Re)

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

vars = Mss_inv.dot(yss)
print()
print("Small Signal Analysis")
print()
print("Iin = ", vars[0])
print("I1 = ", vars[1])
print("Ib = ", vars[2])
print("I3 = ", vars[3])
print("I4 = ", vars[4])
print("Vc = ", vars[5])
print("Vb = ", vars[6])
print("Ve = ", vars[7])

# Available power (assuming load is matched with source resistance)
Pav = ((Vin / (Rs + Rs)) ** 2) * Rs
# Power delivered to load
Pout = ((vars[5] / Rl) ** 2) * Rl
# Gain in dB
G = 10.0 * math.log10(Pout / Pav)

print("Power gain (dB):", G)
print("Zin (ohms):", vars[6] / vars[0])