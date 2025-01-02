from typing import Any
from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, 
QTreeWidget, 
QScrollArea, 
QWidget, 
QCheckBox, 
QGroupBox, 
QFrame, 
QHBoxLayout, 
QSlider, 
QLabel, 
QTreeWidgetItem,
QMessageBox,
QInputDialog,
QLayout,
QDialog,
QMainWindow,
QGridLayout
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QDate, QUrl
from PySide6.QtGui import QPalette, QBrush, QPixmap, QFont
from collections.abc import Callable
from Graphs import GraphsCollection
from Utilitary import BACKGROUND_APP_DARK, DataFrameFloat, GraphFunc

def create_param_widget(
    param_box: QGroupBox, 
    param_layout: QVBoxLayout, 
    values: list[int]
    ) -> tuple[QLabel, QLabel, QLabel, QSlider, QSlider, QSlider]:
    
        param_labels_layout, range_info_label, num_values_info_label, generated_values_label = create_param_labels(values)
        sliders_layout, num_values_layout, start_slider, end_slider, num_values_slider = create_param_sliders(values)
        
        param_layout.addLayout(param_labels_layout)
        param_layout.addLayout(sliders_layout)
        param_layout.addLayout(num_values_layout)
        param_box.setLayout(param_layout)
        
        return range_info_label, num_values_info_label, generated_values_label, start_slider, end_slider, num_values_slider
        
def create_scroll_with_buttons(
    parent_layout: QVBoxLayout,
    select_callback: Callable[[], None],
    unselect_callback: Callable[[], None]
) -> QVBoxLayout:
    scroll_area, _, scroll_layout = create_scroll_area()
    buttons_layout = QHBoxLayout()
    add_select_buttons(buttons_layout, select_callback, unselect_callback)
    parent_layout.addWidget(scroll_area)
    parent_layout.addLayout(buttons_layout)
    return scroll_layout

def create_range_sliders(values: list[int]) -> tuple[QSlider, QSlider]:
    start_slider = QSlider(Qt.Orientation.Horizontal)
    end_slider = QSlider(Qt.Orientation.Horizontal)
    start_slider.setMinimum(0)
    start_slider.setMaximum(11)
    end_slider.setMinimum(0)
    end_slider.setMaximum(12)
    start_slider.setValue(value_to_index(min(values)))
    end_slider.setValue(value_to_index(max(values)))
    return start_slider, end_slider

def create_num_values_slider(num_values: int) -> QSlider:
    num_values_slider = QSlider(Qt.Orientation.Horizontal)
    num_values_slider.setMinimum(1)
    num_values_slider.setMaximum(10)
    num_values_slider.setValue(num_values)
    return num_values_slider

def param_range_values(start: int, end: int, num_values: int) -> list[int]:
    if num_values == 1:
        return [int((start + end) / 2)]
    ratio = (end / start) ** (1 / (num_values - 1))
    return [int(round(start * (ratio ** i))) for i in range(num_values)]

def value_to_index(value: int) -> int:
    return int(value).bit_length() - 1

def index_to_value(index: int) -> int:
    return 2 ** index

def create_scroll_area() ->tuple[QScrollArea, QWidget, QVBoxLayout]:
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout()
    scroll_widget.setLayout(scroll_layout)
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)
    return scroll_area, scroll_widget, scroll_layout

def create_info_labels(values: list[int]) -> tuple[QLabel, QLabel, QLabel]:
    range_info_label = QLabel(f"Range: {min(values)} - {max(values)}")
    num_values_info_label = QLabel(f"Num Values: {len(values)}")
    generated_values_label = QLabel(f"Generated Values: {values}")
    generated_values_label.setWordWrap(False)
    return range_info_label, num_values_info_label, generated_values_label

def create_param_labels(values: list[int]) -> tuple[QVBoxLayout, QLabel, QLabel, QLabel]:
    range_info_label, num_values_info_label, generated_values_label = create_info_labels(values)
    param_layout = QVBoxLayout()
    param_layout.addWidget(range_info_label)
    param_layout.addWidget(num_values_info_label)

    scroll_area, _, _ = create_scroll_area()
    scroll_area.setWidget(generated_values_label)
    scroll_area.setFixedHeight(50)
    param_layout.addWidget(scroll_area)

    return param_layout, range_info_label, num_values_info_label, generated_values_label

