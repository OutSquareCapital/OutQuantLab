from PySide6.QtWidgets import QMainWindow,  QApplication, QProgressBar, QTextEdit
from PySide6.QtGui import QCloseEvent
import sys
import UI
from App_Backend import OutQuantLab
from DataBase import cleanup_temp_files
from PySide6.QtGui import QIcon
from Utilitary import GLOBAL_STYLE

class MainApp(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

    def initialize(self) -> None:
        self.progress_bar:QProgressBar
        self.log_output:QTextEdit
        self.ql = OutQuantLab(progress_callback=self.update_progress)
        self.apply_global_styles(background=self.ql.db.select['app_logo'].full_path)
        self.show_home_page()
        self.showMaximized()

    def apply_global_styles(self, background: str) -> None:
        app.setWindowIcon(QIcon(background)) 
        app.setStyleSheet(GLOBAL_STYLE)

    def show_home_page(self) -> None:
        UI.setup_home_page(
        parent=self,
        run_backtest_callback=self.run_backtest,
        assets_collection=self.ql.assets_collection,
        indicators_collection=self.ql.indicators_collection,
        assets_clusters=self.ql.assets_clusters,
        indicators_clusters=self.ql.indicators_clusters,
        background=self.ql.db.select['home_page'].full_path
        )

    def update_progress(self, value: int, message: str) -> None:
        UI.update_progress_with_events(
            progress_bar=self.progress_bar, 
            log_output=self.log_output, value=value, message=message)

    def run_backtest(self) -> None:
        self.progress_bar, self.log_output = UI.setup_backtest_page(parent=self, background=self.ql.db.select['loading_page'].full_path)
        self.ql.run_backtest()
        self.show_results_page()

    def show_results_page(self) -> None:
        UI.setup_results_page(
        parent=self,
        global_returns_df=self.ql.global_portfolio,
        sub_returns_df=self.ql.sub_portfolios,
        graphs=self.ql.grph,
        back_to_home_callback=self.show_home_page,
        metrics=self.ql.grph.get_metrics(returns_df=self.ql.global_portfolio),
        background=self.ql.db.select['dashboard_page'].full_path
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.ql.save_all()
        cleanup_temp_files()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.initialize()
    sys.exit(app.exec())