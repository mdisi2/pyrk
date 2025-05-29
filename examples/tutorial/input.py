### Pyrk Tutorial By Example
'''

    This follow-along example is written to follow along in VScode. 
    This tutorial also assumes the reader has no prior knowledge of 
    reactor physics and will include some brief explanations of the 
    physics.

'''

### Installation and Pre-simulation Requirements
'''

i) Clone PyRK in VScode

    To clone the official PyRK repository, run this line in the 
    VScode search bar:

        git clone https://github.com/pyrk/pyrk.git

    If you wish to clone your personal fork, change the link.

ii) Install all required libraries

    PyRK requires some additional Python libraries to run simulations.
    A list of these libraries has been included in the source code - 
    so run this line within the terminal to install the required libraries.

         pip install -r requirements.txt

iii) Install PyRK

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

Change each of these components to your desired specifications when running your simulations.
The default example should only take a few seconds to a minute to complete.
May need to change 'python' to 'python3' .

'''

### Tutorial By Example 

### Import required Libraries

from pyrk.utilities.ur import units
from pyrk import th_component as th
import math
from pyrk.materials.flibe import Flibe
from pyrk.materials.graphite import Graphite
from pyrk.materials.kernel import Kernel
from pyrk.timer import Timer

'''
Reactor Kinetics refers to the behavior of a reactor when the multiplication factor (k),
the ratio of neutrons born the next generation over this generation, is not 1. 

Reactivity (rho) measures the change in (k) in the unit pcm. Transients are external changes
that alter the multiplication factor. Reactivity Coefficients (alpha with subscripts 
reflecting the transients) are partial derivatives that describe the change in reactivity
about the change in the transient, for example:

    alpha_temp = change in reactivity (delta rho) / change in temperature (delta kelvin)

'''
