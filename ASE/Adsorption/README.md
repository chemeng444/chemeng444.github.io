---
layout: page
mathjax: true
permalink: /ASE/Adsorption/
---

# ASE Tutorials
1. [Getting Started](../Getting_Started/)
2. [Adsorption](../Adsorption/)
3. [Transition States](../Transition_States/)

## Adsorption on Surfaces

In the second tutorial, you will be calculating the dissociative adsorption of N<sub>2</sub> onto the your cluster and (111) surface.

## Contents
1. [Gaseous molecules](#gaseous-molecules)
2. [Adsorption sites](#adsorption-sites)
3. [Dissociative adsorption](#dissociative-adsorption)

## Required Files

Run the following 

```bash
wget http://chemeng444.github.io/ASE/Adsorption/download_files_2.sh
./download_files_2.sh
```

<a name='gaseous-molecules'></a>
## Gaseous molecules

In this exercise you will be calculating the dissociative adsorption of H<sub>2</sub>O on the Pt(111) surface from the previous exercise. The dissociative adsorption energy is defined as:
<div>
$$
\Delta E_\mathrm{ads} = E_\mathrm{Pt(111) + OH* + H*}  - E_\mathrm{Pt(111)} - E_\mathrm{H_2O}
$$

</div>

where OH\* and H\* refer to adsorbed OH and H. We have \\(E\_\mathrm{Pt(111)}\\) from the previous exercise, so we will need to calculate both \\(E\_\mathrm{Pt(111)+OH\* +H\*}\\) and \\(E\_\mathrm{H\_2O}\\) here. The [`run_N2.py`](run_N2.py) will calculate the optimized geometry, the electronic energy, as well as the vibrational modes of a gaseous N<sub>2</sub> molecule. Run the script and check that the vibrational modes are reasonable.

<a name='adsorption-sites'></a>
## Adsorption sites

There are four adsorption sites on the Pt(111) surface that a molecule can adsorb to: the fcc, hcp, top, and bridge sites. Follow the `ads_Pt111_H2O.py` script, which sets up a variety of configurations of adsorbed N2\* and H\*. In the script, an optimized structure for the Pt(111) surface is read, and then the adsorbate atoms are added manually. The `add_adsorbate()` function is used to add adsorbates:

```python
add_adsorbate(slab, 'N', 1.5, (3, 1.7))
add_adsorbate(slab, 'N', 1.5, (1.5, 0.86))
```

Alternatively, if you set up the surface using the `fcc111` or `fcc100` functions from the `ase.lattice.surface` module, you can use special keywords in the `add_adsorbate()` function to add adsorbates to special sites

```python
atoms = fcc111(Pt, a = 3.989, size = (2,2,4), vacuum = 7.0)
add_adsorbate(atoms, 'N', 1.5, 'fcc')
```

This generates an FCC (111) surface and adds an N onto the fcc site.

More information can be found [here](https://wiki.fysik.dtu.dk/ase/ase/surface.html).

One could also use the ASE graphical user interface ag to add an adsorbate or molecule as well. Use `ag <file>.traj` to open the trajectory file. Then simply click the atom above where the adsorbate will sit, and click `ctrl + A`, then specify the adsorbate and the vertical distance above the site. You can also hold `ctrl` to select multiple atoms and add an adsorbate, which will be at the center of all the selected atoms.

<a name='dissociative-adsorption'></a>
## Dissociative adsorption

We will be focusing on the dissociative adsorption mechanism, where the H<sub>2</sub>O molecule separates as H* and OH* when it adsorbs onto the surface. The [`setup_ads.py`](setup_ads.py) script sets up a Pt(111) with OH* and H* adsorbed on fcc sites. The result is saved into the `surface.traj` file. To run the geometry optimization, submit `opt.py` which reads in `surface.traj`

```batch
python setup_ads.py
sbatch --job-name=$PWD opt.py
```

You should repeat this with all other possible combinations of OH* and H* adsorption where OH* and H* are at nearest neighboring sites.
