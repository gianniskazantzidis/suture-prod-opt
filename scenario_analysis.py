import matplotlib.pyplot as plt
import json
import os
import numpy as np
from datetime import datetime
from run_model import run_selected_model
from parameters import parameter_set_1, parameter_set_2, parameter_set_3, parameter_set_4, parameter_set_5, parameter_set_6

#-----------------------------------------

def scenario_analysis(param_sets, run_no, model_types):
    
    results = {}

    # Create a dictionary of parameter set names to actual parameter sets
    param_sets_dict = {
        'parameter_set_1': parameter_set_1,
        # 'parameter_set_2': parameter_set_2
        # 'parameter_set_3': parameter_set_3
        # 'parameter_set_4': parameter_set_4
        # 'parameter_set_5': parameter_set_5
        'parameter_set_6': parameter_set_6

    }

    param_sets_list = list(param_sets_dict.items())

    # Create directory for results if it doesn't exist
    # directory = f"/Users/johnkazantzidis/dev/gurobi/results/file_{run_no}" # For home pc
    directory = f"/Users/manos/dev/prod-opt/results/file_{run_no}" # For work pc
    os.makedirs(directory, exist_ok=True)
    
    for model_type in model_types:
        for i, (param_name, params) in enumerate(param_sets_list):
            print(f"Running {model_type} with {param_name}")
            try:
                result = run_selected_model(params, model_type, time_limit=3600, directory=directory, param_set_index=i+1)
                results[f"{model_type}_{param_name}"] = result
            except ValueError as e:
                # Log the infeasible case and continue with the next parameter set
                print(f"Error with {model_type} and {param_name}: {e}")
                results[f"{model_type}_{param_name}"] = {"status": "infeasible"}

    # Create a unique filename
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    filename = f"{directory}/model-{timestamp}-{run_no}"
    results_filename = f"{filename}.json"

    # Save results to a file
    with open(results_filename, 'w') as f:
        json.dump(results, f, indent=4)
    
    return results, directory

#-----------------------------------------

def plot_scenario_analysis(results, directory, run_no):

    suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
    ShortageCost = 4

    # Objective Value comparison across scenarios
    objective_values = {k: results[k].get('objective_value', 0) for k in results}
    plt.figure(figsize=(10, 6))
    plt.bar(objective_values.keys(), objective_values.values())
    plt.xlabel('Parameter Set')
    plt.ylabel('Objective Value (Profit)')
    plt.title('Comparison of Objective Values Across Models and Scenarios')
    plt.xticks(rotation=45, ha="right")
    # plt.gca().autoscale(enable=True, axis='y', tight=True)  # Autoscale the y-axis
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f"file_{run_no}_objective_values.png"))
    plt.close()

    # Compare Production of 'silk' across models
    suture_type = 'silk'
    final_stage = 'Sterilization'  # Use the final stage to reflect completed production
    plt.figure(figsize=(10, 6))
    for k in results:
        production = results[k].get(final_stage, {}).get(suture_type, [0]*6)  # Directly fetch the values for 'Sterilization'
        plt.plot(range(1, 7), production, label=k)
    plt.xlabel('Month')
    plt.ylabel(f'Total Production of {suture_type}')
    plt.title(f'Total Production of {suture_type} Across Models and Scenarios')
    plt.legend()
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f"file_{run_no}_total_production_{suture_type}.png"))
    plt.close()

    # Compare Shipping of 'silk' across models
    plt.figure(figsize=(10, 6))
    for k in results:
        shipping = results[k].get('Shipping', {}).get(suture_type, [0]*6)[:6]
        plt.plot(range(1, 7), shipping, label=k)
    plt.xlabel('Month')
    plt.ylabel(f'Shipping of {suture_type}')
    plt.title(f'Shipping of {suture_type} Over Time Across Models')
    plt.legend()
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f"file_{run_no}_shipping_{suture_type}.png"))
    plt.close()


    # Stacked Shortage Penalty Plot
    plt.figure(figsize=(10, 6))
    cumulative_penalty = np.zeros(6)  # Initialize an array to hold the cumulative penalties for stacked bars
    for k in results:
        if 'Shortage' in results[k]:
            # Calculate shortage penalty for each month
            shortage_penalty = [
                sum( ShortageCost * results[k].get('Shortage', {}).get(s, [0]*6)[t] for s in suture_types) 
                for t in range(6)
            ]
            # Plot shortage penalty over the months
            plt.bar(range(1, 7), shortage_penalty, bottom=cumulative_penalty, label=k)
            cumulative_penalty += shortage_penalty
    plt.xlabel('Month')
    plt.ylabel('Shortage Penalty')
    plt.title('Stacked Shortage Penalty Over Time')
    plt.legend()
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f"file_{run_no}_stacked_shortage_penalty.png"))
    plt.close()


    # Shortage Penalty Plot
    plt.figure(figsize=(10, 6))
    for k in results:
        if 'Shortage' in results[k]:
            # Calculate shortage penalty for each month
            shortage_penalty = [
                sum( ShortageCost * results[k].get('Shortage', {}).get(s, [0]*6)[t] for s in suture_types) 
                for t in range(6)
            ]
            # Plot shortage penalty over the months
            plt.bar(range(1, 7), shortage_penalty, label=k, alpha=0.7)
    plt.xlabel('Month')
    plt.ylabel('Shortage Penalty')
    plt.title('Shortage Penalty Over Time')
    plt.legend()
    plt.xticks(range(1, 7))
    plt.tight_layout()
    plt.savefig(os.path.join(directory, f"file_{run_no}_shortage_penalty.png"))
    plt.close()


    # Plot second shift usage for both lines
    if any("second_shift" in k for k in results):
        plt.figure(figsize=(10, 6))
        for k in results:
            if "second_shift" in k:
                second_shift_line1 = results[k].get('SecondShift', {}).get('line1', [0]*6)[:6]
                second_shift_line2 = results[k].get('SecondShift', {}).get('line2', [0]*6)[:6]
                plt.plot(range(1, 7), second_shift_line1, label=f"{k}_line1")
                plt.plot(range(1, 7), second_shift_line2, label=f"{k}_line2")
        plt.xlabel('Month')
        plt.ylabel('Second Shift Usage')
        plt.title('Second Shift Usage Over Time (Both Lines)')
        plt.legend()
        plt.xticks(range(1, 7))
        plt.tight_layout()
        plt.savefig(os.path.join(directory, f"file_{run_no}_second_shift_usage.png"))
        plt.close()


