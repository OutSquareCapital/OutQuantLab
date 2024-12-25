from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
from PySide6.QtCore import QUrl
from Files import BACKGROUND_APP_DARK
import os
import tempfile
from plotly import graph_objects as go # type: ignore

def save_html_temp_file(html_content: str, suffix: str = "outquant.html") -> str:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return temp_file.name

def cleanup_temp_files():
    temp_dir = tempfile.gettempdir()
    for file_name in os.listdir(temp_dir):
        if file_name.endswith("outquant.html"):
            file_path = os.path.join(temp_dir, file_name)
            try:
                os.remove(file_path)
            except Exception as e:
                raise Exception(f"Erreur lors de la suppression du fichier temporaire {file_path} : {e}")

def generate_plot_widget(fig: go.Figure, show_legend:bool=True) -> QWebEngineView:
    if not show_legend:
        fig.update_layout(showlegend=False) # type: ignore

    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True}) # type: ignore
    temp_file_path = save_html_temp_file(html_content) # type: ignore
    plot_widget = QWebEngineView()
    page = plot_widget.page()
    page.settings().setAttribute(QWebEngineSettings.WebAttribute.ShowScrollBars, False)
    page.setBackgroundColor(BACKGROUND_APP_DARK)
    plot_widget.load(QUrl.fromLocalFile(temp_file_path))

    return plot_widget