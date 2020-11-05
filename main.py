import numpy as np
import math
from util import *
from BJTFeedback import *

# These are settings from the amplifier on EMRFD page 5.14
Vcc = 12
Rcc = 22
Rf = 1500
R1 = 680
Re = 47
b0 = 100

br = calc_bias(Vcc, Rcc, Rf, R1, Re, b0)

print("Bias Analysis:")
print()
print("I1:", br["I1"])
print("I2:", br["I2"])
print("Ic:", br["Ic"])
print("Ib:", br["Ib"])
print("Ie:", br["Ie"])
print("Vc:", br["Vc"])
print("Vb:", br["Vb"])
print("Ve:", br["Ve"])
print("Power usage (W):", br["total_power"])

# Create the bias current in mA
Ie_ma = br["Ie"] * 1000
print("Transistor bias current (mA):", Ie_ma)
print("Transistor power (W):", br["device_power"])

# ----- Small signal analysis -----

Re = parallel_r(47, 8.2)
Vin = 1
Rs = 50
# Transformer
Rl = 200
Fr = 1500

Ft = 300
Fop = 7
b = Ft / Fop

ssr = calc_small_signal(Rs, Rf, R1, Re, Rl, br["Ie"], b)

print()
print("Small Signal Analysis")
print()
print("Iin:", ssr["Iin"])
print("I1:", ssr["I1"])
print("Ib:", ssr["Ib"])
print("I3:", ssr["I3"])
print("I4:", ssr["Il"])
print("Ie:", ssr["Ie"])
print("Vc:", ssr["Vc"])
print("Vb:", ssr["Vb"])
print("Ve:", ssr["Ve"])
print("Power gain (dB):", ssr["gain"])
print("Zin (ohms):", ssr["zin"])
print("Re implied (ohms):", ssr["re_implied"])

print("Vin limit", small_signal_limit(br, ssr, 2))

print(get_standard_resistors())