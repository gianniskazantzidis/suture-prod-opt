
suture_types = ['propylen', 'polyamid', 'silk', 'polyester', 'profimed', 'steel', 'supramid', 'pga', 'pgla', 'rapid_pgla', 'monosorb', 'monofast']
raw_material_types = ['propylen_raw', 'polyamid_raw', 'silk_raw', 'polyester_raw', 'profimed_raw', 'steel_raw', 'supramid_raw', 'pga_raw', 'pgla_raw', 'rapid_pgla_raw', 'monosorb_raw', 'monofast_raw']
needle_types = ['straight', 'curve_3_8', 'curve_1_2']
sterilization_methods = ['A', 'B']

#-----------------------------------------

# Parameter set 1

Demand_1 = {
        'propylen': [860, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000],
        'polyamid': [940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740, 720],
        'silk': [620, 620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720],
        'polyester': [820, 840, 840, 860, 860, 880, 880, 900, 900, 920, 920, 940],
        'profimed': [900, 920, 920, 940, 940, 960, 960, 980, 980, 1000, 1000, 1020],
        'steel': [360, 360, 380, 380, 400, 400, 420, 420, 440, 440, 460, 460],
        'supramid': [540, 540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640],
        'pga': [620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740],
        'pgla': [740, 760, 760, 780, 780, 800, 800, 820, 820, 840, 840, 860],
        'rapid_pgla': [580, 600, 600, 620, 620, 640, 640, 660, 660, 680, 680, 700],
        'monosorb': [200, 220, 220, 240, 240, 260, 260, 280, 280, 300, 300, 320],
        'monofast': [540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660]
}

parameter_set_1 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 9000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 60.0 for s in suture_types},
    'Demand': Demand_1,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': {'line1': 20, 'line2': 20},
    'Cost_r': {'propylen_raw': 0.30, 'polyamid_raw': 0.35, 'silk_raw': 0.40, 'polyester_raw': 0.45, 'profimed_raw': 0.50, 'steel_raw': 0.55, 'supramid_raw': 0.60, 'pga_raw': 0.32, 'pgla_raw': 0.38, 'rapid_pgla_raw': 0.42, 'monosorb_raw': 0.47, 'monofast_raw': 0.52},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}
}

#-----------------------------------------

# Parameter Set 2

Demand_2 = {
        'propylen': [880, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000, 1020],
        'polyamid': [960, 940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740],
        'silk': [640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740, 740],
        'polyester': [840, 860, 860, 880, 880, 900, 900, 920, 920, 940, 940, 960],
        'profimed': [920, 940, 940, 960, 960, 980, 980, 1000, 1000, 1020, 1020, 1040],
        'steel': [380, 380, 400, 400, 420, 420, 440, 440, 460, 460, 480, 480],
        'supramid': [560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660, 660],
        'pga': [640, 660, 660, 680, 680, 700, 700, 720, 720, 740, 740, 760],
        'pgla': [760, 780, 780, 800, 800, 820, 820, 840, 840, 860, 860, 880],
        'rapid_pgla': [600, 620, 620, 640, 640, 660, 660, 680, 680, 700, 700, 720],
        'monosorb': [220, 240, 240, 260, 260, 280, 280, 300, 300, 320, 320, 340],
        'monofast': [560, 580, 580, 600, 600, 620, 620, 640, 640, 660, 660, 680]
}

parameter_set_2 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 9000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 65.0 for s in suture_types},
    'Demand': Demand_2,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': {'line1': 20, 'line2': 20},
    'Cost_r': {'propylen_raw': 0.30, 'polyamid_raw': 0.35, 'silk_raw': 0.40, 'polyester_raw': 0.45, 'profimed_raw': 0.50, 'steel_raw': 0.55, 'supramid_raw': 0.60, 'pga_raw': 0.32, 'pgla_raw': 0.38, 'rapid_pgla_raw': 0.42, 'monosorb_raw': 0.47, 'monofast_raw': 0.52},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}
}

#-----------------------------------------

# Parameter set 3 - Scenario 1: Increased Demand for Two Products, Silk and Profimed

Demand_3 = {
    'propylen': [860, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000],
    'polyamid': [940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740, 720],
    'silk': [620, 3080, 3980, 3350, 660, 660, 680, 680, 700, 700, 720, 720],
    'polyester': [820, 840, 840, 860, 860, 880, 880, 900, 900, 920, 920, 940],
    'profimed': [900, 3370, 3410, 3240, 940, 960, 960, 980, 980, 1000, 1000, 1020],
    'steel': [360, 360, 380, 380, 400, 400, 420, 420, 440, 440, 460, 460],
    'supramid': [540, 540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640],
    'pga': [620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740],
    'pgla': [740, 760, 760, 780, 780, 800, 800, 820, 820, 840, 840, 860],
    'rapid_pgla': [580, 600, 600, 620, 620, 640, 640, 660, 660, 680, 680, 700],
    'monosorb': [200, 220, 220, 240, 240, 260, 260, 280, 280, 300, 300, 320],
    'monofast': [540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660]
}

