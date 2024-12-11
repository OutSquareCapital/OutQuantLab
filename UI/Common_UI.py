from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, QTreeWidget, QScrollArea, QWidget, QCheckBox, QGroupBox, QFrame, QHBoxLayout, QSlider, QLabel, QTreeWidgetItem, QMessageBox, QInputDialog
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QPalette, QBrush, QPixmap
from typing import Callable, Tuple, Dict, Any
from PySide6.QtGui import QFont

def add_category(tree: QTreeWidget, tree_structure: Dict[str, Any], data: set):
    category_name, ok = QInputDialog.getText(tree, "New Category", "Category Name:")
    if ok and category_name:
        if category_name in tree_structure:
            QMessageBox.warning(tree, "Warning", f"The category '{category_name}' already exists.")
            return

        tree_structure[category_name] = {}
        category_item = QTreeWidgetItem([category_name])
        category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
        tree.addTopLevelItem(category_item)

def delete_category(tree: QTreeWidget, tree_structure: Dict[str, Any]):
    selected_item = tree.currentItem()
    if selected_item:
        parent = selected_item.parent()
        if parent is None:
            index = tree.indexOfTopLevelItem(selected_item)
            tree.takeTopLevelItem(index)
        else:
            parent.removeChild(selected_item)


def find_element_in_tree(tree: QTreeWidget, element: str) -> bool:
    def traverse(item):
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


def populate_tree_from_dict(tree: QTreeWidget, data: Dict[str, Any], data_set: set, parent_item=None):
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


def create_info_labels(values: list) -> Tuple[QLabel, QLabel, QLabel]:
    range_info_label = QLabel(f"Range: {min(values)} - {max(values)}")
    num_values_info_label = QLabel(f"Num Values: {len(values)}")
    generated_values_label = QLabel(f"Generated Values: {values}")
    generated_values_label.setWordWrap(False)
    return range_info_label, num_values_info_label, generated_values_label

def create_range_sliders(values: list) -> Tuple[QSlider, QSlider]:
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

def value_to_index(value: int) -> int:
    return int(value).bit_length() - 1

def index_to_value(index: int) -> int:
    return 2 ** index

def connect_sliders_to_update(
    start_slider: QSlider, end_slider: QSlider, num_values_slider: QSlider,
    range_info_label: QLabel, num_values_info_label: QLabel, generated_values_label: QLabel,
    update_callback: Callable
):
    def update_values():
        start = index_to_value(start_slider.value())
        end = index_to_value(end_slider.value())
        num_values = num_values_slider.value()

        # Validation des sliders
        if start * 2 > end:
            if start_slider.hasFocus():
                end_slider.setValue(value_to_index(start * 2))
            elif end_slider.hasFocus():
                start_slider.setValue(value_to_index(end // 2))

        # Génération des valeurs
        generated_values = param_range_values(start, end, num_values)
        unique_values = sorted(set(generated_values))
        range_info_label.setText(f"Range: {start} - {end}")
        num_values_info_label.setText(f"Num Values: {len(unique_values)}")
        generated_values_label.setText(f"Generated Values: {unique_values}")

        # Appeler le callback pour sauvegarder les modifications
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


def param_range_values(start: int, end: int, num_values: int) -> list:
    if num_values == 1:
        return [int((start + end) / 2)]
    ratio = (end / start) ** (1 / (num_values - 1))
    return [int(round(start * (ratio ** i))) for i in range(num_values)]

def set_frame_design(frame_style):
    frame = QFrame()
    frame.setStyleSheet(frame_style)
    return frame

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def create_scroll_area() ->tuple[QScrollArea, QWidget, QVBoxLayout]:
    scroll_area = QScrollArea()
    scroll_widget = QWidget()
    scroll_layout = QVBoxLayout()
    scroll_widget.setLayout(scroll_layout)
    scroll_area.setWidget(scroll_widget)
    scroll_area.setWidgetResizable(True)
    return scroll_area, scroll_widget, scroll_layout

def setup_expandable_animation(toggle_button: QPushButton, content_widget: QWidget, animation_duration: int = 500) -> QPropertyAnimation:

    content_widget.setMaximumHeight(0)
    animation = QPropertyAnimation(content_widget, b"maximumHeight")
    animation.setDuration(animation_duration)
    animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

    def toggle_animation(checked: bool):
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

def create_buttons_from_list(layout: QVBoxLayout, buttons_names: list, buttons_actions: Dict[str, Callable]):
    for btn_text in buttons_names:
        button = QPushButton(btn_text)
        button.clicked.connect(buttons_actions.get(btn_text, lambda: None))
        layout.addWidget(button)

def create_expandable_buttons_list(toggle_button_name: str, buttons_names: list, buttons_actions: Dict[str, Callable], open_on_launch: bool = False):
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

def create_expandable_section(category_name: str) -> tuple[QGroupBox, QWidget, QVBoxLayout]:

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

    return category_box, content_widget, content_layout

def create_checkbox_item(parent, item: str, is_checked: bool, callback: Callable[[bool], None]) -> QCheckBox:
    checkbox = QCheckBox(item)
    checkbox.setChecked(is_checked)
    checkbox.stateChanged.connect(lambda: callback(checkbox.isChecked()))
    return checkbox