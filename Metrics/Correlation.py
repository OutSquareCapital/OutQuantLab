from Utilitary import SeriesFloat, Float32, DataFrameFloat

def calculate_correlation_matrix(returns_df: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(returns_df.corr())

def calculate_distance_matrix(returns_df: DataFrameFloat) -> DataFrameFloat:
    return DataFrameFloat(1 - calculate_correlation_matrix(returns_df))

def calculate_pairwise_distances(returns_df: DataFrameFloat) -> DataFrameFloat:
    corr_matrix = calculate_correlation_matrix(returns_df)
    return DataFrameFloat(1 - corr_matrix.abs())

def calculate_rolling_paired_correlation_matrix(returns_df: DataFrameFloat, window: int) -> DataFrameFloat:
    return DataFrameFloat(returns_df.rolling(window=window).corr(pairwise=True))

def calculate_rolling_average_correlation(returns_df: DataFrameFloat, length: int) -> DataFrameFloat:
    return DataFrameFloat(returns_df.rolling(window=length, min_periods=length).corr().groupby(level=0).mean().astype(Float32))

def calculate_overall_average_correlation(returns_df: DataFrameFloat) -> SeriesFloat:
    return SeriesFloat(returns_df.corr().mean(), index=returns_df.columns)
