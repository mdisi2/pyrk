### Pyrk Tutorial By Example
'''
    This follow-along example is written to follow along in VScode. 
    This tutorial also assumes the reader has no prior knowledge of 
    reactor physics and will include some brief explanations of the 
    physics.
'''
### Installation and Pre-simulation Requirements
'''
    i) Cloning PyRK in VScode

        To clone the official PyRK repository, run this line in the 
        VScode search bar:

            git clone https://github.com/pyrk/pyrk.git

        If you wish to clone your personal fork, change the link.

    ii) Installing required libraries

        PyRK requires some additional Python libraries to run simulations.
        A list of these libraries has been included in the source code - 
        so run this line within the terminal to install the required libraries.

            pip install -r requirements.txt

    iii) Installing PyRK

        To install PyRK, copy this line into the terminal:

            python setup.py install

        You should be ready to start using PyRK!   
'''
### Example Simulations
'''
    PyRK executes simulations by taking a driver script and passing two 
    required arguments, the input file and the output folder location. 
    PyRK comes with several examples, so it is recommended to run some of 
    the examples before your own to check if PyRK is installed correctly 
    and to get a sense of how PyRK works. To run the first 'default' example,
    run this line in the terminal:

        python .\pyrk\driver.py --infile=examples\default\input.py --plotdir=out\default

        python ./pyrk/driver.py --infile=examples/default/input.py --plotdir=out/default

            [] '.\pyrk\driver.py' locates and runs the driver.
            [] 'infile=examples...' locates the input (.py file) containing the reactor parameters.
            [] '--plotdir=out...' will create a folder to save the output data.

    Change each of these components to your desired specifications when
    running your simulations. The default example should only take a few 
    seconds to a minute to complete.
'''
### Tutorial By Example 

### Import required Libraries and Functions

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


### Reactivity Coefficients 
'''
    Reactor Kinetics refers to the behavior of a reactor 
    when the multiplication factor (k) is not 1. 

    Reactivity (rho) measures the change in k with the
    unit (pcm). Transients are external changes that alter 
    the multiplication factor. Reactivity Coefficients 
    (alpha with subscripts reflecting the transients) are 
    partial derivatives that describe the change in reactivity
    about the change in the transient.
'''

# Thermal hydraulic params
# Temperature feedbacks of reactivity
alpha_f = -3.8 * units.pcm / units.kelvin
alpha_c = -1.8 * units.pcm / units.kelvin
alpha_m = -0.7 * units.pcm / units.kelvin
alpha_r = 1.8 * units.pcm / units.kelvin
# below from steady state analysis
t_fuel = 955.58086 * units.kelvin
t_cool = 936.57636 * units.kelvin
t_refl = 923.18521 * units.kelvin
t_mod = 937.39862 * units.kelvin
t_graph_peb = 936.40806 * units.kelvin
t_core = 970.54064 * units.kelvin

### Thermal Hydraulic Parameters
'''
    The change in temperature of the coolant 
    is a function of the flow rate velocity.
'''

# the data below comes from design doc rev c
# self._vol_flow_rate = 976.0*0.3 # kg/s TODO 0.3 is nat circ guess
vel_cool = 2. * units.meter / units.second  # m/s
t_inlet = units.Quantity(600.0, units.degC)  # degrees C
# [m] ... matrix(4mm) + coating(1mm)
thickness_fuel_matrix = 0.005 * units.meter
kappa = 0.00  # TODO if you fix omegas, kappa ~ 0.06

### Initialize Core Geometry

core_height = 3.5 * units.meter  # [m] (TODO currently approximate)
core_inner_radius = 0.35 * units.meter  # m
core_outer_radius = 1.25 * units.meter  #

### Time Parameters

t0 = 0.00 * units.seconds
dt = 0.005 * units.seconds
tf = 5.0 * units.seconds

### Pebble, Core, and Particle Volumes

n_pebbles = 470000
n_graph_peb = 218000
n_particles_per_pebble = 4730
r_pebble = 0.015 * units.meter  # [m] diam = 3cm
r_core = 0.0125 * units.meter  # [m] diam = 2.5cm
r_particle = 200 * units.micrometer

