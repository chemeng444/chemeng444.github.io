---
layout: page
mathjax: false 
permalink: /UNIX/
---

# Getting Started
1. [Logging Into the Computing Clusters](../Clusters/)
2. [Basic UNIX](../UNIX/)
3. [Python](../Python/)

____

## Basic UNIX

## Contents
1. [Basic Comamands](#basic-commands)
2. [Wildcards](#wildcards)
3. [Text Editors](#text-editors)
4. [Submitting Jobs](#submitting-jobs)

<a name='basic-commands'></a>

## Basic Commands

These are some of the basic commands that you will be using in the shell on a daily basis.

____

```bash
ase-gui <file_name>
```
Graphical user interface for the Atomic Simulation Environment (ASE). This is the tool you will be using for viewing or setting up your structures.

____

```bash
cd ..
```
Move up one directory. 

____

```bash
cd <directory_name>
```
Changes directory to the one provided. If no directory is given, the default is to return you to your home directory (/home/username/) 

____

```bash
cp <source_file_with_path> <destination_path>
```
Copies files or directories from the source_file_with_path to the destination_path 

____

```bash
cp -r <source_file_with_path> <destination_path>
```
Copy recursively. Useful for copying multiple files and directories (copies contents of the subdirectories). 

____

```bash
cp -u <source_file_with_path> <destination_path>
```
Update. Copies only if the source file is newer than the destination file or the destination file does not exist. 

____

```bash
mkdir <directory_name>
```
Create new a new directory. 

____

```bash
mv <source_file> <destination_file>
```
Move or rename file.

____

```bash
ls <directory_name>
```
Lists the files and directories contained within the directory. Leave blank for present directory.

____

```bash
ls -t
```
List files in chronological order.

____

```bash
ls -la
```
List all files even those starting with a dot '.' which are generally not listed. 

____

```bash
ls | more
```
If the number of files in a directory is too large to fit in a single screen this command lists files and directories page after page on spacebar keystroke. 

____

```bash
pwd
```
Provides the “present working directory,” i.e.   the current folder.

____

```bash
rm <file>
```
Remove files. This is always *permanent*.

____

```bash
rm -r <file_or_directory_with_path>
```
Remove file or the directory and its contents recursively. 

____

```bash
rmdir <directory_name>
```
Remove an empty directory. Use rm -r to remove recursively, such as if directory contains files (be careful).

____

```bash
cat <file_name>
```
Print out contents of a text file or files within the shell.

<a name='wildcards'></a>

## Wildcards
Wildcards can be used to perform commands on multiple files simultaneously.

____

```bash
?
```

Single character. Example: ```ag neb?.traj neb??.traj``` will use ```ag``` to open all files containing one or two characters between neb and .traj

____

```bash
*
```
Any number of characters. Example: ```ls *.traj``` will list all ```.traj``` files.

<a name='text-editors'></a>

## Text Editors
There are several text editors available. Popular ones include ```vim``` and ```nano```. Most people at SUNCAT use ```vim```. To open a file, use ```vim file.txt``` to open a file named ```file.txt```.


<a name='submitting-jobs'></a>

## Submitting Jobs
These instructions are specific to the **Sherlock** cluster. Instructions for the **CEES** cluster below.

```bash
sbatch <script_file>
```
Submit the job defined by the script file to the queue.

____

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
____

```bash
squeue -u your_SUNETID
```
This will list your jobs.

____

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

____

```bash
scancel <job_ID>
```
Delete your job. You can get the job ID from ```squeue```

____

If you are using the **CEES** cluster, the command for submitting a job is

```csh
qsub <script_file>
```

where `<script_file>` is the name of your script (e.g. `opt.py`).

```bash
qstat
```

This will display details about the job. Once the job has finished, this detail won't be available.


