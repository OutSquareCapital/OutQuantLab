# Get_Data

## Overview

The `Get_Data` package is designed to solve common issues in handling financial datasets by offering a streamlined approach to data fetching, normalization, and preparation. It tackles challenges such as inconsistent formats, missing values, and integration of related datasets, ultimately producing clean, standardized `.csv` files ready for analysis.

---

## What It Does

1. **Data Fetching**:
   - Downloads market data from sources like Yahoo Finance.
   - Retrieves daily asset prices and stores them in an accessible format.

2. **Data Normalization**:
   - Converts raw `.txt` files into standardized `.csv` files.
   - Ensures consistent column names (e.g., Date, Open, Close, Volume).
   - Formats dates into a unified structure, regardless of their original form.

3. **Handling Missing Data**:
   - Fills gaps in price data using advanced techniques (e.g., random sampling, bootstrapping returns).
   - Combines related datasets (e.g., futures and ETFs) to reconstruct missing information.

4. **Fixing Anomalies**:
   - Adjusts negative prices to ensure all values are logically correct.
   - Processes incomplete datasets while preserving important trends and relationships.

5. **Dataset Integration**:
   - Aligns multiple assets by their dates, creating a unified dataset.
   - Combines time-series data from different sources into a single `.csv` file.

---

## Problems Solved

- **Inconsistent Formats**:
  Raw data files often lack standardization, making it difficult to analyze them together. This package ensures all data follows a consistent structure.

- **Negative Prices**:
  Sometimes datasets include negative or anomalous prices. The package automatically adjusts these values to ensure realistic datasets.

- **Gaps in Data**:
  Missing values in price data can create issues in analysis. This package fills those gaps intelligently without introducing biases.

- **Misaligned Datasets**:
  When combining data from multiple sources, date mismatches or missing columns can occur. This package ensures proper alignment across all datasets.

---

## Output

The final output is a collection of `.csv` files where:
- All dates are aligned across assets.
- Prices are cleaned, consistent, and adjusted for any anomalies.
- Missing data is resolved.
- The format is standardized, ready for direct use in analytical workflows.
