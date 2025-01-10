Combination 1:

Scenario: Baseline/Average Demand (Parameter Sets 1 and 2)

Models to Run:
- Basic Multi-Period Model
- Multi-Period with Second Shift
- Multi-Period with Backorder Penalty

Why:
These baseline parameter sets represent average scenarios, with no extreme fluctuations in demand or cost. Running all three models in these conditions allows us to establish a "normal" baseline for:
- Objective value (profit)
- Second shift usage (when allowed)
- Shortage penalty (if shortages are present)
- Production and shipping of silk and other products.

What We Will Extract:
- A comparison of performance in average demand situations for all three models, focusing on second shift activation and shortage penalties where applicable.
- Establish which model handles average demand the most effectively, considering profit and fulfillment levels.


Combination 2:

Scenario: High Demand for Silk and Profimed (Parameter Set 3 - Increased Demand for Two Products)

Models to Run:
- Basic Multi-Period Model
- Multi-Period with Second Shift
- Multi-Period with Backorder Penalty

Why:
Parameter Set 3 introduces a spike in demand for two key products (Silk and Profimed), which tests the models under stress. Comparing how the models react to high-demand peaks is crucial to understanding:
- How the basic model without second shifts or backorder penalties handles the load.
- The extent to which the second shift model can absorb the increased demand.
- How the backorder penalty model manages unmet demand when production is insufficient.

What We Will Extract:
- How well each model handles the spike in demand.
- Whether activating a second shift reduces production shortages.
- The trade-off between fulfilling demand versus incurring backorder penalties.
- Insights into shipping performance during high-demand months.


Combination 3:

Scenario: Raw Material Shortage (Parameter Set 4)

Models to Run:
- Basic Multi-Period Model
- Multi-Period with Backorder Penalty

Why:
This scenario examines the impact of raw material shortages on production. We exclude the second shift model here since the focus is on managing raw material availability and backorders.

What We Will Extract:
- A comparison of how the models react to raw material shortages.
- Whether the backorder penalty model mitigates the damage caused by raw material shortages or incurs more penalties.
- Production and shipping disruptions due to the unavailability of raw materials.


Combination 4:

Scenario: High Demand for Silk and Profimed but Increased Labor Costs (Parameter Set 5)

Models to Run:
- Basic Multi-Period Model
- Multi-Period with Second Shift

Why:
With increased labor costs, the second shift becomes more expensive. Running both the basic and second shift models shows how costlier labor impacts production decisions and second shift activation.

What We Will Extract:
- Whether the second shift remains viable when labor costs rise.
- Comparison of objective values (profit) between the two models, and whether second shift usage becomes minimal due to high labor costs.


Combination 5:

Scenario: Increased Raw Material Costs (Parameter Set 6)

Models to Run:
- Basic Multi-Period Model
- Multi-Period with Backorder Penalty

Why:
Increased raw material costs test the models' efficiency under higher production expenses. The focus here is on how the models react to increased costs while balancing production and backorder penalties.

What We Will Extract:
- Profit comparison between models under higher production costs.
- Whether the backorder penalty model sacrifices production to reduce raw material purchases.
- How shipping and production levels change under higher input costs.


Summary of Combinations:

1. Baseline/Average Demand (Parameter Sets 1 and 2): All three models.
   - Comparison of general performance across average demand conditions.

2. High Demand for Silk and Profimed (Parameter Set 3): All three models.
   - Stress test to see how models handle surges in demand.

3. Raw Material Shortage (Parameter Set 4): Basic model and backorder penalty model.
   - Focus on managing raw material shortages and the trade-offs of backordering.

4. Increased Labor Costs (Parameter Set 5): Basic model and second shift model.
   - Evaluate the impact of higher labor costs on second shift usage and overall profitability.

5. Increased Raw Material Costs (Parameter Set 6): Basic model and backorder penalty model.
   - Analyze the effect of higher raw material costs on production and profitability.