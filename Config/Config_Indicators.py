from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QCheckBox, QPushButton, QHBoxLayout, QScrollArea, QLabel
)
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, Signal
from .Config_Backend import save_methods_config, get_active_methods
from typing import List, Callable


class MethodSelectionWidget(QWidget):
    methods_saved = Signal()

    def __init__(self, current_config: dict):
        super().__init__()
        self.current_config = current_config
        self.category_widgets = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()

        for category, methods in self.current_config.items():
            self.add_category_widget(category, methods, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.apply_button = QPushButton("Apply")
        self.apply_button.setEnabled(False)
        self.apply_button.clicked.connect(self.save_configuration)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def save_configuration(self):
        save_methods_config(self.current_config)
        self.apply_button.setEnabled(False)
        self.methods_saved.emit()

    def add_category_widget(self, category: str, methods: dict, layout: QVBoxLayout):
        category_box = QGroupBox(category)
        category_layout = QVBoxLayout()
        category_content_widget = QWidget()
        category_content_layout = QVBoxLayout()
        category_content_widget.setLayout(category_content_layout)

        category_content_widget.setMaximumHeight(0)
        animation = QPropertyAnimation(category_content_widget, b"maximumHeight")
        animation.setDuration(300)
        animation.setEasingCurve(QEasingCurve.InOutCubic)

        edit_button = QPushButton("Expand/Collapse")
        edit_button.setCheckable(True)
        edit_button.toggled.connect(
            lambda checked, widget=category_content_widget, anim=animation: self.toggle_animation(checked, widget, anim)
        )

        button_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        unselect_all_button = QPushButton("Unselect All")
        button_layout.addWidget(select_all_button)
        button_layout.addWidget(unselect_all_button)

        select_all_button.clicked.connect(lambda _, c=category: self.select_all(c))
        unselect_all_button.clicked.connect(lambda _, c=category: self.unselect_all(c))

        for method, is_checked in methods.items():
            self.add_method_checkbox(category, method, is_checked, category_content_layout)

        category_box.setLayout(category_layout)
        category_layout.addWidget(edit_button)
        category_layout.addLayout(button_layout)
        category_layout.addWidget(category_content_widget)
        layout.addWidget(category_box)

    def add_method_checkbox(self, category: str, method: str, is_checked: bool, layout: QVBoxLayout):
        checkbox = QCheckBox(method)
        checkbox.setChecked(is_checked)
        checkbox.stateChanged.connect(lambda _: self.update_method_state(category, method, checkbox.isChecked()))
        layout.addWidget(checkbox)

    def toggle_animation(self, checked: bool, widget: QWidget, animation: QPropertyAnimation):
        if checked:
            animation.setStartValue(0)
            animation.setEndValue(widget.sizeHint().height())
        else:
            animation.setStartValue(widget.sizeHint().height())
            animation.setEndValue(0)
        animation.start()

    def update_method_state(self, category: str, method: str, is_checked: bool):
        self.current_config[category][method] = is_checked
        self.apply_button.setEnabled(True)

    def select_all(self, category: str):
        for method in self.current_config[category]:
            self.current_config[category][method] = True
        self.refresh_category_checkboxes(category)
        self.apply_button.setEnabled(True)

    def unselect_all(self, category: str):
        for method in self.current_config[category]:
            self.current_config[category][method] = False
        self.refresh_category_checkboxes(category)
        self.apply_button.setEnabled(True)

    def refresh_category_checkboxes(self, category: str):
        for checkbox in self.findChildren(QCheckBox):
            if checkbox.text() in self.current_config[category]:
                checkbox.setChecked(self.current_config[category][checkbox.text()])

    def get_data(self) -> dict:
        return self.current_config
    
    def get_active_methods(self) -> List[Callable]:
        return get_active_methods(self.current_config)
        


