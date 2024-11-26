import Config
import UI   
import Portfolio
import Get_Data
import Process_Data
import Dashboard
import Backtest
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QDialog
from PySide6.QtCore import QUrl
import tempfile
import os

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.temp_files = []
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Bouton Run Backtest
        backtest_button = QPushButton("Run Backtest")
        backtest_button.clicked.connect(self.run_backtest)
        main_layout.addWidget(backtest_button)

        # Bouton Open Config
        config_button = QPushButton("Open Config")
        config_button.clicked.connect(self.open_config)
        main_layout.addWidget(config_button)

        # Bouton Refresh Data
        refresh_button = QPushButton("Refresh Data")
        refresh_button.clicked.connect(self.refresh_data)
        main_layout.addWidget(refresh_button)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def show_plot(self, fig):
        # Génère le HTML avec Plotly inclus
        html_content = fig.to_html(full_html=True, include_plotlyjs=True)

        # Crée un fichier temporaire pour le HTML
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        with open(temp_file.name, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Stocke le fichier temporaire pour suppression ultérieure
        self.temp_files.append(temp_file.name)

        # Crée un QWebEngineView et charge le fichier
        dialog = QDialog(self)
        dialog.setWindowTitle("Graphique")
        layout = QVBoxLayout(dialog)
        web_view = QWebEngineView(dialog)
        layout.addWidget(web_view)
        dialog.setLayout(layout)
        web_view.load(QUrl.fromLocalFile(temp_file.name))

        # Affiche le graphique
        dialog.resize(800, 600)
        dialog.exec()

    def cleanup_temp_files(self):
        """Supprime tous les fichiers temporaires stockés."""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier temporaire {temp_file} : {e}")

    def closeEvent(self, event):
        """Nettoie les fichiers temporaires avant la fermeture."""
        self.cleanup_temp_files()
        super().closeEvent(event)

    def open_config(self):
        UI.dynamic_config(Config.yahoo_assets, auto=False, parent=self)

    def refresh_data(self):
        Get_Data.get_yahoo_finance_data(Config.yahoo_assets, Config.FILE_PATH_YF)

    def run_backtest(self):

        data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Config.FILE_PATH_YF)

        indicators_and_params, assets_to_backtest = UI.dynamic_config(assets_names, auto=True)

        (
            prices_array,
            volatility_adjusted_pct_returns_array,
            log_returns_array,
            category_asset_names,
            dates_index,
        ) = Process_Data.process_data(
            assets_names,
            data_prices_df,
            assets_to_backtest,
        )

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            category_asset_names,
            dates_index,
            indicators_and_params
        )

        equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
        equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'equal_weights'})
        test_returns_df = equal_weights_asset_returns

        fig = Dashboard.plot_equity(test_returns_df)
        fig2 = Dashboard.plot_correlation_heatmap(test_returns_df)
        self.show_plot(fig)
        self.show_plot(fig2)
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())