def create_param_sliders(values: list[int]) -> tuple[QHBoxLayout, QHBoxLayout, QSlider, QSlider, QSlider]:
    start_slider, end_slider = create_range_sliders(values)
    num_values_slider = create_num_values_slider(len(values))

    sliders_layout = QHBoxLayout()
    sliders_layout.addWidget(QLabel("Start:"))
    sliders_layout.addWidget(start_slider)
    sliders_layout.addWidget(QLabel("End:"))
    sliders_layout.addWidget(end_slider)

    num_values_layout = QHBoxLayout()
    num_values_layout.addWidget(QLabel("Num Values:"))
    num_values_layout.addWidget(num_values_slider)

    return sliders_layout, num_values_layout, start_slider, end_slider, num_values_slider

def add_cluster(tree: QTreeWidget, tree_structure: dict[str, dict[str, list[str]]]) -> None:
    cluster_name, ok = QInputDialog.getText(parent=tree, title="New Cluster", label="Cluster Name:")
    if ok and cluster_name:
        if cluster_name in tree_structure:
            QMessageBox.warning(parent=tree, title="Warning", text=f"The cluster '{cluster_name}' already exists.")
            return

        tree_structure[cluster_name] = {}
        category_item = QTreeWidgetItem([cluster_name])
        category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        tree.addTopLevelItem(category_item)

def delete_cluster(tree: QTreeWidget, tree_structure: dict[str, dict[str, list[str]]]) -> None:
    selected_cluster: QTreeWidgetItem = tree.currentItem()
    if selected_cluster:
        parent: QTreeWidgetItem = selected_cluster.parent()
        parent.removeChild(selected_cluster)

def create_expandable_section(category_name: str) -> tuple[QGroupBox, QVBoxLayout]:

    category_box = QGroupBox(category_name)
    category_layout = QVBoxLayout()
    category_box.setLayout(category_layout)

    content_widget = QWidget()
    content_layout = QVBoxLayout()
    content_widget.setLayout(content_layout)

    expand_button = QPushButton("Expand/Collapse")
    category_layout.addWidget(expand_button)
    category_layout.addWidget(content_widget)

    setup_expandable_animation(expand_button, content_widget)

    return category_box, content_layout

def find_element_in_tree(tree: QTreeWidget, element: str) -> bool:
    def traverse(item:QTreeWidgetItem) -> bool:
        if item.text(0) == element:
            return True
        for i in range(item.childCount()):
            if traverse(item.child(i)):
                return True
        return False

    for i in range(tree.topLevelItemCount()):
        if traverse(tree.topLevelItem(i)):
            return True
    return False

