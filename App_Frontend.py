from PySide6.QtWidgets import QMainWindow

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

    def initialize(self):
        self.progress_bar:QProgressBar
        self.log_output:QTextEdit
        self.outquantlab = OutQuantLab(self.update_progress)
        self.show_home_page()
        self.showMaximized()

    def show_home_page(self):
        UI.setup_home_page(
        parent=self,
        run_backtest_callback=self.run_backtest,
        refresh_data_callback=self.outquantlab.refresh_data,
        assets_collection=self.outquantlab.assets_collection,
        indicators_collection=self.outquantlab.indicators_collection
        )

    def update_progress(self, value, message):
        UI.update_progress_with_events(self.progress_bar, self.log_output, value, message)


    def run_backtest(self):
        self.progress_bar, self.log_output = UI.setup_backtest_page(self)
        self.outquantlab.run_backtest()
        self.show_results_page()

    def show_results_page(self):
        self.outquantlab.dashboards.metrics = self.outquantlab.dashboards.calculate_metrics()

        UI.setup_results_page(
        parent=self,
        dashboards=self.outquantlab.dashboards,
        back_to_home_callback=self.show_home_page,
        metrics=self.outquantlab.dashboards.metrics
        )

    def closeEvent(self, event):
        self.outquantlab.close()
        UI.cleanup_temp_files()
        super().closeEvent(event)

if __name__ == "__main__":

    import sys
    from PySide6.QtWidgets import QApplication, QProgressBar, QTextEdit
    import UI
    app = QApplication(sys.argv)
    UI.apply_global_styles(app)
    progress_window, progress_bar = UI.setup_launch_page(None)

    QApplication.processEvents()
    progress_bar.setValue(30)
    from App_Backend import OutQuantLab
    main_window = MainApp()
    progress_bar.setValue(100)

    main_window.initialize()
    progress_window.close()
    
    sys.exit(app.exec())