---
layout: page
mathjax: true
permalink: /UNIX/
---

## Basic UNIX
## Contents
1. [Using the UNIX Shell on the Sherlock Cluster] (#using-unix)
2. [Basic Comamands] (#basic-commands)
3. [Wildcards] (#wildcards)
4. [Text Editors] (#text-editors)
5. [Submitting Jobs] (#submitting-jobs)

<a name='using-unix'></a>
## Using the UNIX Shell on the Sherlock Cluster

For most of your work, you will be logging onto the [Sherlock cluster] (http://sherlock.stanford.edu) remotely and submitting jobs there. More details about logging on are included [here] (http://sherlock.stanford.edu/mediawiki/index.php/LogonCluster).

First of all, make sure you download and install the latest version of XQuartz from http://xquartz.macosforge.org. To prevent X11 from timing out, open the terminal and type
```bash
mkdir -p ~/.ssh
echo $'\nHost *\n ForwardX11Timeout 1000000\n' >>~/.ssh/config
```

To connect to the Sherlock cluster, type

```bash
kinit sunetid@stanford.edu
```
to authenticate in Kerberos, then
```bash
ssh -K -X sunetid@sherlock.stanford.edu
```
to log on, where ```sunetid``` is your Stanford SUNET ID. ```kinit``` does not need to be rerun unless the Kererbos ticket is expired.

Once you have logged in run the following commands (you only need to do this during the *first login*)
```bash
￼echo $'\nexport PATH=/home/vossj/suncat/bin:$PATH' >>~/.bashrc
echo 'export LD_LIBRARY_PATH=/home/vossj/suncat/lib:/home/vossj/suncat/lib64:$LD_LIBRARY_PATH' >>~/.bashrc
source ~/.bashrc
```
This will enable you to run SUNCAT specific software on the Sherlock cluster, including the ASE interface to Quantum ESPRESSO.

<a name='basic-commands'></a>
## Basic Commands

These are some of the basic commands that you will be using in the shell on a daily basis.
___
```bash
ag <file_name>
```
Graphical user interface for the Atomic Simulation Environment (ASE). This is the tool you will be using for viewing or setting up your structures.
___

```bash
cd ..
```
Move up one directory. 
___

```bash
cd <directory_name>
```
Changes directory to the one provided. If no directory is given, the default is to return you to your home directory (/home/username/) 
___

```bash
cp <source_file_with_path> <destination_path>
```
Copies files or directories from the source_file_with_path to the destination_path 
___

```bash
cp –r <source_file_with_path> <destination_path>
```
Copy recursively. Useful for copying multiple files and directories (copies contents of the subdirectories). 
___

```bash
cp –u <source_file_with_path> <destination_path>
```
Update. Copies only if the source file is newer than the destination file or the destination file does not exist. 
___

```bash
mkdir <directory_name>
```
Create new a new directory. 
___

```bash
mv <source_file> <destination_file>
```
Move or rename file.
___

```bash
ls <directory_name>
```
Lists the files and directories contained within the directory. Leave blank for present directory.
___

```bash
ls –t
```
List files in chronological order.
___

```bash
ls -la
```
List all files even those starting with a dot '.' which are generally not listed. 
___

```bash
ls | more
```
If the number of files in a directory is too large to fit in a single screen this command lists files and directories page after page on spacebar keystroke. 
___

```bash
pwd
```
Provides the “present working directory,” i.e.   the current folder.
___

```bash
rm <file>
```
Remove files. This is always *permanent*.
___

```bash
rm -r <file_or_directory_with_path>
```
Remove file or the directory and its contents recursively. 
___

```bash
rmdir <directory_name>
```
Remove an empty directory. Use rm –r to remove recursively, such as if directory contains files (be careful).
___

```bash
cat <file_name>
```
Print out contents of a text file or files within the shell.

<a name='wildcards'></a>
## Wildcards
Wildcards can be used to perform commands on multiple files simultaneously.

___
```bash
?
```

Single character. Example: ```ag neb?.traj neb??.traj``` will use ```ag``` to open all files containing one or two characters between neb and .traj
___

```bash
*
```
Any number of characters. Example: ```ls *.traj``` will list all ```.traj``` files.

<a name='text-editors'></a>
## Text Editors
There are several text editors available. Popular ones include ```vim``` and ```nano```. Most people at SUNCAT use ```vim```. To open a file, use ```vim file.txt``` to open a file named ```file.txt```.


<a name='submitting-jobs'></a>
## Submitting Jobs
These instructions are specific to the Sherlock cluster.
```bash
sbatch <script_file>
```
Submit the job defined by the script file to the queue. 
___
```bash
sbatch --job-name=$PWD <script_file>
```
I recommend specifying `--job-name=$PWD` so it will set the current directory as the job name. This way you will have this information in the email.

```bash
squeue
```
Check the status of your jobs. You will get something like the following: 

```
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           1930211    normal slurm_jo   gunhan CG    2:00:20      1 sh-5-25
           1819909    normal feat5_st   cbohon PD       0:00      1 (Dependency)
           1819916    normal feat5_st   cbohon PD       0:00      1 (Dependency)
        1787348_10    normal      ida  reaganc PD       0:00     32 (Resources)
        1787348_11    normal      ida  reaganc PD       0:00     32 (Resources)
           1904877    normal cftr_ref  jadeshi PD       0:00      1 (QOSMaxCpusPerUserLimit)
```
___

```bash
squeue –u your_SUNETID
```
This will list your jobs.
___
```bash
squeue -u your_SUNETID -o '%.7i %.9P %.8j %.8u %.2t %.10M %.6D %R %Z'
```
Shows more useful details about the job, including the working directory of the script. For example
```
JOBID PARTITION     NAME     USER ST       TIME  NODES WORK_DIR
1948301      slac /scratch  ctsai89  R   23:24:47      8 /scratch/users/ctsai89/TS_CH3_Au111/N_NEB
1948505      slac /home/ct  ctsai89  R   19:57:06      1 /scratch/users/ctsai89/Class_remaining/Ag111/fbl
1948506      slac /home/ct  ctsai89  R   19:57:06      1 /scratch/users/ctsai89/Class_remaining/Ag211/fbl
1948302      slac /scratch  ctsai89  R   23:24:11      7 /scratch/users/ctsai89/TS_CH3_Au111/B_NEB
```
___
```bash
qstat -f <job_ID>
```
Details about the job. Once the job has finished, this detail won’t be available.

___
```bash
scancel <job_ID>
```
Delete your job. You can get the job ID from ```squeue```