def populate_tree_from_dict(
    tree: QTreeWidget, 
    clusters: dict[str, dict[str, list[str]]], 
    names: list[str], 
    ) -> None:

    for key, sub_clusters in clusters.items():
        category_item = QTreeWidgetItem([key])
        category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        font = QFont()
        font.setUnderline(True)
        category_item.setFont(0, font)
        tree.addTopLevelItem(category_item)

        for sub_key, elements in sub_clusters.items():
            sub_category_item = QTreeWidgetItem([sub_key])
            sub_category_item.setFlags(sub_category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
            category_item.addChild(sub_category_item)

            for element in elements:
                if element in names:
                    child_item = QTreeWidgetItem([element])
                    child_item.setFlags(child_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                    sub_category_item.addChild(child_item)


    for element in names:
        if not find_element_in_tree(tree=tree, element=element):
            orphan_item = QTreeWidgetItem([element])
            orphan_item.setFlags(orphan_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
            tree.addTopLevelItem(orphan_item)

def connect_sliders_to_update(
    start_slider: QSlider, 
    end_slider: QSlider, 
    num_values_slider: QSlider,
    range_info_label: QLabel, 
    num_values_info_label: QLabel, 
    generated_values_label: QLabel,
    update_callback: Callable[[list[int]], None]
    ) -> None:
    def update_values() -> None:
        start = index_to_value(start_slider.value())
        end = index_to_value(end_slider.value())
        num_values = num_values_slider.value()

        if start * 2 > end:
            if start_slider.hasFocus():
                end_slider.setValue(value_to_index(start * 2))
            elif end_slider.hasFocus():
                start_slider.setValue(value_to_index(end // 2))

        generated_values = param_range_values(start, end, num_values)
        unique_values = sorted(set(generated_values))
        range_info_label.setText(f"Range: {start} - {end}")
        num_values_info_label.setText(f"Num Values: {len(unique_values)}")
        generated_values_label.setText(f"Generated Values: {unique_values}")

        update_callback(unique_values)

    start_slider.valueChanged.connect(update_values)
    end_slider.valueChanged.connect(update_values)
    num_values_slider.valueChanged.connect(update_values)


def add_select_buttons(
    layout: QHBoxLayout, 
    select_callback: Callable[[], None], 
    unselect_callback: Callable[[], None]
    ) -> None:
    select_all_button = QPushButton("Select All")
    select_all_button.clicked.connect(select_callback)
    layout.addWidget(select_all_button)

    unselect_all_button = QPushButton("Unselect All")
    unselect_all_button.clicked.connect(unselect_callback)
    layout.addWidget(unselect_all_button)

def set_frame_design(frame_style: str) -> QFrame:
    frame = QFrame()
    frame.setStyleSheet(frame_style)
    return frame

def set_background_image(widget: QWidget, image_path: str) -> None:
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def setup_expandable_animation(
    toggle_button: QPushButton, 
    content_widget: QWidget, 
    animation_duration: int = 500
    ) -> QPropertyAnimation:

    content_widget.setMaximumHeight(0)
    animation = QPropertyAnimation(content_widget, b"maximumHeight")
    animation.setDuration(animation_duration)
    animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def toggle_animation(checked: bool) -> None:
        if checked:
            animation.setStartValue(0)
            animation.setEndValue(content_widget.sizeHint().height())
        else:
            animation.setStartValue(content_widget.sizeHint().height())
            animation.setEndValue(0)
        animation.start()

    toggle_button.setCheckable(True)
    toggle_button.toggled.connect(toggle_animation)
    return animation

def create_checkbox_item(
    item: str, 
    is_checked: bool, 
    callback: Callable[[bool], None]) -> QCheckBox:
    checkbox = QCheckBox(item)
    checkbox.setChecked(is_checked)
    checkbox.stateChanged.connect(lambda: callback(checkbox.isChecked()))
    return checkbox

def create_button(
    text: str, 
    callback: Callable[..., None], 
    parent_layout: QLayout
    ) -> QPushButton:
    
    button: QPushButton = QPushButton(text)
    button.clicked.connect(callback)
    parent_layout.addWidget(button)
    return button

def plot_graph_in_webview(temp_file_path:str) -> QWebEngineView:
    plot_widget = QWebEngineView()
    page: QWebEnginePage = plot_widget.page()
    page.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
    page.setBackgroundColor(BACKGROUND_APP_DARK)
    plot_widget.load(QUrl.fromLocalFile(temp_file_path))

    return plot_widget

def display_dashboard_plot(
    parent: QMainWindow,
    returns_df: DataFrameFloat,
    dashboard_name: str,
    dashboard_func: GraphFunc
) -> None:
    dialog: QDialog = QDialog(parent)
    dialog.setWindowTitle(f"{dashboard_name} Plot")
    dialog.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)

    graph_path: Any = dashboard_func(
        returns_df = returns_df,
        show_legend=True, 
        as_html=True
        )
    plot_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=graph_path)

    layout: QVBoxLayout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.resize(1200, 800)
    dialog.exec()


def generate_stats_display(metrics: dict[str, float]) -> QVBoxLayout:
    stats_button = QPushButton("Portfolio Statistics")
    stats_layout = QVBoxLayout()
    stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    stats_widget = QWidget()
    stats_inner_layout = QVBoxLayout(stats_widget)
    stats_inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    for label, value in metrics.items():
        row_layout = QHBoxLayout()
        
        left_label = QLabel(label)
        left_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        row_layout.addWidget(left_label)
        
        right_label = QLabel(f"{value}")
        right_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        row_layout.addWidget(right_label)
        
        stats_inner_layout.addLayout(row_layout)
    stats_layout.addWidget(stats_button)
    stats_layout.addWidget(stats_widget)
    setup_expandable_animation(stats_button, stats_widget)
    stats_button.setChecked(True)
    
    return stats_layout

def setup_results_graphs(parent:QFrame, returns_df: DataFrameFloat, graphs:GraphsCollection) -> None:
    bottom_layout = QGridLayout(parent=parent)
    equity_plot: Any = graphs.plot_equity(returns_df=returns_df, show_legend=False, as_html=True)
    sharpe_plot: Any = graphs.plot_rolling_sharpe_ratio(returns_df=returns_df, show_legend=False, as_html=True)
    drawdown_plot: Any = graphs.plot_rolling_drawdown(returns_df=returns_df, show_legend=False, as_html=True)
    vol_plot: Any = graphs.plot_rolling_volatility(returns_df=returns_df, show_legend=False, as_html=True)
    distribution_plot: Any = graphs.plot_returns_distribution_histogram(returns_df=returns_df, show_legend=False, as_html=True)
    violin_plot: Any = graphs.plot_returns_distribution_violin(returns_df=returns_df, show_legend=False, as_html=True)
    
    equity_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=equity_plot)
    sharpe_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=sharpe_plot)
    drawdown_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=drawdown_plot)
    vol_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=vol_plot)
    distribution_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=distribution_plot)
    violin_widget: QWebEngineView = plot_graph_in_webview(temp_file_path=violin_plot)
    
    bottom_layout.addWidget(equity_widget, 0, 0)
    bottom_layout.addWidget(sharpe_widget, 1, 0)
    bottom_layout.addWidget(drawdown_widget, 0, 1)
    bottom_layout.addWidget(vol_widget, 1, 1)
    bottom_layout.addWidget(distribution_widget, 0, 2)
    bottom_layout.addWidget(violin_widget, 1, 2)

