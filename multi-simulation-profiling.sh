#!/bin/bash

reservoir=$1

if [ "$reservoir" = "spe1" ]; then
    case_list=("SPE1CASE1.DATA")
elif [ "$reservoir" = "norne" ]; then
    case_list=("NORNE_ATW2013_1A_MSW.DATA" "NORNE_ATW2013_1A_STDW.DATA" "NORNE_ATW2013_2A_MSW.DATA" "NORNE_ATW2013_2A_STDW.DATA" "NORNE_ATW2013_2B_MSW.DATA" "NORNE_ATW2013_2B_STDW.DATA" "NORNE_ATW2013_3B_MSW.DATA" "NORNE_ATW2013_3B_STDW.DATA" "NORNE_ATW2013_3C_MSW.DATA" "NORNE_ATW2013_3C_STDW.DATA")
#("NORNE_ATW2013.DATA" "NORNE_ATW2013_1A_MSW.DATA" "NORNE_ATW2013_1A_STDW.DATA" "NORNE_ATW2013_1B_MSW.DATA" "NORNE_ATW2013_1B_STDW.DATA" "NORNE_ATW2013_1B_MSW_NO_XFLOW.DATA" "NORNE_ATW2013_2A_MSW.DATA" "NORNE_ATW2013_2A_STDW.DATA" "NORNE_ATW2013_2B_MSW.DATA" "NORNE_ATW2013_2B_STDW.DATA" "NORNE_ATW2013_3A_STDW.DATA" "NORNE_ATW2013_3B_MSW.DATA" "NORNE_ATW2013_3B_STDW.DATA" "NORNE_ATW2013_3C_MSW.DATA" "NORNE_ATW2013_3C_STDW.DATA" "NORNE_ATW2013_4A_MSW.DATA" "NORNE_ATW2013_4B_MSW.DATA" "NORNE_ATW2013_4B_STDW.DATA" "NORNE_ATW2013_4C_MSW.DATA" "NORNE_ATW2013_4C_STDW.DATA")
else
    echo "Unkown reservoir!"
    exit
fi

accelerator_list=("none" "rocsparse")
#("none" "rocalution" "rocsparse")
linear_solver_list=("ilu0")
#("ilu0" "cpr_quasiimpes")
well_contri_list=("false" "true")

#max_jobs=10
#job_count=0

echo "######################################################"
echo "Simulation/Profiling Section!"
echo "######################################################"
echo "" && echo ""

for well_contri in "${well_contri_list[@]}"; do
    for accelerator in "${accelerator_list[@]}"; do
	for linear_solver in "${linear_solver_list[@]}"; do
	    if [ $accelerator = "none" ]; then
		for deck in "${case_list[@]}"; do
		    ./rocprof-profiling.sh $reservoir $deck $accelerator $linear_solver $well_contri
	            #job_count=$((job_count+1))
		    #if [ "$job_count" -ge "$max_jobs" ]; then
			#wait -n
			#job_count=$((job_count-1))
		    #fi
		done
		#wait
	    else
		for deck in "${case_list[@]}"; do
		    ./rocprof-profiling.sh $reservoir $deck $accelerator $linear_solver $well_contri
		done
	    fi
	    echo "##### $accelerator - $linear_solver profiling done! #####"
	    echo ""
	done
    done
done

python3 summarize.py
