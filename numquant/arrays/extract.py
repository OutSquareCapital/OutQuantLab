from numquant.arrays.create import create_empty_like
from numquant.main import Float2D, Float32, Int2D, Nan, np, Int1D

def get_index(array: Float2D) -> Int1D:
    return np.arange(array.shape[0])

def get_sorted_indices(array: Float2D, ascending: bool) -> Int2D:
    sorted_indices: Int2D = np.argsort(array, None)
    if not ascending:
        sorted_indices = sorted_indices[::-1]
    return sorted_indices


def get_log_returns(prices: Float2D) -> Float2D:
    ratios = prices[1:] / prices[:-1]
    log_returns: Float2D = create_empty_like(model=prices)
    log_returns[0] = Nan
    log_returns[1:] = np.log(ratios)
    return log_returns


def get_pct_returns(prices: Float2D) -> Float2D:
    pct_returns: Float2D = create_empty_like(model=prices)
    pct_returns[0] = Nan
    pct_returns[1:] = prices[1:] / prices[:-1] - 1
    return pct_returns


def get_prices(returns: Float2D) -> Float2D:
    temp: Float2D = returns.copy()
    mask: Float2D = np.isnan(temp)
    temp[mask] = 0
    cumulative_returns: Float2D = create_empty_like(model=temp)
    cumulative_returns[:0] = Nan
    cumulative_returns[0:] = np.cumprod(a=1 + temp[0:], axis=0)
    cumulative_returns[mask] = Nan
    return cumulative_returns * Float32(100)
