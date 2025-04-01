# OutQuantLab

OutQuantLab is a comprehensive Python-based quantitative analysis platform for backtesting systematic trading strategies, with emphasis on technical indicators and clustering analysis.

## Development

### Adding New Indicators

1. Define raw calculations in `Indicators/Indics_Raw.py`
2. Add normalized version in `Indicators/Indics_Normalized.py`
3. Use the `@indic` decorator to register the indicator

### Creating new statistic measure

1. Define widget in `stats/graphs.py`
2. Implement data transformations in `stats/processors.py`
3. Instanciate the processor in `stats/main.py`

### Commits

Install mypy, and always use those commands before commiting:

mypy --strict outquantlab
stubtest outquantlab
