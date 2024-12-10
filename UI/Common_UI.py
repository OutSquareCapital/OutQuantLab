from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, QScrollArea, QWidget, QCheckBox, QGroupBox, QFrame, QHBoxLayout
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QPalette, QBrush, QPixmap
from typing import Callable

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
    palette.setBrush(QPalette.Window, QBrush(pixmap))
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
    animation.setEasingCurve(QEasingCurve.InOutCubic)

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

def create_buttons_from_list(layout: QVBoxLayout, buttons_names: list, buttons_actions: list):
    for btn_text in buttons_names:
        button = QPushButton(btn_text)
        button.clicked.connect(buttons_actions.get(btn_text, lambda: None))
        layout.addWidget(button)

def create_expandable_buttons_list(toggle_button_name: str, buttons_names: list, buttons_actions: list, open_on_launch: bool = False):
    toggle_button = QPushButton(toggle_button_name)
    outer_layout = QVBoxLayout()
    outer_layout.setAlignment(Qt.AlignTop)
    buttons_widget = QWidget()
    inner_layout = QVBoxLayout(buttons_widget)
    create_buttons_from_list(inner_layout, buttons_names, buttons_actions)
    outer_layout.addWidget(toggle_button)
    outer_layout.addWidget(buttons_widget)
    setup_expandable_animation(toggle_button, buttons_widget)
    if open_on_launch:
        toggle_button.setChecked(True)
    return outer_layout

def create_expandable_section(category_name: str) -> tuple[QGroupBox, QPushButton, QWidget]:

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