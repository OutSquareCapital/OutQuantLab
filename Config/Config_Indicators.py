from UI_Common import create_scroll_area, add_category_widget_shared, create_apply_button, select_all_items, unselect_all_items, create_checkbox_item
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PySide6.QtCore import Signal
from typing import Dict
from .Config_Backend import save_methods_config, get_active_methods


class MethodSelectionWidget(QWidget):
    methods_saved = Signal()

    def __init__(self, current_config: Dict[str, Dict[str, bool]]):
        super().__init__()
        self.current_config = current_config
        self.category_vars = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create scroll area for methods
        scroll_area, _, scroll_layout = create_scroll_area()

        # Add categories to the scroll area
        for category, methods in self.current_config.items():
            self.add_category_widget(category, methods, scroll_layout)

        layout.addWidget(scroll_area)

        # Add Apply button
        self.apply_button = create_apply_button(self.save_configuration)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, methods: Dict[str, bool], layout: QVBoxLayout):
        if category not in self.category_vars:
            self.category_vars[category] = {}

        def create_checkbox(category: str, method: str, is_checked: bool) -> QCheckBox:
            checkbox = create_checkbox_item(
                self, category, method, is_checked, 
                lambda _: self.update_method_state(category, method, checkbox.isChecked())
            )
            self.category_vars[category][method] = checkbox
            return checkbox

        add_category_widget_shared(
            parent=self,
            category=category,
            items=methods,
            layout=layout,
            create_checkbox=create_checkbox,
            select_all_callback=self.select_all,
            unselect_all_callback=self.unselect_all,
        )

    def update_method_state(self, category: str, method: str, is_checked: bool):
        self.current_config[category][method] = is_checked
        self.apply_button.setEnabled(True)

    def select_all(self, category: str):
        select_all_items(category, self.category_vars[category])
        self.apply_button.setEnabled(True)

    def unselect_all(self, category: str):
        unselect_all_items(category, self.category_vars[category])
        self.apply_button.setEnabled(True)

    def save_configuration(self):
        save_methods_config(self.current_config)
        self.apply_button.setEnabled(False)
        self.methods_saved.emit()

    def get_data(self) -> Dict[str, Dict[str, bool]]:
        return self.current_config

    def get_active_methods(self):
        return get_active_methods(self.current_config)
