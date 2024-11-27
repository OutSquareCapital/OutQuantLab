import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QProgressBar, QPushButton
from PySide6.QtGui import QIcon
import Config
from Main_UI import set_background_image, create_loading_page, update_progress, create_plot_dialog, cleanup_temp_files

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(Config.APP_ICON_PHOTO)) 
        self.setWindowTitle("Main Application")
        self.temp_files = []
        self.backtest_result = None
        self.all_strategies_results = None
        self.init_ui()
        self.resize(Config.DEFAULT_WIDTH, Config.DEFAULT_HEIGHT) 
        self.setStyleSheet("""
            * {
                font-family: 'QuickSand';
                font-size: 10px;
                font: bold;
            }
        """)
        if not os.path.exists(Config.FILE_PATH_YF):
            self.refresh_data()

    def init_ui(self):
        
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        set_background_image(main_widget, Config.HOME_PAGE_PHOTO)

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
        self.loading_widget, self.progress_bar, self.log_output = create_loading_page(Config.LOADING_PAGE_PHOTO)
        self.setCentralWidget(self.loading_widget)

    def update_progress(self, value, message=None):
        update_progress(self.progress_bar, self.log_output, value, message)

    def show_plot(self, fig):
        temp_file = create_plot_dialog(
            fig,
            window_title="Graph",
            default_width=Config.DEFAULT_WIDTH,
            default_height=Config.DEFAULT_HEIGHT,
            background_color=Config.BACKGROUND_GRAPH_WHITE,
        )
        # Stocke le fichier temporaire pour suppression ultérieure
        self.temp_files.append(temp_file)

    def closeEvent(self, event):
        """Nettoie les fichiers temporaires avant la fermeture."""
        cleanup_temp_files(self.temp_files)
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
        set_background_image(self.results_widget, Config.DASHBOARD_PAGE_PHOTO)
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
            #"Overall Sharpe Ratio 3D Scatter": lambda: self.show_plot(Dashboard.plot_overall_sharpe_ratio_3d_scatter(self.all_strategies_results, params=['LenST', 'LenLT', 'MacLength'])),
        }

        for title, func in plots.items():
            button = QPushButton(title, self.results_widget)
            button.clicked.connect(func)
            self.results_layout.addWidget(button)

        self.results_widget.setLayout(self.results_layout)
        self.setCentralWidget(self.results_widget)



if __name__ == "__main__":
    # Initialisation de l'application Qt
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(Config.APP_ICON_PHOTO))  # Définir l'icône de l'application

    # Création de la fenêtre de chargement temporaire
    loading_window = QMainWindow()
    loading_window.setWindowTitle("Launching App..")
    loading_layout = QVBoxLayout()
    loading_widget = QWidget(loading_window)
    loading_window.setCentralWidget(loading_widget)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    loading_layout.addWidget(progress_bar)
    loading_widget.setLayout(loading_layout)

    loading_window.resize(400, 200)
    loading_window.show()

    # Mise à jour de la progression pendant le chargement
    QApplication.processEvents()
    progress_bar.setValue(10)

    # Importations différées avec progression
    import Get_Data
    progress_bar.setValue(30)
    import Process_Data
    progress_bar.setValue(40)
    import Backtest
    progress_bar.setValue(50)
    import Portfolio
    progress_bar.setValue(60)
    import Dashboard
    progress_bar.setValue(70)
    import UI
    progress_bar.setValue(80)
    import os
    progress_bar.setValue(90)

    # Initialisation de la fenêtre principale
    main_window = MainApp()
    progress_bar.setValue(100)

    # Fermeture de la fenêtre de chargement et affichage de l'application principale
    loading_window.close()
    main_window.show()

    sys.exit(app.exec())
