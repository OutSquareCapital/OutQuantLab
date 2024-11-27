import Config
import UI   
import Portfolio
import Get_Data
import Process_Data
import Dashboard
import Backtest
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QProgressBar, QTextEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QVBoxLayout, QDialog
from PySide6.QtCore import QUrl
import tempfile
import os
from PySide6.QtGui import QPalette, QBrush, QPixmap

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Application")
        self.temp_files = []
        self.backtest_result = None
        self.all_strategies_results = None
        self.init_ui()
        self.resize(Config.DEFAULT_WIDTH+5, Config.DEFAULT_HEIGHT+5) 
        self.setStyleSheet("""
            * {
                font-family: 'QuickSand';
                font-size: 10px;
                font: bold;
            }
        """)

    def init_ui(self):
        
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        self.set_background_image(main_widget, Config.HOME_PAGE_PHOTO)

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

    def show_loading_page(self):
        """Affiche une page de chargement avec une image de fond."""
        self.loading_widget = QWidget()
        self.loading_layout = QVBoxLayout(self.loading_widget)
        self.set_background_image(self.loading_widget, Config.LOADING_PAGE_PHOTO)

        # Ajouter un espace pour pousser les éléments vers le bas
        self.loading_layout.addStretch()

        # Barre de progression
        self.progress_bar = QProgressBar(self.loading_widget)
        self.progress_bar.setRange(0, 100)
        self.loading_layout.addWidget(self.progress_bar)

        # Zone de texte pour afficher les logs
        self.log_output = QTextEdit(self.loading_widget)
        self.log_output.setReadOnly(True)
        self.log_output.setFixedHeight(100)
        self.loading_layout.addWidget(self.log_output)

        # Appliquer le layout
        self.loading_widget.setLayout(self.loading_layout)
        self.setCentralWidget(self.loading_widget)

    def update_progress(self, value, message=None):
        """Met à jour la barre de progression et remplace le message."""
        self.progress_bar.setValue(value)
        if message:
            self.log_output.clear()  # Efface les anciens messages
            self.log_output.append(message)  # Affiche uniquement le nouveau message

    def set_background_image(self, widget, image_path):
        palette = QPalette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        widget.setPalette(palette)
        widget.setAutoFillBackground(True)

    def show_plot(self, fig):
        # Génère le HTML avec Plotly inclus
        html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})

        html_content = html_content.replace(
            "<body>",
            f"<body style='background-color: {Config.BACKGROUND_GRAPH_WHITE};'>"
        )

        # Crée un fichier temporaire pour le HTML
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        with open(temp_file.name, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Stocke le fichier temporaire pour suppression ultérieure
        self.temp_files.append(temp_file.name)

        # Crée un QWebEngineView et charge le fichier
        dialog = QDialog(self)
        dialog.setWindowTitle("Graph")
        layout = QVBoxLayout(dialog)
        web_view = QWebEngineView(dialog)
        layout.addWidget(web_view)
        dialog.setLayout(layout)
        web_view.load(QUrl.fromLocalFile(temp_file.name))

        # Affiche le graphique
        dialog.resize(Config.DEFAULT_WIDTH+30, Config.DEFAULT_HEIGHT+40)
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
        self.show_loading_page()

        QApplication.processEvents()

        # Étape 1 : Chargement des données
        self.update_progress(1, "Loading Data...")
        data_prices_df, assets_names = Get_Data.load_prices_from_parquet(Config.FILE_PATH_YF)

        indicators_and_params, assets_to_backtest = UI.dynamic_config(assets_names, auto=True)

        # Étape 2 : Préparation des données
        self.update_progress(5, "Prepare Data...")
        QApplication.processEvents()

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

        # Étape 3 : Exécution du backtest
        self.update_progress(10, "Process Backtest...")
        QApplication.processEvents()

        raw_adjusted_returns_df = Backtest.process_backtest(
            prices_array,
            log_returns_array,
            volatility_adjusted_pct_returns_array,
            category_asset_names,
            dates_index,
            indicators_and_params,
            progress_callback=self.update_progress
        )

        # Étape 4 : Création du portfolio
        self.update_progress(70, "Create Portfolio...")
        QApplication.processEvents()

        equal_weights_asset_returns = Portfolio.calculate_daily_average_returns(raw_adjusted_returns_df, by_asset=True)
        equal_weights_global_returns = Portfolio.calculate_daily_average_returns(equal_weights_asset_returns, global_avg=True)
        equal_weights_global_returns = equal_weights_global_returns.rename(columns={equal_weights_global_returns.columns[0]: 'equal_weights'})
        self.backtest_result = equal_weights_asset_returns
        self.all_strategies_results=raw_adjusted_returns_df
        # Étape finale
        self.update_progress(100, "Backtest Done !")
        self.show_results_page()


    def show_results_page(self):
        """Affiche une page avec les boutons pour afficher les graphiques."""
        self.results_widget = QWidget()
        self.results_layout = QVBoxLayout()
        self.set_background_image(self.results_widget, Config.DASHBOARD_PAGE_PHOTO)
        # Bouton Back to Home Page
        back_to_home_button = QPushButton("Back to Home Page")
        back_to_home_button.clicked.connect(self.init_ui)
        self.results_layout.addWidget(back_to_home_button)

        plots = {
            "Equity Curves": lambda: self.show_plot(Dashboard.plot_equity(self.backtest_result)),
            "Rolling Volatility": lambda: self.show_plot(Dashboard.plot_rolling_volatility(self.backtest_result)),
            "Rolling Drawdowns": lambda: self.show_plot(Dashboard.plot_rolling_drawdown(self.backtest_result, length=1250)),
            "Rolling Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_rolling_sharpe_ratio(self.backtest_result, length=1250)),
            "Rolling Smoothed Skewness": lambda: self.show_plot(Dashboard.plot_rolling_smoothed_skewness(self.backtest_result, length=1250)),
            "Rolling Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_rolling_average_inverted_correlation(self.backtest_result, length=1250)),
            "Overall Sharpe Ratio": lambda: self.show_plot(Dashboard.plot_overall_sharpe_ratio(self.backtest_result)),
            "Overall Volatility": lambda: self.show_plot(Dashboard.plot_overall_volatility(self.backtest_result)),
            "Overall Average Drawdown": lambda: self.show_plot(Dashboard.plot_overall_average_drawdown(self.backtest_result, length=1250)),
            "Overall Average Inverted Correlation": lambda: self.show_plot(Dashboard.plot_overall_average_inverted_correlation(self.backtest_result)),
            "Overall Monthly Skew": lambda: self.show_plot(Dashboard.plot_overall_monthly_skew(self.backtest_result)),
            "Returns Distribution Violin": lambda: self.show_plot(Dashboard.plot_returns_distribution_violin(self.backtest_result)),
            "Returns Distribution Histogram": lambda: self.show_plot(Dashboard.plot_returns_distribution_histogram(self.backtest_result)),
            "Correlation Heatmap": lambda: self.show_plot(Dashboard.plot_correlation_heatmap(self.backtest_result)),
            "Clusters Icicle": lambda: self.show_plot(Dashboard.plot_clusters_icicle(self.backtest_result, max_clusters=5, max_sub_clusters=3, max_sub_sub_clusters=2)),
            "Sharpe Ratio Heatmap": lambda: self.show_plot(Dashboard.plot_sharpe_ratio_heatmap(self.all_strategies_results, param1='LenST', param2='LenLT')),
            "Overall Sharpe Ratio 3D Scatter": lambda: self.show_plot(Dashboard.plot_overall_sharpe_ratio_3d_scatter(self.all_strategies_results, params=['LenST', 'LenLT', 'MacLength'])),
        }

        for title, func in plots.items():
            button = QPushButton(title, self.results_widget)
            button.clicked.connect(func)
            self.results_layout.addWidget(button)

        self.results_widget.setLayout(self.results_layout)
        self.setCentralWidget(self.results_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainApp()
    main_window.show()
    sys.exit(app.exec())