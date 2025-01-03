from PySide6.QtWidgets import (
QAbstractItemView, 
QWidget, 
QVBoxLayout,
QHBoxLayout, 
QTreeWidget, 
QTreeWidgetItem,
QPushButton, 
QApplication,
QInputDialog,
QMessageBox
)
from PySide6.QtCore import Qt
from ConfigClasses import ClustersTree

class TreeStructureWidget(QWidget):
    def __init__(self, entities_names: list[str], clusters: ClustersTree) -> None:
        super().__init__()
        self.entities_names: list[str] = entities_names
        self.clusters_backend: ClustersTree = clusters
        self.clusters_frontend = QTreeWidget()
        self.init_ui()

    def init_ui(self) -> None:
        self.clusters_frontend.setHeaderHidden(True)
        self.clusters_frontend.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.clusters_frontend.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.clusters_frontend.itemClicked.connect(self.handle_item_click)
        layout = QVBoxLayout()
        self.populate_tree_from_dict()
        layout.addWidget(self.clusters_frontend)

        buttons_layout = QHBoxLayout()
        add_button = QPushButton("Add Cluster")
        delete_button = QPushButton("Delete Cluster")

        add_button.clicked.connect(lambda: self.add_cluster())
        delete_button.clicked.connect(lambda: self.delete_cluster())


        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def handle_item_click(self, item: QTreeWidgetItem) -> None:
        if Qt.KeyboardModifier.ControlModifier & QApplication.keyboardModifiers():
            item.setSelected(not item.isSelected())
        elif Qt.KeyboardModifier.ShiftModifier & QApplication.keyboardModifiers():
            current_items: list[QTreeWidgetItem] = self.clusters_frontend.selectedItems()
            if current_items:
                start: int = self.clusters_frontend.indexOfTopLevelItem(current_items[0])
                end: int = self.clusters_frontend.indexOfTopLevelItem(item)
                if start != -1 and end != -1:
                    for i in range(min(start, end), max(start, end) + 1):
                        self.clusters_frontend.topLevelItem(i).setSelected(True)
    
    def add_cluster(self) -> None:
        cluster_name, ok = QInputDialog.getText(self.clusters_frontend, "New Cluster", "Cluster Name:")
        if ok and cluster_name:
            if cluster_name in self.clusters_backend.clusters:
                QMessageBox.warning(parent=self.clusters_frontend, title="Warning", text=f"The cluster '{cluster_name}' already exists.")
                return

            self.clusters_backend.clusters[cluster_name] = {}
            category_item = QTreeWidgetItem([cluster_name])
            category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
            self.clusters_frontend.addTopLevelItem(category_item)

    def delete_cluster(self) -> None:
        selected_cluster = self.clusters_frontend.currentItem()
        if selected_cluster:
            cluster_name = selected_cluster.text(0)
            parent = selected_cluster.parent()
            if parent:
                parent.removeChild(selected_cluster)
                parent_name = parent.text(0)
                del self.clusters_backend.clusters[parent_name][cluster_name]
            else:
                index = self.clusters_frontend.indexOfTopLevelItem(selected_cluster)
                if index != -1:
                    self.clusters_frontend.takeTopLevelItem(index)
                    del self.clusters_backend.clusters[cluster_name]

    def populate_tree_from_dict(self) -> None:
        for key, sub_clusters in self.clusters_backend.clusters.items():
            category_item = QTreeWidgetItem([key])
            category_item.setFlags(category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
            self.clusters_frontend.addTopLevelItem(category_item)

            for sub_key, elements in sub_clusters.items():
                sub_category_item = QTreeWidgetItem([sub_key])
                sub_category_item.setFlags(sub_category_item.flags() | Qt.ItemFlag.ItemIsDropEnabled)
                category_item.addChild(sub_category_item)

                for element in elements:
                    if element in self.entities_names:
                        child_item = QTreeWidgetItem([element])
                        child_item.setFlags(child_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                        sub_category_item.addChild(child_item)


        for element in self.entities_names:
            if not self.find_element_in_tree(element=element):
                orphan_item = QTreeWidgetItem([element])
                orphan_item.setFlags(orphan_item.flags() & ~Qt.ItemFlag.ItemIsDropEnabled)
                self.clusters_frontend.addTopLevelItem(orphan_item)

    def find_element_in_tree(self, element: str) -> bool:
        def traverse(item:QTreeWidgetItem) -> bool:
            if item.text(0) == element:
                return True
            for i in range(item.childCount()):
                if traverse(item.child(i)):
                    return True
            return False

        for i in range(self.clusters_frontend.topLevelItemCount()):
            if traverse(self.clusters_frontend.topLevelItem(i)):
                return True
        return False