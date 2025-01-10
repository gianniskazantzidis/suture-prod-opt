import os
from parameters import parameter_set_1, parameter_set_2, parameter_set_3, parameter_set_4, parameter_set_5, parameter_set_6
from scenario_analysis import scenario_analysis, plot_scenario_analysis

# Parameter sets for sensitivity analysis
param_sets = [parameter_set_1, parameter_set_6] # parameter_set_1, parameter_set_2 , parameter_set_3, parameter_set_4, parameter_set_5, parameter_set_6
model_types = ["multi_period"] # "multi_period", "multi_period_with_second_shift", "multi_period_with_backorder_penalty" 

def get_next_run_number(base_path):
    if not os.path.exists(base_path):
        os.makedirs(base_path)  # Create the base directory if it doesn't exist
    existing_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    run_numbers = [int(d.split('_')[-1]) for d in existing_dirs if d.startswith('file_')]
    if run_numbers:
        return max(run_numbers) + 1
    else:
        return 1

if __name__ == "__main__":

    # base_path = "/Users/johnkazantzidis/dev/gurobi/results" # For home pc
    base_path = "/Users/manos/dev/prod-opt/results" # For work pc
    run_no = get_next_run_number(base_path)
    results, directory = scenario_analysis(param_sets, run_no, model_types)
    plot_scenario_analysis(results, directory, run_no)

    print(f"Results saved in directory: {directory}")
