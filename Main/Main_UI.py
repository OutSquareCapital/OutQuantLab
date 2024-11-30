from PySide6.QtWidgets import (QWidget, 
                               QHBoxLayout, 
                               QVBoxLayout, 
                               QProgressBar, 
                               QTextEdit,
                               QPushButton, 
                               QMainWindow, 
                               QApplication, 
                               QSizePolicy, 
                               QSpacerItem,
                               QGridLayout,
                               QLabel,
                               QSlider
                               )
from Files import ( 
                    BACKTEST_PAGE_PHOTO,
                    HOME_PAGE_PHOTO,
                    DASHBOARD_PAGE_PHOTO,
                    BACKGROUND_APP_DARK
                    )
from PySide6.QtCore import Qt, QDate
from .Widget_Common import setup_expandable_animation, set_background_image, set_frame_design

def setup_home_page(parent: QMainWindow, run_backtest_callback, open_config_callback, refresh_data_callback):
    parent.setWindowTitle("OutQuantLab")

    # Widget principal et layout principal horizontal
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)

    # Moitié gauche
    left_layout = QVBoxLayout()

    # Layout pour les 80% de la hauteur gauche (vide)
    left_top_layout = QVBoxLayout()
    spacer_left_top = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
    left_top_layout.addItem(spacer_left_top)

    # Layout pour les boutons en haut à gauche
    buttons_layout = QVBoxLayout()
    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    buttons_layout.addWidget(backtest_button)

    config_button = QPushButton("Open Config")
    config_button.clicked.connect(open_config_callback)
    buttons_layout.addWidget(config_button)

    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    buttons_layout.addWidget(refresh_button)

    # Ajouter les boutons en haut et l'espace vide en dessous
    left_layout.addLayout(buttons_layout)
    left_layout.addLayout(left_top_layout, stretch=4)

    # Moitié droite (vide, pleine hauteur)
    right_layout = QVBoxLayout()
    spacer_right = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
    right_layout.addItem(spacer_right)

    # Ajouter les layouts gauche et droite au layout principal
    main_layout.addLayout(left_layout, stretch=1)  # Moitié gauche
    main_layout.addLayout(right_layout, stretch=9)  # Moitié droite

    # Appliquer le layout principal au widget
    set_background_image(main_widget, HOME_PAGE_PHOTO)
    parent.setCentralWidget(main_widget)


def setup_backtest_page(parent):
    loading_widget = QWidget()
    main_layout = QVBoxLayout(loading_widget)
    set_background_image(loading_widget, BACKTEST_PAGE_PHOTO)
    top_layout = QHBoxLayout()
    main_layout.addLayout(top_layout, stretch=9)

    bottom_layout = QHBoxLayout()

    left_layout = QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout = QVBoxLayout()

    center_frame = set_frame_design(BACKGROUND_APP_DARK)
    center_frame_layout = QVBoxLayout(center_frame)

    # Layout séparé pour la barre de progression
    progress_bar_layout = QVBoxLayout()
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar_layout.addWidget(progress_bar)

    # Layout séparé pour la zone de logs
    log_output_layout = QVBoxLayout()
    log_output = QTextEdit()
    log_output.setReadOnly(True)
    log_output_layout.addWidget(log_output)

    # Ajouter les deux sous-layouts au layout du QFrame central
    center_frame_layout.addLayout(progress_bar_layout)
    center_frame_layout.addLayout(log_output_layout)

    # Ajouter le QFrame central au layout central
    center_layout.addWidget(center_frame)

    # Ajouter les layouts verticaux au layout horizontal
    bottom_layout.addLayout(left_layout, stretch=1)
    bottom_layout.addLayout(center_layout, stretch=4)
    bottom_layout.addLayout(right_layout, stretch=1)
    # Ajouter le layout horizontal inférieur au layout principal
    main_layout.addLayout(bottom_layout, stretch=1)

    parent.setCentralWidget(loading_widget)
    return progress_bar, log_output


