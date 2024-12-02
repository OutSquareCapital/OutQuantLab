from PySide6.QtWidgets import (QWidget, 
                               QHBoxLayout, 
                               QVBoxLayout, 
                               QProgressBar, 
                               QTextEdit,
                               QPushButton, 
                               QMainWindow, 
                               QApplication,
                               QGridLayout,
                               QLabel,
                               QSlider
                               )
from Files import ( 
                    BACKTEST_PAGE_PHOTO,
                    HOME_PAGE_PHOTO,
                    DASHBOARD_PAGE_PHOTO,
                    OVERALL_BUTTONS_NAMES,
                    ROLLING_BUTTONS_NAMES,
                    ADVANCED_BUTTONS_NAMES,
                    BACKTEST_STATS_RESULTS,
                    CLUSTERS_PARAMETERS,
                    FRAME_STYLE
                    )

from PySide6.QtCore import Qt, QDate
from UI_Common import setup_expandable_animation, set_background_image, set_frame_design, create_expandable_buttons_list
from Config import ParameterWidget, AssetSelectionWidget, MethodSelectionWidget, TreeStructureWidget, get_active_methods

def setup_home_page(
    parent: QMainWindow, 
    run_backtest_callback, 
    refresh_data_callback, 
    param_config, 
    asset_config, 
    methods_config, 
    assets_names
):
    parent.setWindowTitle("OutQuantLab")
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)
    set_background_image(main_widget, HOME_PAGE_PHOTO)

    left_layout = QVBoxLayout()
    buttons_layout = QVBoxLayout()

    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    buttons_layout.addWidget(backtest_button)

    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    buttons_layout.addWidget(refresh_button)

    left_layout.addLayout(buttons_layout)

    right_layout = QVBoxLayout()
    
    top_frame = set_frame_design(FRAME_STYLE)
    bottom_frame = set_frame_design(FRAME_STYLE)
    right_upper_layout = QHBoxLayout(top_frame)
    right_lower_layout = QHBoxLayout(bottom_frame)

    param_widget = ParameterWidget(param_config)
    asset_widget = AssetSelectionWidget(asset_config, assets_names)
    method_widget = MethodSelectionWidget(methods_config)
    right_upper_layout.addWidget(param_widget)
    right_upper_layout.addWidget(asset_widget)
    right_upper_layout.addWidget(method_widget)

    method_names = get_active_methods(methods_config)
    asset_tree_widget = TreeStructureWidget(assets_names)
    method_tree_widget = TreeStructureWidget(methods_config)
    right_lower_layout.addWidget(asset_tree_widget)
    right_lower_layout.addWidget(method_tree_widget)

    right_layout.addWidget(top_frame, stretch=2)
    right_layout.addWidget(bottom_frame, stretch=1)

    main_layout.addLayout(left_layout, stretch=1)
    main_layout.addLayout(right_layout, stretch=19)

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

    center_frame = set_frame_design(FRAME_STYLE)
    center_frame_layout = QVBoxLayout(center_frame)

    progress_bar_layout = QVBoxLayout()
    progress_bar = QProgressBar()
    progress_bar.setRange(0, 100)
    progress_bar_layout.addWidget(progress_bar)

    log_output_layout = QVBoxLayout()
    log_output = QTextEdit()
    log_output.setReadOnly(True)
    log_output_layout.addWidget(log_output)

    center_frame_layout.addLayout(progress_bar_layout)
    center_frame_layout.addLayout(log_output_layout)
    center_layout.addWidget(center_frame)

    bottom_layout.addLayout(left_layout, stretch=1)
    bottom_layout.addLayout(center_layout, stretch=4)
    bottom_layout.addLayout(right_layout, stretch=1)

    main_layout.addLayout(bottom_layout, stretch=1)

    parent.setCentralWidget(loading_widget)
    return progress_bar, log_output

def setup_results_page(parent, plots, back_to_home_callback, metrics):

    results_widget = QWidget()
    results_layout = QVBoxLayout(results_widget)
    set_background_image(results_widget, DASHBOARD_PAGE_PHOTO)
    top_frame = set_frame_design(FRAME_STYLE)
    bottom_frame = set_frame_design(FRAME_STYLE)
    top_layout = QHBoxLayout(top_frame)
    bottom_layout = QGridLayout(bottom_frame)

    overall_metrics_layout = create_expandable_buttons_list("Overall Metrics", OVERALL_BUTTONS_NAMES, plots, True)
    rolling_metrics_layout = create_expandable_buttons_list("Rolling Metrics", ROLLING_BUTTONS_NAMES, plots)
    advanced_metrics_layout = create_expandable_buttons_list("Advanced Metrics", ADVANCED_BUTTONS_NAMES, plots)

    # Tableau des résultats avec animation
    stats_button = QPushButton("Portfolio Statistics")
    stats_layout = QVBoxLayout()
    stats_layout.setAlignment(Qt.AlignTop)
    stats_widget = QWidget()
    stats_inner_layout = QVBoxLayout(stats_widget)
    stats_inner_layout.setAlignment(Qt.AlignTop)

    for label, value in zip(BACKTEST_STATS_RESULTS, metrics):
        row_layout = QHBoxLayout()
        row_layout.addWidget(QLabel(label, alignment=Qt.AlignLeft))
        row_layout.addWidget(QLabel(f"{value}", alignment=Qt.AlignRight))
        stats_inner_layout.addLayout(row_layout)

    stats_layout.addWidget(stats_button)
    stats_layout.addWidget(stats_widget)
    setup_expandable_animation(stats_button, stats_widget)
    stats_button.setChecked(True)

    clusters_toggle_button = QPushButton("Clusters Parameters")
    clusters_buttons_layout = QVBoxLayout()
    clusters_buttons_layout.setAlignment(Qt.AlignTop)
    clusters_buttons_widget = QWidget()
    clusters_buttons_inner_layout = QVBoxLayout(clusters_buttons_widget)

    for param in CLUSTERS_PARAMETERS:
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

    backtest_parameters_button = QPushButton("Backtest Parameters")
    backtest_parameters_layout = QVBoxLayout()
    backtest_parameters_layout.setAlignment(Qt.AlignTop)  # Alignement en haut
    backtest_parameters_widget = QWidget()
    backtest_parameters_inner_layout = QVBoxLayout(backtest_parameters_widget)

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

    back_to_home_button = QPushButton("Home")
    back_to_home_button.clicked.connect(back_to_home_callback)
    home_layout.addWidget(back_to_home_button)

    top_layout.addLayout(stats_layout, stretch=2)
    top_layout.addLayout(overall_metrics_layout, stretch=2)
    top_layout.addLayout(rolling_metrics_layout, stretch=2)
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