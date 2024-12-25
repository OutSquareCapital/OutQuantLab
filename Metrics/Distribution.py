import numpy as np
from numpy.typing import NDArray
from numba import prange  # type: ignore
from numba import njit  # type: ignore

@njit
def calculate_skewness(
    min_length: int,
    observation_count: float,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    consecutive_equal_count: int
) -> float:
    if observation_count >= min_length:
        total_observations = float(observation_count)
        mean = sum_values / total_observations
        variance = sum_values_squared / total_observations - mean * mean
        skewness_numerator = (
            sum_values_cubed / total_observations
            - mean * mean * mean
            - 3 * mean * variance
        )

        if observation_count < 3:
            return np.nan
        elif consecutive_equal_count >= observation_count:
            return 0.0
        elif variance <= 1e-14:
            return np.nan
        else:
            std_dev = np.sqrt(variance)
            return (
                np.sqrt(total_observations * (total_observations - 1))
                * skewness_numerator
                / ((total_observations - 2) * std_dev * std_dev * std_dev)
            )
    else:
        return np.nan


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
    previous_value: float
    ) -> tuple[int, float, float, float, float, float, float, int, float]:

    if value == value:  # Vérification NaN
        observation_count += 1

        # Mise à jour pour la somme des valeurs
        temp = value - compensation_values
        total = sum_values + temp
        compensation_values = total - sum_values - temp
        sum_values = total

        # Mise à jour pour la somme des carrés des valeurs
        temp = value * value - compensation_squared
        total = sum_values_squared + temp
        compensation_squared = total - sum_values_squared - temp
        sum_values_squared = total

        # Mise à jour pour la somme des cubes des valeurs
        temp = value * value * value - compensation_cubed
        total = sum_values_cubed + temp
        compensation_cubed = total - sum_values_cubed - temp
        sum_values_cubed = total

        # Gestion des valeurs consécutives identiques
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
    compensation_cubed: float
    ) -> tuple[int, float, float, float, float, float, float]:
    if value == value:
        observation_count -= 1

        temp = -value - compensation_values
        total = sum_values + temp
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
def rolling_skewness(
    array: NDArray[np.float32],
    length: int,
    min_length: int
) -> NDArray[np.float32]:
    num_rows, num_cols = array.shape
    output: NDArray[np.float32] = np.empty((num_rows, num_cols), dtype=np.float32)
    output.fill(np.nan)

    for col in prange(num_cols):
        observation_count, sum_values, sum_values_squared, sum_values_cubed = 0, 0.0, 0.0, 0.0
        compensation_values, compensation_squared, compensation_cubed = 0.0, 0.0, 0.0
        previous_value = array[0, col]
        consecutive_equal_count = 0

        for row in range(num_rows):
            start_idx = max(0, row - length + 1)
            end_idx = row + 1

            if row == 0 or start_idx >= row - 1:
                observation_count, sum_values, sum_values_squared, sum_values_cubed = 0, 0.0, 0.0, 0.0
                compensation_values, compensation_squared, compensation_cubed = 0.0, 0.0, 0.0
                previous_value = array[start_idx, col]
                consecutive_equal_count = 0
                for idx in range(start_idx, end_idx):
                    observation_count, sum_values, sum_values_squared, sum_values_cubed, compensation_values, compensation_squared, compensation_cubed, consecutive_equal_count, previous_value = \
                        add_skewness_contribution(
                            array[idx, col],
                            observation_count,
                            sum_values,
                            sum_values_squared,
                            sum_values_cubed,
                            compensation_values,
                            compensation_squared,
                            compensation_cubed,
                            consecutive_equal_count,
                            previous_value
                        )
            else:
                for idx in range(max(0, row - length), start_idx):
                    observation_count, sum_values, sum_values_squared, sum_values_cubed, compensation_values, compensation_squared, compensation_cubed = \
                        remove_skewness_contribution(
                            array[idx, col],
                            observation_count,
                            sum_values,
                            sum_values_squared,
                            sum_values_cubed,
                            compensation_values,
                            compensation_squared,
                            compensation_cubed
                        )

                observation_count, sum_values, sum_values_squared, sum_values_cubed, compensation_values, compensation_squared, compensation_cubed, consecutive_equal_count, previous_value = \
                    add_skewness_contribution(
                        array[row, col],
                        observation_count,
                        sum_values,
                        sum_values_squared,
                        sum_values_cubed,
                        compensation_values,
                        compensation_squared,
                        compensation_cubed,
                        consecutive_equal_count,
                        previous_value
                    )

            output[row, col] = calculate_skewness(
                min_length,
                observation_count,
                sum_values,
                sum_values_squared,
                sum_values_cubed,
                consecutive_equal_count
            )

    return output

@njit
def calculate_kurtosis(
    min_length: int,
    observation_count: int,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    sum_values_fourth: float,
    consecutive_equal_count: int
) -> float|np.float32:
    if observation_count >= min_length:
        if observation_count < 4:
            return np.nan
        elif consecutive_equal_count >= observation_count:
            return -3.0
        else:
            total_observations = float(observation_count)
            mean = sum_values / total_observations
            variance = sum_values_squared / total_observations - mean * mean
            skewness_term = (
                sum_values_cubed / total_observations
                - mean * mean * mean
                - 3 * mean * variance
            )
            kurtosis_term = (
                sum_values_fourth / total_observations
                - mean * mean * mean * mean
                - 6 * variance * mean * mean
                - 4 * skewness_term * mean
            )

            if variance <= 1e-14:
                return np.nan
            else:
                kurtosis = (
                    (total_observations * total_observations - 1.0) * kurtosis_term
                    / (variance * variance)
                    - 3.0 * ((total_observations - 1.0) ** 2)
                )
                return kurtosis / ((total_observations - 2.0) * (total_observations - 3.0))
    else:
        return np.nan

