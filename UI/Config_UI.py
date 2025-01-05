from UI.Common_UI import (
create_checkbox_item, 
create_expandable_section,
connect_sliders_to_update, 
create_scroll_with_buttons,
create_param_widget
)
from PySide6.QtWidgets import (
QWidget, 
QVBoxLayout,
QCheckBox,  
QLabel, 
QGroupBox, 
QSlider
)
from ConfigClasses import AssetsCollection, IndicatorsCollection

class AssetSelectionWidget(QWidget):
    def __init__(self, assets_collection: AssetsCollection) -> None:
        super().__init__()
        self.assets_collection: AssetsCollection = assets_collection
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
    
        scroll_layout: QVBoxLayout = create_scroll_with_buttons(
        parent_layout=layout, 
        select_callback=self.select_all_assets, 
        unselect_callback=self.unselect_all_assets
        )
        
        for asset in self.assets_collection.all_entities:
            checkbox: QCheckBox = create_checkbox_item(
            item=asset.name,
            is_checked=asset.active,
            callback=lambda checked, name=asset.name: self.assets_collection.set_active(name=name, active=checked)
            )
            scroll_layout.addWidget(checkbox)
            self.checkboxes[asset.name] = checkbox

        self.setLayout(layout)

    def select_all_assets(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_assets(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

class IndicatorsConfigWidget(QWidget):

    def __init__(self, indics_collection: IndicatorsCollection) -> None:
        super().__init__()
        self.indics_collection: IndicatorsCollection = indics_collection
        self.param_widgets: dict[str, dict[str, dict[str, QSlider | QLabel]]] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        scroll_layout: QVBoxLayout = create_scroll_with_buttons(
        parent_layout=layout, 
        select_callback=self.select_all_indicators, 
        unselect_callback=self.unselect_all_indicators
        )

        for indicator in self.indics_collection.all_entities:
            self.add_indicator_section(
                indicator_name=indicator.name, 
                is_active=indicator.active, 
                params=indicator.params_values, 
                layout=scroll_layout
                )
            
        self.setLayout(layout)

    def add_indicator_section(
        self, 
        indicator_name: str, 
        is_active: bool, 
        params: dict[str, list[int]], 
        layout: QVBoxLayout) -> None:

        indicator_box, content_layout = create_expandable_section(category_name=indicator_name)

        checkbox: QCheckBox = create_checkbox_item(
        item=indicator_name,
        is_checked=is_active,
        callback=lambda checked, name=indicator_name: self.indics_collection.set_active(name=indicator_name, active=checked)
        )
        content_layout.addWidget(checkbox)
        self.checkboxes[indicator_name] = checkbox

        for param_name, values in params.items():
            self.add_param_widget(indicator_name=indicator_name, param_name=param_name, values=values, layout=content_layout)

        layout.addWidget(indicator_box)

    def add_param_widget(
        self, 
        indicator_name: str, 
        param_name: str, 
        values: list[int], 
        layout: QVBoxLayout) -> None:
        
        if not values:
            values = [1]

        param_box = QGroupBox(title=param_name)
        param_layout = QVBoxLayout()
        layout.addWidget(param_box)
        
        (
        range_info_label, 
        num_values_info_label, 
        generated_values_label, 
        start_slider, 
        end_slider, 
        num_values_slider
        ) = create_param_widget(param_box=param_box, param_layout=param_layout, values=values)

        def update_param_values(unique_values: list[int]) -> None:
            self.indics_collection.update_param_values(name=indicator_name, param_key=param_name, values=unique_values)

        connect_sliders_to_update(
        start_slider=start_slider, 
        end_slider=end_slider, 
        num_values_slider=num_values_slider,
        range_info_label=range_info_label, 
        num_values_info_label=num_values_info_label, 
        generated_values_label=generated_values_label,
        update_callback=update_param_values
        )

        self.param_widgets.setdefault(indicator_name, {})[param_name] = {
            "start_slider": start_slider,
            "end_slider": end_slider,
            "num_values_slider": num_values_slider,
            "range_info_label": range_info_label,
            "num_values_info_label": num_values_info_label,
        }

    def select_all_indicators(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_indicators(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
