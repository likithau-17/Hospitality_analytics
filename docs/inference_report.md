# Hospitality Analytics – Business Inference Report

## 1. Introduction

This report analyses the performance of 10 hotels across five Indian cities over a five-year period (2022–2026).

The analysis focuses on five key performance indicators (KPIs):

- Occupancy Rate
- Average Daily Rate (ADR)
- Revenue Per Available Room (RevPAR)
- Guest Satisfaction Score
- Employee Turnover Rate

The dataset was synthetically generated using Python, Pandas and Faker, stored in a MySQL database, and analysed using SQL aggregate tables. An interactive Streamlit dashboard was developed to present the results and allow users to explore hotel performance.

The objective of this analysis is to understand hotel performance trends, identify seasonal variations and derive business insights from the generated dataset.

## 2. Hotel Performance Analysis

### 2.1 Occupancy Rate

Occupancy rate measures the utilisation of available room capacity.

The annual occupancy rates remained relatively stable throughout the five-year period:

| Year | Occupancy Rate |
|---|---:|
| 2022 | 56.43% |
| 2023 | 56.45% |
| 2024 | 56.38% |
| 2025 | 56.42% |
| 2026 | 56.44% |

The occupancy rate remained close to 56% across all five years, indicating consistent room utilisation across the simulated hotel portfolio.

Although the annual figures show limited variation, monthly performance reveals more noticeable seasonal differences.

Tourism demand, holidays, local festivals and business travel are potential factors influencing occupancy across different locations and periods.

### 2.2 Average Daily Rate (ADR)

ADR measures the average room revenue earned per occupied room night.

| Year | ADR |
|---|---:|
| 2022 | ₹4,701.81 |
| 2023 | ₹4,704.08 |
| 2024 | ₹4,712.96 |
| 2025 | ₹4,705.41 |
| 2026 | ₹4,714.14 |

ADR increased slightly from ₹4,701.81 in 2022 to ₹4,714.14 in 2026.

This indicates relatively stable room pricing across the simulated period, with minor annual fluctuations.

Monthly variations are more noticeable because room prices were adjusted according to simulated seasonal demand. Peak-demand periods were assigned higher room prices, while lower-demand periods included discounted pricing.

### 2.3 Revenue Per Available Room (RevPAR)

RevPAR measures the room revenue generated per available room night.

| Year | RevPAR |
|---|---:|
| 2022 | ₹2,653.35 |
| 2023 | ₹2,655.51 |
| 2024 | ₹2,657.35 |
| 2025 | ₹2,654.96 |
| 2026 | ₹2,660.77 |

RevPAR increased slightly from ₹2,653.35 in 2022 to ₹2,660.77 in 2026.

The gradual improvement is consistent with relatively stable occupancy and a small increase in ADR.

This indicates that the simulated hotel portfolio maintained consistent room revenue performance over the five-year period.

## 3. Guest Satisfaction Analysis

Guest satisfaction measures the average rating provided by guests through feedback records, using a scale of 1 to 5.

| Year | Average Satisfaction Score |
|---|---:|
| 2022 | 4.04 |
| 2023 | 4.07 |
| 2024 | 4.01 |
| 2025 | 4.01 |
| 2026 | 4.04 |

Guest satisfaction remained positive throughout the analysis period.

The highest annual satisfaction score was recorded in 2023 at 4.07. A slight decline occurred during 2024 and 2025, followed by a recovery to 4.04 in 2026.

Possible operational factors influencing guest satisfaction include service quality, staff availability, room cleanliness, waiting times and overall guest experience.

The synthetic data also incorporates small rating reductions during selected peak-demand months to represent potential service pressure.

Hotels should continue monitoring guest feedback and maintaining service quality, particularly during periods of higher occupancy.

## 4. Employee Turnover Analysis

Employee turnover measures employee exits relative to the average employee count.

| Year | Employee Exits | Turnover Rate |
|---|---:|---:|
| 2022 | 2 | 6.20% |
| 2023 | 5 | 5.34% |
| 2024 | 8 | 5.14% |
| 2025 | 12 | 5.85% |
| 2026 | 23 | 9.28% |

Employee turnover decreased between 2022 and 2024, followed by an increase in 2025 and 2026.

The highest turnover rate occurred in 2026 at 9.28%, with 23 employee exits.

This increase indicates a potential employee retention concern within the simulated workforce.

Possible business factors influencing employee turnover in the hospitality industry include workload, employee satisfaction, seasonal employment requirements, workplace conditions and career development opportunities.

Hotels should monitor employee retention, workload distribution, training and employee engagement.

**Important limitation:**

All employees in the generated dataset have joining dates within 2022–2026. There is no opening employee workforce carried forward from before 2022.

Therefore, the calculated turnover figures represent the simulated employment history and should not be interpreted as actual industry benchmarks.

Additionally, employee exits were not explicitly weighted according to seasonal demand. Consequently, seasonal employee turnover patterns cannot be established from this dataset.

## 5. Seasonal Variation Analysis

Seasonal variations were incorporated into the synthetic dataset based on the qualitative guidance provided in the project requirements.

The five-year monthly aggregate data was grouped into four seasons:

- Winter: December, January and February
- Summer: March, April, May and June
- Monsoon: July, August and September
- Post-Monsoon: October and November

The following results were obtained from the MySQL aggregate tables.

### 5.1 Seasonal Performance Summary

