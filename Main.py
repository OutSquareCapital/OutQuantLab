import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QIcon
import Config
from Main_UI import (apply_global_styles,
                    setup_home_page, 
                    setup_loading_page,
                    setup_results_page,
                    setup_progress_bar,
                    update_progress, 
                    display_plot_dialog, 
                    cleanup_temp_files
                     )

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(Config.APP_ICON_PHOTO)) 
        self.setWindowTitle("Main Application")
        self.temp_files = []
        self.backtest_result = None
        self.all_strategies_results = None
        self.show_home_page()
        self.resize(Config.DEFAULT_WIDTH, Config.DEFAULT_HEIGHT) 
        if not os.path.exists(Config.FILE_PATH_YF):
            self.refresh_data()

    def show_home_page(self):
        setup_home_page(
            parent=self,
            run_backtest_callback=self.run_backtest,
            open_config_callback=self.open_config,
            refresh_data_callback=self.refresh_data,
            background_image=Config.HOME_PAGE_PHOTO,
        )

    def open_config(self):
        UI.dynamic_config(Config.yahoo_assets, auto=False, parent=self)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(Config.yahoo_assets, Config.FILE_PATH_YF)

    def show_loading_page(self):
        self.progress_bar, self.log_output = setup_loading_page(self, Config.LOADING_PAGE_PHOTO)

    def update_progress(self, value, message=None):
        update_progress(self.progress_bar, self.log_output, value, message)

    def run_backtest(self):
        self.show_loading_page()

        QApplication.processEvents()

        self.update_progress(1, "Loading Data...")
        data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Config.FILE_PATH_YF)

        indicators_and_params, assets_to_backtest = UI.dynamic_config(assets_names, auto=True)

        self.update_progress(5, "Prepare Data...")
        QApplication.processEvents()

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

        self.update_progress(10, "Process Backtest...")
        QApplication.processEvents()

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            category_asset_names,
            dates_index,
            indicators_and_params,
            progress_callback=self.update_progress
        )

        self.update_progress(70, "Create Portfolio...")
        QApplication.processEvents()
        equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
        self.update_progress(80, "Create Portfolio...")
        QApplication.processEvents()
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
        equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'equal_weights'})
        self.update_progress(90, "Create Portfolio...")
        QApplication.processEvents()
        self.backtest_result = equal_weights_asset_returns
        self.all_strategies_results=raw_adjusted_returns_df
        self.update_progress(100, "Backtest Done !")

        self.show_results_page()

    def show_results_page(self):

        plots = {
            "Equity Curves": lambda: self.show_plot(Dashboard.plot_equity(self.backtest_result)),
            "Rolling Volatility": lambda: self.show_plot(Dashboard.plot_rolling_volatility(self.backtest_result)),
            "Rolling Drawdowns": lambda: self.show_plot(Dashboard.plot_rolling_drawdown(self.backtest_result, length=1250)),
            "Rolling Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_rolling_sharpe_ratio(self.backtest_result, length=1250)),
            "Rolling Smoothed Skewness": lambda: self.show_plot(Dashboard.plot_rolling_smoothed_skewness(self.backtest_result, length=1250)),
            "Rolling Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_rolling_average_inverted_correlation(self.backtest_result, length=1250)),
            "Overall Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_overall_sharpe_ratio(self.backtest_result)),
            "Overall Volatility": lambda: self.show_plot(Dashboard.plot_overall_volatility(self.backtest_result)),
            "Overall Average Drawdown": lambda: self.show_plot(Dashboard.plot_overall_average_drawdown(self.backtest_result, length=1250)),
            "Overall Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_overall_average_inverted_correlation(self.backtest_result)),
            "Overall Monthly Skew": lambda: self.show_plot(Dashboard.plot_overall_monthly_skew(self.backtest_result)),
            "Returns Distribution Violin": lambda: self.show_plot(Dashboard.plot_returns_distribution_violin(self.backtest_result)),
            "Returns Distribution Histogram": lambda: self.show_plot(Dashboard.plot_returns_distribution_histogram(self.backtest_result)),
            "Correlation Heatmap": lambda: self.show_plot(Dashboard.plot_correlation_heatmap(self.backtest_result)),
            "Clusters Icicle": lambda: self.show_plot(Dashboard.plot_clusters_icicle(self.backtest_result, max_clusters=5, max_sub_clusters=3, max_sub_sub_clusters=2)),
            "Sharpe Ratio Heatmap": lambda: self.show_plot(Dashboard.plot_sharpe_ratio_heatmap(self.all_strategies_results, param1='LenST', param2='LenLT')),
        }

        setup_results_page(parent=self, 
                           plots=plots, 
                           background_image=Config.DASHBOARD_PAGE_PHOTO, 
                           back_to_home_callback=self.show_home_page)

    def show_plot(self, fig):
        display_plot_dialog(
            parent=self,
            fig=fig,
            window_title="Graph",
            default_width=Config.DEFAULT_WIDTH,
            default_height=Config.DEFAULT_HEIGHT,
            background_color=Config.BACKGROUND_GRAPH_WHITE,
        )

    def closeEvent(self, event):
        cleanup_temp_files(self.temp_files)
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_global_styles(app)
    app.setWindowIcon(QIcon(Config.APP_ICON_PHOTO))

    progress_window, progress_bar = setup_progress_bar(None, "Launching App..")
    progress_window.show()

    QApplication.processEvents()
    progress_bar.setValue(15)
    import Get_Data
    progress_bar.setValue(30)
    import Process_Data
    progress_bar.setValue(45)
    import Backtest
    progress_bar.setValue(60)
    import Portfolio
    progress_bar.setValue(75)
    import Dashboard
    progress_bar.setValue(90)
    import UI
    progress_bar.setValue(95)
    import os
    progress_bar.setValue(100)
    main_window = MainApp()
    progress_window.close()
    main_window.show()

    sys.exit(app.exec())
