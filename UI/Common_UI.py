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
QDialog
)
from functools import partial
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt, QDate
from PySide6.QtGui import QPalette, QBrush, QPixmap
from PySide6.QtGui import QFont
from typing import Any
from collections.abc import Callable
from .Results_UI import generate_plot_widget
from Dashboard import DashboardsCollection

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
    select_callback: Callable,
    unselect_callback: Callable
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

def add_cluster(tree: QTreeWidget, tree_structure: dict[str, Any]):
    cluster_name, ok = QInputDialog.getText(tree, "New Cluster", "Cluster Name:")
    if ok and cluster_name:
        if cluster_name in tree_structure:
            QMessageBox.warning(tree, "Warning", f"The cluster '{cluster_name}' already exists.")
            return

        tree_structure[cluster_name] = {}
        category_item = QTreeWidgetItem([cluster_name])
        category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        tree.addTopLevelItem(category_item)

def delete_cluster(tree: QTreeWidget, tree_structure: dict[str, Any]) -> None:
    selected_cluster = tree.currentItem()
    if selected_cluster:
        cluster_name = selected_cluster.text(0)
        parent = selected_cluster.parent()
        if parent is None:
            index = tree.indexOfTopLevelItem(selected_cluster)
            tree.takeTopLevelItem(index)
            if cluster_name in tree_structure:
                del tree_structure[cluster_name]
        else:
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
    def traverse(item) -> bool:
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

