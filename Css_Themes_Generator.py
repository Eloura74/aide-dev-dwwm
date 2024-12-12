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
    
    # Crée le fichier CSS
    theme_file = os.path.join(output_dir, f"{theme_name.lower()}.css")
    with open(theme_file, "w", encoding="utf-8") as f:
        f.write(css_content)
    return theme_file

def generate_themes(options, output_dir):
    """Génère les thèmes CSS selon les options sélectionnées."""
    themes = []
    
    if "dark" in options:
        themes.append(("Dark", "#00b4d8", "#0077b6", "#1a1a1a", "#ffffff"))
    if "light" in options:
        themes.append(("Light", "#0066cc", "#0099ff", "#ffffff", "#333333"))
    if "corporate" in options:
        themes.append(("Corporate", "#2c3e50", "#34495e", "#ecf0f1", "#2c3e50"))
    
    generated_files = []
    for theme_name, primary, secondary, background, text in themes:
        theme_file = generate_css_theme(theme_name, primary, secondary, background, text, output_dir)
        generated_files.append(theme_file)
    
    return generated_files

def create_theme_preview(output_dir, theme_files):
    """Crée une page HTML pour prévisualiser les thèmes."""
    preview_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Prévisualisation des Thèmes</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .theme-section { margin-bottom: 40px; padding: 20px; border-radius: 8px; }
        .controls { margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>Prévisualisation des Thèmes CSS</h1>
"""
    
    for theme_file in theme_files:
        theme_name = os.path.splitext(os.path.basename(theme_file))[0].title()
        preview_content += f"""
    <div class="theme-section">
        <h2>{theme_name}</h2>
        <link rel="stylesheet" href="{os.path.basename(theme_file)}">
        <div class="controls">
            <button class="btn">Bouton d'exemple</button>
            <a href="#">Lien d'exemple</a>
        </div>
        <div class="card">
            <h3>Carte d'exemple</h3>
            <p>Ceci est un exemple de contenu dans une carte.</p>
        </div>
        <form>
            <input type="text" placeholder="Champ de texte">
            <textarea placeholder="Zone de texte"></textarea>
            <button type="submit" class="btn">Envoyer</button>
        </form>
    </div>
"""
    
    preview_content += """
</body>
</html>
"""
    
    preview_file = os.path.join(output_dir, "preview.html")
    with open(preview_file, "w", encoding="utf-8") as f:
        f.write(preview_content)

def create_themes_directory(base_path):
    """Crée le dossier des thèmes s'il n'existe pas."""
    themes_dir = os.path.join(base_path, "themes")
    os.makedirs(themes_dir, exist_ok=True)
    return themes_dir

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Générateur de thèmes CSS")
    parser.add_argument("--path", required=True, help="Chemin de destination des thèmes")
    parser.add_argument("--options", required=True, help="Liste des options séparées par des virgules (dark,light,corporate)")
    args = parser.parse_args()
    
    # Crée le dossier des thèmes
    themes_dir = create_themes_directory(args.path)
    
    # Génère les thèmes sélectionnés
    options = args.options.split(",")
    generated_files = generate_themes(options, themes_dir)
    
    # Crée la prévisualisation
    if generated_files:
        create_theme_preview(themes_dir, generated_files)
        print(f"Thèmes générés avec succès dans : {themes_dir}")
        print("Les fichiers suivants ont été créés :")
        for file in generated_files:
            print(f"- {os.path.basename(file)}")
        print("- preview.html (prévisualisation des thèmes)")
    else:
        print("Aucun thème n'a été généré. Vérifiez les options sélectionnées.")