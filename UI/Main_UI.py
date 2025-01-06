from PySide6.QtWidgets import (
QFrame,
QPushButton,
QWidget,
QHBoxLayout,
QVBoxLayout,
QProgressBar, 
QTextEdit
)
from collections.abc import Callable
from Utilitary import FRAME_STYLE
from UI.Common_UI import (
set_background_image, 
set_frame_design, 
create_button
)
from UI.Config_UI import (
AssetSelectionWidget, 
IndicatorsConfigWidget,
AssetsCollection, 
IndicatorsCollection
)
from UI.Clusters_UI import TreeStructureWidget, ClustersTree
from UI.Results_UI import GraphsWidget, GraphsCollection

def setup_home_page(
    parent: QWidget, 
    run_backtest_callback: Callable[..., None],
    assets_clusters: ClustersTree,
    indicators_clusters: ClustersTree,
    assets_collection: AssetsCollection,
    indics_collection: IndicatorsCollection
    ) -> None:

    main_layout = QHBoxLayout(parent)
    right_layout = QVBoxLayout()
    left_layout = QVBoxLayout()
    buttons_layout = QVBoxLayout()
    top_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    bottom_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    left_upper_layout = QHBoxLayout(top_frame)
    left_lower_layout = QHBoxLayout(bottom_frame)

    asset_widget = AssetSelectionWidget(assets_collection=assets_collection)
    indicator_widget = IndicatorsConfigWidget(indics_collection=indics_collection)
    asset_tree_widget = TreeStructureWidget(entities_names=assets_collection.all_entities_names, clusters=assets_clusters)
    method_tree_widget = TreeStructureWidget(entities_names=indics_collection.all_entities_names, clusters=indicators_clusters)
    
    button: QPushButton = create_button(text="Run Backtest", callback=run_backtest_callback)
    
    buttons_layout.addWidget(button)
    left_upper_layout.addWidget(asset_widget, stretch=1)
    left_upper_layout.addWidget(indicator_widget, stretch=2)
    left_lower_layout.addWidget(asset_tree_widget)
    left_lower_layout.addWidget(method_tree_widget)
    left_layout.addWidget(top_frame, stretch=1)
    left_layout.addWidget(bottom_frame, stretch=1)
    right_layout.addLayout(buttons_layout)
    main_layout.addLayout(left_layout, stretch=19)
    main_layout.addLayout(right_layout, stretch=1)
    parent.setLayout(main_layout)

def setup_backtest_page(
    parent: QWidget, 
    background: str
    ) -> tuple[QProgressBar, QTextEdit]:
    set_background_image(widget=parent, image_path=background)
    main_layout = QVBoxLayout(parent)
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
    parent.setLayout(main_layout)
    return progress_bar, log_output

def setup_results_page(
    parent: QWidget,
    back_to_home_callback:Callable[..., None], 
    background: str,
    graphs: GraphsCollection) -> GraphsWidget:
    set_background_image(widget=parent, image_path=background)
    main_layout = QVBoxLayout(parent)
    bottom_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
    bottom_layout = QVBoxLayout(bottom_frame)
    graphs_widget = GraphsWidget(graphs=graphs, back_to_home_callback=back_to_home_callback)

    bottom_layout.addWidget(graphs_widget)
    main_layout.addWidget(bottom_frame)
    parent.setLayout(main_layout)
    return graphs_widget