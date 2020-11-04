import numpy as np
import math

def parallel_r(a, b):
    return 1.0 / (1.0 / a + 1.0 / b)

# Feedback Bias
# RCC - From VCC
# RF - Feedback from collector to base
# R1 - From base to ground
# RE - Un-bypassed from emitter to ground

# These are settings from EMRFD page 5.14
Vcc = 12
Rcc = 22
Rf = 1500
R1 = 680
Re = 47
b = 100

# Constants:
# Vcc
# Rcc (from Vcc to Vc)
# Rf (from Vc to Vb)
# R1 (from Vb to ground)
# Re (from Ve to ground)
# b (transistor beta)

# Variables
# 0: I1 (from Vcc to Vc)
# 1: I2 (from Vb to ground)
# 2: Ic (Collector current - inwards)
# 3: Ib (Base current - inwards)
# 4: Ie (Emitter current - outwards)
# 5: Vc
# 6: Vb
# 7: Ve

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
#    0 = -1 * Ic + b * Ib

Mbias = np.array([
# I1   I2   Ic   Ib   Ie   Vc   Vb   Ve
[ Rcc, 0,   0,   0,   0,   1,   0,   0 ],
[ 0,   Rf,  0,   Rf,  0,  -1,   1,   0 ],
[ 0,   R1,  0,   0,   0,   0,  -1,   0 ],
[ 0,   0,   0,   0,  Re,   0,   0,  -1 ],
[ 0,   0,   0,   0,   0,   0,   1,  -1 ],
[-1,   1,   1,   1,   0,   0,   0,   0 ],
[ 0,   0,   1,   1,  -1,   0,   0,   0 ],
[ 0,   0,  -1,   b,   0,   0,   0,   0 ],
])

y = np.array([ Vcc, 0, 0, 0, 0.7, 0, 0, 0])

Mbias_inv = np.linalg.inv(Mbias)
#print(Minv)

vars = Mbias_inv.dot(y)
print("I1 = ", vars[0])
print("I2 = ", vars[1])
print("Ic = ", vars[2])
print("Ib = ", vars[3])
print("Ie = ", vars[4])
print("Vc = ", vars[5])
print("Vb = ", vars[6])
print("Ve = ", vars[7])

# Create the bias currency in mA
Ie_ma = vars[4] * 1000.0

# Small signal analysis

# Variables
# 0: Iin - Input from source
# 1: I1 - From Vb to ground
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

print("Bias current in mA", Ie_ma)

# NOTE: There is a bypassed emitter resistor
Re = parallel_r(47, 8.2)
Vin = 1
Rs = 50
# Transformer
Rl = 200
b = 300 / 7
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
print("Small Signal Analysis")
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

print("Gain dB = ", G)
print("Zin = ", vars[6] / vars[0])