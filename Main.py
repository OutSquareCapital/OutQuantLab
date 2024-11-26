import Config
import UI   
import Portfolio
import Get_Data
import Process_Data
import Dashboard
import Backtest
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Bouton Run Backtest
        backtest_button = QPushButton("Run Backtest")
        backtest_button.clicked.connect(self.run_backtest)
        main_layout.addWidget(backtest_button)

        # Bouton Open Config
        config_button = QPushButton("Open Config")
        config_button.clicked.connect(self.open_config)
        main_layout.addWidget(config_button)

        # Bouton Refresh Data
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.refresh_data)
        main_layout.addWidget(refresh_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def open_config(self):
        UI.dynamic_config(Config.yahoo_assets, auto=False, parent=self)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(Config.yahoo_assets, Config.FILE_PATH_YF)

    def run_backtest(self):

        data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Config.FILE_PATH_YF)

        indicators_and_params, assets_to_backtest = UI.dynamic_config(assets_names, auto=True)

        (
            prices_array,
            volatility_adjusted_pct_returns_array,
            log_returns_array,
            category_asset_names,
            dates_index,
        ) = Process_Data.process_data(
            assets_names,
            data_prices_df,
            assets_to_backtest,
        )

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            category_asset_names,
            dates_index,
            indicators_and_params
        )

        equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
        equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'equal_weights'})
        test_returns_df = equal_weights_asset_returns
        self.close()

        Dashboard.generate_dashboard_plots(
        test_returns_df,
        raw_adjusted_returns_df,
        equity=True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())