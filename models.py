import gurobipy as gp
from gurobipy import GRB
import os

#-----------------------------------------

def validate_parameters(params):
    try:
        # Ensure all parameters are non-negative
        assert all(v >= 0 for v in params['ProdCost'].values()), "Production costs must be non-negative"
        assert all(all(d >= 0 for d in demand_list) for demand_list in params['Demand'].values()), "Demand must be non-negative"
        assert all(v >= 0 for v in params['MaxCapacity'].values()), "Max capacity must be non-negative"
        assert all(v >= 0 for v in params['MaxEmployees'].values()), "Max employees must be non-negative"

        assert all(v >= 0 for v in params['MaxPackagingCapacity'].values()), "Max packaging capacity must be non-negative"
        assert all(v >= 0 for v in params['SafetyStock'].values()), "Safety stock must be non-negative"
    except AssertionError as e:
        raise ValueError(f"Parameter validation failed: {e}")

#-----------------------------------------

def initial_feasibility_check(model):
    model.optimize()
    if model.Status != GRB.OPTIMAL:
        raise ValueError("Initial model run did not find an optimal solution")

#-----------------------------------------

def automated_validation(model, directory, param_set_index):
    violated_constraints = []
    file_path = os.path.join(directory, f'Violated_Constraints_param_set_{param_set_index}.txt')

    # Check if the model has an optimal or feasible solution
    if model.Status == GRB.OPTIMAL or model.Status == GRB.SUBOPTIMAL:
        for constraint in model.getConstrs():
            # Access the Slack attribute safely
            if constraint.Slack < 0:
                violated_constraints.append(constraint.ConstrName)
        with open(file_path, 'w') as f:
            if violated_constraints:
                f.write("Violated Constraints:\n")
                for vc in violated_constraints:
                    f.write(f"{vc}\n")
            else:
                f.write("No constraints violated.\n")
    else:
        # Handle infeasible or unbounded models
        with open(file_path, 'w') as f:
            f.write(f"Model is infeasible or unbounded. Status code: {model.Status}\n")
            f.write("Cannot retrieve constraint slacks because there is no feasible solution.\n")

#-----------------------------------------

