from PySide6.QtWidgets import QMainWindow, QApplication, QProgressBar, QTextEdit, QStackedWidget, QWidget
from UI import setup_home_page, setup_backtest_page, setup_results_page
from App.App_Backend import OutQuantLab
from DataBase import DataBaseQueries
from UI.Results_UI import GraphsWidget
from Utilitary import GLOBAL_STYLE, APP_NAME
from PySide6.QtGui import QIcon

class OutQuantLabGUI(QApplication):
    def __init__(self) -> None:
        super().__init__()
        self.progress_bar: QProgressBar | None = None
        self.log_output: QTextEdit | None = None
        self.aboutToQuit.connect(self.cleanup) 
        self.oql = OutQuantLab(progress_callback=self.update_progress, database=DataBaseQueries())
        self.setup_pages()
        print(f"{APP_NAME} initialized")

    def setup_pages(self) -> None:
        self.setWindowIcon(QIcon(self.oql.db.select['app_logo'].full_path))
        self.setStyleSheet(GLOBAL_STYLE)
        self.main_window = QMainWindow()
        self.main_window.setWindowTitle(APP_NAME)
        self.stacked_widget = QStackedWidget()
        self.home_page = QWidget()
        self.backtest_page = QWidget()
        self.results_page = QWidget()
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.backtest_page)
        self.stacked_widget.addWidget(self.results_page)

        setup_home_page(
            parent=self.home_page,
            run_backtest_callback=self.run_backtest,
            assets_collection=self.oql.assets_collection,
            indics_collection=self.oql.indics_collection,
            assets_clusters=self.oql.assets_clusters,
            indicators_clusters=self.oql.indics_clusters
        )

        self.progress_bar, self.log_output = setup_backtest_page(
            parent=self.backtest_page,
            background=self.oql.db.select['loading_page'].full_path
        )
        self.graphs_widget: GraphsWidget = setup_results_page(
            parent=self.results_page,
            back_to_home_callback=self.show_home_page,
            background=self.oql.db.select['dashboard_page'].full_path,
            graphs=self.oql.grphs
        )
        self.main_window.setCentralWidget(self.stacked_widget)
        self.main_window.showMaximized()

    def show_home_page(self) -> None:
        self.stacked_widget.setCurrentWidget(self.home_page)

    def run_backtest(self) -> None:
        self.stacked_widget.setCurrentWidget(self.backtest_page)
        self.oql.run_backtest()
        self.show_results_page()
    
    def show_results_page(self) -> None:
        self.graphs_widget.update_graphs(new_graphs=self.oql.grphs)
        self.stacked_widget.setCurrentWidget(self.results_page)

    def update_progress(self, value: int, message: str) -> None:
        if self.progress_bar is not None:
            self.progress_bar.setValue(value)
        if message and self.log_output is not None:
            self.log_output.clear()
            self.log_output.append(message)
        QApplication.processEvents()

    def cleanup(self) -> None:
        self.oql.save_all()
        self.oql.db.cleanup_temp_files()