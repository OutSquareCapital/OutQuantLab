from typing import Any
from collections.abc import Callable
from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, 
QWidget,
QHBoxLayout, 
QLabel, 
QDialog,
QGridLayout,
QFrame
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import Qt, QUrl
from Graphs import GraphsCollection
from Utilitary import (
BACKGROUND_APP_DARK,
FRAME_STYLE, 
GraphFunc, 
STATS_GRAPHS,
ROLLING_GRAPHS,
OVERALL_GRAPHS,
CORRELATION_GRAPH,
TITLE_STYLE
)
from UI.Common_UI import setup_expandable_animation, set_frame_design, create_button
from Graphs import GraphsCollection


def generate_graph_buttons_for_category(
    parent: QWidget,
    graph_plots: dict[str, GraphFunc],
    category: str,
    open_on_launch: bool = False
) -> QVBoxLayout:

    toggle_button_name: str = f"{category} Plots"

    return create_expandable_buttons_list(
        parent=parent,
        toggle_button_name=toggle_button_name,
        buttons_actions=graph_plots,
        open_on_launch=open_on_launch
    )

def create_expandable_buttons_list(
    parent: QWidget,
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

def generate_stats_display(metrics: dict[str, float]) -> QVBoxLayout:
    stats_title = QLabel("Portfolio Statistics")
    stats_title.setStyleSheet(TITLE_STYLE)
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
    stats_layout.addWidget(stats_title)
    stats_layout.addWidget(stats_widget)
    
    return stats_layout

def plot_graph_in_webview(temp_file_path: str) -> QFrame:
    frame: QFrame = set_frame_design(FRAME_STYLE)
    layout = QVBoxLayout(frame)
    plot_widget = QWebEngineView()
    plot_widget.page().settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
    plot_widget.page().setBackgroundColor(BACKGROUND_APP_DARK)
    plot_widget.load(QUrl.fromLocalFile(temp_file_path))
    layout.addWidget(plot_widget)
    return frame

def display_dashboard_plot(
    parent: QWidget, 
    dashboard_name: str, 
    dashboard_func: GraphFunc
) -> None:
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{dashboard_name} Plot")
    dialog.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)
    graph_path: Any = dashboard_func(show_legend=True, as_html=True)
    plot_widget: QFrame = plot_graph_in_webview(temp_file_path=graph_path)
    layout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.resize(1200, 800)
    dialog.exec()

def add_graph_to_layout(layout: QGridLayout, temp_file_path: str, row: int, col: int) -> None:
    widget: QFrame = plot_graph_in_webview(temp_file_path=temp_file_path)  # Retourne un QFrame
    layout.addWidget(widget, row, col)

def create_placeholder_webview() -> QFrame:
    frame: QFrame = set_frame_design(FRAME_STYLE)
    layout = QVBoxLayout(frame)
    placeholder_view = QWebEngineView()
    placeholder_view.hide()
    placeholder_view.page().setBackgroundColor(BACKGROUND_APP_DARK)
    placeholder_view.setHtml("<html><body style='background-color: black;'></body></html>")
    layout.addWidget(placeholder_view)
    return frame


class GraphsWidget(QFrame):
    def __init__(self, graphs: GraphsCollection, back_to_home_callback: Callable[..., None]) -> None:
        super().__init__()
        self.graphs: GraphsCollection = graphs
        self.stats_widget_placeholder: QWidget = QWidget()
        self.graph_widgets_placeholders: list[QFrame] = []
        self.setStyleSheet(FRAME_STYLE)
        self.home_button: QPushButton = create_button(text="Home", callback=back_to_home_callback)
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout(self)
        home_layout = QVBoxLayout()
        home_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        home_layout.addWidget(self.home_button)
        self.top_left_layout = QHBoxLayout()
        self.top_right_layout = QVBoxLayout()
        self.top_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
        self.top_layout = QHBoxLayout(self.top_frame)
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.bottom_frame: QFrame = set_frame_design(frame_style=FRAME_STYLE)
        self.bottom_layout = QGridLayout(self.bottom_frame)
        
        overall_plots: QVBoxLayout = generate_graph_buttons_for_category(
            parent=self,
            graph_plots=self.graphs.all_plots_dict[OVERALL_GRAPHS],
            category=OVERALL_GRAPHS,
            open_on_launch=True
        )
        rolling_plots: QVBoxLayout = generate_graph_buttons_for_category(
            parent=self,
            graph_plots=self.graphs.all_plots_dict[ROLLING_GRAPHS],
            category=ROLLING_GRAPHS
        )
        other_plots: QVBoxLayout = generate_graph_buttons_for_category(
            parent=self,
            graph_plots=self.graphs.all_plots_dict[STATS_GRAPHS],
            category=STATS_GRAPHS
        )
        corr_plots: QVBoxLayout = generate_graph_buttons_for_category(
            parent=self,
            graph_plots=self.graphs.all_plots_dict[CORRELATION_GRAPH],
            category=CORRELATION_GRAPH
        )

        self.top_left_layout.addLayout(overall_plots, stretch=2)
        self.top_left_layout.addLayout(rolling_plots, stretch=2)
        self.top_left_layout.addLayout(other_plots, stretch=2)
        self.top_left_layout.addLayout(corr_plots, stretch=2)
        self.top_right_layout.addWidget(self.stats_widget_placeholder)
        self.top_layout.addLayout(self.top_left_layout, stretch=12)
        self.top_layout.addLayout(self.top_right_layout, stretch=6)
        self.top_layout.addLayout(home_layout, stretch=1)
        self.graph_widgets_placeholders = [
            create_placeholder_webview() for _ in range(6)
        ]
        for widget, (row, col) in zip(self.graph_widgets_placeholders, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2), (1, 2)]):
            self.bottom_layout.addWidget(widget, row, col)

        layout.addWidget(self.top_frame)
        layout.addWidget(self.bottom_frame)
        self.setLayout(layout)

    def create_stats_widget(self) -> QWidget:
        stats_layout: QVBoxLayout = generate_stats_display(metrics=self.graphs.get_metrics())
        stats_widget = QWidget()
        stats_widget.setLayout(stats_layout)
        return stats_widget

    def create_graph_widgets(self) -> list[QFrame]:
        plot_paths: list[Any] = [
            self.graphs.plot_stats_equity(show_legend=False, as_html=True),
            self.graphs.plot_rolling_sharpe_ratio(show_legend=False, as_html=True),
            self.graphs.plot_rolling_drawdown(show_legend=False, as_html=True),
            self.graphs.plot_rolling_volatility(show_legend=False, as_html=True),
            self.graphs.plot_stats_distribution_histogram(show_legend=False, as_html=True),
            self.graphs.plot_stats_distribution_violin(show_legend=False, as_html=True),
        ]
        return [plot_graph_in_webview(temp_file_path=path) for path in plot_paths]

    def update_graphs(self, new_graphs: GraphsCollection) -> None:
        self.graphs = new_graphs

        new_stats_widget: QWidget = self.create_stats_widget()
        self.top_right_layout.replaceWidget(self.stats_widget_placeholder, new_stats_widget)
        self.stats_widget_placeholder.deleteLater()
        self.stats_widget_placeholder = new_stats_widget

        new_graph_widgets: list[QFrame] = self.create_graph_widgets()
        for old_widget, new_widget in zip(self.graph_widgets_placeholders, new_graph_widgets):
            self.bottom_layout.replaceWidget(old_widget, new_widget)
            old_widget.deleteLater()
        self.graph_widgets_placeholders = new_graph_widgets
