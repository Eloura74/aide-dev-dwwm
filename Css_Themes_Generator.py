# Nouvelle tâche "Générer des thèmes CSS" :

# Exécute le script css_theme_generator.py pour créer plusieurs thèmes CSS.
# Utilisation :

# Placez css_theme_generator.py dans votre espace de travail.
# Lancez la tâche dans VSCode avec Ctrl+Shift+P > Tasks: Run Task > Générer des thèmes CSS.
# Résultat attendu :

# Vous obtiendrez plusieurs fichiers CSS (par exemple : theme_ocean.css, theme_dark_mode.css) avec des styles bien organisés.
# Personnalisation :

# Ajoutez ou modifiez les thèmes dans la liste themes dans le script pour générer des palettes adaptées à vos besoins.


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
    with open(file_name, "w") as file:
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
    print("=== Génération de Thèmes CSS ===")
    generate_multiple_themes()