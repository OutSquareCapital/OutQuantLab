import bottleneck as bn  # type: ignore

from numquant.main import Float2D


def get_mean(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_mean(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_median(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_median(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_central_point(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    upper: Float2D = get_max(array=array, length=length, min_length=min_length)
    lower: Float2D = get_min(array=array, length=length, min_length=min_length)
    return (upper + lower) / 2


def get_max(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_max(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_min(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_min(array, window=length, min_count=min_length, axis=0)  # type: ignore


def get_sum(array: Float2D, length: int, min_length: int = 1) -> Float2D:
    return bn.move_sum(array, window=length, min_count=min_length, axis=0)  # type: ignore