# Ce script télécharge automatiquement des bibliothèques (comme Bootstrap ou FontAwesome) à partir de leurs 
# liens CDN et les enregistre localement dans un dossier spécifié. Cela permet d’automatiser l’inclusion des 
# fichiers nécessaires à vos projets.

import os
import requests

def download_library(library_url, save_path):
    """Télécharge une bibliothèque depuis une URL et l'enregistre dans un fichier"""
    try:
        response = requests.get(library_url, timeout=10)
        response.raise_for_status()
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Bibliothèque téléchargée : {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement de {library_url} : {e}")

def manage_libraries(libraries, base_dir="libs"):
    """Gère le téléchargement des bibliothèques définies dans une liste"""
    for name, url in libraries.items():
        save_path = os.path.join(base_dir, name)
        download_library(url, save_path)

if __name__ == "__main__":
    print("=== Gestionnaire de Bibliothèques ===")

    libraries = {
        "bootstrap.css": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "bootstrap.js": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js",
        "fontawesome.css": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css",
    }

    base_dir = input("Entrez le chemin où sauvegarder les bibliothèques (laisser vide pour 'libs') : ").strip()
    if not base_dir:
        base_dir = "libs"

    manage_libraries(libraries, base_dir)

    print("Téléchargement des bibliothèques terminé.")