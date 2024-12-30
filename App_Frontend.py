from PySide6.QtWidgets import QMainWindow,  QApplication, QProgressBar, QTextEdit
from PySide6.QtGui import QCloseEvent
import sys
import UI
from Database import DataBaseQueries, cleanup_temp_files


class MainApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> None:
        self.progress_bar:QProgressBar
        self.log_output:QTextEdit
        self.outquantlab = OutQuantLab(progress_callback=self.update_progress, database=db)
        self.show_home_page()
        self.showMaximized()


    def show_home_page(self) -> None:
        UI.setup_home_page(
        parent=self,
        run_backtest_callback=self.run_backtest,
        assets_collection=self.outquantlab.assets_collection,
        indicators_collection=self.outquantlab.indicators_collection,
        assets_clusters=self.outquantlab.assets_clusters,
        indicators_clusters=self.outquantlab.indicators_clusters,
        background=db.home_page.full_path
        )

    def update_progress(self, value: int, message: str) -> None:
        UI.update_progress_with_events(progress_bar=self.progress_bar, log_output=self.log_output, value=value, message=message)


    def run_backtest(self) -> None:
        self.progress_bar, self.log_output = UI.setup_backtest_page(parent=self, background=db.loading_page.full_path)
        self.outquantlab.run_backtest()
        self.show_results_page()

    def show_results_page(self) -> None:

        UI.setup_results_page(
        parent=self,
        dashboards=self.outquantlab.dashboards,
        back_to_home_callback=self.show_home_page,
        metrics=self.outquantlab.dashboards.metrics,
        background=db.dashboard_page.full_path
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.outquantlab.save_all()
        cleanup_temp_files()
        super().closeEvent(event=event)

if __name__ == "__main__":
    db = DataBaseQueries()
    app = QApplication(arg__1=sys.argv)
    UI.apply_global_styles(app=app, background= db.app_logo.full_path)
    progress_window, progress_bar = UI.setup_launch_page(db.app_logo.full_path)
    QApplication.processEvents()
    progress_bar.setValue(30)
    from App_Backend import OutQuantLab
    main_window = MainApp()
    progress_bar.setValue(100)
    progress_window.close()
    main_window.initialize()
    sys.exit(app.exec())