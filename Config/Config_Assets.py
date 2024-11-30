from UI_Common import create_scroll_area, add_category_widget_shared, create_apply_button, select_all_items, unselect_all_items, create_checkbox_item
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from PySide6.QtCore import Signal
from typing import Dict, List
from .Config_Backend import save_assets_to_backtest_config


class AssetSelectionWidget(QWidget):
    assets_saved = Signal()

    def __init__(self, current_config: Dict[str, List[str]], assets_names: List[str]):
        super().__init__()
        self.current_config = current_config
        self.assets_names = assets_names
        self.category_vars = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Create scroll area for assets
        scroll_area, _, scroll_layout = create_scroll_area()

        # Add categories to the scroll area
        for category in self.current_config.keys():
            self.add_category_widget(category, scroll_layout)

        layout.addWidget(scroll_area)

        # Add Apply button
        self.apply_button = create_apply_button(self.save_selection)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, layout: QVBoxLayout):
        if category not in self.category_vars:
            self.category_vars[category] = {}

        def create_checkbox(category: str, asset: str, is_checked: bool) -> QCheckBox:
            checkbox = create_checkbox_item(
                self, category, asset, is_checked, 
                lambda _: self.check_asset_count()
            )
            self.category_vars[category][asset] = checkbox
            return checkbox

        add_category_widget_shared(
            parent=self,
            category=category,
            items={asset: asset in self.current_config.get(category, []) for asset in self.assets_names},
            layout=layout,
            create_checkbox=create_checkbox,
            select_all_callback=self.select_all,
            unselect_all_callback=self.unselect_all,
        )

    def check_asset_count(self):
        warnings_active = False
        for category in ["ratios", "ensembles"]:
            if category in self.category_vars:
                selected_assets = sum(
                    1 for _, checkbox in self.category_vars[category].items() if checkbox.isChecked()
                )
                if selected_assets == 1:  # Disable Apply button if only one is selected
                    warnings_active = True
                    break
        self.apply_button.setEnabled(not warnings_active)

    def save_selection(self):
        for category, asset_vars in self.category_vars.items():
            self.current_config[category] = [
                asset for asset, checkbox in asset_vars.items() if checkbox.isChecked()
            ]
        save_assets_to_backtest_config(self.current_config)
        self.apply_button.setEnabled(False)
        self.assets_saved.emit()

    def select_all(self, category: str):
        select_all_items(category, self.category_vars[category])
        self.check_asset_count()

    def unselect_all(self, category: str):
        unselect_all_items(category, self.category_vars[category])
        self.check_asset_count()

    def get_data(self) -> Dict[str, List[str]]:
        return self.current_config
