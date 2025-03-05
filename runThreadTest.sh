#!/bin/bash

# Change this name to run
test_file=bppc4-08

# let it be
file=/home/jhaas/TEST_LINDO/"$test_file".mps
test_dir=/home/jhaas/TEST_LINDO/"$test_file"

echo "$test_file"
mkdir "$test_dir"

nSecs=9000

# run 1 2 4 8
pbs_file="$test_dir"/"$test_file"_1_2_4_8.pbs
# build the pbs file
echo "#PBS -N "$test_file"_1_2_4_8" > $pbs_file
echo "#PBS -j oe" >> $pbs_file
echo "#PBS -l select=1:ncpus=2:mpiprocs=2:mem=128gb" >> $pbs_file
echo "#PBS -l walltime=10:10:00" >> $pbs_file
#echo "cd \$PBS_O_WORKDIR" >> $pbs_file
echo "-Run 1" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 1 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_1.log  >> $pbs_file
echo "-Run 2" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 2 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_2.log  >> $pbs_file
echo "-Run 4" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 4 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_4.log  >> $pbs_file
echo "-Run 8" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 8 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_8.log  >> $pbs_file
qsub "$pbs_file"

# run 16 32 64
pbs_file="$test_dir"/"$test_file"_16_32_64.pbs
# build the pbs file
echo "#PBS -N "$test_file"_16_32_64" > $pbs_file
echo "#PBS -j oe" >> $pbs_file
echo "#PBS -l select=1:ncpus=2:mpiprocs=2:mem=128gb" >> $pbs_file
echo "#PBS -l walltime=08:10:00" >> $pbs_file
#echo "cd \$PBS_O_WORKDIR" >> $pbs_file
echo "echo -Run 16" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 16 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_16.log  >> $pbs_file
echo "echo -Run 32" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 32 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_32.log  >> $pbs_file
echo "echo -Run 64" >> $pbs_file
echo ./LINDO/lindoapi/bin/linux64/runlindo "$file"  -nthreads 64 -tlim  "$nSecs" ">>" "$test_dir"/"$test_file"_64.log  >> $pbs_file
qsub "$pbs_file"