parameter_set_3 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 9000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 60.0 for s in suture_types},
    'Demand': Demand_3,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': {'line1': 20, 'line2': 20},
    'Cost_r': {'propylen_raw': 0.30, 'polyamid_raw': 0.35, 'silk_raw': 0.40, 'polyester_raw': 0.45, 'profimed_raw': 0.50, 'steel_raw': 0.55, 'supramid_raw': 0.60, 'pga_raw': 0.32, 'pgla_raw': 0.38, 'rapid_pgla_raw': 0.42, 'monosorb_raw': 0.47, 'monofast_raw': 0.52},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}    
}

#-----------------------------------------

# Parameter set 4 - Scenario 2: Machine Breakdown 

Demand_4 = {
        'propylen': [860, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000],
        'polyamid': [940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740, 720],
        'silk': [620, 620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720],
        'polyester': [820, 840, 840, 860, 860, 880, 880, 900, 900, 920, 920, 940],
        'profimed': [900, 920, 920, 940, 940, 960, 960, 980, 980, 1000, 1000, 1020],
        'steel': [360, 360, 380, 380, 400, 400, 420, 420, 440, 440, 460, 460],
        'supramid': [540, 540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640],
        'pga': [620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740],
        'pgla': [740, 760, 760, 780, 780, 800, 800, 820, 820, 840, 840, 860],
        'rapid_pgla': [580, 600, 600, 620, 620, 640, 640, 660, 660, 680, 680, 700],
        'monosorb': [200, 220, 220, 240, 240, 260, 260, 280, 280, 300, 300, 320],
        'monofast': [540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660]
}

parameter_set_4 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 3000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 60.0 for s in suture_types},
    'Demand': Demand_4,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': {'line1': 20, 'line2': 20},
    'Cost_r': {'propylen_raw': 0.30, 'polyamid_raw': 0.35, 'silk_raw': 0.40, 'polyester_raw': 0.45, 'profimed_raw': 0.50, 'steel_raw': 0.55, 'supramid_raw': 0.60, 'pga_raw': 0.32, 'pgla_raw': 0.38, 'rapid_pgla_raw': 0.42, 'monosorb_raw': 0.47, 'monofast_raw': 0.52},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}
}

#-----------------------------------------

# Parameter set 5 - Scenario 3: High Demand for Silk and Profimed but Increased Labor Cost

Demand_5 = {
        'propylen': [860, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000],
        'polyamid': [940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740, 720],
        'silk': [620, 3080, 3980, 3350, 660, 660, 680, 680, 700, 700, 720, 720],
        'polyester': [820, 840, 840, 860, 860, 880, 880, 900, 900, 920, 920, 940],
        'profimed': [900, 3370, 3410, 3240, 940, 960, 960, 980, 980, 1000, 1000, 1020],
        'steel': [360, 360, 380, 380, 400, 400, 420, 420, 440, 440, 460, 460],
        'supramid': [540, 540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640],
        'pga': [620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740],
        'pgla': [740, 760, 760, 780, 780, 800, 800, 820, 820, 840, 840, 860],
        'rapid_pgla': [580, 600, 600, 620, 620, 640, 640, 660, 660, 680, 680, 700],
        'monosorb': [200, 220, 220, 240, 240, 260, 260, 280, 280, 300, 300, 320],
        'monofast': [540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660]
}

LaborCost_increased = {'line1': 40, 'line2': 40}

parameter_set_5 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 9000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 60.0 for s in suture_types},
    'Demand': Demand_5,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': LaborCost_increased,
    'Cost_r': {'propylen_raw': 0.30, 'polyamid_raw': 0.35, 'silk_raw': 0.40, 'polyester_raw': 0.45, 'profimed_raw': 0.50, 'steel_raw': 0.55, 'supramid_raw': 0.60, 'pga_raw': 0.32, 'pgla_raw': 0.38, 'rapid_pgla_raw': 0.42, 'monosorb_raw': 0.47, 'monofast_raw': 0.52},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}
}

#-----------------------------------------

# Parameter set 6 - Scenario 4: Increased Raw Material Cost