def setup_results_page(parent, plots, back_to_home_callback, metrics):

    results_widget = QWidget()
    results_layout = QVBoxLayout(results_widget)
    set_background_image(results_widget, DASHBOARD_PAGE_PHOTO)
    top_frame = set_frame_design(BACKGROUND_APP_DARK)
    bottom_frame = set_frame_design(BACKGROUND_APP_DARK)
    top_layout = QHBoxLayout(top_frame)
    bottom_layout = QGridLayout(bottom_frame)
    rolling_buttons = [
        "Equity", 
        "Sharpe Ratio", 
        "Drawdown", 
        "Volatility", 
        "Smoothed Skewness", 
        "Average Inverted Correlation"]
    cluster_parameters = [
        "Max Clusters", 
        "Max Sub Clusters", 
        "Max Sub-Sub Clusters"]
    overall_buttons = [
        "Total Returns %",
        "Overall Sharpe Ratio",
        "Average Drawdown", 
        "Overall Volatility", 
        "Monthly Skew",
        "Overall Average Decorrelation"]
    advanced_buttons = [
        "Correlation Heatmap", 
        "Clusters Icicle", 
        "Distribution Histogram", 
        "Distribution Violin"]
    results = [
        "Total Return %",
        "Sharpe Ratio",
        "Average Drawdown %",
        "Volatility %",
        "Skewness"]
    
    rolling_toggle_button = QPushButton("Rolling Metrics")
    rolling_metrics_layout = QVBoxLayout()
    rolling_metrics_layout.setAlignment(Qt.AlignTop)  # Alignement en haut
    rolling_buttons_widget = QWidget()
    rolling_buttons_inner_layout = QVBoxLayout(rolling_buttons_widget)

    for btn_text in rolling_buttons:
        button = QPushButton(btn_text)
        button.clicked.connect(plots.get(btn_text, lambda: None))  # Connecter aux graphes associés
        rolling_buttons_inner_layout.addWidget(button)

    rolling_metrics_layout.addWidget(rolling_toggle_button)
    rolling_metrics_layout.addWidget(rolling_buttons_widget)

    setup_expandable_animation(rolling_toggle_button, rolling_buttons_widget)  # Animation préservée

    overall_toggle_button = QPushButton("Overall Metrics")
    overall_metrics_layout = QVBoxLayout()
    overall_metrics_layout.setAlignment(Qt.AlignTop)
    overall_buttons_widget = QWidget()
    overall_buttons_inner_layout = QVBoxLayout(overall_buttons_widget)

    for btn_text in overall_buttons:
        button = QPushButton(btn_text)
        button.clicked.connect(plots.get(btn_text, lambda: None))
        overall_buttons_inner_layout.addWidget(button)

    overall_metrics_layout.addWidget(overall_toggle_button)
    overall_metrics_layout.addWidget(overall_buttons_widget)

    setup_expandable_animation(overall_toggle_button, overall_buttons_widget)

    # Advanced Metrics avec animation et alignement
    advanced_toggle_button = QPushButton("Advanced Metrics")
    advanced_metrics_layout = QVBoxLayout()
    advanced_metrics_layout.setAlignment(Qt.AlignTop)
    advanced_buttons_widget = QWidget()
    advanced_buttons_inner_layout = QVBoxLayout(advanced_buttons_widget)

    for btn_text in advanced_buttons:
        button = QPushButton(btn_text)
        button.clicked.connect(plots.get(btn_text, lambda: None))
        advanced_buttons_inner_layout.addWidget(button)

    advanced_metrics_layout.addWidget(advanced_toggle_button)
    advanced_metrics_layout.addWidget(advanced_buttons_widget)

    setup_expandable_animation(advanced_toggle_button, advanced_buttons_widget)

    # Tableau des résultats avec animation
    stats_button = QPushButton("Portfolio Statistics")
    stats_layout = QVBoxLayout()
    stats_layout.setAlignment(Qt.AlignTop)
    stats_widget = QWidget()
    stats_inner_layout = QVBoxLayout(stats_widget)
    stats_inner_layout.setAlignment(Qt.AlignTop)

    for label, value in zip(results, metrics):
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel(label, alignment=Qt.AlignLeft))
        row_layout.addWidget(QLabel(f"{value}", alignment=Qt.AlignRight))
        stats_inner_layout.addLayout(row_layout)

    stats_layout.addWidget(stats_button)
    stats_layout.addWidget(stats_widget)
    setup_expandable_animation(stats_button, stats_widget)

    # Clusters Parameters avec animation et alignement
    clusters_toggle_button = QPushButton("Clusters Parameters")
    clusters_buttons_layout = QVBoxLayout()
    clusters_buttons_layout.setAlignment(Qt.AlignTop)
    clusters_buttons_widget = QWidget()
    clusters_buttons_inner_layout = QVBoxLayout(clusters_buttons_widget)

    for param in cluster_parameters:
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 10)
        slider.setValue(5)
        label = QLabel(f"{param}: {slider.value()}")
        slider.valueChanged.connect(lambda value, lbl=label, txt=param: lbl.setText(f"{txt}: {value}"))
        clusters_buttons_inner_layout.addWidget(label)
        clusters_buttons_inner_layout.addWidget(slider)

    clusters_buttons_layout.addWidget(clusters_toggle_button)
    clusters_buttons_layout.addWidget(clusters_buttons_widget)

    setup_expandable_animation(clusters_toggle_button, clusters_buttons_widget)
    # Backtest Parameters avec animation et alignement
    backtest_parameters_button = QPushButton("Backtest Parameters")
    backtest_parameters_layout = QVBoxLayout()
    backtest_parameters_layout.setAlignment(Qt.AlignTop)  # Alignement en haut
    backtest_parameters_widget = QWidget()
    backtest_parameters_inner_layout = QVBoxLayout(backtest_parameters_widget)

    # Sliders et labels pour les paramètres de backtest
    length_slider = QSlider(Qt.Horizontal)
    length_slider.setRange(6, 12)  # Log base 2 de 64 à 4096
    length_slider.setValue(10)
    length_label = QLabel(f"Rolling Length: {2 ** length_slider.value()}")
    length_slider.valueChanged.connect(lambda value: length_label.setText(f"Rolling Length: {2 ** value}"))
    backtest_parameters_inner_layout.addWidget(length_label)
    backtest_parameters_inner_layout.addWidget(length_slider)

    leverage_slider = QSlider(Qt.Horizontal)
    leverage_slider.setRange(1, 100)  # 0.1 à 10, step 0.1
    leverage_slider.setValue(10)
    leverage_label = QLabel(f"Leverage: {leverage_slider.value() / 10:.1f}")
    leverage_slider.valueChanged.connect(lambda value: leverage_label.setText(f"Leverage: {value / 10:.1f}"))
    backtest_parameters_inner_layout.addWidget(leverage_label)
    backtest_parameters_inner_layout.addWidget(leverage_slider)

    date_slider = QSlider(Qt.Horizontal)
    date_slider.setRange(0, (2025 - 1950) * 12)  # Range in months from 1950 à 2025
    date_slider.setValue((2025 - 1950) // 2 * 12)  # Par défaut au milieu de la plage
    date_label = QLabel(f"Starting Date: {QDate(1950, 1, 1).addMonths(date_slider.value()).toString('yyyy-MM')}")
    date_slider.valueChanged.connect(lambda value: date_label.setText(f"Starting Date: {QDate(1950, 1, 1).addMonths(value).toString('yyyy-MM')}"))
    backtest_parameters_inner_layout.addWidget(date_label)
    backtest_parameters_inner_layout.addWidget(date_slider)

    backtest_parameters_layout.addWidget(backtest_parameters_button)
    backtest_parameters_layout.addWidget(backtest_parameters_widget)

    setup_expandable_animation(backtest_parameters_button, backtest_parameters_widget)

    home_layout = QVBoxLayout()
    home_layout.setAlignment(Qt.AlignTop)
    # Bouton Home
    back_to_home_button = QPushButton("Home")
    back_to_home_button.clicked.connect(back_to_home_callback)
    home_layout.addWidget(back_to_home_button)

    top_layout.addLayout(stats_layout, stretch=2)
    top_layout.addLayout(rolling_metrics_layout, stretch=2)
    top_layout.addLayout(overall_metrics_layout, stretch=2)
    top_layout.addLayout(advanced_metrics_layout, stretch=2)
    top_layout.addLayout(backtest_parameters_layout, stretch=2)
    top_layout.addLayout(clusters_buttons_layout, stretch=2)
    top_layout.addLayout(home_layout, stretch=1)

    # Ajouter les layouts au layout principal
    results_layout.addWidget(top_frame, stretch=1)
    results_layout.addWidget(bottom_frame, stretch=29)

    parent.setCentralWidget(results_widget)

    return bottom_layout

def update_progress_with_events(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()