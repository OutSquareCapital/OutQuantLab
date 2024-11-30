from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QWidget, QCheckBox, QGroupBox
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPalette, QBrush, QPixmap
from typing import Callable
from typing import Dict

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def create_scroll_area() ->tuple[QScrollArea, QWidget, QVBoxLayout]:
    """
    Creates a scrollable area with a vertical layout.
    """
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


def create_apply_button(apply_callback: Callable[[], None]) -> QPushButton:
    """
    Creates an 'Apply' button, initially disabled.
    """
    apply_button = QPushButton("Apply")
    apply_button.setEnabled(False)
    apply_button.clicked.connect(apply_callback)
    return apply_button

def add_category_widget_shared(
    parent,
    category: str,
    items: Dict[str, bool],
    layout: QVBoxLayout,
    create_checkbox: Callable[[str, str, bool], QCheckBox],
    select_all_callback: Callable[[str], None],
    unselect_all_callback: Callable[[str], None],
):
    category_box, content_widget, content_layout = create_expandable_section(category)

    # Add Select All and Unselect All buttons
    button_layout = QHBoxLayout()
    select_all_button = QPushButton("Select All")
    unselect_all_button = QPushButton("Unselect All")

    select_all_button.clicked.connect(lambda: select_all_callback(category))
    unselect_all_button.clicked.connect(lambda: unselect_all_callback(category))

    button_layout.addWidget(select_all_button)
    button_layout.addWidget(unselect_all_button)
    content_layout.addLayout(button_layout)

    # Create checkboxes for each item
    for item, is_checked in items.items():
        item_checkbox = create_checkbox(category, item, is_checked)
        content_layout.addWidget(item_checkbox)

    layout.addWidget(category_box)

def select_all_items(category: str, items: Dict[str, QCheckBox]):
    """Active toutes les checkboxes d'une catégorie."""
    for checkbox in items.values():
        checkbox.setChecked(True)

def unselect_all_items(category: str, items: Dict[str, QCheckBox]):
    """Désactive toutes les checkboxes d'une catégorie."""
    for checkbox in items.values():
        checkbox.setChecked(False)

def create_checkbox_item(parent, category: str, item: str, is_checked: bool, callback: Callable[[bool], None]) -> QCheckBox:
    """Crée une checkbox avec un état initial et un callback."""
    checkbox = QCheckBox(item)
    checkbox.setChecked(is_checked)
    checkbox.stateChanged.connect(lambda: callback(checkbox.isChecked()))
    return checkbox