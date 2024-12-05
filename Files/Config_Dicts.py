TRADING_DAYS_PER_WEEK = 5
TRADING_DAYS_PER_MONTH = 21
TRADING_DAYS_PER_YEAR = 256
TRADING_DAYS_PER_5_YEARS = 1280
ANNUALIZATION_FACTOR = 16
PERCENTAGE_FACTOR = 100
ANNUALIZED_PERCENTAGE_FACTOR = ANNUALIZATION_FACTOR * PERCENTAGE_FACTOR

portfolio_futures = {
    'Equities': {
        'Large Caps': ['ES', 'YM', 'NQ'],
        'Small Caps': ['RTY'],
        'Volatility': ['VX'],
    },
    'Bonds': {
        'US':['ZF'],
    },
    'Currencies': {
        'Precious Metals': ['GC', 'SI'],
        'FX': ['6A', '6E', '6B', '6C'],
        'Crypto': ['BTC'],
    },
    'Commodities': {
    'Agricultural': ['ZC', 'ZW', 'ZS'],
    'Energy': ['CL', 'NG'],
    'Base Metals': ['HG'],
    }
}