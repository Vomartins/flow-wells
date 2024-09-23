The scripts in this repository perform some computational experiments with **OPM Flow Simulator** (https://opm-project.org/).
The scripts may be changed to run a specific experiment without README update.

## ROCm
We use **ROCProfiler** to measure the execution time of HIP kernels. Thus, it is a prerequisite for these experiments.

## OPM Flow Version
The OPM Flow version necessary for these experiments is the one in https://github.com/Vomartins/opm-simulators/tree/well-gpu. It is a branch based on the 2024.04 release.

## Scripts

### rocprof-profiling.sh
This script is where the simulation is run. The input variables are handled by **multi-simulation-profiling.sh** but one can run this script by itself by providing the following input variable:
1) reservoir : The name of the reservoir one needs to simulate. This can be any of the folder names in **opm-tests** repository;
2) deck : Flow input data filename;
3) accelerator : Any string that is an option of Flow command option --accelerator-mode ("none", "cusparse, "opencl", "amgcl", "rocalution", "rocsparse");
4) linsolver : Any string that is an option of Flow command option --linear-solver ("ilu0", "cprw", "cpr", "cpr_quasiimpes", "cpr_treuimpes", "amg"); 
5) well_contributions : Any string that is an option of Flow command option --matrix-add-well-contributions ("true", "false");
6) trace_option : Rocprofv2 option that specifies which kernel will be considered for tracing (https://rocm.docs.amd.com/projects/rocprofiler/en/latest/how-to/rocprofv2-usage.html).

Two variables in this script save paths, thus these variables must be changed to be adequate with the computer. The first one is **flow_dir** which should store the path to OPM Flow **opm-simulators** binary folder. The second one is **data_dir** which should store the path to **opm-tests** folder (https://github.com/OPM/opm-tests).
The outputs will be a folder containing simulations output, a txt file with command options used by the simulator, and two csv files with profiling info from **rocprofv2** (actually created by rocprof-profiling.sh). These files should be saved in a folder called **rocprof-outputs**, thus one must create this folder before running the script.

### results-analysis.py
If a simulation using rocalution or rocsparse accelerator is run by **rocprof-profiling.sh** this will be done using **rocprofv2** in order to profile the HIP kernels. This script will calculate the average and standard deviation of kernel execution time and save it in a csv file in the same directory of **rocprof-profiling.sh** outputs.

### summarize.py
This script collects specific information about the simulations used in an experiment. The output is the **summarize-table.csv**, which is a csv file with the desirable information about the simulations.

### multi-simulation-profiling.sh
The main workflow is done by running **multi-simulation-profiling.sh**. This script has one input data that can be
1) spe1 -> To perform the experiment with SPE1 model;
2) norne -> to perform the experiment with the Norne model.

It constructs a set of simulations with the chosen model variants and flow command options defined as arrays inside the script. It calls **rocprof-profiling.sh** for each combination of parameters and calls **summarize.py** when the simulations are finished.
