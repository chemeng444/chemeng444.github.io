#!/home/vossj/suncat/bin/python
#above line selects special python interpreter needed to run espresso
#SBATCH -p slac
#################
#set a job name
#SBATCH --job-name=myjob
#################
#a file for job output, you can check job progress
#SBATCH --output=myjob.out
#################
# a file for errors from the job
#SBATCH --error=myjob.err
#################
#time you think you need; default is one hour
#in minutes in this case
#SBATCH --time=48:00:00
#################
# **IMPORTANT** make sure number of nodes matches images
#SBATCH --nodes=5
#################
#SBATCH --mem-per-cpu=4000
#################
#get emailed about job BEGIN, END, and FAIL
#SBATCH --mail-type=ALL
#################
#who to send email to; please change to your email
#SBATCH  --mail-user=SUNETID@stanford.edu
#################
#task to run per node; each node has 16 cores
#SBATCH --ntasks-per-node=16
#################


###############
#More details about NEB here: https://wiki.fysik.dtu.dk/ase/ase/neb.html
###############

from ase import io

from ase.optimize import BFGS as QuasiNewton
from ase.neb import NEB
from espresso.multiespresso import multiespresso

xc = 'BEEF-vdW'

intermediate_images = 5

#set up multiple espresso calculators
#example shown here: slabs: dipole correction is turned on
m = multiespresso(ncalc=intermediate_images,outdirprefix='ekspressen',
		pw=500.,
		dw=5000.,
		xc=xc,
		kpts=(4,4,1),
		nbands=-20,
		spinpol=False,
		dipole={'status':True},
		convergence={'energy':1e-5,'mixing':0.25,'maxsteps':300})


# these trajectories have to contain total energies and forces besides the coordinates
# this means that these have to be the outputs of your structural relaxation calculations
# you will need to optimize the surfaces first and rename the output files to neb0 and neb 6 here 
# in order to use them for the NEB calculation
initial = io.read('neb0.traj')
final = io.read('neb6.traj')


# generate a list of the images for the NEB calculation
# starting from the initial image, copying it for the number of
# intermediate images specified, then attaching the final image
images = [initial]
for i in range(intermediate_images):
    images.append(initial.copy())
images.append(final)

# set up the NEB object, which takes the images and is used to interpolate the 
# reaction path
neb = NEB(images)
m.set_neb(neb)
neb.interpolate()

# set up the optimization for relaxing the entire reaction path
# resulting trajctory files will be named neb*.traj
qn = QuasiNewton(neb, logfile='qn.log')

for j in range(1,intermediate_images+1):
    traj = io.PickleTrajectory('neb%d.traj' % j, 'w', images[j])
    qn.attach(traj)

qn.run(fmax=0.05)
