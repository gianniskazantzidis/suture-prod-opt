# Thesis Repository: Multi-Period Production Scheduling with Scenario Analysis

This repository contains all files and scripts used for my thesis titled **"Optimization of Sutures Production Processes: Multi-Period Mathematical Modeling"**. The thesis explores production optimization through various scenarios and models, aiming to enhance operational efficiency.

## Repository Structure

- **parameters.py**: Parameter definitions used across the models.
- **models.py**: Contains model definitions for the single-period model and the 3 multi-period models.
- **run_model.py**: Function that takes the desired model to test and prepares it for the scenario analysis.
- **scenario_analysis.py**: Analyzes different scenarios and outputs plots of the results.
- **main.py**: The primary script to initialize and run the models.
- ***Combination-* folders**: Each folder contains data and files related to the results of the specific experiment combinations and scenarios analyzed in the thesis.
- **requirements.txt**: List of required Python libraries to run the code.
- **LICENSE**: License for this repository.
- **README.md**: This file.


## How to Use

### Prerequisites
1. Python 3.7 or newer installed on your system.
2. Gurobi Optimizer installed and configured with a valid license.

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>

2. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt

3. Install Gurobi and configure your license:
    - Follow the Gurobi installation instructions for your operating system.
    - Activate your Gurobi license:
         ```bash
         grbgetkey <YOUR_LICENSE_KEY>

4. To run the main script, use:
   ```bash
    python main.py

You can also run specific scenario analysis or parameter testing using the respective scripts.

For questions or further discussion, feel free to contact me at ioanniskazantzidis1@gmail.com.

## Disclaimer

All data, techniques, and details of the production process presented in this repository are entirely fictional and created solely for academic purposes. They do not reflect any real-world processes, methods, or proprietary information.

