from PySide6.QtWidgets import QApplication, QProgressBar, QTextEdit
from DataBase import DataBaseQueries
from App.App_Backend import OutQuantLab
from App.App_Frontend import MainWindow
from PySide6.QtGui import QIcon
from Utilitary import GLOBAL_STYLE, APP_NAME

class OutQuantLabCLI:
    def __init__(self) -> None:
        database = DataBaseQueries()
        self.oql: OutQuantLab = OutQuantLab(
            progress_callback=self.handle_progress,
            database=database
        )
        print(f"{APP_NAME} initialized")
        self.run()

    def handle_progress(self, progress: int, message: str) -> None:
        print(f"[{progress}%] {message}")

    def run(self) -> None:
        self.oql.run_backtest()
        metrics: dict[str, float] = self.oql.grph.get_metrics(returns_df=self.oql.global_portfolio)
        for metric, value in metrics.items():
            print(f"{metric}: {value}")

class OutQuantLabGUI(QApplication):
    def __init__(self) -> None:
        super().__init__()
        database = DataBaseQueries()
        self.setWindowIcon(QIcon(database.select['app_logo'].full_path))
        self.setStyleSheet(GLOBAL_STYLE)
        self.progress_bar:QProgressBar
        self.log_output:QTextEdit
        outquantlab = OutQuantLab(progress_callback=self.update_progress, database=database)
        print(f"{APP_NAME} initialized")
        self.main_window = MainWindow(outquantlab=outquantlab)


    def update_progress(
        self,
        value: int, 
        message: str) -> None:
        
        self.progress_bar.setValue(value)
        if message:
            self.log_output.clear()
            self.log_output.append(message)
        QApplication.processEvents()