# vol of 4730 kernels per pebble, each 400 micrometer diameter
vol_fuel = n_pebbles * n_particles_per_pebble * vol_sphere(r_particle)
vol_core = (n_pebbles) * (vol_sphere(r_core))
vol_mod = (n_pebbles) * (vol_sphere(r_pebble) - vol_sphere(r_core)) - vol_fuel
vol_graph_peb = (n_graph_peb) * (vol_sphere(r_pebble))

#############################################
#
# Required Input
#
#############################################

# Total power, Watts, thermal
power_tot = 236000000.0 * units.watt

# Timer instance, based on t0, tf, dt
ti = Timer(t0=t0, tf=tf, dt=dt)

# Number of precursor groups
n_pg = 6

# Number of decay heat groups
n_dg = 0

# Fissioning Isotope
fission_iso = "u235"

# Spectrum
spectrum = "thermal"

# Feedbacks, False to turn reactivity feedback off. True otherwise.
feedback = True

# External Reactivity
from pyrk.reactivity_insertion import StepReactivityInsertion
rho_ext = StepReactivityInsertion(timer=ti, t_step=1.0 * units.seconds,
                                  rho_init=0.0 * units.delta_k,
                                  rho_final=0.005 * units.delta_k)

# maximum number of internal steps that the ode solver will take
nsteps = 1000


fuel = th.THComponent(name="fuel",
                      mat=Kernel(name="fuelkernel"),
                      vol=vol_fuel,
                      T0=t_fuel,
                      alpha_temp=alpha_f,
                      timer=ti,
                      heatgen=True,
                      power_tot=power_tot)

cool = th.THComponent(name="cool",
                      mat=Flibe(name="flibe"),
                      vol=vol_cool,
                      T0=t_cool,
                      alpha_temp=alpha_c,
                      timer=ti)

refl = th.THComponent(name="refl",
                      mat=Graphite(name="reflgraphite"),
                      vol=vol_refl,
                      T0=t_refl,
                      alpha_temp=alpha_r,
                      timer=ti)

mod = th.THComponent(name="mod",
                     mat=Graphite(name="pebgraphite"),
                     vol=vol_mod,
                     T0=t_mod,
                     alpha_temp=alpha_mod,
                     timer=ti)

core = th.THComponent(name="core",
                      mat=Graphite(name="pebgraphite"),
                      vol=vol_core,
                      T0=t_core,
                      alpha_temp=alpha_core,
                      timer=ti)

graph_peb = th.THComponent(name="graph_peb",
                           mat=Graphite(name="pebgraphite"),
                           vol=vol_mod,
                           T0=t_graph_peb,
                           alpha_temp=alpha_graph_peb,
                           timer=ti)

components = [fuel, cool, refl, mod, graph_peb, core]

# TODO: verify the conduction lengths and maybe calibrate for spherical components
# The fuel conducts to the moderator graphite
fuel.add_conduction('mod', area=a_fuel, L=4 * units.millimeter)

# The moderator graphite conducts to the core graphite
mod.add_conduction('core', area=a_core, L=25 * units.millimeter)
# The moderator graphite conducts to the fuel
mod.add_conduction('fuel', area=a_mod, L=25 * units.millimeter)
# The moderator graphite convects to the coolant
mod.add_convection('cool', h=h_mod, area=a_mod)

# The core graphite conducts to the moderator graphite
core.add_conduction('mod', area=a_core, L=25 * units.centimeter)

# The graphite pebbles convect to the coolant
graph_peb.add_convection('cool', h=h_mod, area=a_graph_peb)

# The coolant convects accross the graphite pebbles
cool.add_convection('graph_peb', h=h_mod, area=a_graph_peb)
# The coolant convects accross the graphite pebbles
cool.add_convection('mod', h=h_mod, area=a_mod)
# The coolant convects accross the reflector
cool.add_convection('refl', h=h_refl, area=a_refl)

# The reflector convects with the coolant
refl.add_convection('cool', h=h_refl, area=a_refl)
