from pyrk.utilities.ur import units
from pyrk import th_component as th
import math
from pyrk.materials.flibe import Flibe
from pyrk.materials.graphite import Graphite
from pyrk.materials.kernel import Kernel
from pyrk.timer import Timer

def area_sphere(r):
    assert(r >= 0 * units.meter)
    return (4.0) * math.pi * pow(r.to('meter'), 2)

def vol_sphere(r):
    assert(r >= 0 * units.meter)
    return (4. / 3.) * math.pi * pow(r.to('meter'), 3)

