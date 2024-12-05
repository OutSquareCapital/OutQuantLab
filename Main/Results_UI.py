from PySide6.QtWidgets import (
                               QVBoxLayout, 
                               QDialog
                               )
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl
from Files import BACKGROUND_APP_DARK
from Config import save_html_temp_file

def generate_plot_widget(fig, show_legend:bool=True):
    if not show_legend:
        fig.update_layout(showlegend=False)

    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    temp_file_path = save_html_temp_file(html_content)
    plot_widget = QWebEngineView()
    page = plot_widget.page()
    page.settings().setAttribute(QWebEngineSettings.ShowScrollBars, False)
    page.setBackgroundColor(BACKGROUND_APP_DARK)
    plot_widget.load(QUrl.fromLocalFile(temp_file_path))

    return plot_widget

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
