from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QTextEdit, QDialog
from PySide6.QtGui import QPalette, QBrush, QPixmap
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import tempfile
import os

def cleanup_temp_files(temp_files: list):
    for temp_file in temp_files:
        try:
            os.remove(temp_file)
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier temporaire {temp_file} : {e}")

def create_plot_dialog(fig, window_title: str, default_width: int, default_height: int, background_color: str):
    """
    Crée et affiche un graphique Plotly dans un QDialog.
    """
    # Génère le HTML avec Plotly inclus
    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    html_content = html_content.replace("<body>", f"<body style='background-color: {background_color};'>")

    # Crée un fichier temporaire pour le HTML
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)

    # Crée un QWebEngineView et charge le fichier
    dialog = QDialog()
    dialog.setWindowTitle(window_title)
    layout = QVBoxLayout(dialog)
    web_view = QWebEngineView(dialog)
    layout.addWidget(web_view)
    dialog.setLayout(layout)
    web_view.load(QUrl.fromLocalFile(temp_file.name))

    # Configure la taille et affiche le dialogue
    dialog.resize(default_width + 30, default_height + 40)
    dialog.exec()

    # Retourne le chemin du fichier temporaire pour nettoyage
    return temp_file.name

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def update_progress(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):

    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)


def create_loading_page(image_path: str):
    loading_widget = QWidget()
    loading_layout = QVBoxLayout(loading_widget)

    set_background_image(loading_widget, image_path)
    loading_layout.addStretch()
    progress_bar = QProgressBar(loading_widget)
    progress_bar.setRange(0, 100)
    loading_layout.addWidget(progress_bar)

    log_output = QTextEdit(loading_widget)
    log_output.setReadOnly(True)
    log_output.setFixedHeight(100)
    loading_layout.addWidget(log_output)

    return loading_widget, progress_bar, log_output