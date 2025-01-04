import sys
from App import OutQuantLabGUI, OutQuantLab
from DataBase import DataBaseQueries

def handle_progress(progress: int, message: str) -> None:
    print(f"[{progress}%] {message}")

def run(gui: bool = False) -> None:
    database = DataBaseQueries()
    if gui:
        app = OutQuantLabGUI(argv=sys.argv, database=database)
        sys.exit(app.exec())
    else:
        oql = OutQuantLab(progress_callback=handle_progress, database=database)
        oql.run_backtest()


run(gui=True)