Demand_6 = {
        'propylen': [860, 800, 820, 840, 860, 880, 900, 920, 940, 960, 980, 1000],
        'polyamid': [940, 920, 900, 880, 860, 840, 820, 800, 780, 760, 740, 720],
        'silk': [620, 620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720],
        'polyester': [820, 840, 840, 860, 860, 880, 880, 900, 900, 920, 920, 940],
        'profimed': [900, 920, 920, 940, 940, 960, 960, 980, 980, 1000, 1000, 1020],
        'steel': [360, 360, 380, 380, 400, 400, 420, 420, 440, 440, 460, 460],
        'supramid': [540, 540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640],
        'pga': [620, 640, 640, 660, 660, 680, 680, 700, 700, 720, 720, 740],
        'pgla': [740, 760, 760, 780, 780, 800, 800, 820, 820, 840, 840, 860],
        'rapid_pgla': [580, 600, 600, 620, 620, 640, 640, 660, 660, 680, 680, 700],
        'monosorb': [200, 220, 220, 240, 240, 260, 260, 280, 280, 300, 300, 320],
        'monofast': [540, 560, 560, 580, 580, 600, 600, 620, 620, 640, 640, 660]
}

parameter_set_6 = {
    'InitialInventory': {'propylen': 50, 'polyamid': 60, 'silk': 40, 'polyester': 50, 'profimed': 55, 'steel': 25, 'supramid': 60, 'pga': 30, 'pgla': 35, 'rapid_pgla': 27, 'monosorb': 20, 'monofast': 35},
    'InitialRawInventory': {'propylen_raw': 500, 'polyamid_raw': 600, 'silk_raw': 400, 'polyester_raw': 500, 'profimed_raw': 550, 'steel_raw': 250, 'supramid_raw': 600, 'pga_raw': 300, 'pgla_raw': 350, 'rapid_pgla_raw': 270, 'monosorb_raw': 200, 'monofast_raw': 350},
    'InitialNeedleInventory': {'straight': 500, 'curve_3_8': 600, 'curve_1_2': 700},
    'MaxCapacity': {'line1': 14000, 'line2': 14000},
    'MaxCapacity_m': {'machine1': 9000, 'machine2': 9000},
    'BatchSize': {'propylen': 100, 'polyamid': 120, 'silk': 110, 'polyester': 130, 'profimed': 140, 'steel': 150, 'supramid': 160, 'pga': 90, 'pgla': 95, 'rapid_pgla': 85, 'monosorb': 80, 'monofast': 75},
    'MaxEmployees': {'line1': 15, 'line2': 15},
    'MaxPackagingCapacity': {'pack_line1': 9000, 'pack_line2': 9000},
    'SafetyStock': {s: 60.0 for s in suture_types},
    'Demand': Demand_6,
    'Price': {'propylen': 5, 'polyamid': 5.5, 'silk': 6, 'polyester': 6.5, 'profimed': 9, 'steel': 7.5, 'supramid': 8, 'pga': 5.2, 'pgla': 6.7, 'rapid_pgla': 6.2, 'monosorb': 6.7, 'monofast': 7.2},
    'ProdCost': {'propylen': 0.70, 'polyamid': 0.85, 'silk': 0.90, 'polyester': 1.00, 'profimed': 1.30, 'steel': 1.30, 'supramid': 1.10, 'pga': 0.75, 'pgla': 0.85, 'rapid_pgla': 0.95, 'monosorb': 1.00, 'monofast': 1.05},
    'LaborCost': {'line1': 20, 'line2': 20},
    'Cost_r': {'propylen_raw': 0.60, 'polyamid_raw': 0.70, 'silk_raw': 0.80, 'polyester_raw': 0.90, 'profimed_raw': 1.00, 'steel_raw': 1.10, 'supramid_raw': 1.20, 'pga_raw': 0.64, 'pgla_raw': 0.76, 'rapid_pgla_raw': 0.84, 'monosorb_raw': 0.94, 'monofast_raw': 1.04},
    'NeedleCost': {n: 0.10 for n in needle_types},
    'PackagingCost': {'propylen': 0.40, 'polyamid': 0.45, 'silk': 0.50, 'polyester': 0.55, 'profimed': 0.60, 'steel': 0.65, 'supramid': 0.70, 'pga': 0.42, 'pgla': 0.47, 'rapid_pgla': 0.52, 'monosorb': 0.57, 'monofast': 0.62},
    'StorageCost': 0.10,
    'SterilizationCost': {'A': 0.15, 'B': 0.25},
    'CuttingCost': 0.05,
    'MaxRawInventory': {r: 3000 for r in raw_material_types},
    'MaxNeedleInventory': {n: 10000 for n in needle_types},
    'MinRawInventory': {r: 50 for r in raw_material_types},
    'MinNeedleInventory': {n: 200 for n in needle_types},
    'MaxFinishedInventory': {s: 3000 for s in suture_types},
    'ShortageCost': {4}
}


#-----------------------------------------


param_sets = [parameter_set_1, parameter_set_2, parameter_set_3, parameter_set_4, parameter_set_5, parameter_set_6]
