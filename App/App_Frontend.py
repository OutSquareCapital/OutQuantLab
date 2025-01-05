from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar, QTextEdit
from UI import setup_home_page, setup_backtest_page, setup_results_page
from App.App_Backend import OutQuantLab
from DataBase import DataBaseQueries
from Utilitary import GLOBAL_STYLE, APP_NAME
from PySide6.QtGui import QIcon

class OutQuantLabGUI(QApplication):
    def __init__(self) -> None:
        super().__init__()
        database = DataBaseQueries()
        self.database = database
        self.setWindowIcon(QIcon(database.select['app_logo'].full_path))
        self.setStyleSheet(GLOBAL_STYLE)
        
        self.progress_bar: QProgressBar | None = None
        self.log_output: QTextEdit | None = None
        self.aboutToQuit.connect(self.cleanup) 
        self.outquantlab = OutQuantLab(progress_callback=self.update_progress, database=database)
        self.main_window = QMainWindow()
        
        self.show_home_page()
        print(f"{APP_NAME} initialized")
        self.main_window.showMaximized()

    def show_home_page(self) -> None:
        setup_home_page(
            parent=self.main_window,
            run_backtest_callback=self.run_backtest,
            assets_collection=self.outquantlab.assets_collection,
            indics_collection=self.outquantlab.indics_collection,
            assets_clusters=self.outquantlab.assets_clusters,
            indicators_clusters=self.outquantlab.indics_clusters,
            background=self.database.select['home_page'].full_path
        )

    def run_backtest(self) -> None:
        self.progress_bar, self.log_output = setup_backtest_page(
            parent=self.main_window,
            background=self.database.select['loading_page'].full_path
        )
        self.outquantlab.run_backtest()
        self.show_results_page()

    def show_results_page(self) -> None:
        setup_results_page(
            parent=self.main_window,
            global_returns_df=self.outquantlab.global_portfolio,
            sub_returns_df=self.outquantlab.sub_portfolios,
            graphs=self.outquantlab.grph,
            back_to_home_callback=self.show_home_page,
            background=self.database.select['dashboard_page'].full_path
        )

    def update_progress(self, value: int, message: str) -> None:
        if self.progress_bar is not None:
            self.progress_bar.setValue(value)
        if message and self.log_output is not None:
            self.log_output.clear()
            self.log_output.append(message)
        QApplication.processEvents()

    def cleanup(self) -> None:
        self.outquantlab.save_all()
        self.database.cleanup_temp_files()