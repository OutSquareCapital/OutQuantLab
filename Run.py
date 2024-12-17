from PySide6.QtWidgets import QMainWindow

class MainApp(QMainWindow):

    def __init__(self):
        super().__init__()

    def initialize(self):
        self.assets_collection = AssetsCollection()
        self.indicators_collection = IndicatorsCollection()
        self.dashboards = Dashboards(length=1250)
        self.show_home_page()
        self.showMaximized()

    def show_home_page(self):
        UI.setup_home_page(
        parent=self,
        run_backtest_callback=self.run_backtest,
        refresh_data_callback=self.refresh_data,
        assets_collection=self.assets_collection,
        indicators_collection=self.indicators_collection
        )

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(self.assets_collection.get_all_entities_names(), FILE_PATH_YF)

    def update_progress(self, value, message):
        UI.update_progress_with_events(self.progress_bar, self.log_output, value, message)

    def run_backtest(self):
        self.progress_bar, self.log_output = UI.setup_backtest_page(self)
        
        self.update_progress(1, "Processing Backtest...")

        config = BacktestConfig(
        FILE_PATH_YF,
        self.assets_collection.get_active_entities_names(),
        self.indicators_collection.get_indicators_and_parameters_for_backtest()
        )

        raw_adjusted_returns_df = Backtest.process_backtest(
        config.signals_array,
        config.data_array,
        config.volatility_adjusted_pct_returns,
        config.dates_index,
        config.indicators_and_params,
        config.multi_index,
        self.update_progress
        )
        
        self.dashboards.sub_portfolios = Portfolio.calculate_daily_average_returns(
        raw_adjusted_returns_df.dropna(axis=0),  
        by_method=True, 
        by_asset=True)

        self.dashboards.global_portfolio = Portfolio.calculate_daily_average_returns(
        self.dashboards.sub_portfolios, 
        global_avg=True
        )

        
        self.update_progress(100, "Plotting Results...")

        self.show_results_page()

    def show_results_page(self):
        
        self.dashboards.metrics = self.dashboards.calculate_metrics()
        
        bottom_layout = UI.setup_results_page(
        parent=self,
        dashboards=self.dashboards,
        back_to_home_callback=self.show_home_page,
        metrics=self.dashboards.metrics
        )

        equity_plot = UI.generate_plot_widget((self.dashboards.plot("Equity", global_plot=True)), show_legend=False)
        sharpe_plot = UI.generate_plot_widget(self.dashboards.plot("Rolling Sharpe Ratio", global_plot=True), show_legend=False)
        drawdown_plot = UI.generate_plot_widget(self.dashboards.plot("Rolling Drawdown", global_plot=True), show_legend=False)
        vol_plot = UI.generate_plot_widget(self.dashboards.plot("Rolling Volatility", global_plot=True), show_legend=False)
        distribution_plot = UI.generate_plot_widget(self.dashboards.plot("Returns Distribution Histogram", global_plot=True), show_legend=False)
        violin_plot = UI.generate_plot_widget(self.dashboards.plot("Returns Distribution Violin", global_plot=True), show_legend=False)
        
        bottom_layout.addWidget(equity_plot, 0, 0)
        bottom_layout.addWidget(drawdown_plot, 1, 0)
        bottom_layout.addWidget(sharpe_plot, 0, 1)
        bottom_layout.addWidget(vol_plot, 1, 1)
        bottom_layout.addWidget(distribution_plot, 0, 2)
        bottom_layout.addWidget(violin_plot, 1, 2)

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
    progress_bar.setValue(30)
    import Get_Data
    progress_bar.setValue(40)
    from Process_Data import BacktestConfig
    progress_bar.setValue(50)
    import Backtest
    progress_bar.setValue(60)
    import Portfolio
    progress_bar.setValue(70)
    from Dashboard import Dashboards
    progress_bar.setValue(80)
    from Config import AssetsCollection, IndicatorsCollection
    progress_bar.setValue(90)
    main_window = MainApp()
    progress_bar.setValue(100)

    main_window.initialize()
    progress_window.close()
    
    sys.exit(app.exec())