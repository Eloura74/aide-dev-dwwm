import os
from tkinter import Tk, simpledialog, filedialog, messagebox

def generate_css_theme(theme_name, primary, secondary, background, text):
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

    h1, h2, h3 {{
        color: var(--primary-color);
    }}

    a {{
        color: var(--secondary-color);
        text-decoration: none;
    }}

    a:hover {{
        text-decoration: underline;
    }}
    """
    file_name = f"theme_{theme_name.lower().replace(' ', '_')}.css"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(css_content)
    print(f"Thème CSS '{theme_name}' généré avec succès dans {file_name}.")

def generate_multiple_themes():
    """Génère plusieurs thèmes CSS prédéfinis."""
    themes = [
        {"name": "Ocean", "primary": "#3498db", "secondary": "#2ecc71", "background": "#ecf0f1", "text": "#2c3e50"},
        {"name": "Sunset", "primary": "#e74c3c", "secondary": "#f39c12", "background": "#fdf5e6", "text": "#2c3e50"},
        {"name": "Dark Mode", "primary": "#1abc9c", "secondary": "#e67e22", "background": "#2c3e50", "text": "#ecf0f1"},
        {"name": "Forest", "primary": "#27ae60", "secondary": "#16a085", "background": "#dff9fb", "text": "#2c3e50"},
        {"name": "Purple Haze", "primary": "#8e44ad", "secondary": "#9b59b6", "background": "#f3e5f5", "text": "#2c3e50"}
    ]

    for theme in themes:
        generate_css_theme(theme["name"], theme["primary"], theme["secondary"], theme["background"], theme["text"])

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # Masquer la fenêtre principale

    result = messagebox.askyesno("Générateur de Thèmes CSS", "Voulez-vous générer les thèmes prédéfinis ?")

    if result:
        generate_multiple_themes()
    else:
        theme_name = simpledialog.askstring("Nom du Thème", "Entrez le nom du thème :")
        primary = simpledialog.askstring("Couleur Primaire", "Entrez la couleur primaire (ex: #3498db) :")
        secondary = simpledialog.askstring("Couleur Secondaire", "Entrez la couleur secondaire (ex: #2ecc71) :")
        background = simpledialog.askstring("Couleur de Fond", "Entrez la couleur de fond (ex: #ecf0f1) :")
        text = simpledialog.askstring("Couleur du Texte", "Entrez la couleur du texte (ex: #2c3e50) :")

        if theme_name and primary and secondary and background and text:
            generate_css_theme(theme_name, primary, secondary, background, text)
        else:
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis pour générer un thème personnalisé.")

# Instructions pour l'utiliser :
# Depuis le GUI :
# - Lancer le script dans un environnement où Tkinter est installé.
# - Une fenêtre apparaîtra pour vous demander si vous souhaitez générer les thèmes prédéfinis ou créer un thème personnalisé.
# Depuis Visual Studio Code :
# - Placez ce script dans votre espace de travail.
# - Ajoutez une tâche dans votre fichier tasks.json pour exécuter le script :
#   {
#     "label": "Générer des thèmes CSS",
#     "type": "shell",
#     "command": "python",
#     "args": ["${workspaceFolder}/css_theme_generator_gui.py"],
#     "problemMatcher": []
#   }
# - Lancez la tâche avec Ctrl+Shift+P > Tasks: Run Task > Générer des thèmes CSS.
# Résultat :
# - Des fichiers CSS correspondant aux thèmes prédéfinis ou personnalisés seront générés dans le répertoire de travail.