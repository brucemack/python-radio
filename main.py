import numpy as np
import math
from util import *
from BJTFeedback import *

# BIASING NOTES:
#
# To provide sufficient feedback (guarding against beta variations),
# Ve is usually chosen to be one-quarter to one-third of Vcc.  This
# is a rule of thumb.

# ----- SoftRock TX Amp ------

Vcc = 12
Rcc = 22.1
Rf = 2210
R1 = 475
Re = 56.2
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
print("Ve/Vcc (should be about 25%):", br["Ve"] / br["Vc"])
print("Vc-Ve:", br["Vc"] - br["Ve"])

# Create the bias current in mA
Ie_ma = br["Ie"] * 1000
print("Transistor bias current (mA):", Ie_ma)
print("Transistor power (W):", br["device_power"])

# ----- Small signal analysis -----

Re = 56
Vin = 1
Rs = 50
# Transformer
Rl = 440
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
print("Ve/Vcc (should be about 25%):", br["Ve"] / br["Vc"])
print("Vc-Ve:", br["Vc"] - br["Ve"])

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

# ----- Lower Bias Current ------

print()
print("===== Example 2 =====")
Vcc = 12
Rcc = 22
Rf = 1500
# DC beta
b0 = 100
# Target bias points
Ve_target = Vcc / 3
Ie_target = 0.025
# Figure out the un-bypassed emitter resistor in order to hit
# the Ve target
Re_unbypassed = standardize_resistor(Ve_target / Ie_target)
# Figure out R1 in order to hit the Vb_target (assuming Rf and R1
# form a voltage divider and the base current is negligible)
Vb_target = Ve_target + 0.7
R1 = standardize_resistor((Vb_target * Rf) / (Vcc - Vb_target))

br = calc_bias(Vcc, Rcc, Rf, R1, Re_unbypassed, b0)

print("Bias Analysis:")
print()
print("Ve_target               :", Ve_target)
print("Ie_target               :", Ie_target)
print("R1 chosen for Vb_target :", R1)
print("Re chosen for Ve_target :", Re_unbypassed)
print("I1                      :", br["I1"])
print("I2                      :", br["I2"])
print("Ic:", br["Ic"])
print("Ib:", br["Ib"])
print("Ie:", br["Ie"])
print("Vc:", br["Vc"])
print("Vb:", br["Vb"])
print("Ve:", br["Ve"])
print("Power usage (W):", br["total_power"])
print("Ve/Vcc (should be ~30%):", br["Ve"] / br["Vc"])
print("Vc-Ve:", br["Vc"] - br["Ve"])

# ----- Small signal analysis -----

Re_bypassed = 5.6
Re = parallel_r(Re_unbypassed, Re_bypassed)
# Source driving impedance
Rs = 50
# Load impedance (possibly via transformer)
Rl = 200
# Beta components
Ft = 300
Fop = 7
b = Ft / Fop

ssr = calc_small_signal(Rs, Rf, R1, Re, Rl, br["Ie"], b)

print()
print("Small Signal Analysis")
print()
print("Iin/Vin           :", ssr["Iin"])
print("I1/Vin            :", ssr["I1"])
print("Ib/Vin            :", ssr["Ib"])
print("I3/Vin            :", ssr["I3"])
print("I4/Vin            :", ssr["Il"])
print("Ie/Vin            :", ssr["Ie"])
print("Vc/Vin            :", ssr["Vc"])
print("Vb/Vin            :", ssr["Vb"])
print("Ve/Vin            :", ssr["Ve"])
print("Power gain (dB)   :", ssr["gain"])
print("Zin (ohms)        :", ssr["zin"])
print("Re implied (ohms) :", ssr["re_implied"])
print("Vin limit         :", small_signal_limit(br, ssr, 2))


# ----- Feedback Amplifier From EMRFD table 2.2 ---------

print()
print("===== EMRFD Table 2.2 Example (10m, 23.9dB) =====")
Vcc = 12
Rcc = 22
Rf = 1600
# DC beta
b0 = 150
# Target bias points
Ve_target = Vcc / 4
Ie_target = 0.025
# ----- Parameters for small signal analysis -----
# Emitter resistor that is bypassed in DC state
Re_bypassed = 6.8
# Source driving impedance
Rs = 50
# Load impedance (possibly via transformer)
Rl = 200
# Beta components
Ft = 300
# Operating frequency in MHz
Fop = 28

# Figure out the un-bypassed emitter resistor in order to hit
# the Ve target
Re_unbypassed = standardize_resistor(Ve_target / Ie_target)
# Figure out R1 in order to hit the Vb_target (assuming Rf and R1
# form a voltage divider and the base current is negligible)
Vb_target = Ve_target + 0.7
R1 = standardize_resistor((Vb_target * Rf) / (Vcc - Vb_target))

br = calc_bias(Vcc, Rcc, Rf, R1, Re_unbypassed, b0)

print("Bias Analysis:")
print()
print("Ve_target                    :", Ve_target)
print("Ie_target                    :", Ie_target)
print("Rcc                          :", Rcc)
print("Rf                           :", Rf)
print("Bypassed Re                  :", Re_bypassed)
print("Bias R1 chosen for Vb_target :", R1)
print("Bias Re chosen for Ve_target :", Re_unbypassed)
print("                     I1 :", br["I1"])
print("                     I2 :", br["I2"])
print("                     Ic :", br["Ic"])
print("                     Ib :", br["Ib"])
print("                     Ie :", br["Ie"])
print("                     Vc :", br["Vc"])
print("                     Vb :", br["Vb"])
print("                     Ve :", br["Ve"])
print("       Static power (W) :", br["total_power"])
print(" Ve/Vc (should be ~25%) :", br["Ve"] / br["Vc"])
print("              Vc-Vb (V) :", br["Vc"] - br["Vb"])
print("              Vc-Ve (V) :", br["Vc"] - br["Ve"])
print("          Rcc power (W) :", br["Rcc_power"])
print("           Rf power (W) :", br["Rf_power"])
print("           R1 power (W) :", br["R1_power"])
print("           Re power (W) :", br["Re_power"])
max_swing = 2.0 * (br["Vc"] - br["Vb"])
print("        Max swing (Vpp) :", max_swing)
max_power_out = (max_swing * max_swing) / (2.0 * Rl)
print("          Max power (W) :", max_power_out)

# ----- Small signal analysis -----

Re = parallel_r(Re_unbypassed, Re_bypassed)
b = Ft / Fop

ssr = calc_small_signal(Rs, Rf, R1, Re, Rl, br["Ie"], b)

print()
print("Small Signal Analysis")
print()
print("Iin/Vin           :", ssr["Iin"])
print("I1/Vin            :", ssr["I1"])
print("Ib/Vin            :", ssr["Ib"])
print("I3/Vin            :", ssr["I3"])
print("I4/Vin            :", ssr["Il"])
print("Ie/Vin            :", ssr["Ie"])
print("Vc/Vin            :", ssr["Vc"])
print("Vb/Vin            :", ssr["Vb"])
print("Ve/Vin            :", ssr["Ve"])
print("Power gain (dB)   :", ssr["gain"])
print("Zin (ohms)        :", ssr["zin"])
print("Re implied (ohms) :", ssr["re_implied"])
print("Vin limit         :", small_signal_limit(br, ssr, 2))


