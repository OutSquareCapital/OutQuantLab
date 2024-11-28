from PySide6.QtWidgets import (
                               QVBoxLayout, 
                               QDialog
                               )
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt
import tempfile
import os
from Files import BACKGROUND_APP_DARK

def generate_plot_widget(fig, show_legend:bool=True):
    if not show_legend:
        fig.update_layout(showlegend=False)

    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="outquant.html")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)
    plot_widget = QWebEngineView()
    page = plot_widget.page()
    page.setBackgroundColor(BACKGROUND_APP_DARK)
    plot_widget.load(QUrl.fromLocalFile(temp_file.name))
    return plot_widget

def cleanup_temp_files():
    temp_dir = tempfile.gettempdir()
    for file_name in os.listdir(temp_dir):
        if file_name.endswith("outquant.html"):
            file_path = os.path.join(temp_dir, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier temporaire {file_path} : {e}")

def display_plot_dialog(parent, fig, window_title: str):
    plot_widget = generate_plot_widget(fig)
    plot_widget.showMaximized
    dialog = QDialog(parent)
    dialog.setWindowTitle(window_title)
    layout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.resize(1200, 800)

    dialog.exec()