| Season | Occupancy Rate | ADR (₹) | RevPAR (₹) | Guest Satisfaction |
|---|---:|---:|---:|---:|
| Winter | 60.29% | 5,028.65 | 3,031.60 | 4.00 |
| Summer | 56.33% | 5,029.04 | 2,832.71 | 3.93 |
| Monsoon | 51.62% | 3,927.83 | 2,027.69 | 4.14 |
| Post-Monsoon | 58.16% | 4,636.67 | 2,696.76 | 4.13 |

These results represent pooled performance across all 10 hotels and the five-year period, rather than individual hotel or year-level results.

### 5.2 Seasonal Business Interpretations

**Winter**

Winter recorded the highest occupancy rate at 60.29% and the highest RevPAR at ₹3,031.60.

ADR was also relatively high at ₹5,028.65.

This reflects the simulated higher tourism demand assumptions for destinations such as Goa and Jaipur during their peak travel months.

The combination of higher occupancy and room pricing contributed to stronger revenue per available room.

**Summer**

Summer recorded the highest ADR at ₹5,029.04, closely followed by Winter at ₹5,028.65.

However, occupancy was lower than Winter at 56.33%, resulting in a RevPAR of ₹2,832.71.

Guest satisfaction was the lowest among the four seasons at 3.93.

This is consistent with the synthetic modelling assumption that higher room pricing and peak-season service pressure may influence the guest experience.

**Monsoon**

Monsoon recorded the lowest occupancy rate at 51.62%, the lowest ADR at ₹3,927.83 and the lowest RevPAR at ₹2,027.69.

These results reflect the simulated lower-demand and discounted-pricing assumptions during the monsoon months.

Guest satisfaction was comparatively high at 4.14, the highest among the four seasons.

This may be consistent with the assumption that lower guest volumes can reduce crowding and waiting times.

**Post-Monsoon**

Post-Monsoon recorded an occupancy rate of 58.16% and a RevPAR of ₹2,696.76.

This indicates a recovery in occupancy and room revenue compared with the Monsoon period.

Guest satisfaction remained relatively high at 4.13.

The results demonstrate how seasonal demand and pricing assumptions can influence hotel performance.

### 5.3 Overall Seasonal Findings

The seasonal analysis highlights the following observations:

1. Winter generated the highest occupancy and RevPAR.
2. Summer recorded the highest ADR, reflecting the simulated peak-season pricing assumptions.
3. Monsoon recorded the lowest occupancy, ADR and RevPAR.
4. Guest satisfaction was lowest during Summer and highest during Monsoon.
5. Post-Monsoon showed a recovery in occupancy and revenue compared with Monsoon.

These findings demonstrate the relationship between seasonal demand, room pricing, revenue generation and guest satisfaction in the synthetic dataset.

## 6. Key Business Recommendations

Based on the annual and seasonal analysis, the following recommendations can be considered:

**1. Improve occupancy**

Use targeted promotions, seasonal packages and special offers during lower-demand periods to improve room utilisation.

**2. Optimise room pricing**

Adjust room rates according to seasonal demand. Maintain competitive pricing during low-demand periods while using appropriate peak-season pricing strategies.

**3. Improve revenue performance**

Monitor ADR and RevPAR together to understand the relationship between room pricing and occupancy. Focus on improving revenue without negatively affecting room utilisation.

**4. Maintain guest satisfaction**

Monitor guest feedback and improve service quality, staff responsiveness and operational efficiency, particularly during periods of higher guest demand.

**5. Reduce employee turnover**

Strengthen employee engagement, training, workload management and retention practices to support workforce stability.

**6. Monitor hotel-level performance**

Compare individual hotels and locations to identify differences in occupancy, pricing, revenue, guest satisfaction and employee turnover. Use these comparisons to identify hotels requiring operational improvements.

## 7. Data Limitations and Assumptions

The following limitations should be considered when interpreting the results:

- The dataset is synthetically generated and does not represent actual hotel operations.
- The analysis covers 10 hotels across five Indian cities.
- The five-year analysis period is 2022–2026.
- The complete year 2026 is simulated, including dates after the actual data-generation date.
- Seasonal patterns are based on qualitative project guidance and modelling assumptions rather than additional numerical trend files.
- Events, conferences and festivals were not explicitly modelled as separate demand drivers.
- Length of stay was not separately modelled as a seasonal factor.
- Employee joining and exit events are simulated, and employee exits are not explicitly weighted by season.
- There is no opening employee workforce before 2022, which affects the interpretation of employee turnover.
- Seasonal results are pooled across hotels and years, which may hide individual hotel and year-level differences.
- Annual aggregates may hide variations occurring at the monthly level.

The findings should therefore be interpreted as insights from a synthetic analytical exercise rather than verified real-world hospitality performance.

## 8. Conclusion

This project demonstrates how dimensional modelling, Python-based data generation, MySQL aggregation and interactive dashboards can be used to analyse hospitality business performance.

The annual analysis indicates relatively stable occupancy, ADR and RevPAR across the five-year period. Guest satisfaction remained positive, with minor annual fluctuations, while employee turnover increased noticeably in 2026.

The seasonal analysis provides further insight into the relationship between demand, room pricing, revenue and guest satisfaction. Winter recorded the strongest occupancy and RevPAR, while Monsoon showed lower occupancy and room revenue. Summer recorded the highest ADR but the lowest guest satisfaction.

The project provides a structured approach to monitoring hospitality KPIs, understanding seasonal variations and identifying potential areas for operational improvement.

The Streamlit dashboard enables users to explore hotel performance through interactive city, hotel, year and month filters, supporting comparisons across locations and time periods.
