import os
from tkinter import Tk, simpledialog, filedialog, messagebox
import shutil
import argparse

def generate_css_theme(theme_name, primary, secondary, background, text, output_dir):
    """Génère un fichier CSS pour un thème donné."""
    css_content = f"""
/* Thème : {theme_name} */
:root {{
    --primary-color: {primary};
    --secondary-color: {secondary};
    --background-color: {background};
    --text-color: {text};
}}

body {{
    background-color: var(--background-color);
    color: var(--text-color);
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
}}

/* En-têtes */
h1, h2, h3, h4, h5, h6 {{
    color: var(--primary-color);
    margin-bottom: 1rem;
}}

/* Liens */
a {{
    color: var(--secondary-color);
    text-decoration: none;
    transition: color 0.3s ease;
}}

a:hover {{
    color: var(--primary-color);
    text-decoration: underline;
}}

/* Boutons */
.btn {{
    background-color: var(--primary-color);
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}}

.btn:hover {{
    background-color: var(--secondary-color);
}}

/* Cartes */
.card {{
    background-color: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}}

/* Formulaires */
input, textarea, select {{
    border: 1px solid var(--secondary-color);
    padding: 0.5rem;
    border-radius: 4px;
    margin-bottom: 1rem;
}}

/* Navigation */
nav {{
    background-color: var(--primary-color);
    padding: 1rem;
}}

nav a {{
    color: white;
    margin-right: 1rem;
}}

/* Footer */
footer {{
    background-color: var(--background-color);
    color: var(--text-color);
    padding: 1rem;
    text-align: center;
    border-top: 2px solid var(--secondary-color);
}}

/* Classes utilitaires */
.text-primary {{ color: var(--primary-color); }}
.text-secondary {{ color: var(--secondary-color); }}
.bg-primary {{ background-color: var(--primary-color); }}
.bg-secondary {{ background-color: var(--secondary-color); }}
"""
    
    file_name = f"theme_{theme_name.lower().replace(' ', '_')}.css"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(css_content)
    print(f"Thème CSS '{theme_name}' généré avec succès dans {file_path}.")
    return file_path

def generate_multiple_themes(output_dir):
    """Génère plusieurs thèmes CSS prédéfinis."""
    themes = [
        {"name": "Ocean", "primary": "#3498db", "secondary": "#2ecc71", "background": "#ecf0f1", "text": "#2c3e50"},
        {"name": "Sunset", "primary": "#e74c3c", "secondary": "#f39c12", "background": "#fdf5e6", "text": "#2c3e50"},
        {"name": "Dark Mode", "primary": "#1abc9c", "secondary": "#e67e22", "background": "#2c3e50", "text": "#ecf0f1"},
        {"name": "Forest", "primary": "#27ae60", "secondary": "#16a085", "background": "#dff9fb", "text": "#2c3e50"},
        {"name": "Purple Haze", "primary": "#8e44ad", "secondary": "#9b59b6", "background": "#f3e5f5", "text": "#2c3e50"},
        {"name": "Modern Light", "primary": "#00bcd4", "secondary": "#009688", "background": "#ffffff", "text": "#333333"},
        {"name": "Modern Dark", "primary": "#673ab7", "secondary": "#3f51b5", "background": "#121212", "text": "#ffffff"},
        {"name": "Earthy", "primary": "#795548", "secondary": "#8d6e63", "background": "#efebe9", "text": "#3e2723"},
        {"name": "Minimal", "primary": "#212121", "secondary": "#757575", "background": "#fafafa", "text": "#212121"},
        {"name": "Vibrant", "primary": "#ff4081", "secondary": "#7c4dff", "background": "#ffffff", "text": "#333333"}
    ]

    generated_files = []
    for theme in themes:
        file_path = generate_css_theme(
            theme["name"], 
            theme["primary"], 
            theme["secondary"], 
            theme["background"], 
            theme["text"],
            output_dir
        )
        generated_files.append(file_path)
    
    # Créer un fichier index.html pour prévisualiser les thèmes
    create_theme_preview(output_dir, themes)
    return generated_files

def create_theme_preview(output_dir, themes):
    """Crée une page HTML pour prévisualiser tous les thèmes."""
    preview_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prévisualisation des Thèmes CSS</title>
    <style>
        .theme-preview {
            margin: 20px;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        .color-sample {
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <h1>Prévisualisation des Thèmes CSS</h1>
"""
    
    for theme in themes:
        preview_content += f"""
    <div class="theme-preview">
        <h2>{theme["name"]}</h2>
        <p>
            <span class="color-sample" style="background-color: {theme["primary"]}"></span>Primary: {theme["primary"]}
            <span class="color-sample" style="background-color: {theme["secondary"]}"></span>Secondary: {theme["secondary"]}
            <span class="color-sample" style="background-color: {theme["background"]}"></span>Background: {theme["background"]}
            <span class="color-sample" style="background-color: {theme["text"]}"></span>Text: {theme["text"]}
        </p>
        <a href="theme_{theme["name"].lower().replace(' ', '_')}.css">Voir le fichier CSS</a>
    </div>
"""
    
    preview_content += """
</body>
</html>
"""
    
    with open(os.path.join(output_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(preview_content)

def create_themes_directory(base_path):
    """Crée un dossier pour les thèmes s'il n'existe pas."""
    themes_dir = os.path.join(base_path, "css_themes")
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir)
    return themes_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de thèmes CSS")
    parser.add_argument("--path", required=True, help="Chemin de destination des thèmes")
    args = parser.parse_args()

    root = Tk()
    root.withdraw()

    themes_dir = create_themes_directory(args.path)
    generate_multiple_themes(themes_dir)
    messagebox.showinfo("Succès", f"Les thèmes ont été générés dans le dossier {themes_dir}")