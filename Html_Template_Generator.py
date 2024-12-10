import os

def generate_html_template(template_name, title, content):
    """Génère un fichier HTML basé sur un modèle prédéfini"""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <link rel="stylesheet" href="css/style.css">
    </head>
    <body>
        <header>
            <h1>{title}</h1>
        </header>
        <main>
            {content}
        </main>
        <footer>
            <p>&copy; 2023 - Exemple de footer</p>
        </footer>
        <script src="js/app.js"></script>
    </body>
    </html>
    """
    with open(f"{template_name}.html", "w") as file:
        file.write(html_content)
    print(f"Template HTML '{template_name}.html' généré avec succès.")

def generate_multiple_templates():
    """Génère plusieurs fichiers HTML prédéfinis"""
    templates = [
        {"name": "index", "title": "Page d'accueil", "content": "<p>Bienvenue sur la page d'accueil.</p>"},
        {"name": "about", "title": "À propos", "content": "<p>Voici la page à propos.</p>"},
        {"name": "contact", "title": "Contact", "content": "<p>Contactez-nous via cette page.</p>"},
        {"name": "services", "title": "Services", "content": "<p>Découvrez nos services ici.</p>"}
    ]

    os.makedirs("templates", exist_ok=True)
    for template in templates:
        generate_html_template(
            os.path.join("templates", template["name"]),
            template["title"],
            template["content"]
        )

if __name__ == "__main__":
    print("=== Génération de Templates HTML ===")
    generate_multiple_templates()
