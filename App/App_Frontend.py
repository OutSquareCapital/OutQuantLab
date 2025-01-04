from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QCloseEvent
from UI import setup_home_page, setup_backtest_page, setup_results_page
from App.App_Backend import OutQuantLab

class MainWindow(QMainWindow):
    def __init__(self, outquantlab: OutQuantLab) -> None:
        super().__init__()
        self.oql: OutQuantLab = outquantlab
        self.show_home_page()
        self.showMaximized()

    def show_home_page(self) -> None:
        setup_home_page(
        parent=self,
        run_backtest_callback=self.run_backtest,
        assets_collection=self.oql.assets_collection,
        indicators_collection=self.oql.indicators_collection,
        assets_clusters=self.oql.assets_clusters,
        indicators_clusters=self.oql.indicators_clusters,
        background=self.oql.db.select['home_page'].full_path
        )

    def run_backtest(self) -> None:
        self.progress_bar, self.log_output = setup_backtest_page(
            parent=self, 
            background=self.oql.db.select['loading_page'].full_path)
        self.oql.run_backtest()
        self.show_results_page()

    def show_results_page(self) -> None:
        setup_results_page(
        parent=self,
        global_returns_df=self.oql.global_portfolio,
        sub_returns_df=self.oql.sub_portfolios,
        graphs=self.oql.grph,
        back_to_home_callback=self.show_home_page,
        background=self.oql.db.select['dashboard_page'].full_path
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        self.oql.save_all()
        self.oql.db.cleanup_temp_files()
        super().closeEvent(event)