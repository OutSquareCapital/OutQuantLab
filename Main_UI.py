from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QProgressBar, QTextEdit, QDialog, QPushButton, QMainWindow, QApplication, QLineEdit, QGridLayout
from PySide6.QtGui import QPalette, QBrush, QPixmap, QIcon
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import tempfile
import os
import UI
import Dashboard

def generate_plot_widget(fig):

    fig.update_layout(autosize=True)
    html_content = fig.to_html(full_html=True, include_plotlyjs='True', config={"responsive": True})
    html_content = html_content.replace("<body>", f"<body style='background-color: {UI.BACKGROUND_GRAPH_DARK};'>")
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix="outquant.html")
    with open(temp_file.name, 'w', encoding='utf-8') as f:
        f.write(html_content)
    plot_widget = QWebEngineView()
    plot_widget.load(QUrl.fromLocalFile(temp_file.name))
    return plot_widget


def apply_global_styles(app:QApplication):
    app.setWindowIcon(QIcon(UI.APP_ICON_PHOTO)) 
    app.setStyleSheet(f"""
        * {{
            font-family: '{UI.FONT_FAMILY}';
            font-size: {UI.FONT_SIZE};
            font: {UI.FONT_TYPE};
        }}
    """)

def cleanup_temp_files():
    # Supprimer tous les fichiers avec le suffixe 'outquant.html' dans le répertoire temporaire
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
    dialog = QDialog(parent)
    dialog.setWindowTitle(window_title)
    layout = QVBoxLayout(dialog)
    layout.addWidget(plot_widget)
    dialog.setLayout(layout)
    dialog.exec()

def set_background_image(widget: QWidget, image_path: str):
    palette = QPalette()
    pixmap = QPixmap(image_path)
    palette.setBrush(QPalette.Window, QBrush(pixmap))
    widget.setPalette(palette)
    widget.setAutoFillBackground(True)

def setup_home_page(parent: QMainWindow, run_backtest_callback, open_config_callback, refresh_data_callback):

    parent.setWindowTitle("OutQuantLab")
    
    main_widget = QWidget()
    main_layout = QVBoxLayout()
    set_background_image(main_widget, UI.HOME_PAGE_PHOTO,)

    # Bouton Run Backtest
    backtest_button = QPushButton("Run Backtest")
    backtest_button.clicked.connect(run_backtest_callback)
    main_layout.addWidget(backtest_button)

    # Bouton Open Config
    config_button = QPushButton("Open Config")
    config_button.clicked.connect(open_config_callback)
    main_layout.addWidget(config_button)

    # Bouton Refresh Data
    refresh_button = QPushButton("Refresh Data")
    refresh_button.clicked.connect(refresh_data_callback)
    main_layout.addWidget(refresh_button)

    main_widget.setLayout(main_layout)
    parent.setCentralWidget(main_widget)

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

def setup_loading_page(parent):

    loading_widget, progress_bar, log_output = create_loading_page(UI.LOADING_PAGE_PHOTO)
    parent.setCentralWidget(loading_widget)
    return progress_bar, log_output

def create_results_page(dashboard_plots, back_to_home_callback, parent):
    results_widget = QWidget()
    results_layout = QHBoxLayout(results_widget)  # Layout principal horizontal
    # Définir l'image de fond
    set_background_image(results_widget, UI.DASHBOARD_PAGE_PHOTO)
    # Section gauche : Boutons de graphiques
    left_layout = QVBoxLayout()

    for title, plot_func in dashboard_plots.items():
        button = QPushButton(title, results_widget)
        button.clicked.connect(plot_func)
        left_layout.addWidget(button)

    equity_plot = generate_plot_widget(
        Dashboard.plot_equity(parent.global_result))
    sharpe_plot = generate_plot_widget(
        Dashboard.plot_rolling_sharpe_ratio(parent.global_result, length=1250))
    drawdown_plot = generate_plot_widget(
        Dashboard.plot_rolling_drawdown(parent.global_result, length=1250))
    vol_plot = generate_plot_widget(
        Dashboard.plot_rolling_volatility(parent.global_result))

    # Layout droit : champs de saisie et graphiques
    right_top_layout = QVBoxLayout()
    back_to_home_button = QPushButton("Back to Home Page")
    back_to_home_button.clicked.connect(back_to_home_callback)
    right_top_layout.addWidget(back_to_home_button)
    length_input = QLineEdit(results_widget)
    length_input.setPlaceholderText("Rolling length (e.g., 1250)")
    right_top_layout.addWidget(length_input)

    max_clusters_input = QLineEdit(results_widget)
    max_clusters_input.setPlaceholderText("Max Clusters (e.g., 5)")
    right_top_layout.addWidget(max_clusters_input)

    max_sub_clusters_input = QLineEdit(results_widget)
    max_sub_clusters_input.setPlaceholderText("Max Sub Clusters (e.g., 3)")
    right_top_layout.addWidget(max_sub_clusters_input)

    max_sub_sub_clusters_input = QLineEdit(results_widget)
    max_sub_sub_clusters_input.setPlaceholderText("Max Sub Sub Clusters (e.g., 2)")
    right_top_layout.addWidget(max_sub_sub_clusters_input)

    # Grille pour les graphiques
    right_bottom_layout = QGridLayout()
    plots = [equity_plot, sharpe_plot, drawdown_plot, vol_plot]
    for i, plot in enumerate(plots):
        right_bottom_layout.addWidget(plot, i // 2, i % 2)  # Ajouter dans une grille 2x2

    # Layout principal pour la section droite
    right_layout = QVBoxLayout()
    right_layout.addLayout(right_top_layout)  # Boutons et champs de saisie en haut
    right_layout.addLayout(right_bottom_layout)  # Grille des graphiques en bas

    # Ajouter les layouts gauche et droite au layout principal
    results_layout.addLayout(left_layout)
    results_layout.addLayout(right_layout)
    return results_widget


def setup_results_page(parent, plots, back_to_home_callback):

    results_widget = create_results_page(
        dashboard_plots=plots,
        back_to_home_callback=back_to_home_callback,
        parent=parent
    )
    parent.setCentralWidget(results_widget)

def setup_progress_bar(parent, title: str, max_value: int = 100):

    progress_window = QMainWindow(parent)
    progress_window.setWindowTitle(title)

    layout = QVBoxLayout()
    widget = QWidget(progress_window)
    progress_window.setCentralWidget(widget)

    progress_bar = QProgressBar()
    progress_bar.setRange(0, max_value)
    layout.addWidget(progress_bar)

    widget.setLayout(layout)

    return progress_window, progress_bar

def update_progress_with_events(progress_bar: QProgressBar, log_output: QTextEdit, value: int, message: str = None):
    progress_bar.setValue(value)
    if message:
        log_output.clear()
        log_output.append(message)
    QApplication.processEvents()