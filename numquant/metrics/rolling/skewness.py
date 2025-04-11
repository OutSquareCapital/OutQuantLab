from numba import njit, prange  # type: ignore

from numquant.main import Float2D, Nan, np
from numquant.arrays import create_nan

@njit
def compute_skewness(
    min_length: int,
    observation_count: float,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    consecutive_equal_count: int,
) -> float:
    if observation_count >= min_length:
        total_observations = float(observation_count)
        mean: float = sum_values / total_observations
        variance: float = sum_values_squared / total_observations - mean * mean
        skewness_numerator: float = (
            sum_values_cubed / total_observations
            - mean * mean * mean
            - 3 * mean * variance
        )

        if observation_count < 3:
            return Nan
        elif consecutive_equal_count >= observation_count:
            return 0.0
        elif variance <= 1e-14:
            return Nan
        else:
            std_dev = np.sqrt(variance)
            return (
                np.sqrt(total_observations * (total_observations - 1))
                * skewness_numerator
                / ((total_observations - 2) * std_dev * std_dev * std_dev)
            )
    else:
        return Nan


@njit
def add_skewness_contribution(
    value: float,
    observation_count: int,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    compensation_values: float,
    compensation_squared: float,
    compensation_cubed: float,
    consecutive_equal_count: int,
    previous_value: float,
) -> tuple[int, float, float, float, float, float, float, int, float]:
    if value == value:
        observation_count += 1

        temp: float = value - compensation_values
        total: float = sum_values + temp
        compensation_values = total - sum_values - temp
        sum_values = total

        temp = value * value - compensation_squared
        total = sum_values_squared + temp
        compensation_squared = total - sum_values_squared - temp
        sum_values_squared = total

        temp = value * value * value - compensation_cubed
        total = sum_values_cubed + temp
        compensation_cubed = total - sum_values_cubed - temp
        sum_values_cubed = total

        if value == previous_value:
            consecutive_equal_count += 1
        else:
            consecutive_equal_count = 1
        previous_value = value

    return (
        observation_count,
        sum_values,
        sum_values_squared,
        sum_values_cubed,
        compensation_values,
        compensation_squared,
        compensation_cubed,
        consecutive_equal_count,
        previous_value,
    )


@njit
def remove_skewness_contribution(
    value: float,
    observation_count: int,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    compensation_values: float,
    compensation_squared: float,
    compensation_cubed: float,
) -> tuple[int, float, float, float, float, float, float]:
    if value == value:
        observation_count -= 1

        temp: float = -value - compensation_values
        total: float = sum_values + temp
        compensation_values = total - sum_values - temp
        sum_values = total

        temp = -value * value - compensation_squared
        total = sum_values_squared + temp
        compensation_squared = total - sum_values_squared - temp
        sum_values_squared = total

        temp = -value * value * value - compensation_cubed
        total = sum_values_cubed + temp
        compensation_cubed = total - sum_values_cubed - temp
        sum_values_cubed = total

    return (
        observation_count,
        sum_values,
        sum_values_squared,
        sum_values_cubed,
        compensation_values,
        compensation_squared,
        compensation_cubed,
    )


@njit
def get_skewness(
    array: Float2D, length: int, min_length: int = 4
) -> Float2D:
    num_rows, num_cols = array.shape
    output = create_nan(length=num_rows, width=num_cols)

    for col in prange(num_cols):
        observation_count, sum_values, sum_values_squared, sum_values_cubed = (
            0,
            0.0,
            0.0,
            0.0,
        )
        compensation_values, compensation_squared, compensation_cubed = 0.0, 0.0, 0.0
        previous_value = array[0, col]
        consecutive_equal_count = 0

        for row in range(num_rows):
            start_idx: int = max(0, row - length + 1)
            end_idx: int = row + 1

            if row == 0 or start_idx >= row - 1:
                observation_count, sum_values, sum_values_squared, sum_values_cubed = (
                    0,
                    0.0,
                    0.0,
                    0.0,
                )
                compensation_values, compensation_squared, compensation_cubed = (
                    0.0,
                    0.0,
                    0.0,
                )
                previous_value = array[start_idx, col]
                consecutive_equal_count = 0
                for idx in range(start_idx, end_idx):
                    (
                        observation_count,
                        sum_values,
                        sum_values_squared,
                        sum_values_cubed,
                        compensation_values,
                        compensation_squared,
                        compensation_cubed,
                        consecutive_equal_count,
                        previous_value,
                    ) = add_skewness_contribution(
                        value=array[idx, col],
                        observation_count=observation_count,
                        sum_values=sum_values,
                        sum_values_squared=sum_values_squared,
                        sum_values_cubed=sum_values_cubed,
                        compensation_values=compensation_values,
                        compensation_squared=compensation_squared,
                        compensation_cubed=compensation_cubed,
                        consecutive_equal_count=consecutive_equal_count,
                        previous_value=previous_value,
                    )
            else:
                for idx in range(max(0, row - length), start_idx):
                    (
                        observation_count,
                        sum_values,
                        sum_values_squared,
                        sum_values_cubed,
                        compensation_values,
                        compensation_squared,
                        compensation_cubed,
                    ) = remove_skewness_contribution(
                        value=array[idx, col],
                        observation_count=observation_count,
                        sum_values=sum_values,
                        sum_values_squared=sum_values_squared,
                        sum_values_cubed=sum_values_cubed,
                        compensation_values=compensation_values,
                        compensation_squared=compensation_squared,
                        compensation_cubed=compensation_cubed,
                    )

                (
                    observation_count,
                    sum_values,
                    sum_values_squared,
                    sum_values_cubed,
                    compensation_values,
                    compensation_squared,
                    compensation_cubed,
                    consecutive_equal_count,
                    previous_value,
                ) = add_skewness_contribution(
                    value=array[row, col],
                    observation_count=observation_count,
                    sum_values=sum_values,
                    sum_values_squared=sum_values_squared,
                    sum_values_cubed=sum_values_cubed,
                    compensation_values=compensation_values,
                    compensation_squared=compensation_squared,
                    compensation_cubed=compensation_cubed,
                    consecutive_equal_count=consecutive_equal_count,
                    previous_value=previous_value,
                )

            output[row, col] = compute_skewness(
                min_length=min_length,
                observation_count=observation_count,
                sum_values=sum_values,
                sum_values_squared=sum_values_squared,
                sum_values_cubed=sum_values_cubed,
                consecutive_equal_count=consecutive_equal_count,
            )

    return output

def get_expanding_skewness(
    array: Float2D, min_length: int = 4
) -> Float2D:
    return get_skewness(array=array, length=array.shape[0], min_length=min_length)