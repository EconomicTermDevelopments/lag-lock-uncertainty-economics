---
language:
- en
license: mit
task_categories:
- tabular-classification
tags:
- economics
- lag-lock-uncertainty
- computational-economics
- climate-economics
- emerging-terminology
pretty_name: lag-lock uncertainty Economics Dataset
size_categories:
- n<1K
---

# lag-lock uncertainty Economics Dataset

## Dataset Description
### Summary
Synthetic 200-row dataset for `lag-lock uncertainty` measurement and computational experiments.

### Supported Tasks
- Economic analysis
- Climate Economics research
- Computational economics

### Languages
- English (metadata and documentation)
- Python (code examples)

## Dataset Structure
### Data Fields
- `id`: Unique observation id
- `year`: Synthetic climate-policy year
- `climate_inertia`: Committed warming inertia from past emissions
- `policy_response_lag`: Lag between policy action and observed response
- `threshold_uncertainty`: Uncertainty around tipping threshold locations
- `feedback_strength`: Strength of nonlinear climate feedback channels
- `attribution_noise`: Noise in attributing outcomes to interventions
- `adaptation_gap`: Gap between required and realized adaptation capacity
- `monitoring_capacity`: Strength of monitoring and verification systems
- `lag_lock_uncertainty_index`: Composite term index

### Data Splits
- Full dataset: 200 examples

## Dataset Creation
### Source Data
Synthetic data generated for demonstrating lag-lock uncertainty applications.

### Data Generation
Channels are sampled from controlled distributions with correlated structure. The term index is computed from normalized channels and directional weights.

## Considerations
### Social Impact
Research-only synthetic data for method development and reproducibility testing.

## Additional Information
### Licensing
MIT License - free for academic and commercial use.

### Citation
@dataset{lag-lock-uncertainty2026,
title={{lag-lock uncertainty Economics Dataset}},
author={{Economic Research Collective}},
year={{2026}}
}
