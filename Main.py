from PySide6.QtWidgets import QApplication, QMainWindow
import sys
import Main as m

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.temp_files = []
        self.backtest_result = None
        self.global_result = None

    def initialize(self):
        self.show_home_page()
        self.showMaximized()
        if not os.path.exists(Files.FILE_PATH_YF):
            self.refresh_data()

    def show_home_page(self):
        del self.backtest_result
        m.setup_home_page(
            parent=self,
            run_backtest_callback=self.run_backtest,
            open_config_callback=self.open_config,
            refresh_data_callback=self.refresh_data
            )

    def open_config(self):
        Config.dynamic_config(Files.yahoo_assets, auto=False, parent=self)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(Files.yahoo_assets, Files.FILE_PATH_YF)

    def update_progress(self, value, message=None):
        m.update_progress_with_events(self.progress_bar, self.log_output, value, message)

    def show_backtest_page(self):
        self.progress_bar, self.log_output = m.setup_backtest_page(self)

    def show_plot(self, fig):
        m.display_plot_dialog(
            parent=self,
            fig=fig,
            window_title="Graph"
        )

    def run_backtest(self):
        self.show_backtest_page()
        self.update_progress(1, "Loading Data...")
        data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Files.FILE_PATH_YF)

        indicators_and_params, assets_to_backtest = Config.dynamic_config(assets_names, auto=True)

        self.update_progress(5, "Prepare Data...")

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
        equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
        self.update_progress(80, "Create Portfolio...")
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
        equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'All'})
        self.update_progress(90, "Create Portfolio...")
        self.backtest_result = equal_weights_asset_returns
        self.global_result = equal_weights_global_returns
        self.update_progress(100, "Plotting Results...")

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
            "Clusters Icicle": lambda: self.show_plot(Dashboard.plot_clusters_icicle(self.backtest_result, max_clusters=5, max_sub_clusters=3, max_sub_sub_clusters=2))
        }

        # Appelle setup_results_page et récupère la grille des graphiques
        right_bottom_layout = m.setup_results_page(
            parent=self,
            plots=plots,
            back_to_home_callback=self.show_home_page
        )

        # Génération et insertion dynamique des graphiques
        equity_plot = m.generate_plot_widget(Dashboard.plot_equity(self.global_result), show_legend=False)
        sharpe_plot = m.generate_plot_widget(Dashboard.plot_rolling_sharpe_ratio(self.global_result, length=1250), show_legend=False)
        drawdown_plot = m.generate_plot_widget(Dashboard.plot_rolling_drawdown(self.global_result, length=1250), show_legend=False)
        vol_plot = m.generate_plot_widget(Dashboard.plot_rolling_volatility(self.global_result), show_legend=False)

        right_bottom_layout.addWidget(equity_plot, 0, 0)
        right_bottom_layout.addWidget(sharpe_plot, 0, 1)
        right_bottom_layout.addWidget(drawdown_plot, 1, 0)
        right_bottom_layout.addWidget(vol_plot, 1, 1)

    def closeEvent(self, event):
        m.cleanup_temp_files()
        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    m.apply_global_styles(app)
    progress_window, progress_bar = m.setup_launch_page(None, "Launching App..")

    QApplication.processEvents()

    import os
    progress_bar.setValue(20)
    import Files
    progress_bar.setValue(30)
    import Get_Data
    progress_bar.setValue(40)
    import Process_Data
    progress_bar.setValue(50)
    import Backtest
    progress_bar.setValue(60)
    import Portfolio
    progress_bar.setValue(70)
    import Dashboard
    progress_bar.setValue(80)
    import Config
    progress_bar.setValue(90)
    main_window = MainApp()
    progress_bar.setValue(100)

    main_window.initialize()
    progress_window.close()
    
    sys.exit(app.exec())