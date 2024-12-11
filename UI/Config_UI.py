from .Common_UI import (create_scroll_area, 
                        create_checkbox_item, 
                        create_expandable_section, 
                        add_select_buttons, 
                        create_range_sliders, 
                        create_info_labels, 
                        create_num_values_slider, 
                        connect_sliders_to_update, 
                        populate_tree_from_dict, 
                        add_category, 
                        delete_category
)
from PySide6.QtWidgets import (QAbstractItemView, 
                               QWidget, 
                               QVBoxLayout, 
                               QCheckBox,  
                               QLabel, 
                               QGroupBox, 
                               QHBoxLayout, 
                               QSlider, 
                               QTreeWidget, 
                               QPushButton, 
                               QApplication
)
from PySide6.QtCore import Qt

from Config import AssetsCollection, IndicatorsCollection, BaseCollection

class AssetSelectionWidget(QWidget):
    def __init__(self, assets_collection: AssetsCollection, parent=None):
        super().__init__(parent)
        self.assets_collection = assets_collection
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        scroll_area, scroll_widget, scroll_layout = create_scroll_area()
        for asset in self.assets_collection.get_all_entities():
            checkbox = create_checkbox_item(
                parent=self,
                item=asset.name,
                is_checked=asset.active,
                callback=lambda checked, name=asset.name: self.update_asset_state(name, checked)
            )
            scroll_layout.addWidget(checkbox)
            self.checkboxes[asset.name] = checkbox

        scroll_area.setWidget(scroll_widget)

        layout.addWidget(scroll_area)
        buttons_layout = QHBoxLayout()
        add_select_buttons(buttons_layout, self.select_all_assets, self.unselect_all_assets)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def update_asset_state(self, asset_name: str, is_checked: bool):
        self.assets_collection.set_active(asset_name, is_checked)

    def select_all_assets(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_assets(self):
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

class IndicatorsConfigWidget(QWidget):

    def __init__(self, indicators_collection: IndicatorsCollection, parent=None):
        super().__init__(parent)
        self.indicators_collection = indicators_collection
        self.param_widgets: dict[str, dict[str, dict[str, QSlider | QLabel]]] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        scroll_area, scroll_widget, scroll_layout = create_scroll_area()

        for indicator in self.indicators_collection.get_all_entities():
            self.add_indicator_section(indicator.name, indicator.active, indicator.params, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        layout.addWidget(scroll_area)

        buttons_layout = QHBoxLayout()
        add_select_buttons(buttons_layout, self.select_all_indicators, self.unselect_all_indicators)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)

    def add_indicator_section(self, indicator_name: str, is_active: bool, params: dict[str, list[int]], layout: QVBoxLayout):

        indicator_box, content_widget, content_layout = create_expandable_section(indicator_name)

        checkbox = create_checkbox_item(
            parent=self,
            item=indicator_name,
            is_checked=is_active,
            callback=lambda checked, name=indicator_name: self.update_indicator_state(name, checked)
        )
        content_layout.addWidget(checkbox)
        self.checkboxes[indicator_name] = checkbox

        for param_name, values in params.items():
            self.add_param_widget(indicator_name, param_name, values, content_layout)

        layout.addWidget(indicator_box)

    def add_param_widget(self, indicator_name: str, param_name: str, values: list[int], layout: QVBoxLayout):
        param_box = QGroupBox(param_name)
        param_layout = QVBoxLayout()

        if not values:
            values = [1]

        range_info_label, num_values_info_label, generated_values_label = create_info_labels(values)
        param_layout.addWidget(range_info_label)
        param_layout.addWidget(num_values_info_label)

        scroll_area, _, _ = create_scroll_area()
        scroll_area.setWidget(generated_values_label)
        scroll_area.setFixedHeight(50)
        param_layout.addWidget(scroll_area)

        start_slider, end_slider = create_range_sliders(values)
        num_values_slider = create_num_values_slider(len(values))

        sliders_layout = QHBoxLayout()
        sliders_layout.addWidget(QLabel("Start:"))
        sliders_layout.addWidget(start_slider)
        sliders_layout.addWidget(QLabel("End:"))
        sliders_layout.addWidget(end_slider)
        param_layout.addLayout(sliders_layout)

        num_values_layout = QHBoxLayout()
        num_values_layout.addWidget(QLabel("Num Values:"))
        num_values_layout.addWidget(num_values_slider)
        param_layout.addLayout(num_values_layout)

        # Connecter les sliders à la mise à jour des valeurs
        connect_sliders_to_update(
            start_slider, end_slider, num_values_slider,
            range_info_label, num_values_info_label, generated_values_label,
            lambda unique_values: self.indicators_collection.update_param_values(indicator_name, param_name, unique_values)
        )

        param_box.setLayout(param_layout)
        layout.addWidget(param_box)

        self.param_widgets.setdefault(indicator_name, {})[param_name] = {
            "start_slider": start_slider,
            "end_slider": end_slider,
            "num_values_slider": num_values_slider,
            "range_info_label": range_info_label,
            "num_values_info_label": num_values_info_label,
        }

    def update_indicator_state(self, indicator_name: str, is_checked: bool):
        self.indicators_collection.set_active(indicator_name, is_checked)

    def select_all_indicators(self):

        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_indicators(self):

        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)
class TreeStructureWidget(QWidget):
    def __init__(self, collection: BaseCollection, parent=None):
        super().__init__(parent)
        self.collection = collection
        self.tree_structure = self.collection.clusters
        self.data = set(self.collection.get_all_entities_names())

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree.itemClicked.connect(self.handle_item_click)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        populate_tree_from_dict(self.tree, self.tree_structure, self.data)
        layout.addWidget(self.tree)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton("Add Category")
        delete_button = QPushButton("Delete Category")

        add_button.clicked.connect(lambda: add_category(self.tree, self.tree_structure, self.data))
        delete_button.clicked.connect(lambda: delete_category(self.tree, self.tree_structure))

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def handle_item_click(self, item, column):
        if Qt.KeyboardModifier.ControlModifier & QApplication.keyboardModifiers():
            item.setSelected(not item.isSelected())
        elif Qt.KeyboardModifier.ShiftModifier & QApplication.keyboardModifiers():
            current_items = self.tree.selectedItems()
            if current_items:
                start = self.tree.indexOfTopLevelItem(current_items[0])
                end = self.tree.indexOfTopLevelItem(item)
                if start != -1 and end != -1:
                    for i in range(min(start, end), max(start, end) + 1):
                        self.tree.topLevelItem(i).setSelected(True)