TRADING_DAYS_PER_WEEK = 5
TRADING_DAYS_PER_MONTH = 21
TRADING_DAYS_PER_YEAR = 256
TRADING_DAYS_PER_5_YEARS = 1280
ANNUALIZATION_FACTOR = 16
PERCENTAGE_FACTOR = 100
ANNUALIZED_PERCENTAGE_FACTOR = ANNUALIZATION_FACTOR * PERCENTAGE_FACTOR

# Spécification des chemins de fichiers
file_path_yf = "C:\\Users\\stett\\Documents\\FinancialData\\YahooFinance\\price_data.csv"
file_path_tradingview = "D:\\Python\\Data\\Excel_Data\\TradingView\\combined_data.csv"
#file_path_spot_3M_data = "D:\\Python\\Data\\Excel_Data\\SpotData\\US03MY.csv"
#file_path_spot_10Y_data = "D:\\Python\\Data\\Excel_Data\\SpotData\\US10Y.csv"
#file_path_main_data = "D:\\Python\\Data\\Excel_Data\\Divers\\MainData\\main_data.csv"

#file_path_txt = "D:\\Python\\Data\\Excel_Data\\Turtle data\\raw_txt"
#file_path_out = "D:\\Python\\Data\\Excel_Data\\Turtle data\\raw_csv"

#file_path_test = "D:\\Python\\Data\\Excel_Data\\Turtle data\\raw_csv\\SP"


# Spécification des structures de portfolio et stratégies

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
        'PriceBased':[
            'FixedBias'
        ]
    },
    'Divergent': {
        'Direction': {  
            'Trend': [
                'Trend_SmaRatio',
                'Trend_MedianRatio',
                'Trend_CentralPointRatio'
                'Trend_RateOfChangeSmoothed'
                'Trend_MeanReturnsRatio',
                'Trend_MedianReturnsRatio',
                'Trend_QuantileReturnsSignal'
            ],
        },
        'Speed': {
            'Acceleration': [
                'Acceleration_SmaMacd',
                'Acceleration_MedianMacd',
                'Acceleration_CentralPointMacd'
                'Acceleration_MeanReturnsMacd',
                'Acceleration_MedianReturnsMacd',
                'Acceleration_QuantileReturnsMacd'
            ],
            'AccelerationTrend': [
                'AccelerationTrend_SmaMacdTrend',
                'AccelerationTrend_MedianMacdTrend',
                'AccelerationTrend_CentralPointMacdTrend',
                'AccelerationTrend_MeanMacdTrend',
                'AccelerationTrend_MedianMacdTrend',
                'AccelerationTrend_QuantilesMacdTrend',
            ]
        }
    },
    'Convergent': {
        'MeanReversion': {
            'MR': [
                'MeanReversion_SmaRatioNormalised',
                'MeanReversion_MedianRatioNormalised',
                'MeanReversion_ZScoreNormalised',
                'MeanReversion_RsiNormalised',
                'MeanReversion_BreakoutNormalised',
            ],
            'MRTrend': [
                'MeanReversionTrend_SmaRatioNormalisedTrend',
                'MeanReversionTrend_MedianRatioNormalisedTrend',
                'MeanReversionTrend_ZScoreNormalisedTrend',
                'MeanReversionTrend_RsiNormalisedTrend',
                'MeanReversionTrend_BreakoutNormalisedTrend',
            ],
        },
        'Stats': {
            'ReturnsDistribution': [
                'ReturnsDistribution_Skewness',
                'ReturnsDistribution_RelativeSkewness',
                'ReturnsDistributionTrend_SkewnessTrend'
                'ReturnsDistributionTrend_SkewnessOnKurtosis'
            ],
            'Volatility': [
                'Volatility_NetVolatility',
                'VolatilityTrend_NetVolatilityTrend'
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
'TLT',
'GLD',
'SLV',
'CORN',
'WEAT',
'SOYB', 
'USO',
'UNG',
'FXA',
'FXE',
'FXB',
'FXC',
'GBTC',
'VIXY',
'DBB'
]