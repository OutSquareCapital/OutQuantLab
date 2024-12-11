from PySide6.QtWidgets import QMainWindow

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.assets_collection = AssetsCollection()
        self.indicators_collection = IndicatorsCollection()
        self.show_home_page()
        self.showMaximized()

    def show_home_page(self):
        UI.setup_home_page(
            parent=self,
            run_backtest_callback=self.run_backtest,
            refresh_data_callback=self.refresh_data,
            assets_collection=self.assets_collection,
            indicators_collection=self.indicators_collection)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(self.assets_collection.get_all_entities_names(), FILE_PATH_YF)

    def update_progress(self, value, message):
        UI.update_progress_with_events(self.progress_bar, self.log_output, value, message)

    def show_backtest_page(self):
        self.progress_bar, self.log_output = UI.setup_backtest_page(self)

    def show_plot(self, fig):
        UI.display_plot_dialog(
            parent=self,
            fig=fig,
            window_title="Graph"
        )

    def run_backtest(self):
        self.show_backtest_page()
        self.update_progress(1, "Loading Data...")

        data_prices_df = Get_Data.load_prices(FILE_PATH_YF, self.assets_collection.get_active_entities_names())

        (
            prices_array,
            volatility_adjusted_pct_returns_array,
            log_returns_array,
            asset_names,
            dates_index,
        ) = Process_Data.process_data(data_prices_df)

        indicators_and_params = self.indicators_collection.get_indicators_and_parameters_for_backtest()

        self.update_progress(10, "Processing Backtest...")

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            asset_names,
            dates_index,
            indicators_and_params,
            progress_callback=self.update_progress
        )

        self.update_progress(80, "Creating Portfolio...")
        backtest_result = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df.dropna(axis=0),  
                                                                                by_method=True, 
                                                                                by_asset=True)
                                                                                
        global_result = Portfolio.calculate_daily_average_returns(backtest_result, 
                                                                global_avg=True)

        self.update_progress(100, "Plotting Results...")

        self.show_results_page(backtest_result, global_result)

    def show_results_page(self, backtest_result, global_result):
        plots = {
            "Equity": lambda: self.show_plot(Dashboard.plot_equity(backtest_result)),
            "Total Returns %": lambda: self.show_plot(Dashboard.plot_overall_returns(backtest_result)),
            "Volatility": lambda: self.show_plot(Dashboard.plot_rolling_volatility(backtest_result)),
            "Drawdown": lambda: self.show_plot(Dashboard.plot_rolling_drawdown(backtest_result, length=1250)),
            "Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_rolling_sharpe_ratio(backtest_result, length=1250)),
            "Smoothed Skewness": lambda: self.show_plot(Dashboard.plot_rolling_smoothed_skewness(backtest_result, length=1250)),
            "Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_rolling_average_inverted_correlation(backtest_result, length=1250)),
            "Overall Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_overall_sharpe_ratio(backtest_result)),
            "Overall Volatility": lambda: self.show_plot(Dashboard.plot_overall_volatility(backtest_result)),
            "Average Drawdown": lambda: self.show_plot(Dashboard.plot_overall_average_drawdown(backtest_result, length=1250)),
            "Overall Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_overall_average_inverted_correlation(backtest_result)),
            "Monthly Skew": lambda: self.show_plot(Dashboard.plot_overall_monthly_skew(backtest_result)),
            "Distribution Violin": lambda: self.show_plot(Dashboard.plot_returns_distribution_violin(backtest_result)),
            "Distribution Histogram": lambda: self.show_plot(Dashboard.plot_returns_distribution_histogram(backtest_result)),
            "Correlation Heatmap": lambda: self.show_plot(Dashboard.plot_correlation_heatmap(backtest_result)),
            "Clusters Icicle": lambda: self.show_plot(Dashboard.plot_clusters_icicle(backtest_result, max_clusters=5, max_sub_clusters=3, max_sub_sub_clusters=2))
        }
        metrics: List[float] = [
            round(Dashboard.calculate_overall_returns(global_result).item(
                                                                        ), 2),
            round(Dashboard.calculate_overall_sharpe_ratio(global_result
                                                           ).item(), 2),
            round(Dashboard.calculate_overall_average_drawdown(global_result, length=1250
                                                               ).item(), 2),
            round(Dashboard.calculate_overall_volatility(global_result
                                                         ).item(), 2),
            round(Dashboard.calculate_overall_monthly_skew(global_result
                                                           ).item(), 2)
        ]
        bottom_layout = UI.setup_results_page(
                                            parent=self,
                                            plots=plots,
                                            back_to_home_callback=self.show_home_page,
                                            metrics=metrics
                                            )

        #'''
        equity_plot = UI.generate_plot_widget(Dashboard.plot_equity(global_result), show_legend=False)
        sharpe_plot = UI.generate_plot_widget(Dashboard.plot_rolling_sharpe_ratio(global_result, length=1250), show_legend=False)
        drawdown_plot = UI.generate_plot_widget(Dashboard.plot_rolling_drawdown(global_result, length=1250), show_legend=False)
        vol_plot = UI.generate_plot_widget(Dashboard.plot_rolling_volatility(global_result), show_legend=False)
        distribution_plot = UI.generate_plot_widget(Dashboard.plot_returns_distribution_histogram(global_result), show_legend=False)
        violin_plot = UI.generate_plot_widget(Dashboard.plot_returns_distribution_violin(global_result), show_legend=False)
        
        bottom_layout.addWidget(equity_plot, 0, 0)
        bottom_layout.addWidget(drawdown_plot, 1, 0)
        bottom_layout.addWidget(sharpe_plot, 0, 1)
        bottom_layout.addWidget(vol_plot, 1, 1)
        bottom_layout.addWidget(distribution_plot, 0, 2)
        bottom_layout.addWidget(violin_plot, 1, 2)
        #'''

    def closeEvent(self, event):
        self.assets_collection.save()
        self.indicators_collection.save()
        UI.cleanup_temp_files()
        super().closeEvent(event)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication
    import UI
    app = QApplication(sys.argv)
    UI.apply_global_styles(app)
    progress_window, progress_bar = UI.setup_launch_page(None)

    QApplication.processEvents()
    from Files import FILE_PATH_YF
    progress_bar.setValue(20)
    progress_bar.setValue(30)
    import Get_Data
    progress_bar.setValue(40)
    import Process_Data
    from typing import List
    progress_bar.setValue(50)
    import Backtest
    progress_bar.setValue(60)
    import Portfolio
    progress_bar.setValue(70)
    import Dashboard
    progress_bar.setValue(80)
    from Config import AssetsCollection, IndicatorsCollection
    progress_bar.setValue(90)
    main_window = MainApp()
    progress_bar.setValue(100)

    main_window.initialize()
    progress_window.close()
    
    sys.exit(app.exec())