# Function to run the single period model
def run_model_single_period(params, directory, param_set_index):
    validate_parameters(params)

    # Define indices
    suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
    raw_material_types = ['propylen_raw', 'polyamid_raw', 'silk_raw', 'polyester_raw', 'profimed_raw', 'steel_raw', 'supramid_raw', 'pga_raw', 'pgla_raw', 'rapid_pgla_raw', 'monosorb_raw', 'monofast_raw']
    needle_types = ['straight', 'curve_3_8', 'curve_1_2']
    production_lines = ['line1', 'line2']
    packaging_lines = ['pack_line1', 'pack_line2']
    time_periods = [1]  # Single period

    suture_to_raw_material = {s: s + '_raw' for s in suture_types}

    InitialInventory = params['InitialInventory']
    InitialRawInventory = params['InitialRawInventory']
    InitialNeedleInventory = params['InitialNeedleInventory']
    MaxCapacity = params['MaxCapacity']
    MaxCapacity_m = params['MaxCapacity_m']
    BatchSize = params['BatchSize']
    MaxEmployees = params['MaxEmployees']
    MaxPackagingCapacity = params['MaxPackagingCapacity']
    SafetyStock = params['SafetyStock']
    Demand = params['Demand']
    Price = params['Price']
    ProdCost = params['ProdCost']
    LaborCost = params['LaborCost']
    Cost_r = params['Cost_r']
    NeedleCost = params['NeedleCost']
    PackagingCost = params['PackagingCost']
    StorageCost = params['StorageCost']
    SterilizationCost = params['SterilizationCost']
    CuttingCost = params['CuttingCost']
    MaxRawInventory = params['MaxRawInventory']
    MaxNeedleInventory = params['MaxNeedleInventory']
    MinRawInventory = params['MinRawInventory']
    MinNeedleInventory = params['MinNeedleInventory']
    MaxFinishedInventory = params['MaxFinishedInventory']

    model = gp.Model("Single_Period_Model")

    I_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.CONTINUOUS, name="RawInventory", lb=0)
    I_needles = model.addVars(needle_types, time_periods, vtype=GRB.CONTINUOUS, name="NeedleInventory", lb=0)
    I_finished = model.addVars(suture_types, time_periods, vtype=GRB.CONTINUOUS, name="FinishedInventory", lb=0)
    Q_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityRaw", lb=0)
    Q_needles = model.addVars(needle_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityNeedles", lb=0)
    D = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Shipping", lb=0)

    P_preparation = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Preparation", lb=0)
    P_cutting = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Cutting", lb=0)
    P_needle_attachment = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="NeedleAttachment", lb=0)
    P_packaging = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Packaging", lb=0)
    P_sterilization = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Sterilization", lb=0)

    B = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Batch", lb=0)
    M = model.addVars(['machine1', 'machine2'], time_periods, vtype=GRB.BINARY, name="MachineOp")
    E = model.addVars(production_lines, time_periods, vtype=GRB.INTEGER, name="Employees", lb=0, ub=MaxEmployees)
    K = model.addVars(packaging_lines, time_periods, vtype=GRB.BINARY, name="PackLinesOp")
    
    revenue = gp.quicksum(Price[s] * D[s, t] for s in suture_types for t in time_periods)
    production_cost = gp.quicksum(ProdCost[s] * P_preparation[s, t] for s in suture_types for t in time_periods)
    cutting_cost = gp.quicksum(CuttingCost * P_cutting[s, t] for s in suture_types for t in time_periods)
    raw_material_cost = gp.quicksum(Cost_r[r] * Q_raw[r, t] for r in raw_material_types for t in time_periods)
    needle_cost = gp.quicksum(NeedleCost[n] * Q_needles[n, t] for n in needle_types for t in time_periods)
    labor_cost = gp.quicksum(LaborCost[l] * E[l, t] for l in production_lines for t in time_periods)
    storage_cost = gp.quicksum(StorageCost * I_finished[s, t] for s in suture_types for t in time_periods) + gp.quicksum(StorageCost * I_raw[r, t] for r in raw_material_types for t in time_periods) + gp.quicksum(StorageCost * I_needles[n, t] for n in needle_types for t in time_periods)
    packaging_cost = gp.quicksum(PackagingCost[s] * P_packaging[s, t] for s in suture_types for t in time_periods)
    sterilization_cost = gp.quicksum(SterilizationCost['A'] * P_sterilization[s, t] for s in suture_types if s not in ['silk', 'polyester'] for t in time_periods) + gp.quicksum(SterilizationCost['B'] * P_sterilization[s, t] for s in ['silk', 'polyester'] for t in time_periods)

    model.setObjective(revenue - (production_cost + cutting_cost + raw_material_cost + needle_cost + labor_cost + storage_cost + packaging_cost + sterilization_cost), GRB.MAXIMIZE)

    # Constraints

    # Production Capacity
    for t in time_periods:
        for l in production_lines:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= MaxCapacity[l], name=f"ProdCap_{l}_{t}")

    # Machine Availability
    for t in time_periods:
        for m in ['machine1', 'machine2']:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= M[m, t] * MaxCapacity_m[m], name=f"MachCap_{m}_{t}")

    # Batch Size
    for t in time_periods:
        for s in suture_types:
            model.addConstr(B[s, t] * BatchSize[s] == P_preparation[s, t], name=f"Batch_{s}_{t}")

    # Initial Inventory Balance for Finished Goods
    for s in suture_types:
        model.addConstr(I_finished[s, 1] == InitialInventory[s] + P_sterilization[s, t] - D[s, 1], name=f"InvBal_{s}_1")

    # Raw Material Inventory Update
    for r in raw_material_types:
        model.addConstr(I_raw[r, 1] == InitialRawInventory[r] + Q_raw[r, 1] - gp.quicksum(P_preparation[s, 1] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_1")

    # Needle Inventory Update
    for n in needle_types:
        model.addConstr(I_needles[n, 1] == InitialNeedleInventory[n] + Q_needles[n, 1] - gp.quicksum(P_needle_attachment[s, 1] for s in suture_types), name=f"NeedleInv_{n}_1")

    # Non-negativity of Inventory
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] >= MinRawInventory[r], name=f"MinRawInv_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] >= MinNeedleInventory[n], name=f"MinNeedleInv_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] >= SafetyStock[s], name=f"MinFinInv_{s}_{t}")

    # Maximum inventory limits for raw materials, needles and finished goods
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] <= MaxRawInventory[r], name=f"MaxRawInventory_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] <= MaxNeedleInventory[n], name=f"MaxNeedleInventory_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] <= MaxFinishedInventory[s], name=f"MaxFinishedInventory_{s}_{t}")

    # Staffing Levels
    for t in time_periods:
        for l in production_lines:
            model.addConstr(E[l, t] >= gp.quicksum(P_preparation[s, t] for s in suture_types) / 700, name=f"Staff_{l}_{t}")
            model.addConstr(E[l, t] <= MaxEmployees[l], name=f"MaxEmployees_{l}_{t}")

    # Demand Fulfillment
    for t in time_periods:
        for s in suture_types:
            model.addConstr(D[s, t] == Demand[s][t-1], name=f"Demand_{s}_{t}")

    # Packaging Line Capacity
    for t in time_periods:
        for p in packaging_lines:
            model.addConstr(gp.quicksum(P_packaging[s, t] for s in suture_types) <= K[p, t] * MaxPackagingCapacity[p], name=f"PackCap_{p}_{t}")

    # Binary Machine Operation
    for m in ['machine1', 'machine2']:
        for t in time_periods:
            model.addConstr(M[m, t] <= 1, name=f"BinaryMach_{m}_{t}")

    # Multi-stage Production Constraints
    for t in time_periods:
        for s in suture_types:
            # Preparation to Cutting
            model.addConstr(P_cutting[s, t] == P_preparation[s, t], name=f"Cutting_{s}_{t}")

            # Cutting to Needle Attachment
            model.addConstr(P_needle_attachment[s, t] == P_cutting[s, t], name=f"NeedleAttach_{s}_{t}")

            # Needle Attachment to Packaging
            model.addConstr(P_packaging[s, t] == P_needle_attachment[s, t], name=f"PackReq_{s}_{t}")

            # Packaging to Sterilization
            model.addConstr(P_sterilization[s, t] == P_packaging[s, t], name=f"Sterilization_{s}_{t}")

    # Solve the model
    # initial_feasibility_check(model)  # Initial Feasibility Check
    model.optimize()
    automated_validation(model, directory, param_set_index)  # Automated Validation

    # Check for infeasibility, unboundedness, or optimal solution
    if model.Status == GRB.INFEASIBLE:
        print(f"Model {param_set_index} is infeasible! Writing IIS to file.")
        model.computeIIS()
        model.write(f'{directory}/model_{param_set_index}_iis.ilp')
        raise ValueError(f"Model {param_set_index} is infeasible! Check the IIS file.")
    
    elif model.Status == GRB.UNBOUNDED:
        print(f"Model {param_set_index} is unbounded!")
        raise ValueError(f"Model {param_set_index} is unbounded!")

    elif model.Status != GRB.OPTIMAL:
        print(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")
        raise ValueError(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")



    results = {}
    if model.Status == GRB.OPTIMAL:
        results['objective_value'] = model.objVal
        results['Preparation'] = {s: [P_preparation[s, t].x for t in time_periods] for s in suture_types}
        results['Cutting'] = {s: [P_cutting[s, t].x for t in time_periods] for s in suture_types}
        results['NeedleAttachment'] = {s: [P_needle_attachment[s, t].x for t in time_periods] for s in suture_types}
        results['Packaging'] = {s: [P_packaging[s, t].x for t in time_periods] for s in suture_types}
        results['Sterilization'] = {s: [P_sterilization[s, t].x for t in time_periods] for s in suture_types}
        results['Shipping'] = {s: [D[s, t].x for t in time_periods] for s in suture_types}
        results['RawInventory'] = {r: [I_raw[r, t].x for t in time_periods] for r in raw_material_types}
        results['NeedleInventory'] = {n: [I_needles[n, t].x for t in time_periods] for n in needle_types}
        results['FinishedInventory'] = {s: [I_finished[s, t].x for t in time_periods] for s in suture_types}
    else:
        results['status'] = model.Status

    print(f"RawInventory: {results['RawInventory']}\n\n")
    print(f"NeedleInventory: {results['NeedleInventory']}\n\n")
    print(f"FinishedInventory: {results['FinishedInventory']}\n\n")

    return results

#-----------------------------------------

# Function to run the multi-period model
def run_model_multi_period(params, time_limit, directory, param_set_index):
    validate_parameters(params)

    # Define indices
    suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
    raw_material_types = ['propylen_raw', 'polyamid_raw', 'silk_raw', 'polyester_raw', 'profimed_raw', 'steel_raw', 'supramid_raw', 'pga_raw', 'pgla_raw', 'rapid_pgla_raw', 'monosorb_raw', 'monofast_raw']
    needle_types = ['straight', 'curve_3_8', 'curve_1_2']
    production_lines = ['line1', 'line2']
    packaging_lines = ['pack_line1', 'pack_line2']
    time_periods = list(range(1, 7))  # 6 months

    suture_to_raw_material = {s: s + '_raw' for s in suture_types}

    InitialInventory = params['InitialInventory']
    InitialRawInventory = params['InitialRawInventory']
    InitialNeedleInventory = params['InitialNeedleInventory']
    MaxCapacity = params['MaxCapacity']
    MaxCapacity_m = params['MaxCapacity_m']
    BatchSize = params['BatchSize']
    MaxEmployees = params['MaxEmployees']
    MaxPackagingCapacity = params['MaxPackagingCapacity']
    SafetyStock = params['SafetyStock']
    Demand = params['Demand']
    Price = params['Price']
    ProdCost = params['ProdCost']
    LaborCost = params['LaborCost']
    Cost_r = params['Cost_r']
    NeedleCost = params['NeedleCost']
    PackagingCost = params['PackagingCost']
    StorageCost = params['StorageCost']
    SterilizationCost = params['SterilizationCost']
    CuttingCost = params['CuttingCost']
    MaxRawInventory = params['MaxRawInventory']
    MaxNeedleInventory = params['MaxNeedleInventory']
    MinRawInventory = params['MinRawInventory']
    MinNeedleInventory = params['MinNeedleInventory']
    MaxFinishedInventory = params['MaxFinishedInventory']

    model = gp.Model("Multi_Period_Model")

    I_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.CONTINUOUS, name="RawInventory", lb=0)
    I_needles = model.addVars(needle_types, time_periods, vtype=GRB.CONTINUOUS, name="NeedleInventory", lb=0)
    I_finished = model.addVars(suture_types, time_periods, vtype=GRB.CONTINUOUS, name="FinishedInventory", lb=0)
    Q_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityRaw", lb=0)
    Q_needles = model.addVars(needle_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityNeedles", lb=0)
    D = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Shipping", lb=0)

    P_preparation = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Preparation", lb=0)
    P_cutting = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Cutting", lb=0)
    P_needle_attachment = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="NeedleAttachment", lb=0)
    P_packaging = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Packaging", lb=0)
    P_sterilization = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Sterilization", lb=0)

    B = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Batch", lb=0)
    M = model.addVars(['machine1', 'machine2'], time_periods, vtype=GRB.BINARY, name="MachineOp")
    E = model.addVars(production_lines, time_periods, vtype=GRB.INTEGER, name="Employees", lb=0, ub=MaxEmployees)
    K = model.addVars(packaging_lines, time_periods, vtype=GRB.BINARY, name="PackLinesOp")

    revenue = gp.quicksum(Price[s] * D[s, t] for s in suture_types for t in time_periods)
    production_cost = gp.quicksum(ProdCost[s] * P_preparation[s, t] for s in suture_types for t in time_periods)
    cutting_cost = gp.quicksum(CuttingCost * P_cutting[s, t] for s in suture_types for t in time_periods)
    raw_material_cost = gp.quicksum(Cost_r[r] * Q_raw[r, t] for r in raw_material_types for t in time_periods)
    needle_cost = gp.quicksum(NeedleCost[n] * Q_needles[n, t] for n in needle_types for t in time_periods)
    labor_cost = gp.quicksum(LaborCost[l] * E[l, t] for l in production_lines for t in time_periods)
    storage_cost = gp.quicksum(StorageCost * I_finished[s, t] for s in suture_types for t in time_periods) + gp.quicksum(StorageCost * I_raw[r, t] for r in raw_material_types for t in time_periods) + gp.quicksum(StorageCost * I_needles[n, t] for n in needle_types for t in time_periods)
    packaging_cost = gp.quicksum(PackagingCost[s] * P_packaging[s, t] for s in suture_types for t in time_periods)
    sterilization_cost = gp.quicksum(SterilizationCost['A'] * P_sterilization[s, t] for s in suture_types if s not in ['silk', 'polyester'] for t in time_periods) + gp.quicksum(SterilizationCost['B'] * P_sterilization[s, t] for s in ['silk', 'polyester'] for t in time_periods)
   

    model.setObjective(revenue - (production_cost + cutting_cost + raw_material_cost + needle_cost + labor_cost + storage_cost + packaging_cost + sterilization_cost), GRB.MAXIMIZE)

    # Constraints

    # Production Capacity
    for t in time_periods:
        for l in production_lines:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= MaxCapacity[l], name=f"ProdCap_{l}_{t}")

    # Machine Availability
    for t in time_periods:
        for m in ['machine1', 'machine2']:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= M[m, t] * MaxCapacity_m[m], name=f"MachCap_{m}_{t}")

    # Batch Size
    for t in time_periods:
        for s in suture_types:
            model.addConstr(B[s, t] * BatchSize[s] == P_preparation[s, t], name=f"Batch_{s}_{t}")

    # Initial Inventory Balance for Finished Goods
    for s in suture_types:
        model.addConstr(I_finished[s, 1] == InitialInventory[s] + P_sterilization[s, 1] - D[s, 1], name=f"InvBal_{s}_1")

    # Inventory Balance for Finished Goods in subsequent periods
    for t in time_periods[1:]:
        for s in suture_types:
            model.addConstr(I_finished[s, t] == I_finished[s, t-1] + P_sterilization[s, t] - D[s, t], name=f"InvBal_{s}_{t}")

    # Raw Material Inventory Update
    for r in raw_material_types:
        model.addConstr(I_raw[r, 1] == InitialRawInventory[r] + Q_raw[r, 1] - gp.quicksum(P_preparation[s, 1] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_1")
        for t in time_periods[1:]:
            model.addConstr(I_raw[r, t] == I_raw[r, t-1] + Q_raw[r, t] - gp.quicksum(P_preparation[s, t] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_{t}")

    # Needle Inventory Update
    for n in needle_types:
        model.addConstr(I_needles[n, 1] == InitialNeedleInventory[n] + Q_needles[n, 1] - gp.quicksum(P_needle_attachment[s, 1] for s in suture_types), name=f"NeedleInv_{n}_1")
        for t in time_periods[1:]:
            model.addConstr(I_needles[n, t] == I_needles[n, t-1] + Q_needles[n, t] - gp.quicksum(P_needle_attachment[s, t] for s in suture_types), name=f"NeedleInv_{n}_{t}")

    # Non-negativity of Inventory
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] >= MinRawInventory[r], name=f"MinRawInv_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] >= MinNeedleInventory[n], name=f"MinNeedleInv_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] >= SafetyStock[s], name=f"MinFinInv_{s}_{t}")
    
    # Maximum inventory limits for raw materials, needles and finished goods
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] <= MaxRawInventory[r], name=f"MaxRawInventory_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] <= MaxNeedleInventory[n], name=f"MaxNeedleInventory_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] <= MaxFinishedInventory[s], name=f"MaxFinishedInventory_{s}_{t}")

    # Staffing Levels
    for t in time_periods:
        for l in production_lines:
            model.addConstr(E[l, t] >= gp.quicksum(P_preparation[s, t] for s in suture_types) / 800, name=f"Staff_{l}_{t}")
            model.addConstr(E[l, t] <= MaxEmployees[l], name=f"MaxEmployees_{l}_{t}")

    # Demand Fulfillment
    for t in time_periods:
        for s in suture_types:
            model.addConstr(D[s, t] == Demand[s][t-1], name=f"Demand_{s}_{t}")

    # Packaging Line Capacity
    for t in time_periods:
        for p in packaging_lines:
            model.addConstr(gp.quicksum(P_packaging[s, t] for s in suture_types) <= K[p, t] * MaxPackagingCapacity[p], name=f"PackCap_{p}_{t}")

    # Binary Machine Operation
    for m in ['machine1', 'machine2']:
        for t in time_periods:
            model.addConstr(M[m, t] <= 1, name=f"BinaryMach_{m}_{t}")

    # Multi-stage Production Constraints
    for t in time_periods:
        for s in suture_types:
            # Preparation to Cutting
            model.addConstr(P_cutting[s, t] == P_preparation[s, t], name=f"Cutting_{s}_{t}")

            # Cutting to Needle Attachment
            model.addConstr(P_needle_attachment[s, t] == P_cutting[s, t], name=f"NeedleAttach_{s}_{t}")

            # Needle Attachment to Packaging
            model.addConstr(P_packaging[s, t] == P_needle_attachment[s, t], name=f"PackReq_{s}_{t}")

            # Packaging to Sterilization
            model.addConstr(P_sterilization[s, t] == P_packaging[s, t], name=f"Sterilization_{s}_{t}")

    # Solve the model
    model.Params.TimeLimit = time_limit  # Set a time limit for the solver
    # initial_feasibility_check(model)  # Initial Feasibility Check
    model.optimize()
    automated_validation(model, directory, param_set_index)  # Automated Validation


    # Check for infeasibility, unboundedness, or optimal solution
    if model.Status == GRB.INFEASIBLE:
        print(f"Model {param_set_index} is infeasible! Writing IIS to file.")
        model.computeIIS()
        model.write(f'{directory}/model_{param_set_index}_iis.ilp')
        raise ValueError(f"Model {param_set_index} is infeasible! Check the IIS file.")
    
    elif model.Status == GRB.UNBOUNDED:
        print(f"Model {param_set_index} is unbounded!")
        raise ValueError(f"Model {param_set_index} is unbounded!")

    elif model.Status != GRB.OPTIMAL:
        print(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")
        raise ValueError(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")


    results = {}
    if model.Status == GRB.OPTIMAL:
        results['objective_value'] = model.objVal
        results['Preparation'] = {s: [P_preparation[s, t].x for t in time_periods] for s in suture_types}
        results['Cutting'] = {s: [P_cutting[s, t].x for t in time_periods] for s in suture_types}
        results['NeedleAttachment'] = {s: [P_needle_attachment[s, t].x for t in time_periods] for s in suture_types}
        results['Packaging'] = {s: [P_packaging[s, t].x for t in time_periods] for s in suture_types}
        results['Sterilization'] = {s: [P_sterilization[s, t].x for t in time_periods] for s in suture_types}
        results['Shipping'] = {s: [D[s, t].x for t in time_periods] for s in suture_types}
        results['RawInventory'] = {r: [I_raw[r, t].x for t in time_periods] for r in raw_material_types}
        results['NeedleInventory'] = {n: [I_needles[n, t].x for t in time_periods] for n in needle_types}
        results['FinishedInventory'] = {s: [I_finished[s, t].x for t in time_periods] for s in suture_types}
    else:
        results['status'] = model.Status

    print(f"Objective Value without second shift and backorder penalty: {results['objective_value']}")

    return results

#-----------------------------------------

# Function to run the multi-period model with second shift penalty
def run_model_with_second_shift(params, time_limit, directory, param_set_index):
    validate_parameters(params)

    # Define indices
    suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
    raw_material_types = ['propylen_raw', 'polyamid_raw', 'silk_raw', 'polyester_raw', 'profimed_raw', 'steel_raw', 'supramid_raw', 'pga_raw', 'pgla_raw', 'rapid_pgla_raw', 'monosorb_raw', 'monofast_raw']
    needle_types = ['straight', 'curve_3_8', 'curve_1_2']
    production_lines = ['line1', 'line2']
    packaging_lines = ['pack_line1', 'pack_line2']
    time_periods = list(range(1, 7))  # 6 months

    suture_to_raw_material = {s: s + '_raw' for s in suture_types}

    InitialInventory = params['InitialInventory']
    InitialRawInventory = params['InitialRawInventory']
    InitialNeedleInventory = params['InitialNeedleInventory']
    MaxCapacity = params['MaxCapacity']
    MaxCapacity_m = params['MaxCapacity_m']
    BatchSize = params['BatchSize']
    MaxEmployees = params['MaxEmployees']
    MaxPackagingCapacity = params['MaxPackagingCapacity']
    SafetyStock = params['SafetyStock']
    Demand = params['Demand']
    Price = params['Price']
    ProdCost = params['ProdCost']
    LaborCost = params['LaborCost']
    Cost_r = params['Cost_r']
    NeedleCost = params['NeedleCost']
    PackagingCost = params['PackagingCost']
    StorageCost = params['StorageCost']
    SterilizationCost = params['SterilizationCost']
    CuttingCost = params['CuttingCost']
    MaxRawInventory = params['MaxRawInventory']
    MaxNeedleInventory = params['MaxNeedleInventory']
    MinRawInventory = params['MinRawInventory']
    MinNeedleInventory = params['MinNeedleInventory']
    MaxFinishedInventory = params['MaxFinishedInventory']

    model = gp.Model("Multi_Period_Model_With_Second_Shift")

    I_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.CONTINUOUS, name="RawInventory", lb=0)
    I_needles = model.addVars(needle_types, time_periods, vtype=GRB.CONTINUOUS, name="NeedleInventory", lb=0)
    I_finished = model.addVars(suture_types, time_periods, vtype=GRB.CONTINUOUS, name="FinishedInventory", lb=0)
    Q_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityRaw", lb=0)
    Q_needles = model.addVars(needle_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityNeedles", lb=0)
    D = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Shipping", lb=0)

    P_preparation = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Preparation", lb=0)
    P_cutting = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Cutting", lb=0)
    P_needle_attachment = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="NeedleAttachment", lb=0)
    P_packaging = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Packaging", lb=0)
    P_sterilization = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Sterilization", lb=0)

    B = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Batch", lb=0)
    M = model.addVars(['machine1', 'machine2'], time_periods, vtype=GRB.BINARY, name="MachineOp")
    E = model.addVars(production_lines, time_periods, vtype=GRB.INTEGER, name="Employees", lb=0)
    K = model.addVars(packaging_lines, time_periods, vtype=GRB.BINARY, name="PackLinesOp")
    S = model.addVars(production_lines, time_periods, vtype=GRB.BINARY, name="SecondShift")
    
    revenue = gp.quicksum(Price[s] * D[s, t] for s in suture_types for t in time_periods)
    production_cost = gp.quicksum(ProdCost[s] * P_preparation[s, t] for s in suture_types for t in time_periods)
    cutting_cost = gp.quicksum(CuttingCost * P_cutting[s, t] for s in suture_types for t in time_periods)
    raw_material_cost = gp.quicksum(Cost_r[r] * Q_raw[r, t] for r in raw_material_types for t in time_periods)
    needle_cost = gp.quicksum(NeedleCost[n] * Q_needles[n, t] for n in needle_types for t in time_periods)
    labor_cost = gp.quicksum(LaborCost[l] * E[l, t] for l in production_lines for t in time_periods)
    storage_cost = gp.quicksum(StorageCost * I_finished[s, t] for s in suture_types for t in time_periods) + gp.quicksum(StorageCost * I_raw[r, t] for r in raw_material_types for t in time_periods) + gp.quicksum(StorageCost * I_needles[n, t] for n in needle_types for t in time_periods)
    packaging_cost = gp.quicksum(PackagingCost[s] * P_packaging[s, t] for s in suture_types for t in time_periods)
    sterilization_cost = gp.quicksum(SterilizationCost['A'] * P_sterilization[s, t] for s in suture_types if s not in ['silk', 'polyester'] for t in time_periods) + gp.quicksum(SterilizationCost['B'] * P_sterilization[s, t] for s in ['silk', 'polyester'] for t in time_periods)
    second_shift_cost = gp.quicksum(1.05 * LaborCost[l] * E[l,t] * S[l, t] for l in production_lines for t in time_periods)

    model.setObjective(revenue - (production_cost + cutting_cost + raw_material_cost + needle_cost + labor_cost + second_shift_cost + storage_cost + packaging_cost + sterilization_cost), GRB.MAXIMIZE)

    # Constraints

    # Production Capacity
    for t in time_periods:
        for l in production_lines:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= MaxCapacity[l] * (1 + S[l, t]), name=f"ProdCap_{l}_{t}")

    # Machine Availability
    for t in time_periods:
        for m in ['machine1', 'machine2']:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= M[m, t] * MaxCapacity_m[m] * (1 + S[l, t]), name=f"MachCap_{m}_{t}")

    # Batch Size
    for t in time_periods:
        for s in suture_types:
            model.addConstr(B[s, t] * BatchSize[s] == P_preparation[s, t], name=f"Batch_{s}_{t}")

    # Initial Inventory Balance for Finished Goods
    for s in suture_types:
        model.addConstr(I_finished[s, 1] == InitialInventory[s] + P_sterilization[s, 1] - D[s, 1], name=f"InvBal_{s}_1")

    # Inventory Balance for Finished Goods in subsequent periods
    for t in time_periods[1:]:
        for s in suture_types:
            model.addConstr(I_finished[s, t] == I_finished[s, t-1] + P_sterilization[s, t] - D[s, t], name=f"InvBal_{s}_{t}")

    # Raw Material Inventory Update
    for r in raw_material_types:
        model.addConstr(I_raw[r, 1] == InitialRawInventory[r] + Q_raw[r, 1] - gp.quicksum(P_preparation[s, 1] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_1")
        for t in time_periods[1:]:
            model.addConstr(I_raw[r, t] == I_raw[r, t-1] + Q_raw[r, t] - gp.quicksum(P_preparation[s, t] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_{t}")

    # Needle Inventory Update
    for n in needle_types:
        model.addConstr(I_needles[n, 1] == InitialNeedleInventory[n] + Q_needles[n, 1] - gp.quicksum(P_needle_attachment[s, 1] for s in suture_types), name=f"NeedleInv_{n}_1")
        for t in time_periods[1:]:
            model.addConstr(I_needles[n, t] == I_needles[n, t-1] + Q_needles[n, t] - gp.quicksum(P_needle_attachment[s, t] for s in suture_types), name=f"NeedleInv_{n}_{t}")

    # Non-negativity of Inventory
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] >= MinRawInventory[r], name=f"MinRawInv_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] >= MinNeedleInventory[n], name=f"MinNeedleInv_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] >= SafetyStock[s], name=f"MinFinInv_{s}_{t}")

    # Maximum inventory limits for raw materials, needles and finished goods
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] <= MaxRawInventory[r], name=f"MaxRawInventory_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] <= MaxNeedleInventory[n], name=f"MaxNeedleInventory_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] <= MaxFinishedInventory[s], name=f"MaxFinishedInventory_{s}_{t}")

    # Staffing Levels
    for t in time_periods:
        for l in production_lines:
            model.addConstr(E[l, t] >= gp.quicksum(P_preparation[s, t] for s in suture_types) / 800, name=f"Staff_{l}_{t}")
            model.addConstr(E[l, t] <= MaxEmployees[l] * (1 + S[l, t]), name=f"MaxEmployees_With_SecondShift_{l}_{t}")

    # Demand Fulfillment
    for t in time_periods:
        for s in suture_types:
            model.addConstr(D[s, t] <= Demand[s][t-1], name=f"Demand_{s}_{t}")

    # Packaging Line Capacity
    for t in time_periods:
        for p in packaging_lines:
            model.addConstr(gp.quicksum(P_packaging[s, t] for s in suture_types) <= K[p, t] * MaxPackagingCapacity[p] * (1 + S[l, t]), name=f"PackCap_{p}_{t}")

    # Binary Machine Operation
    for m in ['machine1', 'machine2']:
        for t in time_periods:
            model.addConstr(M[m, t] <= 1, name=f"BinaryMach_{m}_{t}")

    # Multi-stage Production Constraints
    for t in time_periods:
        for s in suture_types:
            # Preparation to Cutting
            model.addConstr(P_cutting[s, t] == P_preparation[s, t], name=f"Cutting_{s}_{t}")

            # Cutting to Needle Attachment
            model.addConstr(P_needle_attachment[s, t] == P_cutting[s, t], name=f"NeedleAttach_{s}_{t}")

            # Needle Attachment to Packaging
            model.addConstr(P_packaging[s, t] == P_needle_attachment[s, t], name=f"PackReq_{s}_{t}")

            # Packaging to Sterilization
            model.addConstr(P_sterilization[s, t] == P_packaging[s, t], name=f"Sterilization_{s}_{t}")

    # Solve the model
    model.Params.TimeLimit = time_limit  # Set a time limit for the solver
    # initial_feasibility_check(model)  # Initial Feasibility Check
    model.optimize()
    automated_validation(model, directory, param_set_index)  # Automated Validation


    # Check for infeasibility, unboundedness, or optimal solution
    if model.Status == GRB.INFEASIBLE:
        print(f"Model {param_set_index} is infeasible! Writing IIS to file.")
        model.computeIIS()
        model.write(f'{directory}/model_{param_set_index}_iis.ilp')
        raise ValueError(f"Model {param_set_index} is infeasible! Check the IIS file.")
    
    elif model.Status == GRB.UNBOUNDED:
        print(f"Model {param_set_index} is unbounded!")
        raise ValueError(f"Model {param_set_index} is unbounded!")

    elif model.Status != GRB.OPTIMAL:
        print(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")
        model.computeIIS()
        model.write(f'{directory}/model_{param_set_index}_iis.ilp')
        raise ValueError(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")


    results = {}
    if model.Status == GRB.OPTIMAL:
        results['objective_value'] = model.objVal
        results['Preparation'] = {s: [P_preparation[s, t].x for t in time_periods] for s in suture_types}
        results['Cutting'] = {s: [P_cutting[s, t].x for t in time_periods] for s in suture_types}
        results['NeedleAttachment'] = {s: [P_needle_attachment[s, t].x for t in time_periods] for s in suture_types}
        results['Packaging'] = {s: [P_packaging[s, t].x for t in time_periods] for s in suture_types}
        results['Sterilization'] = {s: [P_sterilization[s, t].x for t in time_periods] for s in suture_types}
        results['Shipping'] = {s: [D[s, t].x for t in time_periods] for s in suture_types}
        results['RawInventory'] = {r: [I_raw[r, t].x for t in time_periods] for r in raw_material_types}
        results['NeedleInventory'] = {n: [I_needles[n, t].x for t in time_periods] for n in needle_types}
        results['FinishedInventory'] = {s: [I_finished[s, t].x for t in time_periods] for s in suture_types}
        results['SecondShift'] = {l: [S[l, t].x for t in time_periods] for l in production_lines}

        for t in time_periods:
            second_shift_cost_t = gp.quicksum(1.1 * LaborCost[l] * E[l,t].x * S[l, t].x for l in production_lines).getValue()
            print(f"Second Shift Cost for month {t}: {second_shift_cost_t}")
            for l in production_lines:
                print(f"Second Shift (S) for production line {l} in month {t}: {S[l, t].x}")

        print(f"Objective Value with second shift: {results['objective_value']}")

    else:
        results['status'] = model.Status

    return results

#-----------------------------------------


def run_model_with_backorder_penalty(params, time_limit, directory, param_set_index):
    validate_parameters(params)

    # Define indices
    suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
    raw_material_types = ['propylen_raw', 'polyamid_raw', 'silk_raw', 'polyester_raw', 'profimed_raw', 'steel_raw', 'supramid_raw', 'pga_raw', 'pgla_raw', 'rapid_pgla_raw', 'monosorb_raw', 'monofast_raw']
    needle_types = ['straight', 'curve_3_8', 'curve_1_2']
    production_lines = ['line1', 'line2']
    packaging_lines = ['pack_line1', 'pack_line2']
    time_periods = list(range(1, 7))  # 6 months

    suture_to_raw_material = {s: s + '_raw' for s in suture_types}

    InitialInventory = params['InitialInventory']
    InitialRawInventory = params['InitialRawInventory']
    InitialNeedleInventory = params['InitialNeedleInventory']
    MaxCapacity = params['MaxCapacity']
    MaxCapacity_m = params['MaxCapacity_m']
    BatchSize = params['BatchSize']
    MaxEmployees = params['MaxEmployees']
    MaxPackagingCapacity = params['MaxPackagingCapacity']
    SafetyStock = params['SafetyStock']
    Demand = params['Demand']
    Price = params['Price']
    ProdCost = params['ProdCost']
    LaborCost = params['LaborCost']
    Cost_r = params['Cost_r']
    NeedleCost = params['NeedleCost']
    PackagingCost = params['PackagingCost']
    StorageCost = params['StorageCost']
    SterilizationCost = params['SterilizationCost']
    CuttingCost = params['CuttingCost']
    MaxRawInventory = params['MaxRawInventory']
    MaxNeedleInventory = params['MaxNeedleInventory']
    MinRawInventory = params['MinRawInventory']
    MinNeedleInventory = params['MinNeedleInventory']
    MaxFinishedInventory = params['MaxFinishedInventory']
    ShortageCost = 4  # Backorder cost per unit of unmet demand


    model = gp.Model("Multi_Period_Model_With_Backorder_Penalty")

    # Decision Variables
    I_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.CONTINUOUS, name="RawInventory", lb=0)
    I_needles = model.addVars(needle_types, time_periods, vtype=GRB.CONTINUOUS, name="NeedleInventory", lb=0)
    I_finished = model.addVars(suture_types, time_periods, vtype=GRB.CONTINUOUS, name="FinishedInventory", lb=0)
    Q_raw = model.addVars(raw_material_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityRaw", lb=0)
    Q_needles = model.addVars(needle_types, time_periods, vtype=GRB.INTEGER, name="OrderQuantityNeedles", lb=0)
    D = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Shipping", lb=0)
    Shortage = model.addVars(suture_types, time_periods, vtype=GRB.CONTINUOUS, name="Shortage", lb=0)  # variable for unmet demand

    P_preparation = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Preparation", lb=0)
    P_cutting = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Cutting", lb=0)
    P_needle_attachment = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="NeedleAttachment", lb=0)
    P_packaging = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Packaging", lb=0)
    P_sterilization = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Sterilization", lb=0)

    B = model.addVars(suture_types, time_periods, vtype=GRB.INTEGER, name="Batch", lb=0)
    M = model.addVars(['machine1', 'machine2'], time_periods, vtype=GRB.BINARY, name="MachineOp")
    E = model.addVars(production_lines, time_periods, vtype=GRB.INTEGER, name="Employees", lb=0, ub=MaxEmployees)
    K = model.addVars(packaging_lines, time_periods, vtype=GRB.BINARY, name="PackLinesOp")


    # Objective Function
    revenue = gp.quicksum(Price[s] * D[s, t] for s in suture_types for t in time_periods)
    production_cost = gp.quicksum(ProdCost[s] * P_preparation[s, t] for s in suture_types for t in time_periods)
    cutting_cost = gp.quicksum(CuttingCost * P_cutting[s, t] for s in suture_types for t in time_periods)
    raw_material_cost = gp.quicksum(Cost_r[r] * Q_raw[r, t] for r in raw_material_types for t in time_periods)
    needle_cost = gp.quicksum(NeedleCost[n] * Q_needles[n, t] for n in needle_types for t in time_periods)
    labor_cost = gp.quicksum(LaborCost[l] * E[l, t] for l in production_lines for t in time_periods)
    storage_cost = gp.quicksum(StorageCost * I_finished[s, t] for s in suture_types for t in time_periods) + gp.quicksum(StorageCost * I_raw[r, t] for r in raw_material_types for t in time_periods) + gp.quicksum(StorageCost * I_needles[n, t] for n in needle_types for t in time_periods)
    packaging_cost = gp.quicksum(PackagingCost[s] * P_packaging[s, t] for s in suture_types for t in time_periods)
    sterilization_cost = gp.quicksum(SterilizationCost['A'] * P_sterilization[s, t] for s in suture_types if s not in ['silk', 'polyester'] for t in time_periods) + gp.quicksum(SterilizationCost['B'] * P_sterilization[s, t] for s in ['silk', 'polyester'] for t in time_periods)
    shortage_penalty = gp.quicksum(ShortageCost * Shortage[s, t] for s in suture_types for t in time_periods)  # Shortage penalty

    model.setObjective(revenue - (production_cost + cutting_cost + raw_material_cost + needle_cost + labor_cost + storage_cost + packaging_cost + sterilization_cost + shortage_penalty), GRB.MAXIMIZE)


    # Constraints

    # Production Capacity
    for t in time_periods:
        for l in production_lines:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= MaxCapacity[l], name=f"ProdCap_{l}_{t}")

    # Machine Availability
    for t in time_periods:
        for m in ['machine1', 'machine2']:
            model.addConstr(gp.quicksum(P_preparation[s, t] for s in suture_types) <= M[m, t] * MaxCapacity_m[m], name=f"MachCap_{m}_{t}")

    # Batch Size
    for t in time_periods:
        for s in suture_types:
            model.addConstr(B[s, t] * BatchSize[s] == P_preparation[s, t], name=f"Batch_{s}_{t}")

    # Initial Inventory Balance for Finished Goods
    for s in suture_types:
        model.addConstr(I_finished[s, 1] == InitialInventory[s] + P_sterilization[s, 1] - D[s, 1], name=f"InvBal_{s}_1")

    # Inventory Balance for Finished Goods in subsequent periods
    for t in time_periods[1:]:
        for s in suture_types:
            model.addConstr(I_finished[s, t] == I_finished[s, t-1] + P_sterilization[s, t] - D[s, t], name=f"InvBal_{s}_{t}")

       # Raw Material Inventory Update
    for r in raw_material_types:
        model.addConstr(I_raw[r, 1] == InitialRawInventory[r] + Q_raw[r, 1] - gp.quicksum(P_preparation[s, 1] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_1")
        for t in time_periods[1:]:
            model.addConstr(I_raw[r, t] == I_raw[r, t-1] + Q_raw[r, t] - gp.quicksum(P_preparation[s, t] for s in suture_types if suture_to_raw_material[s] == r), name=f"RawInv_{r}_{t}")

    # Needle Inventory Update
    for n in needle_types:
        model.addConstr(I_needles[n, 1] == InitialNeedleInventory[n] + Q_needles[n, 1] - gp.quicksum(P_needle_attachment[s, 1] for s in suture_types), name=f"NeedleInv_{n}_1")
        for t in time_periods[1:]:
            model.addConstr(I_needles[n, t] == I_needles[n, t-1] + Q_needles[n, t] - gp.quicksum(P_needle_attachment[s, t] for s in suture_types), name=f"NeedleInv_{n}_{t}")

    # Non-negativity of Inventory
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] >= MinRawInventory[r], name=f"MinRawInv_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] >= MinNeedleInventory[n], name=f"MinNeedleInv_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] >= SafetyStock[s], name=f"MinFinInv_{s}_{t}")
    
    # Maximum inventory limits for raw materials, needles and finished goods
    for t in time_periods:
        for r in raw_material_types:
            model.addConstr(I_raw[r, t] <= MaxRawInventory[r], name=f"MaxRawInventory_{r}_{t}")
        for n in needle_types:
            model.addConstr(I_needles[n, t] <= MaxNeedleInventory[n], name=f"MaxNeedleInventory_{n}_{t}")
        for s in suture_types:
            model.addConstr(I_finished[s, t] <= MaxFinishedInventory[s], name=f"MaxFinishedInventory_{s}_{t}")

    # Staffing Levels
    for t in time_periods:
        for l in production_lines:
            model.addConstr(E[l, t] >= gp.quicksum(P_preparation[s, t] for s in suture_types) / 800, name=f"Staff_{l}_{t}")
            model.addConstr(E[l, t] <= MaxEmployees[l], name=f"MaxEmployees_{l}_{t}")

    # Demand Fulfillment with Shortage Option
    for t in time_periods:
        for s in suture_types:
            model.addConstr(D[s, t] <= Demand[s][t-1], name=f"Demand_{s}_{t}")
            model.addConstr(Shortage[s, t] == Demand[s][t-1] - D[s, t], name=f"Shortage_{s}_{t}") # Shortage is the unmet demand (Demand - D[s, t])
    
    # Packaging Line Capacity
    for t in time_periods:
        for p in packaging_lines:
            model.addConstr(gp.quicksum(P_packaging[s, t] for s in suture_types) <= K[p, t] * MaxPackagingCapacity[p], name=f"PackCap_{p}_{t}")

    # Binary Machine Operation
    for m in ['machine1', 'machine2']:
        for t in time_periods:
            model.addConstr(M[m, t] <= 1, name=f"BinaryMach_{m}_{t}")

    # Multi-stage Production Constraints
    for t in time_periods:
        for s in suture_types:
            # Preparation to Cutting
            model.addConstr(P_cutting[s, t] == P_preparation[s, t], name=f"Cutting_{s}_{t}")

            # Cutting to Needle Attachment
            model.addConstr(P_needle_attachment[s, t] == P_cutting[s, t], name=f"NeedleAttach_{s}_{t}")

            # Needle Attachment to Packaging
            model.addConstr(P_packaging[s, t] == P_needle_attachment[s, t], name=f"PackReq_{s}_{t}")

            # Packaging to Sterilization
            model.addConstr(P_sterilization[s, t] == P_packaging[s, t], name=f"Sterilization_{s}_{t}")



    # Solve the model
    model.Params.TimeLimit = time_limit  # Set a time limit for the solver
    # initial_feasibility_check(model)  # Initial Feasibility Check
    model.optimize()
    automated_validation(model, directory, param_set_index)  # Automated Validation


    # Check for infeasibility, unboundedness, or optimal solution
    if model.Status == GRB.INFEASIBLE:
        print(f"Model {param_set_index} is infeasible! Writing IIS to file.")
        model.computeIIS()
        model.write(f'{directory}/model_{param_set_index}_iis.ilp')
        raise ValueError(f"Model {param_set_index} is infeasible! Check the IIS file.")
    
    elif model.Status == GRB.UNBOUNDED:
        print(f"Model {param_set_index} is unbounded!")
        raise ValueError(f"Model {param_set_index} is unbounded!")

    elif model.Status != GRB.OPTIMAL:
        print(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")
        raise ValueError(f"Model {param_set_index} did not find an optimal solution. Status code: {model.Status}")


    results = {}
    if model.Status == GRB.OPTIMAL:
        results['objective_value'] = model.objVal
        results['Preparation'] = {s: [P_preparation[s, t].x for t in time_periods] for s in suture_types}
        results['Cutting'] = {s: [P_cutting[s, t].x for t in time_periods] for s in suture_types}
        results['NeedleAttachment'] = {s: [P_needle_attachment[s, t].x for t in time_periods] for s in suture_types}
        results['Packaging'] = {s: [P_packaging[s, t].x for t in time_periods] for s in suture_types}
        results['Sterilization'] = {s: [P_sterilization[s, t].x for t in time_periods] for s in suture_types}
        results['Shipping'] = {s: [D[s, t].x for t in time_periods] for s in suture_types}
        results['Shortage'] = {s: [Shortage[s, t].x for t in time_periods] for s in suture_types}  # Track shortage
    
        for t in time_periods:
            shortage_penalty_t = gp.quicksum(ShortageCost * Shortage[s, t].x for s in suture_types).getValue()
            print(f"Shortage Penalty for month {t}: {shortage_penalty_t}")
            for s in suture_types:
                print(f"Shortage for suture type {s} in month {t}: {Shortage[s, t].x}")
    
    else:
        results['status'] = model.Status

    print(f"Objective Value with backorder penalty: {results['objective_value']}")

    return results

