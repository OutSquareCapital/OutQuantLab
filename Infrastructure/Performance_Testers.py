import pandas as pd
import numpy as np
import timeit
from typing import Dict, Tuple
import matplotlib.pyplot as plt

def format_time(seconds):
    """
    Format the time in seconds to an appropriate unit (microseconds, milliseconds, or seconds).

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted time as a string.
    """
    if seconds < 1e-3:
        return f"{seconds * 1e6:.2f} microseconds"
    elif seconds < 1:
        return f"{seconds * 1e3:.2f} milliseconds"
    else:
        return f"{seconds:.2f} seconds"
    

def determine_time_unit(times: pd.Series) -> Tuple[pd.Series, str]:

    max_time = times.max()
    if max_time < 1e-3:
        return times * 1e6, 'microseconds'
    elif max_time < 1:
        return times * 1e3, 'milliseconds'
    else:
        return times, 'seconds'
    
def measure_performance(func, num_iterations = 1000, *args, **kwargs) -> Tuple[Dict[str, float], pd.DataFrame]:
    """
    Measure the performance of a function by executing it multiple times and recording the execution times.

    Args:
        func (callable): Function to measure.
        num_iterations (int): Number of iterations to run the function.
        *args: Variable length argument list for the function.
        **kwargs: Arbitrary keyword arguments for the function.

    Returns:
        Tuple[Dict[str, float], pd.DataFrame]: Dictionary of performance statistics and DataFrame of execution times.
    """
    execution_times = []

    # Définition d'un wrapper pour la fonction à mesurer
    def wrapper():
        func(*args, **kwargs)

    # Exécution initiale pour ignorer le temps de la première exécution
    wrapper()
    
    # Mesure des temps d'exécution
    for _ in range(num_iterations):
        execution_time = timeit.timeit(wrapper, number=1)
        execution_times.append(execution_time)

    # Enregistrer les temps d'exécution dans un DataFrame
    execution_times_df = pd.DataFrame(execution_times, columns=['execution_time'])

    # Calcul des statistiques des temps d'exécution
    median_time = np.median(execution_times)
    percentile_0_1 = np.percentile(execution_times, 0.1)
    percentile_1 = np.percentile(execution_times, 1)
    percentile_99 = np.percentile(execution_times, 99)
    percentile_99_9 = np.percentile(execution_times, 99.9)

    # Retourner les statistiques sous forme de dictionnaire et le Dataframe
    return {
        'median_time': median_time,
        'percentile_0_1': percentile_0_1,
        'percentile_1': percentile_1,
        'percentile_99': percentile_99,
        'percentile_99.9': percentile_99_9
    }, execution_times_df


def performance_compare(func1, func2, num_iterations=1000, *args, **kwargs) -> None:
    """
    Compare the performance of two functions by executing them multiple times and recording the execution times.

    Args:
        func1 (callable): First function to compare.
        func2 (callable): Second function to compare.
        num_iterations (int): Number of iterations to run each function.
        *args: Variable length argument list for the functions.
        **kwargs: Arbitrary keyword arguments for the functions.

    Returns:
        None
    """
    # Mesurer les performances des deux fonctions
    stats1, execution_times_df1 = measure_performance(func1, num_iterations, *args, **kwargs)
    stats2, execution_times_df2 = measure_performance(func2, num_iterations, *args, **kwargs)
    
    # Noms des fonctions
    func1_name = func1.__name__
    func2_name = func2.__name__
    
    # Comparer les statistiques et afficher les résultats
    print("Comparison Report")
    print("=================")
    
    def compare_and_print(stat_name, stat_label):
        value1 = stats1[stat_name]
        value2 = stats2[stat_name]

        if value1 < value2:
            winner = func1_name
            ratio = (value2 / value1) - 1
        else:
            winner = func2_name
            ratio = (value1 / value2) - 1

        formatted_value1 = format_time(value1)
        formatted_value2 = format_time(value2)

        print(f"{stat_label}:")
        print(f"  Winner: {winner}")
        print(f"  {stat_label} {func1_name}: {formatted_value1}")
        print(f"  {stat_label} {func2_name}: {formatted_value2}")
        print(f"  Ratio: {ratio:.2f}x faster")
        print("")
    
    # Comparer et afficher les résultats pour chaque statistique
    compare_and_print('median_time', 'Median execution time')
    compare_and_print('percentile_0_1', '0.1st percentile')
    compare_and_print('percentile_1', '1st percentile')
    compare_and_print('percentile_99', '99th percentile')
    compare_and_print('percentile_99.9', '99.9th percentile')

    # Tracer les distributions des temps d'exécution

    execution_times_df1['execution_time'], unit1 = determine_time_unit(execution_times_df1['execution_time'])
    execution_times_df2['execution_time'], unit2 = determine_time_unit(execution_times_df2['execution_time'])

    # Superposer les histogrammes
    plt.figure(figsize=(16, 8))
    plt.hist(execution_times_df1['execution_time'], bins=50, alpha=0.75, label=f'{func1_name} ({unit1})')
    plt.hist(execution_times_df2['execution_time'], bins=50, alpha=0.75, label=f'{func2_name} ({unit2})')
    plt.title('Execution Time Distribution')
    plt.xlabel('Execution Time')
    plt.ylabel('Frequency')
    plt.legend(loc='upper right')
    plt.show()




def performance_test(func, num_iterations=1000, *args, **kwargs) -> None:
    """
    Test the performance of a function by executing it multiple times and recording the execution times.

    Args:
        func (callable): Function to test.
        num_iterations (int): Number of iterations to run the function.
        *args: Variable length argument list for the function.
        **kwargs: Arbitrary keyword arguments for the function.

    Returns:
        None
    """
    # Mesurer les performances de la fonction
    stats, execution_times_df = measure_performance(func, num_iterations, *args, **kwargs)
    
    # Nom de la fonction
    func_name = func.__name__
    
    # Afficher les résultats
    print("Performance Report")
    print("=================")
    
    def print_stat(stat_name, stat_label):
        value = stats[stat_name]
        formatted_value = format_time(value)

        print(f"{stat_label}: {formatted_value}")
        print("")

    # Afficher les résultats pour chaque statistique
    print_stat('median_time', 'Median execution time')
    print_stat('percentile_0_1', '0.1st percentile')
    print_stat('percentile_1', '1st percentile')
    print_stat('percentile_99', '99th percentile')
    print_stat('percentile_99.9', '99.9th percentile')

    # Tracer la distribution des temps d'exécution
    print("Execution Time Distribution")
    print("===========================")
    execution_times_df['execution_time'], unit = determine_time_unit(execution_times_df['execution_time'])
    execution_times_df.plot(kind='hist', title=f'Execution Time Distribution of {func_name} ({unit})', bins=50, figsize=(16, 8))