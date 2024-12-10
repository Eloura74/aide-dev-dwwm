# Exécute le script static_site_search.py pour analyser les fichiers HTML et générer un fichier search.js.
# Utilisation :

# Placez le fichier static_site_search.py dans votre espace de travail.
# Exécutez la tâche dans Visual Studio Code via Ctrl+Shift+P > Tasks: Run Task > Générer le moteur de recherche statique.
# Résultat attendu :

# Un fichier search.js sera généré, contenant un tableau des contenus des pages HTML spécifiées et une fonction de recherche simple.


import os
import json

def generate_search_js(pages):
    """Génère un script JavaScript pour un moteur de recherche basique."""
    search_data = []
    for page in pages:
        if os.path.exists(page):
            with open(page, "r", encoding="utf-8") as file:
                content = file.read()
            search_data.append({"page": page, "content": content})
        else:
            print(f"Avertissement : Le fichier {page} n'existe pas et sera ignoré.")

    # Générer le contenu du fichier JavaScript
    js_content = f"const searchData = {json.dumps(search_data, indent=2)};\n\n"
    js_content += "function search(query) {\n"
    js_content += "  return searchData.filter(entry => entry.content.toLowerCase().includes(query.toLowerCase()));\n"
    js_content += "}\n\n"
    js_content += "console.log(search('votre recherche ici')); // Exemple d'utilisation\n"

    # Écrire le fichier JS
    with open("search.js", "w", encoding="utf-8") as file:
        file.write(js_content)

    print("Script de recherche généré avec succès dans 'search.js'.")

if __name__ == "__main__":
    print("=== Génération du moteur de recherche pour site statique ===")
    pages = input("Entrez les noms des fichiers HTML à inclure (séparés par des virgules) : ").strip().split(",")
    pages = [page.strip() for page in pages]
    generate_search_js(pages)