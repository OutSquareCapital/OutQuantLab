from UI_Common import create_scroll_area, add_category_widget_shared, create_apply_button, select_all_items, unselect_all_items, create_checkbox_item
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PySide6.QtCore import Signal
from .Config_Backend import save_config_file
from typing import Dict, List
from Files import METHODS_CONFIG_FILE, ASSETS_TO_TEST_CONFIG_FILE

class GenericSelectionWidget(QWidget):
    saved_signal = Signal()

    def __init__(self, current_config: Dict, items: List[str], config_file: str, parent=None):
        super().__init__(parent)
        self.current_config = current_config
        self.items = items
        self.config_file = config_file
        self.category_vars = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        scroll_area, _, scroll_layout = create_scroll_area()

        for category in self.current_config.keys():
            self.add_category_widget(category, scroll_layout)

        layout.addWidget(scroll_area)

        self.apply_button = create_apply_button(self.save_selection)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, layout: QVBoxLayout):
        if category not in self.category_vars:
            self.category_vars[category] = {}

        def create_checkbox(category: str, item: str, is_checked: bool) -> QCheckBox:
            checkbox = create_checkbox_item(
                self, category, item, is_checked, 
                lambda _: self.check_item_count()
            )
            self.category_vars[category][item] = checkbox
            return checkbox

        add_category_widget_shared(
            parent=self,
            category=category,
            items={item: item in self.current_config.get(category, []) for item in self.items},
            layout=layout,
            create_checkbox=create_checkbox,
            select_all_callback=self.select_all,
            unselect_all_callback=self.unselect_all,
        )

    def save_selection(self):
        for category, item_vars in self.category_vars.items():
            self.current_config[category] = [
                item for item, checkbox in item_vars.items() if checkbox.isChecked()
            ]
        
        save_config_file(self.config_file, self.current_config, 3)
        self.apply_button.setEnabled(False)
        self.saved_signal.emit()

    def select_all(self, category: str):
        select_all_items(category, self.category_vars[category])

    def unselect_all(self, category: str):
        unselect_all_items(category, self.category_vars[category])

class MethodSelectionWidget(GenericSelectionWidget):
    def __init__(self, current_config: Dict[str, Dict[str, bool]]):
        # Les noms des méthodes sont les clés internes du dictionnaire par catégorie.
        super().__init__(current_config, [], METHODS_CONFIG_FILE)

    def add_category_widget(self, category: str, layout: QVBoxLayout):
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
            items=self.current_config[category],
            layout=layout,
            create_checkbox=create_checkbox,
            select_all_callback=self.select_all,
            unselect_all_callback=self.unselect_all,
        )

    def update_method_state(self, category: str, method: str, is_checked: bool):
        self.current_config[category][method] = is_checked
        self.apply_button.setEnabled(True)

    def save_selection(self):
        save_config_file(self.config_file, self.current_config, 4)
        self.apply_button.setEnabled(False)
        self.saved_signal.emit()

    def select_all(self, category: str):
        select_all_items(category, self.category_vars[category])
        self.apply_button.setEnabled(True)

    def unselect_all(self, category: str):
        unselect_all_items(category, self.category_vars[category])
        self.apply_button.setEnabled(True)


class AssetSelectionWidget(GenericSelectionWidget):
    def __init__(self, current_config: Dict[str, List[str]], assets_names: List[str]):
        super().__init__(current_config, assets_names, ASSETS_TO_TEST_CONFIG_FILE)

    def check_item_count(self):
        warnings_active = False
        for category in ["ratios", "ensembles"]:
            if category in self.category_vars:
                selected_items = sum(
                    1 for _, checkbox in self.category_vars[category].items() if checkbox.isChecked()
                )
                if selected_items == 1:
                    warnings_active = True
                    break
        self.apply_button.setEnabled(not warnings_active)