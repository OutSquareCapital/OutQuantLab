from .Common_UI import param_range_values, create_scroll_area, create_checkbox_item, create_expandable_section
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox,  QLabel, QMessageBox, QGroupBox, QHBoxLayout, QSlider, QTreeWidget, QTreeWidgetItem, QPushButton, QInputDialog, QApplication
from PySide6.QtCore import Qt
from typing import Dict, List, Any
from PySide6.QtGui import QFont
from Config import AssetsCollection, IndicatorsCollection

class AssetSelectionWidget(QWidget):
    def __init__(self, assets_collection: AssetsCollection, parent=None):
        super().__init__(parent)
        self.assets_collection = assets_collection
        self.checkboxes: Dict[str, QCheckBox] = {}
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

        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_assets)
        buttons_layout.addWidget(select_all_button)

        unselect_all_button = QPushButton("Unselect All")
        unselect_all_button.clicked.connect(self.unselect_all_assets)
        buttons_layout.addWidget(unselect_all_button)

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
        self.param_widgets: Dict[str, Dict[str, Dict[str, QSlider]]] = {}
        self.checkboxes: Dict[str, QCheckBox] = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Créer une zone de défilement principale
        scroll_area, scroll_widget, scroll_layout = create_scroll_area()

        # Ajouter une section pour chaque indicateur avec checkbox d'activation + paramètres
        for indicator in self.indicators_collection.get_all_entities():
            self.add_indicator_section(indicator.name, indicator.active, indicator.params, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        layout.addWidget(scroll_area)

        # Boutons "Select All" et "Unselect All" pour activer/désactiver tous les indicateurs
        buttons_layout = QHBoxLayout()
        select_all_button = QPushButton("Select All")
        select_all_button.clicked.connect(self.select_all_indicators)
        buttons_layout.addWidget(select_all_button)

        unselect_all_button = QPushButton("Unselect All")
        unselect_all_button.clicked.connect(self.unselect_all_indicators)
        buttons_layout.addWidget(unselect_all_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def add_indicator_section(self, indicator_name: str, is_active: bool, params: Dict[str, List[int]], layout: QVBoxLayout):
        # Section extensible par indicateur
        indicator_box, content_widget, content_layout = create_expandable_section(indicator_name)

        # Ajout de la checkbox pour l'activation de l'indicateur
        checkbox = create_checkbox_item(
            parent=self,
            item=indicator_name,
            is_checked=is_active,
            callback=lambda checked, name=indicator_name: self.update_indicator_state(name, checked)
        )
        content_layout.addWidget(checkbox)
        self.checkboxes[indicator_name] = checkbox

        # Ajouter les widgets de paramètres si l'indicateur en a
        if params:
            for param_name, values in params.items():
                self.add_param_widget(indicator_name, param_name, values, content_layout)

        layout.addWidget(indicator_box)

    def add_param_widget(self, indicator_name: str, param_name: str, values: List[int], layout: QVBoxLayout):
        param_box = QGroupBox(param_name)
        param_layout = QVBoxLayout()

        # Si values est vide ou None, on le remplace par [1]
        if not values:
            values = [1]

        range_info_label, num_values_info_label, scroll_area = self.create_info_labels(values)
        param_layout.addWidget(range_info_label)
        param_layout.addWidget(num_values_info_label)
        param_layout.addWidget(scroll_area)

        start_slider, end_slider = self.create_range_sliders(values)
        num_values_slider = self.create_num_values_slider(len(values))

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

        self.connect_sliders_to_update(
            indicator_name, param_name, start_slider, end_slider, num_values_slider,
            range_info_label, num_values_info_label, scroll_area.widget()
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

    def create_info_labels(self, values: list):
        range_info_label = QLabel(f"Range: {min(values)} - {max(values)}")
        num_values_info_label = QLabel(f"Num Values: {len(values)}")

        generated_values_label = QLabel(f"Generated Values: {values}")
        generated_values_label.setWordWrap(False)
        scroll_area, _, _ = create_scroll_area()
        scroll_area.setWidget(generated_values_label)
        scroll_area.setFixedHeight(50)

        return range_info_label, num_values_info_label, scroll_area

    def create_range_sliders(self, values: list):
        start_slider = QSlider(Qt.Horizontal)
        end_slider = QSlider(Qt.Horizontal)

        # On travaille sur des puissances de 2, de 1 à 4096 (2^12)
        # start_slider : 0 à 11  (2^0 =1, 2^11=2048)
        # end_slider   : 0 à 12  (2^0 =1, 2^12=4096)
        start_slider.setMinimum(0)
        start_slider.setMaximum(11)
        end_slider.setMinimum(0)
        end_slider.setMaximum(12)

        start_slider.setValue(self.value_to_index(min(values)))
        end_slider.setValue(self.value_to_index(max(values)))

        return start_slider, end_slider

    def create_num_values_slider(self, num_values: int):
        num_values_slider = QSlider(Qt.Horizontal)
        num_values_slider.setMinimum(1)
        num_values_slider.setMaximum(10)
        num_values_slider.setValue(num_values)
        return num_values_slider

    def value_to_index(self, value: int) -> int:
        return int(value).bit_length() - 1

    def index_to_value(self, index: int) -> int:
        return 2 ** index

    def connect_sliders_to_update(self, indicator_name: str, param_name: str,
                                  start_slider: QSlider, end_slider: QSlider, num_values_slider: QSlider,
                                  range_info_label: QLabel, num_values_info_label: QLabel, generated_values_label: QLabel):
        def update_values():
            start = self.index_to_value(start_slider.value())
            end = self.index_to_value(end_slider.value())
            num_values = num_values_slider.value()

            # Validation des valeurs
            if start * 2 > end:
                if start_slider.hasFocus():
                    end_slider.setValue(self.value_to_index(start * 2))
                    end = self.index_to_value(end_slider.value())
                elif end_slider.hasFocus():
                    start_slider.setValue(self.value_to_index(end // 2))
                    start = self.index_to_value(start_slider.value())

            generated_values = param_range_values(start, end, num_values)
            unique_values = list(sorted(set(generated_values)))
            range_info_label.setText(f"Range: {start} - {end}")
            num_values_info_label.setText(f"Num Values: {len(unique_values)}")
            generated_values_label.setText(f"Generated Values: {unique_values}")

            self.indicators_collection.update_param_values(indicator_name, param_name, unique_values)

        start_slider.valueChanged.connect(update_values)
        end_slider.valueChanged.connect(update_values)
        num_values_slider.valueChanged.connect(update_values)

    def update_indicator_state(self, indicator_name: str, is_checked: bool):
        self.indicators_collection.set_active(indicator_name, is_checked)

    def select_all_indicators(self):

        for checkbox in self.checkboxes.values():
            checkbox.setChecked(True)

    def unselect_all_indicators(self):

        for checkbox in self.checkboxes.values():
            checkbox.setChecked(False)

class TreeStructureWidget(QWidget):
    def __init__(self, collection, parent=None):
        super().__init__(parent)
        self.collection = collection

        # Récupérer la structure de clusters et les noms des objets
        self.tree_structure = self.collection.clusters
        self.data = set(self.collection.get_all_entities_names())

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree.itemClicked.connect(self.handle_item_click)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.populate_tree_from_dict(self.tree_structure)
        layout.addWidget(self.tree)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton("Add Category")
        delete_button = QPushButton("Delete Category")
        apply_button = QPushButton("Apply Changes")

        add_button.clicked.connect(self.add_category)
        delete_button.clicked.connect(self.delete_category)
        apply_button.clicked.connect(self.apply_changes)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(apply_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def populate_tree_from_dict(self, data: Dict[str, Any], parent_item=None):
        if parent_item is None:
            parent_item = self.tree

        for key, value in data.items():
            category_item = QTreeWidgetItem([key])
            category_item.setFlags(category_item.flags() | Qt.ItemIsDropEnabled)
            font = QFont()
            font.setUnderline(True)
            category_item.setFont(0, font)
            if isinstance(parent_item, QTreeWidget):
                parent_item.addTopLevelItem(category_item)
            else:
                parent_item.addChild(category_item)

            if isinstance(value, dict):
                self.populate_tree_from_dict(value, category_item)
            elif isinstance(value, list):
                for element in value:
                    if element in self.data:
                        child_item = QTreeWidgetItem([element])
                        child_item.setFlags(child_item.flags() & ~Qt.ItemIsDropEnabled)
                        category_item.addChild(child_item)

        # Ajouter les éléments non catégorisés
        if parent_item is self.tree:
            for element in self.data:
                if not self.find_element_in_tree(element):
                    orphan_item = QTreeWidgetItem([element])
                    orphan_item.setFlags(orphan_item.flags() & ~Qt.ItemIsDropEnabled)
                    self.tree.addTopLevelItem(orphan_item)

    def find_element_in_tree(self, element: str) -> bool:
        def traverse(item):
            if item.text(0) == element:
                return True
            for i in range(item.childCount()):
                if traverse(item.child(i)):
                    return True
            return False

        for i in range(self.tree.topLevelItemCount()):
            if traverse(self.tree.topLevelItem(i)):
                return True
        return False

    def apply_changes(self):
        def traverse_tree(item):
            if item.childCount() == 0:
                return item.text(0)

            result = {}
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() > 0:
                    result[child.text(0)] = traverse_tree(child)
                else:
                    if child.text(0) in self.data:
                        if isinstance(result, dict):
                            result = []
                        result.append(child.text(0))
            return result

        # Réinitialiser la structure
        self.tree_structure.clear()
        uncategorized_elements = []

        for i in range(self.tree.topLevelItemCount()):
            category_item = self.tree.topLevelItem(i)
            if category_item.childCount() > 0:
                self.tree_structure[category_item.text(0)] = traverse_tree(category_item)
            else:
                if category_item.text(0) in self.data:
                    uncategorized_elements.append(category_item.text(0))
                else:
                    self.tree_structure[category_item.text(0)] = []

        if uncategorized_elements:
            self.tree_structure["Uncategorized"] = uncategorized_elements

        # Mettre à jour la structure dans la collection
        self.collection.update_clusters_structure(self.tree_structure)

    def add_category(self):
        category_name, ok = QInputDialog.getText(self, "New Category", "Category Name:")
        if ok and category_name:
            if category_name in self.tree_structure:
                QMessageBox.warning(self, "Warning", f"The category '{category_name}' already exists.")
                return

            # Ajouter à la structure en mémoire
            self.tree_structure[category_name] = {}

            # Ajouter dans le widget
            category_item = QTreeWidgetItem([category_name])
            category_item.setFlags(category_item.flags() | Qt.ItemIsDropEnabled)
            self.tree.addTopLevelItem(category_item)

    def delete_category(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            parent = selected_item.parent()
            if parent is None:
                index = self.tree.indexOfTopLevelItem(selected_item)
                self.tree.takeTopLevelItem(index)
            else:
                parent.removeChild(selected_item)

    def handle_item_click(self, item, column):
        if Qt.ControlModifier & QApplication.keyboardModifiers():
            item.setSelected(not item.isSelected())
        elif Qt.ShiftModifier & QApplication.keyboardModifiers():
            current_items = self.tree.selectedItems()
            if current_items:
                start = self.tree.indexOfTopLevelItem(current_items[0])
                end = self.tree.indexOfTopLevelItem(item)
                if start != -1 and end != -1:
                    for i in range(min(start, end), max(start, end) + 1):
                        self.tree.topLevelItem(i).setSelected(True)