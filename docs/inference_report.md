# Hospitality Analytics – Business Inference Report

## 1. Introduction

This report analyses the performance of 10 hotels across five Indian cities over the period 2022–2026.

The analysis focuses on five key performance indicators (KPIs):

- Occupancy Rate
- Average Daily Rate (ADR)
- Revenue Per Available Room (RevPAR)
- Guest Satisfaction Score
- Employee Turnover Rate

The data was synthetically generated using Python and Faker, stored in MySQL, and analysed through SQL aggregate tables and a Streamlit dashboard.

## 2. Hotel Performance Analysis

### Occupancy Rate

Occupancy remained relatively stable throughout the five-year period, ranging from 56.38% to 56.45%.

This indicates consistent room utilisation across the simulated hotel portfolio.

Possible business factors influencing occupancy include seasonal tourism, public holidays, local festivals, business travel and conferences.

### Average Daily Rate (ADR)

ADR increased slightly from ₹4,701.81 in 2022 to ₹4,714.14 in 2026.

This suggests a small increase in average room pricing over the simulated period.

Possible influencing factors include peak-season pricing, room demand, hotel category and pricing strategies.

### Revenue Per Available Room (RevPAR)

RevPAR increased from ₹2,653.35 in 2022 to ₹2,660.77 in 2026.

The gradual increase is consistent with the slight improvement in ADR while occupancy remained stable.

This indicates that room revenue per available room improved marginally over the five years.

## 3. Guest Satisfaction Analysis

Guest satisfaction remained positive throughout the analysis period.

- 2022: 4.04
- 2023: 4.07
- 2024: 4.01
- 2025: 4.01
- 2026: 4.04

The highest satisfaction score was recorded in 2023.

The slight decline during 2024 and 2025 could potentially be associated with increased guest volumes, service delays, staffing availability or operational challenges.

The recovery in 2026 suggests an improvement in the simulated guest experience.

Hotels should continue monitoring service quality, staff responsiveness, room cleanliness and guest feedback.

## 4. Employee Turnover Analysis

Employee turnover showed variation over the five-year period.

- 2022: 6.20%
- 2023: 5.34%
- 2024: 5.14%
- 2025: 5.85%
- 2026: 9.28%

Turnover decreased between 2022 and 2024, followed by an increase in 2025 and 2026.

The highest turnover rate occurred in 2026, at 9.28%, with 23 employee exits.

Possible contributing factors include seasonal employment patterns, increased workload during peak periods, employee dissatisfaction and staffing changes.

Hotels should monitor employee retention, workload distribution, training and workplace satisfaction.

**Important limitation:** All employees in the generated dataset have joining dates within 2022–2026. There is no opening employee workforce carried forward from before 2022. Therefore, turnover figures represent the simulated employment history and should not be treated as actual industry benchmarks.

## 5. Seasonal Variation and Business Interpretation

The synthetic dataset incorporates qualitative seasonal assumptions based on the supplied project guidance.

The assumptions include:

- Occupancy may increase during holidays, festivals, tourist seasons and major local events.
- ADR may increase during periods of high demand and decrease during off-peak periods.
- RevPAR may improve when higher room rates and occupancy occur together.
- Guest satisfaction may decrease during peak periods due to crowding, waiting times or increased service pressure.
- Employee turnover may increase during periods of seasonal employment demand or workload pressure.

These are the intended business scenarios used in synthetic data generation.

The annual summaries in this report do not independently establish monthly seasonal patterns. Monthly aggregate data should be examined to identify and validate those patterns.

## 6. Key Business Recommendations

1. **Improve occupancy:** Use targeted promotions and packages during periods of lower demand.

2. **Optimise room pricing:** Adjust room rates according to seasonal demand while maintaining competitive pricing.

3. **Improve revenue performance:** Monitor ADR and RevPAR together to understand the relationship between pricing and room utilisation.

4. **Maintain guest satisfaction:** Monitor guest feedback and improve service quality, especially during peak periods.

5. **Reduce employee turnover:** Strengthen employee engagement, training, workload management and retention practices.

6. **Monitor hotel-level performance:** Compare hotels individually to identify locations that require operational improvements.

## 7. Data Limitations and Assumptions

- The dataset is synthetically generated and does not represent actual hotel operations.
- The analysis covers 10 hotels across five Indian cities.
- The five-year period is 2022–2026.
- The complete year 2026 is simulated, including dates after the actual data-generation date.
- Seasonal patterns are based on qualitative project guidance rather than additional numerical trend files.
- Employee joining and exit events are simulated.
- Employee turnover calculations are affected by the absence of an opening workforce before 2022.
- Annual aggregates may hide variations occurring at the monthly or hotel level.

These limitations should be considered when interpreting the results.

## 8. Conclusion

The analysis demonstrates how dimensional modelling, SQL aggregation and Python-based dashboards can be used to monitor hotel business performance.

Occupancy, ADR and RevPAR remained relatively stable, while guest satisfaction showed minor fluctuations. Employee turnover increased noticeably in 2026 and may require further investigation.

The project provides a structured approach to analysing hospitality KPIs and identifying areas for operational improvement.

The Streamlit dashboard enables users to explore performance through interactive city, hotel, year and month filters.
