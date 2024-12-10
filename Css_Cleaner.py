
# Ouvrez Visual Studio Code.
# Appuyez sur Ctrl+Shift+P, recherchez Tasks: Run Task, et sélectionnez "Nettoyer les fichiers CSS inutilisés".
# Résultat attendu :

# Le script analysera votre fichier CSS spécifié et les fichiers HTML donnés.
# Un fichier cleaned.css sera généré, contenant uniquement les classes CSS utilisées.



import re
import os

def clean_css(css_file, html_files):
    """Nettoie un fichier CSS en supprimant les classes non utilisées dans les fichiers HTML."""
    if not os.path.exists(css_file):
        print(f"Erreur : Le fichier CSS '{css_file}' n'existe pas.")
        return

    with open(css_file, "r", encoding="utf-8") as css:
        css_content = css.read()

    used_classes = set()
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as html:
                # Trouver toutes les classes utilisées dans les fichiers HTML
                used_classes.update(re.findall(r'class="(.*?)"', html.read()))
        else:
            print(f"Avertissement : Le fichier HTML '{html_file}' n'existe pas et sera ignoré.")

    # Filtrer le CSS pour ne garder que les classes utilisées
    cleaned_css = "\n".join([
        line for line in css_content.splitlines()
        if any(cls in line for cls in used_classes)
    ])

    # Écrire le CSS nettoyé dans un nouveau fichier
    with open("cleaned.css", "w", encoding="utf-8") as file:
        file.write(cleaned_css)

    print("CSS nettoyé avec succès dans 'cleaned.css'.")

if __name__ == "__main__":
    print("=== Nettoyeur de Fichiers CSS Inutilisés ===")
    css_file = input("Entrez le chemin du fichier CSS : ").strip()
    html_files = input("Entrez les chemins des fichiers HTML (séparés par des virgules) : ").strip().split(",")
    html_files = [file.strip() for file in html_files]


# Ouvrez Visual Studio Code.
# Appuyez sur Ctrl+Shift+P, recherchez Tasks: Run Task, et sélectionnez "Nettoyer les fichiers CSS inutilisés".
# Résultat attendu :

# Le script analysera votre fichier CSS spécifié et les fichiers HTML donnés.
# Un fichier cleaned.css sera généré, contenant uniquement les classes CSS utilisées.



import re
import os

def clean_css(css_file, html_files):
    """Nettoie un fichier CSS en supprimant les classes non utilisées dans les fichiers HTML."""
    if not os.path.exists(css_file):
        print(f"Erreur : Le fichier CSS '{css_file}' n'existe pas.")
        return

    with open(css_file, "r", encoding="utf-8") as css:
        css_content = css.read()

    used_classes = set()
    for html_file in html_files:
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as html:
                # Trouver toutes les classes utilisées dans les fichiers HTML
                used_classes.update(re.findall(r'class="(.*?)"', html.read()))
        else:
            print(f"Avertissement : Le fichier HTML '{html_file}' n'existe pas et sera ignoré.")

    # Filtrer le CSS pour ne garder que les classes utilisées
    cleaned_css = "\n".join([
        line for line in css_content.splitlines()
        if any(cls in line for cls in used_classes)
    ])

    # Écrire le CSS nettoyé dans un nouveau fichier
    with open("cleaned.css", "w", encoding="utf-8") as file:
        file.write(cleaned_css)

    print("CSS nettoyé avec succès dans 'cleaned.css'.")

if __name__ == "__main__":
    print("=== Nettoyeur de Fichiers CSS Inutilisés ===")
    css_file = input("Entrez le chemin du fichier CSS : ").strip()
    html_files = input("Entrez les chemins des fichiers HTML (séparés par des virgules) : ").strip().split(",")
    html_files = [file.strip() for file in html_files]

    clean_css(css_file, html_files)