def create_slider_with_label(
    layout: QVBoxLayout, 
    slider_range: tuple[int, int], 
    initial_value: int, 
    value_transform: Callable[[int], str], 
) -> None:
    slider = QSlider(Qt.Orientation.Horizontal)
    slider.setRange(*slider_range)
    slider.setValue(initial_value)
    label = QLabel(value_transform(slider.value()))
    on_slider_value_change(slider=slider, label=label, value_transform=value_transform)
    layout.addWidget(label)
    layout.addWidget(slider)

def generate_home_button(back_to_home_callback: Callable[..., None]) -> QVBoxLayout:
    home_layout = QVBoxLayout()
    home_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    back_to_home_button = QPushButton("Home")
    back_to_home_button.clicked.connect(back_to_home_callback)
    home_layout.addWidget(back_to_home_button)
    
    return home_layout


def organize_buttons_by_category(graphs:GraphsCollection) -> dict[str, dict[str, GraphFunc]]:
    overall = "Overall"
    rolling = "Rolling"
    other = "Other"
    categorized_buttons: dict[str, dict[str, GraphFunc]] = {
        f'{overall}': {}, 
        f'{rolling}': {}, 
        f'{other}': {}
        }

    for plot_name, func in graphs.get_all_plots_dict().items():
        if overall in plot_name:
            category = overall
        elif rolling in plot_name:
            category = rolling
        else:
            category = other
        
        categorized_buttons[category][plot_name] = func
    return categorized_buttons
    
def generate_graphs_buttons(
    parent: QMainWindow,
    returns_df: DataFrameFloat,
    graphs:GraphsCollection
    ) -> tuple[QVBoxLayout, QVBoxLayout, QVBoxLayout]:
    categorized_buttons: dict[str, dict[str, GraphFunc]] = organize_buttons_by_category(graphs=graphs)
    overall = "Overall"
    rolling = "Rolling"
    other = "Other"
    metrics = "Metrics"

    overall_metrics_actions: dict[str, GraphFunc] = categorized_buttons[overall]
    rolling_metrics_actions: dict[str, GraphFunc] = categorized_buttons[rolling]
    other_metrics_actions: dict[str, GraphFunc] = categorized_buttons[other]

    overall_metrics_layout: QVBoxLayout = create_expandable_buttons_list(
        parent=parent,
        returns_df=returns_df,
        toggle_button_name=f'{overall} {metrics}', 
        buttons_actions=overall_metrics_actions, 
        open_on_launch=True
    )
    rolling_metrics_layout: QVBoxLayout = create_expandable_buttons_list(
        parent=parent,
        returns_df=returns_df,
        toggle_button_name=f'{rolling} {metrics}', 
        buttons_actions=rolling_metrics_actions
    )
    advanced_metrics_layout: QVBoxLayout = create_expandable_buttons_list(
        parent=parent,
        returns_df=returns_df,
        toggle_button_name=f'{other} {metrics}',
        buttons_actions=other_metrics_actions
    )

    return overall_metrics_layout, rolling_metrics_layout, advanced_metrics_layout

