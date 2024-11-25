import os

TRADING_DAYS_PER_WEEK = 5
TRADING_DAYS_PER_MONTH = 21
TRADING_DAYS_PER_YEAR = 256
TRADING_DAYS_PER_5_YEARS = 1280
ANNUALIZATION_FACTOR = 16
PERCENTAGE_FACTOR = 100
ANNUALIZED_PERCENTAGE_FACTOR = ANNUALIZATION_FACTOR * PERCENTAGE_FACTOR

SAVED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Saved_Data")

ASSETS_TO_TEST_CONFIG_FILE = os.path.join(SAVED_DATA_FOLDER, "assets_to_backtest.json")
PARAM_CONFIG_FILE = os.path.join(SAVED_DATA_FOLDER, "param_values.json")
METHODS_CONFIG_FILE = os.path.join(SAVED_DATA_FOLDER, "methods_config.json")

FILE_PATH_YF = os.path.join(SAVED_DATA_FOLDER, "price_data.parquet")

DEFAULT_TEMPLATE = "plotly_white"
COLOR_ADJUSTMENT = 'black'
DEFAULT_HEIGHT = 800

portfolio_etf = {
    'Equities': {
        'Large Caps': ['SPY', 'DIA', 'QQQ'],
        'Small Caps': ['IWM'],
        'Volatility': ['VIXY'],
    },
    'Bonds': {
        'US':['TLT'],
    },
    'Currencies': {
        'Precious Metals': ['GLD', 'SLV'],
        'FX': ['FXA', 'FXE', 'FXB', 'FXC'],
        'Crypto': ['GBTC'],
    },
    'Commodities': {
    'Agricultural': ['CORN', 'WEAT', 'SOYB'],
    'Energy': ['USO', 'UNG'],
    'Base Metals': ['DBB'],
    }
}


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

portfolio_strategies = {
    'RiskPremium': {
        'PriceBased': [
            'FixedBias'
        ]
    },
    'Divergent': {
        'Direction': {  
            'Trend': [
                'Trend_MeanPriceRatio',
                'Trend_MedianPriceRatio',
                'Trend_CentralPriceRatio',
                'Trend_MeanRateOfChange',
                'Trend_MedianRateOfChange',
                'Trend_CentralRateOfChange',
            ]
        },
        'Speed': {
            'Acceleration': [
                'Acceleration_MeanPriceMacd',
                'Acceleration_MedianPriceMacd',
                'Acceleration_CentralPriceMacd',
                'Acceleration_MeanRateOfChangeMacd',
                'Acceleration_MedianRateOfChangeMacd',
                'Acceleration_CentralRateOfChangeMacd',
            ],
            'AccelerationTrend': [
                'AccelerationTrend_MeanPriceMacdTrend',
                'AccelerationTrend_MedianPriceMacdTrend',
                'AccelerationTrend_CentralPriceMacdTrend',
                'AccelerationTrend_MeanRateOfChangeMacdTrend',
                'AccelerationTrend_MedianRateOfChangeMacdTrend',
                'AccelerationTrend_CentralRateOfChangeMacdTrend',
            ]
        }
    },
    'Convergent': {
        'MeanReversion': {
            'MR': [
                'MeanReversion_MeanPriceRatioNormalised',
                'MeanReversion_MeanRateOfChangeNormalised',
            ],
            'MRTrend': [
                'MeanReversionTrend_MeanPriceRatioNormalisedTrend',
                'MeanReversionTrend_MeanRateOfChangeNormalisedTrend',
            ],
        },
        'Stats': {
            'ReturnsDistribution': [
                'ReturnsDistribution_Skewness',
                'ReturnsDistribution_RelativeSkewness',
                'ReturnsDistribution_SkewnessOnKurtosis_ST',
                'ReturnsDistribution_SkewnessOnKurtosis_LT',
                'ReturnsDistribution_RelativeSkewnessOnKurtosis_ST',
                'ReturnsDistribution_RelativeSkewnessOnKurtosis_LT',
            ],
            'ReturnsDistributionTrend': [
                'ReturnsDistributionTrend_Skewness',
                'ReturnsDistributionTrend_RelativeSkewness',
                'ReturnsDistributionTrend_SkewnessOnKurtosis_ST_Trend',
                'ReturnsDistributionTrend_SkewnessOnKurtosis_LT_Trend',
                'ReturnsDistributionTrend_RelativeSkewnessOnKurtosis_ST_Trend',
                'ReturnsDistributionTrend_RelativeSkewnessOnKurtosis_LT_Trend',
            ],
            'Volatility': [
                'Volatility_RelativeDirectionalVolatility',
                'Volatility_NormalisedDirectionalVolatility',
            ],
            'VolatilityTrend': [
                'VolatilityTrend_RelativeDirectionalVolatilityTrend',
                'VolatilityTrend_NormalisedDirectionalVolatilityTrend',
            ]
        }
    }
}


paires_futures_etf = [
("6A", "AD"),
("6B", "BP"),
("6C", "CD"),
("YM", "1YM"),
("RTY", "TF"),
("RTY", "SMC"),
("6E", "URO"),
("ZS", "S"),
("ZC", "C"),
("ZW", "W"),
("ES", "SP"),
("ZB", "US"),
("ZF", "FV"),
]

yahoo_assets = [
'SPY',
'IWM', 
'DIA', 
'QQQ',
'VIXY',
'TLT',
'CORN',
'WEAT',
'SOYB', 
'USO',
'UNG',
'DBB',
'GLD',
'SLV',
'FXA',
'FXE',
'FXB',
'FXC',
'GBTC',
]