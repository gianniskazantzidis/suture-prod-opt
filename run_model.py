from models import run_model_single_period, run_model_multi_period, run_model_with_second_shift, run_model_with_backorder_penalty

#-----------------------------------------

# Function to select and run the appropriate model
def run_selected_model(params, model_type, time_limit, directory, param_set_index):
    if model_type == "single_period":
        return run_model_single_period(params, directory, param_set_index)
    elif model_type == "multi_period":
        return run_model_multi_period(params, time_limit, directory, param_set_index)
    elif model_type == "multi_period_with_second_shift":
        return run_model_with_second_shift(params, time_limit, directory, param_set_index)
    elif model_type == "multi_period_with_backorder_penalty":
        return run_model_with_backorder_penalty(params, time_limit, directory, param_set_index)

