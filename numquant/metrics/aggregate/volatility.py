from numquant.metrics.constants import ANNUALIZED_PERCENTAGE
from numquant.main import Float2D
import bottleneck as bn  # type: ignore

def get_volatility(returns_array: Float2D) -> Float2D:
    return bn.nanstd(returns_array, axis=0, ddof=1)  # type: ignore

def get_volatility_annualized(returns_array: Float2D) -> Float2D:
    return get_volatility(returns_array=returns_array) * ANNUALIZED_PERCENTAGE
