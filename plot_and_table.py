import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# root directory for test data
rootDir = "TEST_LINDO"
# set unit of time in seconds
unit_time = 5
# list of completed tests
tests = ["bppc4-08",            
"gen-ip054",           
"neos-3083819-nubu",   
"pk1",                 
"sct2",                
"chromaticindex512-7", 
"graph20-20-1rand",    
"neos-3627168-kasai",  
"railway_8_1_0",       
"trento1",             
"gen-ip002",           
"mushroom-best",       
"nu25-pr12",           
"s250r10",             
"var-smallemery-m6j6"]
# threads tested
threads = [1,2,4,8,16,32,64]


#
# Build reports from each ***_results.csv
# Then build report for branches per unit time 
#
for test in tests:

    dirName = f"{rootDir}/{test}"
    # read ***_results.csv to dataframe
    test_csv = f"{dirName}/{test}_results.csv"
    test_df = pd.read_csv(test_csv)

    # write Threads, Total_Branches, Total_Time to numpy arrays
    threads = test_df['Threads'].values
    log_threads = np.log10(threads)
    branches = test_df['Total_Branches'].values
    log_branches = np.log10(branches)
    tot_time = test_df['Total_Time'].values
    log_tot_time = np.log10(tot_time)
    best_bound = test_df['Best_Bound'].values
    best_obj = test_df['Objective_Value'].values
    status = test_df['Status'].values

    # if any status == 1 then print name
    # if(1 not in status):
    #     print(f"{test} was not solved in time limit")

    # compare total number of branches used to nThread=1
    branches_scale = branches/branches[0]
    branches_scale_log = np.log10(branches_scale)
    branches_scale_ticks = np.linspace(min(branches_scale ), max(branches_scale ), 5)
    branches_scale_ticks_log = np.log10(branches_scale_ticks)  
    branches_scale_ticks = np.round(branches_scale_ticks, 2)

    # compare solve time to the solve time of nThread=1
    time_scale = tot_time/tot_time[0]
    time_scale_log = np.log10(time_scale)
    time_scale_ticks = np.linspace(min(time_scale), max(time_scale), 5)
    time_scale_ticks_log = np.log10(time_scale_ticks)  
    time_scale_ticks = np.round(time_scale_ticks, 2)

    # total branches used during run by each thread config
    branch_ticks = np.linspace(min(branches), max(branches), 5)
    branch_ticks_log = np.log10(branch_ticks)
    branch_ticks = np.round(branch_ticks, 2)

    # solve time for each thread config
    time_ticks = np.linspace(min(tot_time), max(tot_time), 5)
    time_ticks_log = np.log10(time_ticks)   
    time_ticks = np.round(time_ticks, 2)

    # plot and save threads vs branches
    branch_plot_png = f"{dirName}/{test}_branch_plot"
    plt.plot(log_threads, log_branches,  marker="o")
    plt.yticks(branch_ticks_log, branch_ticks)
    plt.xticks(log_threads, threads)
    plt.xlabel('Threads')
    plt.ylabel('Total_Branches')
    plt.title(f"{test}: Branches processed in 2.5 hours")
    plt.savefig(branch_plot_png, bbox_inches='tight')
    plt.clf()

    # plot and save threads vs solve time
    time_plot_png = f"{dirName}/{test}_time_plot"
    plt.plot(log_threads, log_tot_time, marker="o")
    plt.yticks(time_ticks_log, time_ticks)
    plt.xticks(log_threads, threads)
    plt.xlabel('Threads')
    plt.ylabel('Time')
    plt.title(f"{test}: Solve time")
    plt.savefig(time_plot_png, bbox_inches='tight')
    plt.clf()
    
    # plot the scaled branches
    branch_plot_scaled_png = f"{dirName}/{test}_time_plot_scaled"
    plt.plot(log_threads, branches_scale_log, marker="o")
    plt.yticks(branches_scale_ticks_log, branches_scale_ticks)
    plt.xticks(log_threads, threads)
    plt.xlabel('Threads')
    plt.ylabel('Branch Multiplier')
    plt.title(f"{test}: Branch Multipliers vs. Number of Threads")
    plt.savefig(branch_plot_scaled_png, bbox_inches='tight')
    plt.clf()

    # plot the scaled time
    time_plot_scaled_png = f"{dirName}/{test}_time_plot_scaled"
    plt.plot(log_threads, time_scale_log, marker="o")
    plt.yticks(time_scale_ticks_log, time_scale_ticks)
    plt.xticks(log_threads, threads)
    plt.xlabel('Threads')
    plt.ylabel('Performance Multiplier')
    plt.title(f"{test}: Performance Multipliers vs. Number of Threads ")
    plt.savefig(time_plot_scaled_png, bbox_inches='tight')
    plt.clf()

    # table for models that were solved in time limit
    solve_table =  f"{dirName}/solve_time.md"
    with open(solve_table, "w+") as f:
        f.write("|Threads | Time | Multiplier | Best Objective |")
        f.write("\n")
        f.write("| - | - | - | - |")
        f.write("\n")
        for i in range(0,len(threads)):
            f.write(f"|{threads[i]}|{tot_time[i]:.2f}|{time_scale[i]:.2f}|{best_obj[i]:.2f}|")
            f.write("\n")




    med_branches_per_time = []
    # loop over each bounding 
    for thread in threads:
        threadCSV = f"{dirName}/{test}_bounding_{thread}.csv"
        threadDF = pd.read_csv(threadCSV)
        branches = threadDF['BRANCHs'].values
        time = threadDF['TIME'].values

        # compute branches per unit time
        # sum up branches for each time step
        branches_per_time = []
        branches_per_step = 0
        initTime = time[0]
        for t in np.arange(initTime + unit_time,max(time),unit_time):
            mask = (time <= t) & (time >= t - unit_time)
            branches_per_step_arr = branches[mask]
            if(len(branches_per_step_arr) > 0):
                branches_per_step = np.median(branches_per_step_arr)
                branches_per_step_arr[-1] - branches_per_step_arr[0]
                branches_per_time.append(branches_per_step)       

        # loop over branches_per_time an subtract the preve
        for i in range(1, len(branches_per_time)):
            branches_per_time[i] = branches_per_time[i] - branches_per_time[i-1]

        # if no data in branches_per_time use median of branches
        if(len(branches_per_time) == 0):
           branches_per_time.append(np.median(branches))
                                    
        med_branches_per_time.append(np.median(branches_per_time))

    # scale branches by the first entry
    med_branches_per_time_scale = np.array(med_branches_per_time)/med_branches_per_time[0]
    
    # plot branchs per unit of times
    branch_per_unit_png = f"{dirName}/branch_per_unit"
    plt.plot(threads,med_branches_per_time_scale, marker="o")
    plt.ylabel('Median Branches')
    plt.xticks(threads,threads)
    plt.xlabel('Threads')
    plt.ylabel('Performance Multiplier')
    plt.title(f"{test}: Branch Multipliers vs. Number of Threads (Median branches per {unit_time}(sec))")
    plt.savefig(branch_per_unit_png,  bbox_inches='tight')
    plt.clf()

    # table for problems that were bounded during time limit
    branch_per_unit_table = f"{dirName}/branch_per_unit.md"
    with open(branch_per_unit_table, "w+") as f:
        f.write("|Threads | Median Branches | Multiplier | Best Objective | Best Bound |")
        f.write("\n")
        f.write("| - | - | - | - | - |")
        f.write("\n")
        for i in range(0,len(threads)):
            f.write(f"|{threads[i]}|{med_branches_per_time[i]:.2f}|{med_branches_per_time_scale[i]:.2f}|{best_bound[i]:.2f}|{best_obj[i]:.2f}|")
            f.write("\n")

