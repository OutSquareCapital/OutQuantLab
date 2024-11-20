import json
import os
from typing import Dict, List
from Config import assets_to_backtest, DYNAMIC_CONFIG_FILE
import tkinter as tk
from tkinter import ttk

def load_last_config(assets_names: List[str]) -> Dict[str, List[str]]:
    """Charge la dernière configuration sauvegardée depuis un fichier JSON.
       Si aucun fichier n'est trouvé, ouvre la fenêtre Tkinter pour configurer."""
    if os.path.exists(DYNAMIC_CONFIG_FILE):
        with open(DYNAMIC_CONFIG_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                pass  # Si le fichier est corrompu, passe à la configuration Tkinter

    # Si le fichier n'existe pas ou est invalide, ouvrir la fenêtre Tkinter
    print("No configuration file found. Opening configuration window...")
    return select_assets(assets_names)

def save_last_config(config: Dict[str, List[str]]):
    """Sauvegarde la configuration actuelle dans un fichier JSON."""
    with open(DYNAMIC_CONFIG_FILE, "w") as file:
        json.dump(config, file)

def select_assets(assets_names: List[str]) -> Dict[str, List[str]]:
    """Ouvre une interface Tkinter pour configurer les actifs à backtester."""

    # Charger la configuration existante ou utiliser la structure par défaut
    current_config = assets_to_backtest

    # Fonction pour sauvegarder la sélection depuis Tkinter
    def save_selection():
        for category, asset_vars in category_vars.items():
            current_config[category] = [asset for asset, var in asset_vars.items() if var.get()]
        save_last_config(current_config)  # Sauvegarde dans le fichier JSON
        root.destroy()

    # Fonction pour mettre à jour l'état de "All"
    def update_all_checkbox(category: str):
        all_selected = all(var.get() for var in category_vars[category].values())
        all_vars[category].set(all_selected)

    # Fonction pour gérer le clic sur une case d'actif
    def on_asset_toggle(category: str):
        update_all_checkbox(category)

    # Fonction pour sélectionner/désélectionner tous les actifs d'une catégorie
    def toggle_all(category: str):
        new_state = all_vars[category].get()
        for var in category_vars[category].values():
            var.set(new_state)

    # Création de l'interface Tkinter
    root = tk.Tk()
    root.title("Assets to backtest selection")

    # Variables pour chaque catégorie et chaque actif
    category_vars = {
        category: {
            asset: tk.BooleanVar(value=(asset in current_config.get(category, [])))
            for asset in assets_names
        }
        for category in current_config.keys()
    }
    all_vars = {
        category: tk.BooleanVar(value=all(asset in current_config.get(category, []) for asset in assets_names))
        for category in current_config.keys()
    }

    # Gestion des frames pour chaque catégorie
    for category in current_config.keys():
        frame = ttk.LabelFrame(root, text=f"{category}")
        frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Case "All" pour sélectionner tous les actifs
        all_checkbox = ttk.Checkbutton(
            frame,
            text="All",
            variable=all_vars[category],
            command=lambda c=category: toggle_all(c)
        )
        all_checkbox.pack(anchor="w")
        ttk.Label(frame, text="").pack(anchor="w", pady=5)

        # Actifs individuels
        for asset in assets_names:
            cb = ttk.Checkbutton(
                frame,
                text=asset,
                variable=category_vars[category][asset],
                command=lambda c=category: on_asset_toggle(c)
            )
            cb.pack(anchor="w")

    # Bouton pour sauvegarder
    save_button = ttk.Button(root, text="Apply selection", command=save_selection)
    save_button.pack(pady=10)

    # Initialiser les cases "All" en fonction de l'état des actifs
    for category in current_config.keys():
        update_all_checkbox(category)

    root.mainloop()
    return current_config  # Retourner la configuration mise à jour
