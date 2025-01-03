from PySide6.QtWidgets import (
QVBoxLayout, 
QPushButton, 
QScrollArea, 
QWidget, 
QCheckBox, 
QGroupBox, 
QFrame, 
QHBoxLayout, 
QSlider, 
QLabel, 
QLayout
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PySide6.QtGui import QPalette, QBrush, QPixmap
from collections.abc import Callable

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
