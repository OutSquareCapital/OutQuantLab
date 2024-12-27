from .Common_UI import (
create_checkbox_item, 
create_expandable_section,
connect_sliders_to_update, 
populate_tree_from_dict, 
add_cluster, 
delete_cluster,
create_scroll_with_buttons,
create_param_widget
)
from PySide6.QtWidgets import (
QAbstractItemView, 
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
from Config import AssetsCollection, ClustersTree, IndicatorsCollection, Asset, IndicatorState

class AssetSelectionWidget(QWidget):
    def __init__(self, assets_collection: AssetsCollection, parent=None):
        super().__init__(parent)
        self.assets_collection = assets_collection
        self.entities: list[Asset] = self.assets_collection.all_entities
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
    
        scroll_layout = create_scroll_with_buttons(
        layout, 
        self.select_all_assets, 
        self.unselect_all_assets
        )
        
        for asset in self.entities:
            checkbox = create_checkbox_item(
            item=asset.name,
            is_checked=asset.active,
            callback=lambda checked, name=asset.name: self.update_asset_state(name, checked)
            )
            scroll_layout.addWidget(checkbox)
            self.checkboxes[asset.name] = checkbox

        self.setLayout(layout)
        
    def update_asset_state(self, asset_name: str, is_checked: bool) -> None:
        self.assets_collection.set_active(asset_name, is_checked)

    def select_all_assets(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_assets(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

class IndicatorsConfigWidget(QWidget):

    def __init__(self, indicators_collection: IndicatorsCollection, parent=None):
        super().__init__(parent)
        self.indicators_collection = indicators_collection
        self.entities:list[IndicatorState] = self.indicators_collection.all_entities
        self.param_widgets: dict[str, dict[str, dict[str, QSlider | QLabel]]] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self) -> None:
        layout = QVBoxLayout()
        scroll_layout = create_scroll_with_buttons(
        layout, 
        self.select_all_indicators, 
        self.unselect_all_indicators
        )

        for indicator in self.entities:
            self.add_indicator_section(indicator.name, indicator.active, indicator.params_values, scroll_layout)
            
        self.setLayout(layout)

    def add_indicator_section(
        self, 
        indicator_name: str, 
        is_active: bool, 
        params: dict[str, list[int]], 
        layout: QVBoxLayout) -> None:

        indicator_box, content_layout = create_expandable_section(indicator_name)

        checkbox = create_checkbox_item(
        item=indicator_name,
        is_checked=is_active,
        callback=lambda checked, name=indicator_name: self.update_indicator_state(name, checked)
        )
        content_layout.addWidget(checkbox)
        self.checkboxes[indicator_name] = checkbox

        for param_name, values in params.items():
            self.add_param_widget(indicator_name, param_name, values, content_layout)

        layout.addWidget(indicator_box)

    def add_param_widget(
        self, 
        indicator_name: str, 
        param_name: str, 
        values: list[int], 
        layout: QVBoxLayout) -> None:
        
        if not values:
            values = [1]

        param_box = QGroupBox(param_name)
        param_layout = QVBoxLayout()
        layout.addWidget(param_box)
        
        (
        range_info_label, 
        num_values_info_label, 
        generated_values_label, 
        start_slider, 
        end_slider, 
        num_values_slider
        ) = create_param_widget(param_box, param_layout, values)

        connect_sliders_to_update(
        start_slider, end_slider, num_values_slider,
        range_info_label, num_values_info_label, generated_values_label,
        lambda unique_values: self.indicators_collection.update_param_values(indicator_name, param_name, unique_values)
        )

        self.param_widgets.setdefault(indicator_name, {})[param_name] = {
            "start_slider": start_slider,
            "end_slider": end_slider,
            "num_values_slider": num_values_slider,
            "range_info_label": range_info_label,
            "num_values_info_label": num_values_info_label,
        }

    def update_indicator_state(self, indicator_name: str, is_checked: bool) -> None:
        self.indicators_collection.set_active(indicator_name, is_checked)

    def select_all_indicators(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_indicators(self) -> None:
        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

class TreeStructureWidget(QWidget):
    def __init__(self, collection, clusters: ClustersTree, parent=None) -> None:
        super().__init__(parent)
        self.collection = collection
        self.clusters_tree = clusters
        self.tree_structure = self.clusters_tree.clusters
        self.data = set(self.collection.all_entities_names)

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
        add_button = QPushButton("Add Cluster")
        delete_button = QPushButton("Delete Cluster")

        add_button.clicked.connect(lambda: add_cluster(self.tree, self.tree_structure))
        delete_button.clicked.connect(lambda: delete_cluster(self.tree, self.tree_structure))


        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def handle_item_click(self, item):
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