from UI_Common import create_scroll_area, add_category_widget_shared, create_apply_button, select_all_items, unselect_all_items, create_checkbox_item, create_expandable_section, create_apply_button
from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox,  QLabel, QGroupBox, QHBoxLayout, QSlider, QComboBox, QTreeWidget, QTreeWidgetItem, QPushButton, QInputDialog, QApplication
from PySide6.QtCore import Qt, Signal
from typing import Dict, List, Any
from Files import METHODS_CONFIG_FILE, ASSETS_TO_TEST_CONFIG_FILE, PARAM_CONFIG_FILE
from .Config_Backend import param_range_values, save_config_file, load_config_file
from PySide6.QtGui import QFont

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

class ParameterWidget(QWidget):
    parameters_saved = Signal()

    def __init__(self, current_config: Dict[str, Any]):
        super().__init__()
        self.current_config = current_config
        self.param_widgets = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Create scrollable area using shared function
        scroll_area, scroll_widget, scroll_layout = create_scroll_area()

        for category, params in self.current_config.items():
            self.add_category_widget(category, params, scroll_layout)

        scroll_widget.setLayout(scroll_layout)
        layout.addWidget(scroll_area)

        # Create and add Apply button using shared function
        self.apply_button = create_apply_button(self.save_configuration)
        layout.addWidget(self.apply_button)

        self.setLayout(layout)

    def add_category_widget(self, category: str, params: Dict[str, Any], layout: QVBoxLayout):
        # Use shared expandable section
        category_box, content_widget, content_layout = create_expandable_section(category)

        for param, values in params.items():
            self.add_param_widget(category, param, values, content_layout)

        layout.addWidget(category_box)

    def add_param_widget(self, category: str, param: str, values: list, layout: QVBoxLayout):
        param_box = QGroupBox(param)
        param_layout = QVBoxLayout()

        if not values:
            values = [1]

        # Informations dynamiques
        range_info_label, num_values_info_label, scroll_area = self.create_info_labels(values)
        param_layout.addWidget(range_info_label)
        param_layout.addWidget(num_values_info_label)
        param_layout.addWidget(scroll_area)

        # Sliders
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

        mode_combobox = self.create_mode_combobox()
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        mode_layout.addWidget(mode_combobox)
        param_layout.addLayout(mode_layout)

        self.connect_sliders_to_update(
            category, param, start_slider, end_slider, num_values_slider, mode_combobox,
            range_info_label, num_values_info_label, scroll_area.widget(), param_box
        )

        param_box.setLayout(param_layout)
        layout.addWidget(param_box)

        self.param_widgets.setdefault(category, {})[param] = {
            "start_slider": start_slider,
            "end_slider": end_slider,
            "num_values_slider": num_values_slider,
            "mode_combobox": mode_combobox,
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

        start_slider.setMinimum(0)  # Index correspondant à 1
        start_slider.setMaximum(11)  # Index correspondant à 2048
        end_slider.setMinimum(0)  # Index correspondant à 1
        end_slider.setMaximum(12)  # Index correspondant à 4096

        start_slider.setValue(self.value_to_index(min(values)))
        end_slider.setValue(self.value_to_index(max(values)))

        return start_slider, end_slider

    def create_num_values_slider(self, num_values: int):
        num_values_slider = QSlider(Qt.Horizontal)
        num_values_slider.setMinimum(1)
        num_values_slider.setMaximum(10)
        num_values_slider.setValue(num_values)
        return num_values_slider

    def create_mode_combobox(self):
        mode_combobox = QComboBox()
        mode_combobox.addItems(["Linear", "Ratio"])
        return mode_combobox

    def value_to_index(self, value: int) -> int:
        return int(value).bit_length() - 1

    def index_to_value(self, index: int) -> int:
        return 2 ** index

    def connect_sliders_to_update(self, category, param, start_slider, end_slider, num_values_slider, mode_combobox,
                                  range_info_label, num_values_info_label, generated_values_label, param_box):
        def update_values():
            start = self.index_to_value(start_slider.value())
            end = self.index_to_value(end_slider.value())
            num_values = num_values_slider.value()
            mode = mode_combobox.currentText()

            if start * 2 > end:
                if start_slider.hasFocus():
                    end_slider.setValue(self.value_to_index(start * 2))
                    end = self.index_to_value(end_slider.value())
                elif end_slider.hasFocus():
                    start_slider.setValue(self.value_to_index(end // 2))
                    start = self.index_to_value(start_slider.value())

            linear = (mode == "Linear")
            generated_values = param_range_values(start, end, num_values, linear=linear)

            # Limiter les doublons
            unique_values = list(sorted(set(generated_values)))
            while len(unique_values) < num_values:
                num_values -= 1
                unique_values = list(sorted(set(param_range_values(start, end, num_values, linear=linear))))

            # Update the num_values slider if reduced
            if num_values < num_values_slider.value():
                num_values_slider.setValue(num_values)

            range_info_label.setText(f"Range: {start} - {end}")
            num_values_info_label.setText(f"Num Values: {num_values}")
            generated_values_label.setText(f"Generated Values: {unique_values}")
            self.current_config[category][param] = unique_values
            self.apply_button.setEnabled(True)

        start_slider.valueChanged.connect(update_values)
        end_slider.valueChanged.connect(update_values)
        num_values_slider.valueChanged.connect(update_values)
        mode_combobox.currentTextChanged.connect(update_values)

    def save_configuration(self):
        save_config_file(PARAM_CONFIG_FILE, self.current_config, 4)
        self.apply_button.setEnabled(False)
        self.parameters_saved.emit()

class TreeStructureWidget(QWidget):
    def __init__(self, json_file_path: str, data: List[str], parent=None):
        super().__init__(parent)
        self.json_file_path = json_file_path
        self.data = set(data)  # Convertir data en set pour une recherche rapide
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setDragDropMode(QTreeWidget.InternalMove)
        self.tree.setSelectionMode(QTreeWidget.ExtendedSelection)
        self.tree.itemClicked.connect(self.handle_item_click)

        # Charger la structure JSON
        self.tree_structure = load_config_file(self.json_file_path) or {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Remplir l'arborescence à partir du JSON et de data
        self.populate_tree_from_dict(self.tree_structure)
        layout.addWidget(self.tree)

        buttons_layout = QHBoxLayout()

        add_button = QPushButton("Add Category")
        delete_button = QPushButton("Delete Category")
        save_button = QPushButton("Save")

        add_button.clicked.connect(self.add_category)
        delete_button.clicked.connect(self.delete_category)
        save_button.clicked.connect(self.save_structure)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def populate_tree_from_dict(self, data: dict, parent_item=None):
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

            if isinstance(value, dict):  # Sous-catégorie
                self.populate_tree_from_dict(value, category_item)
            elif isinstance(value, list):  # Éléments finaux
                for element in value:
                    if element in self.data:
                        child_item = QTreeWidgetItem([element])
                        child_item.setFlags(child_item.flags() & ~Qt.ItemIsDropEnabled)
                        category_item.addChild(child_item)

        # Ajouter les éléments de data sans correspondance dans une catégorie spéciale
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

    def save_structure(self):
        def traverse_tree(item):
            if item.childCount() == 0:  # Éléments finaux
                return item.text(0)

            result = {}
            for i in range(item.childCount()):
                child = item.child(i)
                if child.childCount() == 0:  # Éléments finaux dans une liste
                    result.setdefault("elements", []).append(child.text(0))
                else:  # Sous-catégories
                    result[child.text(0)] = traverse_tree(child)
            return result.get("elements", []) if len(result) == 1 and "elements" in result else result

        result = {}
        for i in range(self.tree.topLevelItemCount()):
            category_item = self.tree.topLevelItem(i)
            if category_item.childCount() > 0:
                result[category_item.text(0)] = traverse_tree(category_item)
            else:  # Éléments finaux directement au niveau supérieur
                result.setdefault("Uncategorized", []).append(category_item.text(0))

        save_config_file(self.json_file_path, result, indent=4)

    def add_category(self):
        category_name, ok = QInputDialog.getText(self, "New Category", "Category Name:")
        if ok and category_name:
            category_item = QTreeWidgetItem([category_name])
            category_item.setFlags(category_item.flags() | Qt.ItemIsDropEnabled)
            self.tree.addTopLevelItem(category_item)

    def delete_category(self):
        selected_item = self.tree.currentItem()
        if selected_item:
            parent = selected_item.parent()
            if parent is None:  # Supprimer une catégorie
                index = self.tree.indexOfTopLevelItem(selected_item)
                self.tree.takeTopLevelItem(index)
            else:  # Supprimer un sous-élément
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
