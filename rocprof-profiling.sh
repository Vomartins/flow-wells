#!/bin/bash

flow_dir=/home/vinicius/Dev/flow-release/opm-simulators/build/bin

current_dir=$(pwd)
current_time=$(date +%H%M%S)

reservoir=$1
deck=$2
case=${deck%.*}
accelerator=$3
linsolver=$4
well_contributions=$5
trace_option=$6

#if [ "$accelerator" = "rocalution" ]; then
#    well_contributions='true'
#else
#    well_contributions='false'
#fi

file_name=$case-$current_time

threads=1

echo "$file_name --- $accelerator ––– $linsolver --- $trace_option"

data_dir=/home/vinicius/Dev/opm-tests/$reservoir/$deck
output_dir=$current_dir/rocprof-outputs/$file_name

mkdir $output_dir

cd $flow_dir

if [ "$accelerator" = "none" ]; then
    ./flow_blackoil --threads-per-process=$threads --accelerator-mode=$accelerator --matrix-add-well-contributions=$well_contributions --linear-solver=$linsolver $data_dir > $output_dir/$file_name-sim-output.txt
elif [ -z "$trace_option" ]; then
    rocprofv2 --plugin file -o $file_name -d $output_dir ./flow_blackoil --threads-per-process=$threads --accelerator-mode=$accelerator --matrix-add-well-contributions=$well_contributions --linear-solver=$linsolver $data_dir > $output_dir/$file_name-sim-output.txt
    cd $output_dir
    python3 $current_dir/results-analysis.py $file_name
else
   rocprofv2 $trace_option --plugin file -o $file_name -d $output_dir ./flow_blackoil --threads-per-process=$threads --accelerator-mode=$accelerator --matrix-add-well-contributions=$well_contributions --linear-solver=$linsolver $data_dir > $output_dir/$file_name-sim-output.txt
fi

echo "" >> $output_dir/command-line-options.txt
echo "### Flow options ###" >> $output_dir/command-line-options.txt
echo "--accelerator-mode = $accelerator" >> $output_dir/command-line-options.txt
echo "--linear-solver = $linsolver" >> $output_dir/command-line-options.txt
echo "--matrix-add-well-contributions = $well_contributions" >> $output_dir/command-line-options.txt
echo "--threads-per-process = $threads" >> $output_dir/command-line-options.txt
echo "" >> $output_dir/command-line-options.txt
echo "### Rocprof options ###" >> $output_dir/command-line-options.txt
echo "Trace: $trace_option" >> $output_dir/command-line-options.txt
echo "Plugin: file" >> $output_dir/command-line-options.txt
