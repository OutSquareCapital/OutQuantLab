# Process_Data

## Overview

The `Process_Data` package is a comprehensive set of tools designed to structure and transform financial data into meaningful categories, calculate advanced metrics, and prepare datasets for in-depth analysis. It focuses on organizing data streams, extracting valuable insights, and creating derived datasets, ensuring data consistency and usability across various analytical workflows.

---

## What It Does

### 1. **Data Organization**

The package organizes raw financial data into logical categories based on user-defined rules:
- Splits assets into predefined groups such as `assets`, `ratios`, `ensembles`, and their corresponding `canary` categories.
- Ensures each category contains its relevant subset of data for specialized analysis.

### 2. **Category-Based Transformations**

For each category, the package computes:
- **Volatility Adjusted Returns**: Normalizes returns to a target volatility for risk-adjusted comparisons.
- **Ratios**: Calculates the difference in returns between pairs of assets in a category.
- **Ensembles**: Combines assets into groups and computes their average returns for collective performance evaluation.

### 3. **Recombination and Hierarchical Analysis**

Once the transformations are applied, categories are recombined into:
- **Returnstreams**: All main categories (`assets`, `ratios`, and `ensembles`) combined.
- **Canary_All**: A specialized category combining all `canary` data for leading indicator analysis.

### 4. **Data Extraction**

The package supports comprehensive data extraction:
- Converts percentage returns to price levels.
- Computes log returns and historical volatility arrays.
- Provides raw and transformed data in both `DataFrame` and `NumPy array` formats for flexibility.

---

## Problems Solved

1. **Fragmented Data Streams**:
   - Automatically categorizes assets, ensuring logical grouping for focused analysis.

2. **Volatility Normalization**:
   - Adjusts returns to account for varying risk levels, making comparisons between assets meaningful.

3. **Derived Metrics**:
   - Generates complex derived datasets such as ratios and ensembles, enabling advanced studies without manual effort.

4. **Data Recombination**:
   - Consolidates fragmented datasets into unified streams for a holistic view.

5. **Preparation for Simulation and Modeling**:
   - Outputs standardized data structures, making the datasets ready for downstream tasks like backtesting or predictive modeling.

---

## Output

The package generates:
- **Category-Based DataFrames**: Separate DataFrames for each user-defined category, containing returns or transformed metrics.
- **Consolidated DataFrames**: Unified streams for `returnstreams` and `canary_all`.
- **Extracted Data**: Comprehensive outputs in multiple formats (prices, returns, log returns, volatility arrays).

This ensures that all relevant data is structured, categorized, and enhanced for immediate use in analytical workflows.
