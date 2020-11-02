import numpy as np

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

M = np.array([
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

Minv = np.linalg.inv(M)
#print(Minv)

vars = Minv.dot(y)
print("I1 = ", vars[0])
print("I2 = ", vars[1])
print("Ic = ", vars[2])
print("Ib = ", vars[3])
print("Ie = ", vars[4])
print("Vc = ", vars[5])
print("Vb = ", vars[6])
print("Ve = ", vars[7])