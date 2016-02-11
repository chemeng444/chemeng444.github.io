---
layout: page
mathjax: true
permalink: /Project/
---

## Course Project ##
1. [Introduction](#intro)
3. [Calculations](#calcs)
3. [Analysis](#analysis)
4. [Report](#report)
5. [Research Paper](#paper)
6. [Grading](#grading)
7. [Summary of Requirements](#reqs)


For the course project, you will be studying thermo-chemical ammonia synthesis on metallic clusters and surfaces. Each student will be assigned one metal or bimetallic alloy. 

<a name='intro'></a>

## Introduction ##

The thermo-chemical synthesis of ammonia is accomplished through the [Haber-Bosch process](https://en.wikipedia.org/wiki/Haber_process), where nitrogen gas reacts with hydrogen gas via:

$$
\mathrm{N_2+3H_2\rightarrow 2NH_3}
$$

This process is crucial for the industrial production of fertilizers and chemical feedstocks. Typically, an iron catalyst is used to stabilize the bond-breaking of the N<sub>2</sub> species. The reaction can be separated into elementary reaction steps ([Honkala et. al. (2015)](https://dx.doi.org/10.1126/science.1106435) for more details):

$$
\begin{align}
\mathrm{N_{2\,(g)}} &\rightarrow \mathrm{2N*}\\
\mathrm{H_{2\,(g)}} &\rightarrow \mathrm{2H*}\\
\mathrm{N* + H*} &\rightarrow \mathrm{NH*}\\
\mathrm{NH* + H*} &\rightarrow \mathrm{NH_2*}\\
\mathrm{NH_2* + H*} &\rightarrow \mathrm{NH_3*}\\
\mathrm{NH_3*} &\rightarrow \mathrm{NH_{3\,(g)}}
\end{align}
$$

A free energy diagram is illustrated below:

<center><img src="../Images/N2_path.jpg" alt="N2 path" style="width: 400px;"/>
<br>Ammonia synthesis pathway on a Ru catalyst (<a href="https://dx.doi.org/10.1126/science.1106435">Honkala et. al. (2015)</a>)</center>

Due to the high operating pressures and temperatures required for this reaction, alternative catalysts are still needed for this process. [Medford et. al. (2015)](https://dx.doi.org/10.1016/j.jcat.2014.12.033) have suggested that the linear scaling between the dissociation energy of N<sub>2</sub> and its transition state energy prevents most catalysts from achieving a high rate. Assuming that the bond-breaking of N<sub>2</sub> is rate limiting, then traditional metal catalysts have a transition state that is too high in energy.

<center><img src="../Images/N2_volcano.png" alt="N2 volcano" style="width: 400px;"/>
<br>Filled contour plot for the turnover frequencies</center>

Your goals for the project will be to: (1) explore this reaction to find unique adsorption configurations where the dissociation energy leads to a more favorable transition state energy, and (2) explore additional relations between the reaction intermediates in the pathway. You will be studying 13-atom metal clusters (M<sub>13</sub>) consisting of either pure metals or binary alloys. 

<a name='calcs'></a>

## Calculations ##

For Sherlock, create a `CHE444Project` folder in your `$SCRATCH` directory by running:

```bash
mkdir $SCRATCH/CHE444Project/
```

for CEES:

```bash
mkdir /data/cees/$SUNETID/CHE444Project
```

You may run the exercises in any directory, but keep all the final files for the project organized in the following structure:

```bash
../CHE444Project/Adsorption/
../CHE444Project/Adsorption/2N/
../CHE444Project/Adsorption/N/
../CHE444Project/Adsorption/NH/
...
../CHE444Project/TransitionStates/2N_to_N2/
...
```


For the first step, N<sub>2</sub> → 2N\*, you *are required* to calculate the transition state. To do this, you will need to calculate the final adsorbed state with two nitrogen atoms (2N\*).

To describe the full reaction on your catalytic system, you will need to calculate the adsorption energies of all intermediates, in their most stable configuration (N\*, NH\*, NH<sub>2</sub>\*, NH<sub>3</sub>\*, H\*). A mean field approximation can be used in the analysis (*e.g.* ∆*E*<sub>2NH</sub> = 2∆*E*<sub>NH</sub>). You are not required to calculate the transition states for these steps, though you are welcome to.

In summary:

1. Structural relaxations on both your assigned M<sub>13</sub> cluster and a (111) surface for the same metals. [Project Part 1](../ASE/Getting_Started)
2. **For the M<sub>13</sub> cluster only**: Adsorption energies for the remaining intermediates in the adsorbed state (N\*, NH\*, NH<sub>2</sub>\*, NH<sub>3</sub>\*, H\*). Check all possible sites in order to determine optimal adsorption configurations. [Project Part 2](../ASE/Adsorption)
3. **For both M<sub>13</sub> cluster and metal surface**: Fixed bond length (FBL) calculation for the activation barrier for N<sub>2</sub> → 2N\*. You will need to perform an adsorption energy calculation for 2N\*, which will serve as the starting point for the FBL. [Project Part 3](../ASE/Transition_States)
4. Vibrational analysis for the transition state **and** the adsorbed states. Calculation of the reaction rate and also a free energy diagram with some temperature and pressure dependence. [Project Part 3](../ASE/Transition_States)

**IMPORTANT:**

When you have finished all your calculations. Run the following to copy all your files into the shared course directory, so your classmates may access the results:

```bash
wget http://chemeng444.github.io/collect_data.sh
./collect_data.sh
```

<a name='analysis'></a>

## Analysis ##

Your analysis should include the following:

* Discussion of the optimal binding configurations on the surface
* Comparison between the (111) surface and the M<sub>13</sub> cluster
* Analysis of rate as a function of the temperature

In addition, you may wish to address the following questions:

* Do the reaction intermediates (adsorbates) show the same dependence on surface site or surface termination?
* What are other factors that can affect adsorbate-metal interaction?
* How important is the coordination number of the metal? Compare the metal cluster to the metal surface.

You are welcome to share data amongst your peers to discuss broader trends. (We encourage you to use [Piazza](https://piazza.com/class/ij0k0xrcxrz5pa) for questions and discussions so you can help each other troubleshoot and share data. You may also include additional calculations into your project (scripts available), but this is not required:

* Density of states calculations on the surfaces
* Error analysis using the BEEF ensembles

<a name='report'></a>

## Report ##

Your report should be between 3 to 5 pages long including figures and tables. Please be succinct and organize it in the following way:

* Introduction (brief) - don't write too much
* Calculation details
* Results and discussion
* Conclusion (brief)

<a name='paper'></a>

## Research Paper ##

We expect that your results will form the basis of a manuscript that we will be putting together as a class. 

<a name='grading'></a>

## Grading ##

* 30% exercises
* 20% write-up
* 20% kinetics
* 30% calculations

<a name='reqs'></a>

## Summary of Requirements ##

At a minimum you should accomplish the following:

1. Complete the [three exercises](../ASE/).
2. Setup a M<sub>13</sub> cluster and a (111) surface and calculate adsorption energies for all intermediates.
3. Calculate transition states for the first step N<sub>2</sub> dissociation) using the fixed bond-length method. Extra credit for calculating the hydrogenation barriers.
4. Vibrational frequency and free energy calculations (initial, transition, and final states, and all adsorbed intermediates). 
5. Analysis
    1. Optimal adsorption sites (relation to transition states)
    2. Kinetic rate analysis
6. Report (3~5 pages maximum)
