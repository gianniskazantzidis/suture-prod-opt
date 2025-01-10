### Experiment Combinations

#### **Combination 1: Baseline/Average Demand (Parameter Sets 1 and 2)**

**Models to Run:**
- Basic Multi-Period Model
- Multi-Period with Second Shift
- Multi-Period with Backorder Penalty

**Why:**
The baseline parameter sets represent average conditions, without extreme fluctuations in demand or cost. Running all three models under these conditions establishes a "normal" baseline for:
- Objective value (profit)
- Second shift usage (when allowed)
- Shortage penalties (if applicable)
- Production and shipping volumes for silk and other products.

**What We Will Extract:**
- Performance comparisons under average demand conditions for all three models.
- Insights into second shift activation and shortage penalties.
- Identification of the most effective model for managing average demand in terms of profit and fulfillment levels.

---

#### **Combination 2: High Demand for Silk and Profimed (Parameter Set 3)**

**Models to Run:**
- Basic Multi-Period Model
- Multi-Period with Second Shift
- Multi-Period with Backorder Penalty

**Why:**
Parameter Set 3 introduces a significant spike in demand for two key products (Silk and Profimed), providing a stress test for the models. This scenario helps evaluate:
- The basic model's ability to handle high-demand peaks without second shifts or backorder penalties.
- The second shift model's capacity to absorb increased demand.
- The backorder penalty model's strategy for managing unmet demand.

**What We Will Extract:**
- Performance of each model under high-demand scenarios.
- Effectiveness of second shift activation in reducing production shortages.
- Trade-offs between fulfilling demand and incurring backorder penalties.
- Shipping performance during peak demand periods.

---

#### **Combination 3: Raw Material Shortage (Parameter Set 4)**

**Models to Run:**
- Basic Multi-Period Model
- Multi-Period with Backorder Penalty

**Why:**
This scenario focuses on the impact of raw material shortages on production. The second shift model is excluded to prioritize managing raw material constraints and backorder penalties.

**What We Will Extract:**
- Model performance in response to raw material shortages.
- Effectiveness of the backorder penalty model in mitigating disruptions versus penalty costs.
- Analysis of production and shipping disruptions caused by material unavailability.

---

#### **Combination 4: High Demand for Silk and Profimed with Increased Labor Costs (Parameter Set 5)**

**Models to Run:**
- Basic Multi-Period Model
- Multi-Period with Second Shift

**Why:**
Increased labor costs make the second shift more expensive, providing an opportunity to examine its viability under these conditions. Comparing both models reveals how costlier labor affects production and second shift decisions.

**What We Will Extract:**
- Second shift viability under higher labor costs.
- Profit comparison between the two models.
- Analysis of second shift usage and its impact on overall profitability.

---

#### **Combination 5: Increased Raw Material Costs (Parameter Set 6)**

**Models to Run:**
- Basic Multi-Period Model
- Multi-Period with Backorder Penalty

**Why:**
Increased raw material costs challenge the models to optimize efficiency under higher production expenses. This scenario focuses on balancing production costs and backorder penalties.

**What We Will Extract:**
- Profitability comparisons under higher raw material costs.
- Strategies employed by the backorder penalty model to reduce material expenses.
- Changes in production and shipping levels due to increased input costs.

---

### **Summary of Combinations**

1. **Baseline/Average Demand (Parameter Sets 1 and 2):** All three models.
   - Establishes a performance baseline under average demand conditions.

2. **High Demand for Silk and Profimed (Parameter Set 3):** All three models.
   - Stress test for handling demand surges.

3. **Raw Material Shortage (Parameter Set 4):** Basic model and backorder penalty model.
   - Focuses on managing material shortages and backordering.

4. **Increased Labor Costs (Parameter Set 5):** Basic model and second shift model.
   - Evaluates the impact of higher labor costs on second shift usage and profitability.

5. **Increased Raw Material Costs (Parameter Set 6):** Basic model and backorder penalty model.
   - Analyzes the effect of increased material costs on production and profitability.