@njit
def add_kurtosis_contribution(
    value: float,
    observation_count: int,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    sum_values_fourth: float,
    compensation_values: float,
    compensation_squared: float,
    compensation_cubed: float,
    compensation_fourth: float,
    consecutive_equal_count: int,
    previous_value: float
) -> tuple[int, float, float, float, float, float, float, float, float, int, float]:

    if value == value:
        observation_count += 1

        temp = value - compensation_values
        total = sum_values + temp
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

        temp = value * value * value * value - compensation_fourth
        total = sum_values_fourth + temp
        compensation_fourth = total - sum_values_fourth - temp
        sum_values_fourth = total

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
        sum_values_fourth,
        compensation_values,
        compensation_squared,
        compensation_cubed,
        compensation_fourth,
        consecutive_equal_count,
        previous_value,
    )

@njit
def remove_kurtosis_contribution(
    value: float,
    observation_count: int,
    sum_values: float,
    sum_values_squared: float,
    sum_values_cubed: float,
    sum_values_fourth: float,
    compensation_values: float,
    compensation_squared: float,
    compensation_cubed: float,
    compensation_fourth: float
) -> tuple[
    int, float, float, float, float, float, float, float, float
]:
    if value == value:
        observation_count -= 1

        temp = -value - compensation_values
        total = sum_values + temp
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

        temp = -value * value * value * value - compensation_fourth
        total = sum_values_fourth + temp
        compensation_fourth = total - sum_values_fourth - temp
        sum_values_fourth = total

    return (
        observation_count,
        sum_values,
        sum_values_squared,
        sum_values_cubed,
        sum_values_fourth,
        compensation_values,
        compensation_squared,
        compensation_cubed,
        compensation_fourth,
    )

@njit
def rolling_kurtosis(
    array: NDArray[np.float32],
    length: int,
    min_length: int
) -> NDArray[np.float32]:
    num_rows, num_cols = array.shape
    output: NDArray[np.float32] = np.empty((num_rows, num_cols), dtype=np.float32)
    output.fill(np.nan)

    for col in prange(num_cols):
        observation_count, sum_values, sum_values_squared, sum_values_cubed, sum_values_fourth = 0, 0.0, 0.0, 0.0, 0.0
        compensation_values, compensation_squared, compensation_cubed, compensation_fourth = 0.0, 0.0, 0.0, 0.0
        previous_value = array[0, col]
        consecutive_equal_count = 0

        for row in range(num_rows):
            start_idx = max(0, row - length + 1)
            end_idx = row + 1

            if row == 0 or start_idx >= row - 1:
                observation_count, sum_values, sum_values_squared, sum_values_cubed, sum_values_fourth = 0, 0.0, 0.0, 0.0, 0.0
                compensation_values, compensation_squared, compensation_cubed, compensation_fourth = 0.0, 0.0, 0.0, 0.0
                previous_value = array[start_idx, col]
                consecutive_equal_count = 0
                for idx in range(start_idx, end_idx):
                    observation_count, sum_values, sum_values_squared, sum_values_cubed, sum_values_fourth, compensation_values, compensation_squared, compensation_cubed, compensation_fourth, consecutive_equal_count, previous_value = \
                        add_kurtosis_contribution(
                            array[idx, col],
                            observation_count,
                            sum_values,
                            sum_values_squared,
                            sum_values_cubed,
                            sum_values_fourth,
                            compensation_values,
                            compensation_squared,
                            compensation_cubed,
                            compensation_fourth,
                            consecutive_equal_count,
                            previous_value
                        )
            else:
                for idx in range(max(0, row - length), start_idx):
                    observation_count, sum_values, sum_values_squared, sum_values_cubed, sum_values_fourth, compensation_values, compensation_squared, compensation_cubed, compensation_fourth = \
                        remove_kurtosis_contribution(
                            array[idx, col],
                            observation_count,
                            sum_values,
                            sum_values_squared,
                            sum_values_cubed,
                            sum_values_fourth,
                            compensation_values,
                            compensation_squared,
                            compensation_cubed,
                            compensation_fourth
                        )

                observation_count, sum_values, sum_values_squared, sum_values_cubed, sum_values_fourth, compensation_values, compensation_squared, compensation_cubed, compensation_fourth, consecutive_equal_count, previous_value = \
                    add_kurtosis_contribution(
                        array[row, col],
                        observation_count,
                        sum_values,
                        sum_values_squared,
                        sum_values_cubed,
                        sum_values_fourth,
                        compensation_values,
                        compensation_squared,
                        compensation_cubed,
                        compensation_fourth,
                        consecutive_equal_count,
                        previous_value
                    )

            output[row, col] = calculate_kurtosis(
                min_length,
                observation_count,
                sum_values,
                sum_values_squared,
                sum_values_cubed,
                sum_values_fourth,
                consecutive_equal_count
            )

    return output