def populate_tree_from_dict(tree: QTreeWidget, data: dict[str, Any], data_set: set, parent_item=None):
    if parent_item is None:
        parent_item = tree

    for key, value in data.items():
        category_item = QTreeWidgetItem([key])
        category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        font = QFont()
        font.setUnderline(True)
        category_item.setFont(0, font)
        if isinstance(parent_item, QTreeWidget):
            parent_item.addTopLevelItem(category_item)
        else:
            parent_item.addChild(category_item)

        if isinstance(value, dict):
            populate_tree_from_dict(tree, value, data_set, category_item)
        elif isinstance(value, list):
            for element in value:
                if element in data_set:
                    child_item = QTreeWidgetItem([element])
                    child_item.setFlags(child_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                    category_item.addChild(child_item)

    if parent_item is tree:
        for element in data_set:
            if not find_element_in_tree(tree, element):
                orphan_item = QTreeWidgetItem([element])
                orphan_item.setFlags(orphan_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                tree.addTopLevelItem(orphan_item)

def connect_sliders_to_update(
    start_slider: QSlider, end_slider: QSlider, num_values_slider: QSlider,
    range_info_label: QLabel, num_values_info_label: QLabel, generated_values_label: QLabel,
    update_callback: Callable
) -> None:
    def update_values():
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
    
def add_select_buttons(layout: QHBoxLayout, select_callback: Callable, unselect_callback: Callable):
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

def create_button(
    text: str, 
    callback: Callable, 
    parent_layout: QLayout
    ) -> QPushButton:
    
    button: QPushButton = QPushButton(text)
    button.clicked.connect(callback)
    parent_layout.addWidget(button)
    return button

def create_buttons_from_list(layout: QVBoxLayout, buttons_names: list[str], buttons_actions: dict[str, Callable]) -> None:

    for btn_text in buttons_names:
        button = QPushButton(btn_text)
        action = buttons_actions.get(btn_text, lambda: None)
        button.clicked.connect(action)
        layout.addWidget(button)


def create_checkbox_item(
    item: str, 
    is_checked: bool, 
    callback: Callable[[bool], None]) -> QCheckBox:
    checkbox = QCheckBox(item)
    checkbox.setChecked(is_checked)
    checkbox.stateChanged.connect(lambda: callback(checkbox.isChecked()))
    return checkbox

def create_expandable_buttons_list(
    toggle_button_name: str, 
    buttons_names: list[str], 
    buttons_actions: dict[str, Callable], 
    open_on_launch: bool = False
    ) -> QVBoxLayout:
    
    toggle_button = QPushButton(toggle_button_name)
    outer_layout = QVBoxLayout()
    outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    buttons_widget = QWidget()
    inner_layout = QVBoxLayout(buttons_widget)
    create_buttons_from_list(inner_layout, buttons_names, buttons_actions)
    outer_layout.addWidget(toggle_button)
    outer_layout.addWidget(buttons_widget)
    setup_expandable_animation(toggle_button, buttons_widget)
    if open_on_launch:
        toggle_button.setChecked(True)
    return outer_layout

def organize_buttons_by_category(dashboards:DashboardsCollection):

    categorized_buttons = {"overall": [], "rolling": [], "other": []}
    actions = {"overall": {}, "rolling": {}, "other": {}}

    for name, dashboard in dashboards.all_dashboards.items():
        categorized_buttons[dashboard.category].append(dashboard.name)

    return categorized_buttons, actions
    
def generate_graphs_buttons(dashboards:DashboardsCollection, parent_window):
    categorized_buttons, actions = organize_buttons_by_category(dashboards)

    for category, buttons in categorized_buttons.items():
        for button_name in buttons:
            actions[category][button_name] = partial(
                display_dashboard_plot, parent_window, dashboards, button_name
            )

    overall_metrics_layout = create_expandable_buttons_list(
        "Overall Metrics", categorized_buttons["overall"], actions["overall"], open_on_launch=True
    )
    rolling_metrics_layout = create_expandable_buttons_list(
        "Rolling Metrics", categorized_buttons["rolling"], actions["rolling"]
    )
    advanced_metrics_layout = create_expandable_buttons_list(
        "Advanced Metrics", categorized_buttons["other"], actions["other"]
    )

    return overall_metrics_layout, rolling_metrics_layout, advanced_metrics_layout

def display_dashboard_plot(parent, dashboards:DashboardsCollection, dashboard_name: str, global_plot: bool = False):

    fig = dashboards.plot(dashboard_name, global_plot=global_plot)
    
    dialog = QDialog(parent)
    dialog.setWindowTitle(f"{dashboard_name} Plot")
    dialog.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint)
    
    plot_widget = generate_plot_widget(fig)
    layout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.resize(1200, 800)
    
    dialog.exec()


def generate_stats_display(stats_results, metrics) -> QVBoxLayout:
    stats_button = QPushButton("Portfolio Statistics")
    stats_layout = QVBoxLayout()
    stats_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    stats_widget = QWidget()
    stats_inner_layout = QVBoxLayout(stats_widget)
    stats_inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    for label, value in zip(stats_results, metrics):
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

def generate_home_button(back_to_home_callback: Callable) -> QVBoxLayout:
    home_layout = QVBoxLayout()
    home_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    back_to_home_button = QPushButton("Home")
    back_to_home_button.clicked.connect(back_to_home_callback)
    home_layout.addWidget(back_to_home_button)
    
    return home_layout

def generate_backtest_params_sliders(clusters_params) -> tuple[QVBoxLayout, QVBoxLayout]:
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
        slider.valueChanged.connect(lambda value, lbl=slider_label, txt=param: lbl.setText(f"{txt}: {value}"))
        clusters_buttons_inner_layout.addWidget(slider_label)
        clusters_buttons_inner_layout.addWidget(slider)

    clusters_buttons_layout.addWidget(clusters_toggle_button)
    clusters_buttons_layout.addWidget(clusters_buttons_widget)
    setup_expandable_animation(clusters_toggle_button, clusters_buttons_widget)

    backtest_parameters_button = QPushButton("Backtest Parameters")
    backtest_parameters_layout = QVBoxLayout()
    backtest_parameters_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    backtest_parameters_widget = QWidget()
    backtest_parameters_inner_layout = QVBoxLayout(backtest_parameters_widget)

    length_slider = QSlider(Qt.Orientation.Horizontal)
    length_slider.setRange(6, 12)
    length_slider.setValue(10)
    length_label = QLabel(f"Rolling Length: {2 ** length_slider.value()}")
    length_slider.valueChanged.connect(lambda value: length_label.setText(f"Rolling Length: {2 ** value}"))
    backtest_parameters_inner_layout.addWidget(length_label)
    backtest_parameters_inner_layout.addWidget(length_slider)

    leverage_slider = QSlider(Qt.Orientation.Horizontal)
    leverage_slider.setRange(1, 100)
    leverage_slider.setValue(10)
    leverage_label = QLabel(f"Leverage: {leverage_slider.value() / 10:.1f}")
    leverage_slider.valueChanged.connect(lambda value: leverage_label.setText(f"Leverage: {value / 10:.1f}"))
    backtest_parameters_inner_layout.addWidget(leverage_label)
    backtest_parameters_inner_layout.addWidget(leverage_slider)

    date_slider = QSlider(Qt.Orientation.Horizontal)
    date_slider.setRange(0, (2025 - 1950) * 12)
    date_slider.setValue((2025 - 1950) // 2 * 12)
    date_label = QLabel(f"Starting Date: {QDate(1950, 1, 1).addMonths(date_slider.value()).toString('yyyy-MM')}")
    date_slider.valueChanged.connect(lambda value: date_label.setText(f"Starting Date: {QDate(1950, 1, 1).addMonths(value).toString('yyyy-MM')}"))
    backtest_parameters_inner_layout.addWidget(date_label)
    backtest_parameters_inner_layout.addWidget(date_slider)

    backtest_parameters_layout.addWidget(backtest_parameters_button)
    backtest_parameters_layout.addWidget(backtest_parameters_widget)
    setup_expandable_animation(backtest_parameters_button, backtest_parameters_widget)
    
    return backtest_parameters_layout, clusters_buttons_layout