def create_expandable_buttons_list(
    parent: QMainWindow,
    returns_df: DataFrameFloat,
    toggle_button_name: str, 
    buttons_actions: dict[str, GraphFunc], 
    open_on_launch: bool = False
    ) -> QVBoxLayout:
    
    toggle_button = QPushButton(toggle_button_name)
    outer_layout = QVBoxLayout()
    outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    buttons_widget = QWidget()
    inner_layout = QVBoxLayout(buttons_widget)
    
    for name, func in buttons_actions.items():
        button = QPushButton(name)
        
        def action_closure(func: GraphFunc=func, name: str=name):
            return lambda: display_dashboard_plot(
                parent=parent, 
                returns_df=returns_df, 
                dashboard_name=name, 
                dashboard_func=func
            )
        
        button.clicked.connect(action_closure())
        inner_layout.addWidget(button)
        
    outer_layout.addWidget(toggle_button)
    outer_layout.addWidget(buttons_widget)
    setup_expandable_animation(toggle_button=toggle_button, content_widget=buttons_widget)
    
    if open_on_launch:
        toggle_button.setChecked(True)
    
    return outer_layout

def on_slider_value_change(slider: QSlider, label: QLabel, value_transform: Callable[[int], str]) -> None:
    def update_label(value: int) -> None:
        label.setText(value_transform(value))
    slider.valueChanged.connect(update_label)

def generate_clusters_button_layout(clusters_params: list[str]) -> QVBoxLayout:
    clusters_toggle_button = QPushButton("Clusters Parameters")
    clusters_buttons_layout = QVBoxLayout()
    clusters_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    clusters_buttons_widget = QWidget()
    clusters_buttons_inner_layout = QVBoxLayout(clusters_buttons_widget)

    for param in clusters_params:
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 10)
        slider.setValue(5)
        slider_label = QLabel(f"{param}: {slider.value()}")
        def update_slider_label(value: int, label:QLabel=slider_label, txt: str = param) -> None:
            label.setText(f"{txt}: {value}")
        slider.valueChanged.connect(update_slider_label)
        clusters_buttons_inner_layout.addWidget(slider_label)
        clusters_buttons_inner_layout.addWidget(slider)

    clusters_buttons_layout.addWidget(clusters_toggle_button)
    clusters_buttons_layout.addWidget(clusters_buttons_widget)
    setup_expandable_animation(clusters_toggle_button, clusters_buttons_widget)

    return clusters_buttons_layout

def generate_backtest_params_sliders() -> QVBoxLayout:
    backtest_parameters_button = QPushButton("Backtest Parameters")
    backtest_parameters_layout = QVBoxLayout()
    backtest_parameters_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    backtest_parameters_widget = QWidget()
    backtest_parameters_inner_layout = QVBoxLayout(backtest_parameters_widget)

    create_slider_with_label(
        layout=backtest_parameters_inner_layout,
        slider_range=(6, 12),
        initial_value=10,
        value_transform=lambda value: f"Rolling Length: {value ** 2}"
    )
    create_slider_with_label(
        layout=backtest_parameters_inner_layout,
        slider_range=(1, 100),
        initial_value=10,
        value_transform=lambda value: f"Leverage: {value / 10:.1f}"
    )
    create_slider_with_label(
        layout=backtest_parameters_inner_layout,
        slider_range=(0, (2025 - 1950) * 12),
        initial_value=((2025 - 1950) // 2) * 12,
        value_transform=lambda value: f"Starting Date: {QDate(1950, 1, 1).addMonths(value).toString('yyyy-MM')}"
    )
    backtest_parameters_layout.addWidget(backtest_parameters_button)
    backtest_parameters_layout.addWidget(backtest_parameters_widget)
    setup_expandable_animation(toggle_button=backtest_parameters_button, content_widget=backtest_parameters_widget)
    
    return backtest_parameters_layout