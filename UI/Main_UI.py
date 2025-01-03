from PySide6.QtWidgets import (
QFrame,
QWidget,
QHBoxLayout,
QVBoxLayout,
QProgressBar, 
QTextEdit,
QMainWindow,
QApplication
)
from collections.abc import Callable
from Utilitary import (
CLUSTERS_PARAMETERS,
FRAME_STYLE
)
from UI.Results_UI import (
generate_stats_display,
generate_home_button,
setup_results_graphs,
generate_clusters_button_layout,
generate_graphs_buttons,
generate_backtest_params_sliders
)
from UI.Common_UI import (
set_background_image, 
set_frame_design, 
create_button,
)
from UI.Config_UI import (
AssetSelectionWidget, 
IndicatorsConfigWidget,
AssetsCollection, 
IndicatorsCollection
)
from UI.Clusters_UI import TreeStructureWidget, ClustersTree
from Graphs import GraphsCollection
from Utilitary import DataFrameFloat

def setup_home_page(
    parent: QMainWindow, 
    run_backtest_callback: Callable[..., None],
    assets_clusters: ClustersTree,
    indicators_clusters: ClustersTree,
    assets_collection: AssetsCollection,
    indicators_collection: IndicatorsCollection,
    background:str
    ) -> None:

    parent.setWindowTitle("OutQuantLab")
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)
    right_layout = QVBoxLayout()
    left_layout = QVBoxLayout()
    buttons_layout = QVBoxLayout()
    top_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    bottom_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    right_upper_layout = QHBoxLayout(top_frame)
    right_lower_layout = QHBoxLayout(bottom_frame)
    set_background_image(widget=main_widget, image_path=background)
    
    asset_widget = AssetSelectionWidget(assets_collection=assets_collection)
    indicator_widget = IndicatorsConfigWidget(indicators_collection=indicators_collection)
    asset_tree_widget = TreeStructureWidget(entities_names=assets_collection.all_entities_names, clusters=assets_clusters)
    method_tree_widget = TreeStructureWidget(entities_names=indicators_collection.all_entities_names, clusters=indicators_clusters)
    
    create_button(text="Run Backtest", callback=run_backtest_callback, parent_layout=buttons_layout)
    
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

def setup_backtest_page(parent: QMainWindow, background: str) -> tuple[QProgressBar, QTextEdit]:
    loading_widget = QWidget()
    main_layout = QVBoxLayout(loading_widget)
    set_background_image(loading_widget, background)
    top_layout = QHBoxLayout()
    main_layout.addLayout(top_layout, stretch=9)

    bottom_layout = QHBoxLayout()
    left_layout =   QVBoxLayout()
    center_layout = QVBoxLayout()
    right_layout =  QVBoxLayout()

    center_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
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
    global_returns_df: DataFrameFloat,
    sub_returns_df: DataFrameFloat,
    graphs: GraphsCollection,
    back_to_home_callback:Callable[..., None], 
    background: str) -> None:

    results_widget = QWidget()
    results_layout = QVBoxLayout(results_widget)
    set_background_image(widget=results_widget, image_path=background)
    top_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    bottom_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    top_layout = QHBoxLayout(top_frame)
    setup_results_graphs(parent=bottom_frame, returns_df=global_returns_df, graphs=graphs)
    (    
    overall_plots, 
    rolling_plots, 
    other_plots
    ) = generate_graphs_buttons(parent=parent,returns_df=sub_returns_df, graphs=graphs)

    stats_layout: QVBoxLayout = generate_stats_display( metrics=graphs.get_metrics(returns_df=global_returns_df))
    backtest_parameters_layout: QVBoxLayout = generate_backtest_params_sliders()
    clusters_buttons_layout: QVBoxLayout = generate_clusters_button_layout(clusters_params=CLUSTERS_PARAMETERS)
    home_layout: QVBoxLayout = generate_home_button(back_to_home_callback=back_to_home_callback)
    
    top_layout.addLayout(stats_layout, stretch=2)
    top_layout.addLayout(overall_plots, stretch=2)
    top_layout.addLayout(rolling_plots, stretch=2)
    top_layout.addLayout(other_plots, stretch=2)
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