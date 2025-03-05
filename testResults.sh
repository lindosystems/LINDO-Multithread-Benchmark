#!/bin/bash
# Change this name to run
test_files="bppc4-08 gen-ip054 neos-3083819-nubu pk1 sct2 chromaticindex512-7 graph20-20-1rand neos-3627168-kasai railway_8_1_0 trento1 gen-ip002 mushroom-best nu25-pr12 s250r10 var-smallemery-m6j6"

# patterns for output csv
status_pat="Status                       :"
obj_pat="Objective Value              :"
bound_pat="Best Bound                   :"
nBranches_pat="Total Branches               :"
time_pat="Total Time (sec.)            :"



for test_file in $test_files; do
    # path to tests
    logs_dir=/home/jhaas/TEST_LINDO/"$test_file"/

    # output csv file
    output_csv="$logs_dir""$test_file"_results.csv


    # csv header
    header="Test_File,Threads,Status,Objective_Value,Best_Bound,Total_Branches,Total_Time"
    # write header to csv
    echo $header > "$output_csv"
    bounding_header="BRANCHs,NODEs,LPs,BEST_BOUND,BEST_IP,RGAP,TIME,OPTIME"
    for threads in  1 2 4 8 16 32 64; do
        log_file="$logs_dir"/"$test_file"_"$threads".log

        # Status
        status=$(grep "$status_pat" "$log_file" | sed 's/Status                       :\s*//')
        # Objective Value
        obj=$(grep "$obj_pat" "$log_file" | sed 's/Objective Value              :\s*//')
        # Best Bound
        bound=$(grep "$bound_pat" "$log_file" | sed 's/Best Bound                   :\s*//')
        # Total Branches
        nBranches=$(grep "$nBranches_pat" "$log_file" | sed 's/Total Branches               :\s*//')
        # Total Time
        time=$(grep "$time_pat" "$log_file" | sed 's/Total Time (sec.)            :\s*//')
        
        # write row to csv
        row="$test_file,$threads,$status,$obj,$bound,$nBranches,$time"
        echo "$row" >> "$output_csv"

        bounding_csv="$logs_dir""$test_file"_bounding_"$threads".csv
        echo $bounding_header > "$bounding_csv"
        # get the bounding data
        cat "$log_file"            | 
            grep -E '^\s*[1-9]' |
            sed 's/^\s*//g'     | 
            sed 's/\s*$//g'     | 
            sed 's/\s\+/,/g'    | 
            grep -v '[(|)]'     >> "$bounding_csv"
    done
done
