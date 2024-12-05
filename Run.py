from PySide6.QtWidgets import QMainWindow

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.methods_funcs=Config.get_all_methods_from_module('Signals')
        self.methods_names=list(self.methods_funcs.keys())
        self.methods_to_test = Config.load_config_file(METHODS_TO_TEST_FILE)
        self.methods_classes=Config.load_config_file(METHODS_CLASSES_FILE)
        self.assets_names=Get_Data.load_asset_names(FILE_PATH_YF)
        self.assets_to_test = Config.load_config_file(ASSETS_TO_TEST_CONFIG_FILE)
        self.assets_classes=Config.load_config_file(ASSETS_CLASSES_FILE)
        self.params_config = Config.load_config_file(PARAM_CONFIG_FILE)
        self.show_home_page()
        self.showMaximized()

    def show_home_page(self):
        Main.setup_home_page(
            parent=self,
            run_backtest_callback=self.run_backtest,
            refresh_data_callback=self.refresh_data,
            assets_to_test=self.assets_to_test,
            assets_names=self.assets_names,
            methods_names=self.methods_names,
            methods_params=self.params_config,
            methods_to_test=self.methods_to_test,
            assets_classes=self.assets_classes,
            methods_classes=self.methods_classes)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(self.assets_names, FILE_PATH_YF)

    def update_progress(self, value, message=None):
        Main.update_progress_with_events(self.progress_bar, self.log_output, value, message)

    def show_backtest_page(self):
        self.progress_bar, self.log_output = Main.setup_backtest_page(self)

    def show_plot(self, fig):
        Main.display_plot_dialog(
            parent=self,
            fig=fig,
            window_title="Graph"
        )

    def run_backtest(self):
        self.show_backtest_page()
        self.update_progress(1, "Loading Data...")

        data_prices_df = Get_Data.load_prices(FILE_PATH_YF, self.assets_names)
        (
            prices_array,
            volatility_adjusted_pct_returns_array,
            log_returns_array,
            category_asset_names,
            dates_index,
        ) = Process_Data.process_data(
            self.assets_names,
            data_prices_df,
            self.assets_to_test,
        )

        indicators_and_params = Config.dynamic_config(self.methods_funcs, self.methods_to_test, self.params_config)


        self.update_progress(10, "Processing Backtest...")

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            category_asset_names,
            dates_index,
            indicators_and_params,
            progress_callback=self.update_progress
        )

        self.update_progress(80, "Creating Portfolio...")
        equal_weights_method_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df,  by_method=True, by_asset=True)
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_method_returns, global_avg=True)

        backtest_result = equal_weights_method_returns

        global_result = equal_weights_global_returns

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
        metrics = [
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
        bottom_layout = Main.setup_results_page(
                                            parent=self,
                                            plots=plots,
                                            back_to_home_callback=self.show_home_page,
                                            metrics=metrics
                                            )

        '''
        equity_plot = Main.generate_plot_widget(Dashboard.plot_equity(global_result), show_legend=False)
        sharpe_plot = Main.generate_plot_widget(Dashboard.plot_rolling_sharpe_ratio(global_result, length=1250), show_legend=False)
        drawdown_plot = Main.generate_plot_widget(Dashboard.plot_rolling_drawdown(global_result, length=1250), show_legend=False)
        vol_plot = Main.generate_plot_widget(Dashboard.plot_rolling_volatility(global_result), show_legend=False)
        distribution_plot = Main.generate_plot_widget(Dashboard.plot_returns_distribution_histogram(global_result), show_legend=False)
        violin_plot = Main.generate_plot_widget(Dashboard.plot_returns_distribution_violin(global_result), show_legend=False)
        
        bottom_layout.addWidget(equity_plot, 0, 0)
        bottom_layout.addWidget(drawdown_plot, 1, 0)
        bottom_layout.addWidget(sharpe_plot, 0, 1)
        bottom_layout.addWidget(vol_plot, 1, 1)
        bottom_layout.addWidget(distribution_plot, 0, 2)
        bottom_layout.addWidget(violin_plot, 1, 2)
        '''

    def closeEvent(self, event):
        Main.cleanup_temp_files()
        Config.save_config_file(ASSETS_TO_TEST_CONFIG_FILE, self.assets_to_test, 3)
        Config.save_config_file(PARAM_CONFIG_FILE, self.params_config, 3)
        Config.save_config_file(METHODS_TO_TEST_FILE, self.methods_to_test, 3)
        Config.save_config_file(ASSETS_CLASSES_FILE, self.assets_classes, 3)
        Config.save_config_file(METHODS_CLASSES_FILE, self.methods_classes, 3)
        super().closeEvent(event)

if __name__ == "__main__":

    import sys
    import UI_Common
    from PySide6.QtWidgets import QApplication
    import Main

    app = QApplication(sys.argv)

    UI_Common.apply_global_styles(app)
    progress_window, progress_bar = UI_Common.setup_launch_page(None)

    QApplication.processEvents()

    progress_bar.setValue(20)
    from Files import FILE_PATH_YF, ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE, METHODS_TO_TEST_FILE, ASSETS_CLASSES_FILE, METHODS_CLASSES_FILE
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