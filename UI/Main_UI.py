from PySide6.QtWidgets import (
QWidget,
QHBoxLayout,
QVBoxLayout,
QProgressBar, 
QTextEdit,
QMainWindow,
QApplication,
QGridLayout
)
from collections.abc import Callable
from Utilitary import (
CLUSTERS_PARAMETERS,
FRAME_STYLE
)
from Database import MEDIA
from UI.Common_UI import (
generate_backtest_params_sliders, 
set_background_image, 
set_frame_design, 
generate_graphs_buttons,
create_button,
generate_stats_display,
generate_home_button,
generate_plot_widget
)
from UI.Config_UI import (
AssetSelectionWidget, 
IndicatorsConfigWidget, 
TreeStructureWidget,
ClustersTree,
AssetsCollection, 
IndicatorsCollection
)
from Dashboard import DashboardsCollection

def setup_home_page(
    parent: QMainWindow, 
    run_backtest_callback: Callable[..., None],
    refresh_data_callback: Callable[..., None],
    assets_clusters: ClustersTree,
    indicators_clusters: ClustersTree,
    assets_collection: AssetsCollection,
    indicators_collection: IndicatorsCollection
    ) -> None:

    parent.setWindowTitle("OutQuantLab")
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)
    right_layout = QVBoxLayout()
    left_layout = QVBoxLayout()
    buttons_layout = QVBoxLayout()
    top_frame = set_frame_design(FRAME_STYLE)
    bottom_frame = set_frame_design(FRAME_STYLE)
    right_upper_layout = QHBoxLayout(top_frame)
    right_lower_layout = QHBoxLayout(bottom_frame)
    set_background_image(main_widget, MEDIA.home_page)
    
    asset_widget = AssetSelectionWidget(assets_collection)
    indicator_widget = IndicatorsConfigWidget(indicators_collection)
    asset_tree_widget = TreeStructureWidget(assets_collection, assets_clusters)
    method_tree_widget = TreeStructureWidget(indicators_collection, indicators_clusters)
    
    create_button("Run Backtest", run_backtest_callback, buttons_layout)
    create_button("Refresh Data", refresh_data_callback, buttons_layout)
    
    left_layout.addLayout(buttons_layout)
    right_upper_layout.addWidget(asset_widget, stretch=1)
    right_upper_layout.addWidget(indicator_widget, stretch=2)
    right_lower_layout.addWidget(asset_tree_widget)
    right_lower_layout.addWidget(method_tree_widget)
    right_layout.addWidget(top_frame, stretch=1)
    right_layout.addWidget(bottom_frame, stretch=1)
    main_layout.addLayout(left_layout, stretch=1)
    main_layout.addLayout(right_layout, stretch=19)

    parent.setCentralWidget(main_widget)

def setup_backtest_page(parent: QMainWindow) -> tuple[QProgressBar, QTextEdit]:
    loading_widget = QWidget()
    main_layout = QVBoxLayout(loading_widget)
    set_background_image(loading_widget, MEDIA.loading_page)
    top_layout = QHBoxLayout()
    main_layout.addLayout(top_layout, stretch=9)

    bottom_layout = QHBoxLayout()
    left_layout =   QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout =  QVBoxLayout()

    center_frame = set_frame_design(FRAME_STYLE)
    center_frame_layout = QVBoxLayout(center_frame)

    progress_bar_layout = QVBoxLayout()
    progress_bar = QProgressBar()
    log_output_layout = QVBoxLayout()
    log_output = QTextEdit()
    
    progress_bar.setRange(0, 100)
    progress_bar_layout.addWidget(progress_bar)
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

def setup_results_page(
    parent: QMainWindow,
    dashboards: DashboardsCollection,
    back_to_home_callback:Callable[..., None], 
    metrics: dict[str, float]) -> None:

    results_widget = QWidget()
    results_layout = QVBoxLayout(results_widget)
    set_background_image(results_widget, MEDIA.dashboard_page)
    top_frame = set_frame_design(FRAME_STYLE)
    bottom_frame = set_frame_design(FRAME_STYLE)
    top_layout = QHBoxLayout(top_frame)
    bottom_layout = QGridLayout(bottom_frame)

    overall_metrics_layout, rolling_metrics_layout, advanced_metrics_layout = generate_graphs_buttons(dashboards, parent)

    stats_layout = generate_stats_display( metrics)
    backtest_parameters_layout, clusters_buttons_layout = generate_backtest_params_sliders(CLUSTERS_PARAMETERS)
    home_layout = generate_home_button(back_to_home_callback)

    equity_plot = generate_plot_widget((dashboards.plot("Equity", global_plot=True)), show_legend=False)
    sharpe_plot = generate_plot_widget(dashboards.plot("Rolling Sharpe Ratio", global_plot=True), show_legend=False)
    drawdown_plot = generate_plot_widget(dashboards.plot("Rolling Drawdown", global_plot=True), show_legend=False)
    vol_plot = generate_plot_widget(dashboards.plot("Rolling Volatility", global_plot=True), show_legend=False)
    distribution_plot = generate_plot_widget(dashboards.plot("Returns Distribution Histogram", global_plot=True), show_legend=False)
    violin_plot = generate_plot_widget(dashboards.plot("Returns Distribution Violin", global_plot=True), show_legend=False)
    
    bottom_layout.addWidget(equity_plot, 0, 0)
    bottom_layout.addWidget(drawdown_plot, 1, 0)
    bottom_layout.addWidget(sharpe_plot, 0, 1)
    bottom_layout.addWidget(vol_plot, 1, 1)
    bottom_layout.addWidget(distribution_plot, 0, 2)
    bottom_layout.addWidget(violin_plot, 1, 2)
    
    top_layout.addLayout(stats_layout, stretch=2)
    top_layout.addLayout(overall_metrics_layout, stretch=2)
    top_layout.addLayout(rolling_metrics_layout, stretch=2)
    top_layout.addLayout(advanced_metrics_layout, stretch=2)
    top_layout.addLayout(backtest_parameters_layout, stretch=2)
    top_layout.addLayout(clusters_buttons_layout, stretch=2)
    top_layout.addLayout(home_layout, stretch=1)
    results_layout.addWidget(top_frame, stretch=1)
    results_layout.addWidget(bottom_frame, stretch=29)

    parent.setCentralWidget(results_widget)

def update_progress_with_events(
    progress_bar: QProgressBar, 
    log_output: QTextEdit, 
    value: int, 
    message: str) -> None:
    
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()