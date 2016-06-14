"""

Script to generate INC files for Povray

We load 3 states: skyrmion, ferromagnetic, and sk destruction
from the NEBM npys output folder

the .inc files include a row of data for every spin, with
the sentence:
    spins(x, y, z, mx, my, mz, r, g, b)

i.e. positions, spin orientations, and rgb colours with the
mz magnitude (colours are normalised, [0,1])


Created by David Cortes on Fri 09 Oct 2015
University of Southampton
Contact to: d.i.cortes@soton.ac.uk

"""

# FIDIMAG Simulation imports:
from fidimag.atomistic import Sim
from fidimag.common import CuboidMesh
from fidimag.atomistic.hexagonal_mesh import HexagonalMesh
from fidimag.atomistic import DMI
from fidimag.atomistic import UniformExchange
from fidimag.atomistic import Zeeman
from fidimag.atomistic import Constant

# Import physical constants from fidimag
const = Constant()

# Import the NEB method
from fidimag.common.neb_cartesian import NEB_Sundials

# Numpy utilities
import numpy as np
from matplotlib import cm
import matplotlib as mpl

# Create 2 custom colormaps
cdict_BlOr = {'red': ((0.0, 1., 1.),
                      (0.5, 0.9976163, 0.9976163),
                      (1.0, 3 / 255., 3 / 255.),
                      ),
              'green': ((0.0, 69 / 255., 69 / 255.),
                        (0.5, 0.9990772, 0.9990772),
                        (1.0, 33 / 255., 33 / 255.)
                        ),
              'blue': ((0.0, 0.0, 0.0),
                       (0.5, 0.753402, 0.753402),
                       (1.0, 73 / 255., 73 / 255.)
                       )
              }


# Transform to colormaps
BlOr = mpl.colors.LinearSegmentedColormap('BlOr',
                                          cdict_BlOr,
                                          256)
BlOr_r = cm.revcmap(BlOr._segmentdata)
BlOr_r = mpl.colors.LinearSegmentedColormap('BlOr', BlOr_r, 256)

# mesh = CuboidMesh(nx=21, ny=21,
#                   dx=0.5, dy=0.5,
#                   unit_length=1e-9,
#                   periodicity=(True, True, False)
#                   )

mesh = HexagonalMesh(.5, 41, 41,
                     periodicity=(True, True)
                     )

# Initialise a simulation object and load the skyrmion
# or ferromagnetic states
sim = Sim(mesh, name='neb_21x21-spins_fm-sk_atomic')

sk = '../hexagonal_system/relaxation/npys/2Dhex_41x41_FePd-Ir_B-15e-1_J588e-2_sk-up_npys/m_689.npy'
fm = '../../npys/neb_21x21-spins_fm-sk_atomic_k1e10_216/image_17.npy'
ds = '../../npys/neb_21x21-spins_fm-sk_atomic_k1e10_216/image_11.npy'

# For now we will just generate a skyrmion
states = {'skyrmion': sk,
          # 'ferromagnetic': fm,
          # 'destruction': ds
          }

for key in states.keys():
    sim.set_m(np.load(states[key]))

    # Append coordinates and spin orientations by column
    data = np.append(sim.mesh.coordinates,
                     sim.spin.reshape(-1, 3), axis=1)

    # Get the colormap using the last row, i.e. mz
    # We must normalise it: [-1, 1]  --> [0, 1]
    # So we sum by 1 to shift the scale and divide by 1 - (-1) = 2
    mz_rgb = BlOr_r((data[:, -1] + 1) * 0.5)
    # Remove last column with alpha values
    mz_rgb = mz_rgb[:, :-1]

    data = np.append(data, mz_rgb, axis=1)

    # Open the output file
    _file = open('{}.inc'.format(key), 'w')

    # Now we write the spins(...) sentence for every spin
    xs = np.unique(sim.mesh.coordinates[:, 0])
    centre = (xs[len(xs) / 2],
              sim.mesh.coordinates[:, 1][sim.mesh.nx * (sim.mesh.ny / 2)]
              )

    print centre

    for row in data:
        if (row[0] - centre[0]) ** 2 + (row[1] - centre[1]) ** 2 < 10 ** 2:
            line = 'spins('
            # We transform the axes according to POVRAY's coordinate
            # system: x --> -z, y --> x, x --> y
            line += '{},{},{},'.format(row[1], row[2], -row[0])
            # The same for the spins orientations, but we multiply by
            # -1 to get the right orientations (I should check this with a
            # proper rotation matrix in the future)
            line += '{},{},{},'.format(-row[4], -row[5], +row[3])

            # Now the colours
            for num in row[6:]:
                line += '{},'.format(num)

            # Remove last comma and close brackets
            line = line[:-1]
            line += ')\n'

            _file.write(line)

    _file.close()
