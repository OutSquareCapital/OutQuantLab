from typing import Any
from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, 
QWidget,
QFrame, 
QHBoxLayout, 
QSlider, 
QLabel, 
QDialog,
QMainWindow,
QGridLayout
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings
from PySide6.QtCore import Qt, QDate, QUrl
from Graphs import GraphsCollection
from Utilitary import BACKGROUND_APP_DARK, DataFrameFloat, GraphFunc
from UI.Common_UI import setup_expandable_animation
from collections.abc import Callable

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
