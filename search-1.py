import numpy as np
import math
from util import *
from BJTFeedback import *

# These are settings from the amplifier on EMRFD page 5.14
Vcc = 12
Rcc = 22
#Rf = 1500
R1 = 680
#Re = 47
b0 = 100

Rf_range = get_standard_resistors_in_range(100, 10000)
Re_unbypassed_range = get_standard_resistors_in_range(10, 1000)
zin_target = 50
Ie_bias_




br = calc_bias(Vcc, Rcc, Rf, R1, Re, b0)
