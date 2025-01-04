from PySide6.QtWidgets import QMainWindow,  QApplication, QProgressBar, QTextEdit
from PySide6.QtGui import QCloseEvent
from UI import setup_home_page, setup_backtest_page, setup_results_page
from App.App_Backend import OutQuantLab
from DataBase import cleanup_temp_files, DataBaseQueries
from PySide6.QtGui import QIcon
from Utilitary import GLOBAL_STYLE


class OutQuantLabGUI(QApplication):
    def __init__(self, argv: list[str], database: DataBaseQueries) -> None:
        super().__init__(argv)
        self.setWindowIcon(QIcon(database.select['app_logo'].full_path))
        self.setStyleSheet(GLOBAL_STYLE)
        self.main_window = MainWindow(database=database)

class MainWindow(QMainWindow):
    def __init__(self, database: DataBaseQueries) -> None:
        super().__init__()
        self.progress_bar:QProgressBar
        self.log_output:QTextEdit
        self.oql = OutQuantLab(progress_callback=self.update_progress, database=database)
        self.show_home_page()
        self.showMaximized()

    def update_progress(
        self,
        value: int, 
        message: str) -> None:
        
        self.progress_bar.setValue(value)
        if message:
            self.log_output.clear()
            self.log_output.append(message)
        QApplication.processEvents()

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
        cleanup_temp_files()
        super().closeEvent(event)